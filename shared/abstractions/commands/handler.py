from abc import ABC

from shared.abstractions.commands.command import Command


class CommandHandler(ABC):
    def handle(self, command: Command):
        pass
