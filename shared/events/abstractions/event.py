from dataclasses import dataclass


@dataclass
class Event:
    name: str

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items()}
