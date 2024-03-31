import json
from common.codec.camera_base import CameraArray
from common.codec.camera_dppt import CameraDPPt

with open("data/camera_names_dppt.txt", "r") as names, \
    open("data/camera_data_dppt.bin", "rb") as data, \
    open("data/camera_data_dppt.json", "w") as out:
    json.dump(CameraArray[CameraDPPt].from_files(data, names).to_json(), out, indent = 2)
