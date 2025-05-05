from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Event:
    event_id: str
    event_type: str
    timestamp: datetime

    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()