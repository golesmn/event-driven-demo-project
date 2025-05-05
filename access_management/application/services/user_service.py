from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from sqlalchemy import Column, Integer, String, Boolean

from access_management.domain.aggregates.user import User
from shared.infrastructure.db.db import Base, SessionLocal

class SAUser(Base):
    __tablename__ = "users"  # Matches Django’s table name
    __table_args__ = {'extend_existing': True}  # Avoid redefinition errors
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


def create_user(user: User) -> User:
    hashed_password = generate_password_hash(user.password)
    db_user = SAUser(username=user.username, email=user.email.value, hashed_password=hashed_password, is_active=True)
    db = SessionLocal()
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    finally:
        db.close()
    return user