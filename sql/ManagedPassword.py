from __future__ import annotations

import PasswordCypher as pC


class ManagedPassword:
    url: str
    username: str
    password: str

    def __init__(self, url: str):
        self.url = url
        pass

    def __str__(self) -> str:
        return "ManagedPassword:[%s,%s,%s]" % (self.url, self.username, self.password)

    def equals(self, other: ManagedPassword) -> bool:
        if other is None:
            return False

        return self.url == other.url and self.password == other.password and self.username == other.username


pass


def new(url: str, username: str, password: str) -> ManagedPassword:
    p = ManagedPassword(url)
    p.username = username
    p.password = password
    return p


def new_decoded(url: str, username: bytes, password: bytes) -> ManagedPassword:
    return new(url, pC.decode(username), pC.decode(password))
