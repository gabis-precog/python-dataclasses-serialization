from pydash import snake_case


def normalize_key_case(key: str) -> str:
    """
    Normalize dataclass keys to match python conventions.
    """
    return snake_case(key)
