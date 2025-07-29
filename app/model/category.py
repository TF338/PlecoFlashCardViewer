from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    id: int
    name: str
    created: Optional[int] = None
    modified: Optional[int] = None
    parent: Optional[int] = None  # Parent category ID
    sort: Optional[int] = None  # Sort order
    hidden: Optional[int] = None  # 0 or 1
    class_: Optional[int] = None  # 'class' is a reserved word in Python

    @property
    def is_hidden(self) -> bool:
        return self.hidden == 1