from app.repository.category_repository import CategoryRepository
from app.repository.flash_card_respository import FlashCardRepository
from app.service.definition_service import DefinitionService
from sqlalchemy.orm import Session


class ServiceContainer:
    def __init__(self, session: Session):
        self._db_session = session
        self._definition_service = DefinitionService()
        self._category_repository = CategoryRepository(self._db_session)
        self._flashcard_repository = FlashCardRepository(self._db_session, self._definition_service)

    @property
    def definition_service(self) -> DefinitionService:
        return self._definition_service

    @property
    def category_repository(self) -> CategoryRepository:
        return self._category_repository

    @property
    def flashcard_repository(self) -> FlashCardRepository:
        return self._flashcard_repository