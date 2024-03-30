def generate_ar_code(
    address: int,
    data: bytes
) -> bytes:
    arr = bytearray(data + b"\0" * (7 - (len(data) - 1) % 8))
    for i in range(0, len(arr), 4):
        arr[i : i + 4] = arr[i + 3 : i - 1 if i else None : -1]
    return b"".join((
        (0xE0000000 | address).to_bytes(4),
        len(data).to_bytes(4),
        arr,
        b"\xD2\xB4\xC0\x1E\x36\x91\x20\x00"
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