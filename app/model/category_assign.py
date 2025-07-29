from dataclasses import dataclass

@dataclass
class CategoryAssign:
    id: int
    card: int  # FlashCard ID
    cat: int  # Category ID