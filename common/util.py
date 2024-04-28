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
    data: bytes,                                                # data to write
    sep: str = "\n"
) -> str:
    code = generate_ar_code(address, data)                      # get code as bytes
    return sep.join(                                            # format code as text
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
    digits = len(x) # n
    options.append("0") # allow 0
    if digits > 1:
        options.append(f"[1-9][0-9]{{0,{digits - 2}}}") # allow [1, 9{n-1}]
    if x[0] != "1":
        options.append(f"[1-{chr(ord(x[0]) - 1)}][0-9]{{{digits - 1}}}") # allow [10{n-1}, (x[0]-1)9{n-1}]
    for i in range(1, digits - 1): # i in [1, n-2]
        if x[i] != "0":
            options.append(f"{x[: i]}[0-{chr(ord(x[i]) - 1)}][0-9]{{{digits - i - 1}}}") # allow [x[0-(i-1)]0{n-i}, x[0-(i-1)](x[i]-1)0{n-i-1}]
    options.append(f"{x[: -1]}[0-{x[-1]}]") # allow [x[0-(n-2)]0, x]
    return f"(?:{'|'.join(options)})"

def re_nat_lt(x: int):
    return re_nat_lte(x - 1)

def uint_to_int(size: int, value: int) -> int:
    return int.from_bytes(value.to_bytes(size), signed = True)

def int_to_uint(size: int, value: int) -> int:
    return int.from_bytes(value.to_bytes(size, signed = True))