from abc import ABC, abstractmethod

from .event import Event


class EventDispatcher(ABC):
    """Responsible for dispatching Event objects on the boundaries
    of Domain and Application layer.
    """

    @abstractmethod
    def add(self, *events: Event) -> None: ...

    @abstractmethod
    def dispatch_all(self) -> None: ...