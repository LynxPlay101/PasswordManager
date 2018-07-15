import base64


def encode(message: str) -> bytes:
    return base64.standard_b64encode(bytes(message, "utf-8"))


def decode(message: bytes) -> str:
    return str(base64.standard_b64decode(message), "utf-8")
