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