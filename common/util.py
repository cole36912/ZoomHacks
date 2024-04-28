def generate_ar_code(                                           # generate action replay code to write data to memory
    address: int,                                               # memory address
    data: bytes                                                 # data to write
) -> bytes:
    arr = bytearray(data + b"\0" * (7 - (len(data) - 1) % 8))   # pad to a multiple of 8 and copy to a mutable object
    for i in range(0, len(arr), 4):
        arr[i : i + 4] = arr[i + 3 : i - 1 if i else None : -1] # reverse every four bytes
    return b"".join((
        (0xE0000000 | address).to_bytes(4),                     # write instruction and address
        len(data).to_bytes(4),                                  # number of bytes to write
        arr,                                                    # bytes to write
        b"\xD2\xB4\xC0\x1E\x36\x91\x20\x00"                     # end code instruction
    ))

def generate_pretty_ar_code(                                    # generate text formatted code
    address: int,                                               # memory address
    data: bytes                                                 # data to write
) -> str:
    code = generate_ar_code(address, data)                      # get code as bytes
    return "\n".join(                                           # format code as text
        code[i : i + 8].hex(" ", 4).upper()
        for i in range(0, len(code), 8)
    )

class BracketFunction:
    def __init__(self, f):
        self.f = f

    def __getitem__(self, arg):
        return self.f(arg)

def re_nat_lte(x: int):
    options = []
    x = str(x)
    digits = len(x)
    options.append("0")
    if digits > 1:
        options.append(f"[1-9][0-9]{{0,{digits - 2}}}")
    if x[0] != "1":
        options.append(f"[1-{chr(ord(x[0]) - 1)}][0-9]{{{digits - 1}}}")
    for i in range(1, digits - 1):
        if x[i] != "0":
            options.append(f"{x[: i]}[0-{chr(ord(x[i]) - 1)}][0-9]{{{digits - i - 1}}}")
    options.append(f"{x[: -1]}[0-{x[-1]}]")
    return f"(?:{'|'.join(options)})"

def re_nat_lt(x: int):
    return re_nat_lte(x - 1)

def size_of(value_type):
    if value_type in ("int16", "uint16"):
        return 2
    if value_type in ("int32", "uint32"):
        return 4
    raise ValueError(value_type)