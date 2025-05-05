from dataclasses import dataclass
from shared.abstractions.events.event import Event

@dataclass
class UserCreated(Event):
    user_id: str
    email: str