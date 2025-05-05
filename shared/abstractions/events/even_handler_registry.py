from abc import abstractmethod, ABC

from shared.abstractions.events.event_handler import TEvent, EventHandler


class EventHandlerRegistry(ABC):
    """Responsible for registration of EventHandlers, and matching
    them to Events.
    Is being used by EventDispatcher.
    """

    @abstractmethod
    def register(
        self, event_type: type[TEvent], event_handler: type[EventHandler[TEvent]]
    ) -> None: ...

    @abstractmethod
    def get(self, event: TEvent) -> list[type[EventHandler[TEvent]]]: ...
