from typing import List

from sqlalchemy import text

from app.model.category import Category
from app.repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def get_all(self) -> List[Category]:
        result = self.session.execute(text("""
            SELECT id, name, created, modified, parent, sort, hidden, class AS class_
            FROM pleco_flash_categories
            ORDER BY name
        """))

        return [
            Category(
                id=row.id,
                name=row.name,
                created=row.created,
                modified=row.modified,
                parent=row.parent,
                sort=row.sort,
                hidden=row.hidden,
                class_=row.class_
            ) for row in result
        ]
