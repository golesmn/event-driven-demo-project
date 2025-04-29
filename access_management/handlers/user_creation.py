from dataclasses import dataclass

from commands.create_user import CreateUser


@dataclass
class User:
    name: str
    address: str
    age: int


class UserCreationHandler:
    @classmethod
    def handle(cls, command: CreateUser):
        return command.__dict__
