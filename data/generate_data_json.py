import json

with open("camera_names.txt", "r") as names, \
    open("camera_data.bin", "rb") as data, \
    open("camera_data.json", "w") as out:
    get_int = lambda s : int.from_bytes(data.read(s), byteorder = "little")
    json.dump([
        {
            "name": names.readline().strip(),
            "distance": get_int(4),
            "angle": [
                get_int(2),
                get_int(2),
                get_int(2),
                get_int(2)
            ][: 3],
            "is_2d": bool(get_int(2)),
            "perspective": get_int(2),
            "near": get_int(4),
            "far": get_int(4)
        } 
        for _ in range(16)
    ], out, indent = 2)
