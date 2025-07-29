from abc import ABC, abstractmethod

class BaseRepository(ABC):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, id: int):
        if not self.table:
            raise NotImplementedError("Subclasses must define 'self.table'")
        return self.session.get(self.table, id)