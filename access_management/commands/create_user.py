from dataclasses import dataclass


@dataclass
class CreateUser:
    name: str
    address: str
