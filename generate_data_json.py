import json
from common.camera_codec import CameraArray

with open("data/camera_names.txt", "r") as names, \
    open("data/camera_data.bin", "rb") as data, \
    open("data/camera_data.json", "w") as out:
    json.dump(CameraArray.from_files(data, names).to_json(), out, indent = 2)
