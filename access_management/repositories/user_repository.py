from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from shared.infrastructure.db.sqlalchemy_repository import SQLAlchemyRepository
from access_management.domain.aggregates.user import User
from access_management import UserRepository
from access_management.domain.value_objects.email import Email

class SQLAlchemyUserRepository(SQLAlchemyRepository, UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def save(self, user: User) -> None:
        # Map User domain model to SQLAlchemy table (assumes table matches Django model)
        await self.session.execute(
            """
            INSERT INTO user_management_user (id, email, password_hash, is_active)
            VALUES (:id, :email, :password_hash, :is_active)
            ON CONFLICT (id) DO UPDATE
            SET email = :email, password_hash = :password_hash, is_active = :is_active
            """,
            {
                "id": user.id,
                "email": str(user.email),
                "password_hash": user.password_hash,
                "is_active": user.is_active
            }
        )
        await self.session.commit()

    async def find_by_email(self, email: str) -> User:
        result = await self.session.execute(
            select(User).where(User.email == Email(email))
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User with email {email} not found")
        return user