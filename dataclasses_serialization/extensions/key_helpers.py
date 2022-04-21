from pydash import snake_case


def normalize_key_case(key: str) -> str:
    return snake_case(key)
