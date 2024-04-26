import json
from common.codec.camera_base import CameraArray
from common.codec.camera_dppt import CameraDPPt
from common.codec.camera_hgss import CameraHGSS
import common.util as util
import io

# DPPt
with open("data/original/binary/camera_data_dppt.bin", "rb") as data, \
    open("data/meta/payload_info_dppt.json", "r") as meta:
    meta = json.load(meta)
    addr_dp = int(meta["addresses"]["dp"], 16)
    addr_pt = int(meta["addresses"]["pt"], 16)
    data = data.read(CameraDPPt.byte_length * meta["count"])
    with open("ar_codes/dp/control.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(addr_dp, data))
    with open("ar_codes/pt/control.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(addr_pt, data))
    arr = CameraArray[CameraDPPt].from_files(io.BytesIO(data))
    buildings = next(camera for camera in arr.cameras if camera.is_2d)        # get the first (and only) 2d camera
    arr.cameras = [buildings] * meta["count"]                                 # assign to all cameras
    with open("ar_codes/dp/2d.txt", "w") as file:                             # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(addr_dp, arr.to_bytes()))
    with open("ar_codes/pt/2d.txt", "w") as file:                             # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(addr_pt, arr.to_bytes()))

with open("data/modified/2x_zoom_out/binary/camera_data_dppt.bin", "rb") as data, \
    open("data/meta/payload_info_dppt.json", "r") as meta:
    meta = json.load(meta)
    addr_dp = int(meta["addresses"]["dp"], 16)
    addr_pt = int(meta["addresses"]["pt"], 16)
    data = data.read(CameraDPPt.byte_length * meta["count"])
    with open("ar_codes/dp/2x_zoom_out.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(addr_dp, data))

with open("data/modified/360p/binary/camera_data_dppt.bin", "rb") as data, \
    open("data/meta/payload_info_dppt.json", "r") as meta:
    meta = json.load(meta)
    addr_dp = int(meta["addresses"]["dp"], 16)
    addr_pt = int(meta["addresses"]["pt"], 16)
    data = data.read(CameraDPPt.byte_length * meta["count"])
    with open("ar_codes/dp/360p.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(addr_dp, data))

# HGSS
with open("data/original/binary/camera_data_hgss.bin", "rb") as data, \
    open("data/meta/payload_info_hgss.json", "r") as meta:
    meta = json.load(meta)
    addr_hgss = int(meta["addresses"]["hgss"], 16)
    data = data.read(CameraHGSS.byte_length * meta["count"])
    with open("ar_codes/hgss/control.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(addr_hgss, data))
    arr = CameraArray[CameraHGSS].from_files(io.BytesIO(data))
    buildings = next(camera for camera in arr.cameras if camera.is_2d)          # get the first 2d camera
    arr.cameras = [buildings] * meta["count"]                                   # assign to all cameras
    with open("ar_codes/hgss/2d.txt", "w") as file:                             # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(addr_hgss, arr.to_bytes()))
        