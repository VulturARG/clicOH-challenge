from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ServerConfiguration:
    api_root_url: str
    user: str
    password: str
