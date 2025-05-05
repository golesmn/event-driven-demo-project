from dataclasses import dataclass

from shared.abstractions.commands.command import Command

@dataclass
class CreateUser(Command):
    name: str
    address: str
