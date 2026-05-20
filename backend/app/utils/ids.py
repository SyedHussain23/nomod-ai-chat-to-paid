import secrets
import string

ALPHABET = string.ascii_lowercase + string.digits


def short_id(length: int = 8) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def payment_id() -> str:
    return f"pay_{short_id(10)}"


def link_token() -> str:
    return short_id(7)
