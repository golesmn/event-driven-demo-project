


from sqlalchemy.orm import Session
from sqlalchemy import select
from .base_repository import BaseRepository
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: T) -> None:
        self.session.add(entity)
        self.session.commit()

    def find_by_id(self, id: str) -> Optional[T]:
        entity_type = getattr(self, "_entity_type", None)
        if not entity_type:
            raise ValueError("Entity type not specified")
        result = self.session.execute(
            select(entity_type).where(entity_type.id == id)
        )
        return result.scalar_one_or_none()