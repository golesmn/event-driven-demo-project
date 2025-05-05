from dataclasses import dataclass

from access_management.application.commands.create_user import CreateUser
from shared.abstractions.commands.handler import CommandHandler
from shared.abstractions.events.handler import EventHandler


@dataclass
class User:
    name: str
    address: str
    age: int


class UserCreationHandler(CommandHandler):
    def handle(self, command: CreateUser):
        return command.__dict__
