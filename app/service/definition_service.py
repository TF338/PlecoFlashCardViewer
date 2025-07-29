import logging
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class DefinitionService:
    _cedict_data = None

    def __init__(self):
        if not DefinitionService._cedict_data:
            DefinitionService._cedict_data = self.load_dictionary_from_file()
        self.dictionary = DefinitionService._cedict_data


    def load_dictionary_from_file(self, path = Path(__file__).parent.parent.parent / "cedict/cedict_ts.u8"):
        logger = logging.getLogger(__name__)
        logger.info(f"Loading CC-CEDICT from {path}...")

        self.dictionary = {}  # <--- FIX: define before using

        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("#"):
                        continue
                    parts = line.strip().split(" ", 2)
                    if len(parts) < 3:
                        continue
                    trad, simp, rest = parts
                    pinyin_def = rest.split("] ", 1)
                    if len(pinyin_def) < 2:
                        continue
                    pinyin = pinyin_def[0].lstrip("[")
                    definitions = pinyin_def[1].strip("/").split("/")
                    self.dictionary[simp] = {
                        "traditional": trad,
                        "pinyin": pinyin,
                        "definitions": definitions
                    }

            logger.info(f"Loaded {len(self.dictionary)} entries from CC-CEDICT.")
            return self.dictionary

        except Exception as e:
            logger.error(f"Failed to load CC-CEDICT: {e}", exc_info=True)
            return {}

    def lookup(self, word: str) -> Optional[str]:
        """Lookup definitions by simplified Chinese word and return them as a single string."""
        entry = self.dictionary.get(word)
        if entry:
            return "; ".join(entry["definitions"])
        return None