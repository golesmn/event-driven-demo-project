from abc import abstractmethod
from typing import Generic, TypeVar

from .event import Event

TEvent = TypeVar("TEvent", bound=Event)


class EventHandler(Generic[TEvent]):
    """Application-level EventHandler.
    Handles domain Events, these events are being handled in the same Transaction
    in which scope they were recorded - transactional processing.
    """

    @abstractmethod
    def handle(self, event: TEvent) -> None: ...