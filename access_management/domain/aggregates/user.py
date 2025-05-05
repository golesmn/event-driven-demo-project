from dataclasses import dataclass
from typing import Optional
from access_management.domain.value_objects.email import Email
from access_management.domain.events.user_created import UserCreated

@dataclass
class User:
    username: str
    email: Email
    password: str
    is_active: bool = True

    # def __post_init__(self):
    #     if not self.id:
    #         self.id = self._generate_id()

    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

    # def create(self) -> UserCreated:
    #     if not self.is_active:
    #         raise ValueError("Cannot create an inactive user")
    #     return UserCreated(user_id=self.id, email=str(self.email))

    def deactivate(self):
        self.is_active = False