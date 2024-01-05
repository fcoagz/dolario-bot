from dataclasses import dataclass

@dataclass
class User:
    id: int
    created: str
    user: dict