code = 0xE0000000

def generate_ar_code(
    address: int,
    data: bytes
) -> bytes:
    data = bytearray(data + b"\0" * (7 - (len(data) - 1) % 8))
    for i in range(0, len(data), 4):
        data[i : i + 4] = data[i + 3 : i - 1 if i else None : -1]
    return b"".join((
        (code + address).to_bytes(4),
        len(data).to_bytes(4),
        data
    ))

def generate_pretty_ar_code(
    address: int,
    data: bytes
) -> str:
    code = generate_ar_code(address, data)
    return "\n".join(
        code[i : i + 8].hex(" ", 4).upper()
        for i in range(0, len(code), 8)
    )