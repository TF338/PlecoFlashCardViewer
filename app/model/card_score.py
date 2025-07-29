from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
import json

@dataclass
class CardScore:
    card: int  # FlashCard ID (primary key)
    score: int
    difficulty: int
    history: Dict[str, Any]  # JSON data
    correct: int
    incorrect: int
    reviewed: int
    sincelastchange: int
    firstreviewedtime: Optional[int] = None
    lastreviewedtime: Optional[int] = None
    scoreinctime: Optional[int] = None
    scoredectime: Optional[int] = None

    def __post_init__(self):
        # Parse history JSON string if needed
        if isinstance(self.history, str):
            self.history = json.loads(self.history) if self.history else {}

    @property
    def last_reviewed_date(self) -> Optional[datetime]:
        return datetime.fromtimestamp(self.lastreviewedtime) if self.lastreviewedtime else None