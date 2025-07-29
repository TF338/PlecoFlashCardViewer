import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class FlashCard:
    id: int
    lang: int
    hw: str  # Headword
    althw: Optional[str] = None  # Alternate headword
    pron: Optional[str] = None  # Pronunciation
    defn: Optional[str] = None  # Definition
    dictcreator: Optional[int] = None
    dictid: Optional[int] = None
    dictentry: Optional[int] = None
    altdictrefs: Optional[str] = None
    wordlength: Optional[int] = None
    created: Optional[int] = None  # Unix timestamp
    modified: Optional[int] = None  # Unix timestamp
    categories: List['Category'] = None
    score: Optional['CardScore'] = None


    @property
    def created_date(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.created) if self.created else None

    @property
    def modified_date(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.modified) if self.modified else None

    @property
    def word(self) -> str:
        """Clean headword by removing @ symbols"""
        return self.hw.replace('@', '')
