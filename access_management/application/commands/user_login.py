from dataclasses import dataclass


@dataclass
class UserLogin:
    username: str
    email: str
    password: str