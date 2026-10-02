ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = len(ALPHABET)


def encode_base62(value: int) -> str:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be >= 0")
    if value == 0:
        return ALPHABET[0]
    out = []
    while value > 0:
        value, rem = divmod(value, BASE)
        out.append(ALPHABET[rem])
    return "".join(reversed(out))
