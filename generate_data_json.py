import json
from common.camera_codec import Camera

with open("data/camera_names.txt", "r") as names, \
    open("data/camera_data.bin", "rb") as data, \
    open("data/camera_data.json", "w") as out:
    json.dump([
        Camera.from_bytes(data.read(24), names.readline().strip()).to_json()
        for _ in range(16)
    ], out, indent = 2)
