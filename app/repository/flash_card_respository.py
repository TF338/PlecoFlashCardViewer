import json

from sqlalchemy import text
from typing import List
import re

from app.model.card_score import CardScore
from app.model.flash_card import FlashCard
from app.repository.base_repository import BaseRepository

TONE_MARKS = {
    'a': ['ā', 'á', 'ǎ', 'à'],
    'e': ['ē', 'é', 'ě', 'è'],
    'i': ['ī', 'í', 'ǐ', 'ì'],
    'o': ['ō', 'ó', 'ǒ', 'ò'],
    'u': ['ū', 'ú', 'ǔ', 'ù'],
    'ü': ['ǖ', 'ǘ', 'ǚ', 'ǜ'],
}


class FlashCardRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.table = FlashCard

    def get_by_category_and_score(self, category_id: int, max_score: int) -> List[FlashCard]:
        print(f"Querying cards for category={category_id}, max_score={max_score}")
        query = text("""
            SELECT 
                c.*, 
                s.score, s.difficulty, s.history, 
                s.correct, s.incorrect, s.reviewed,
                s.sincelastchange, s.firstreviewedtime,
                s.lastreviewedtime, s.scoreinctime, s.scoredectime
            FROM pleco_flash_cards c
            JOIN pleco_flash_categoryassigns a ON c.id = a.card
            LEFT JOIN pleco_flash_scores_1 s ON c.id = s.card
            WHERE a.cat = :cat_id 
            AND (s.score IS NULL OR s.score <= :max_score)
            ORDER BY COALESCE(s.score, 999) ASC
        """)
        result = self.session.execute(query, {
            'cat_id': category_id,
            'max_score': max_score
        })

        cards = []
        for row in result:
            # Clean the word (hw) by removing @ symbols
            cleaned_word = row.hw.replace('@', '') if row.hw else ""

            # Clean the pronunciation (pron) - remove @ and tone numbers
            cleaned_pron = self.__pinyin(row.pron)

            cards.append(FlashCard(
                id=row.id,
                lang=row.lang,
                hw=cleaned_word,  # Now storing cleaned word
                althw=row.althw.replace('@', '') if row.althw else None,
                pron=cleaned_pron,  # Now storing cleaned pinyin
                defn=row.defn,
                dictcreator=row.dictcreator,
                dictid=row.dictid,
                dictentry=row.dictentry,
                altdictrefs=row.altdictrefs,
                wordlength=row.wordlength,
                created=row.created,
                modified=row.modified,
                score=CardScore(
                    card=row.id,
                    score=row.score,
                    difficulty=row.difficulty,
                    history=self.__parse_history(row.history),
                    correct=row.correct,
                    incorrect=row.incorrect,
                    reviewed=row.reviewed,
                    sincelastchange=row.sincelastchange,
                    firstreviewedtime=row.firstreviewedtime,
                    lastreviewedtime=row.lastreviewedtime,
                    scoreinctime=row.scoreinctime,
                    scoredectime=row.scoredectime
                ) if row.score is not None else None
            ))

        return cards

    def __convert_syllable(self, syllable: str) -> str:
        match = re.match(r"([a-zü]+)([1-5])", syllable)
        if not match:
            return syllable
        base, tone = match.groups()
        tone = int(tone)
        if tone == 5:
            return base  # neutral tone
        for vowel_group in ['a', 'e', 'o', 'iu', 'i', 'u', 'ü']:
            for v in vowel_group:
                if v in base:
                    return base.replace(v, TONE_MARKS[v][tone - 1], 1)
        return base

    def __numbered_to_accented(self, pinyin: str) -> str:
        return ' '.join([self.__convert_syllable(syl) for syl in pinyin.split()])

    def __pinyin(self, pinying: str) -> str:
        """Convert numbered pinyin with tone (e.g. ni3@hao3) to accented (nǐ hǎo)."""
        if not pinying:
            return ""

        # Preserve syllable separation by splitting on @ or space
        syllables = re.split(r'[@\s]+', pinying.strip())
        accented = [self.__convert_syllable(syl) for syl in syllables if syl]
        return ' '.join(accented)

    def __parse_history(self, history):
        """Parse the history JSON field if it exists"""
        if isinstance(history, str):
            try:
                return json.loads(history) if history else {}
            except json.JSONDecodeError:
                return {}
        return history or {}