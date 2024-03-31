import json
from common.codec.camera_base import CameraArray
from common.codec.camera_dppt import CameraDPPt
from common.codec.camera_hgss import CameraHGSS
import common.util as util
import io

# DPPt
with open("data/original/binary/camera_data_dppt.bin", "rb") as data:
    data = data.read(CameraDPPt.byte_length * 16)
    with open("ar_codes/dp/control.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(0x021F6608, data))
    with open("ar_codes/pt/control.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(0x021F8AE4, data))
    arr = CameraArray[CameraDPPt].from_files(io.BytesIO(data))
    buildings = next(camera for camera in arr.cameras if camera.is_2d)        # get the first (and only) 2d camera
    arr.cameras = [buildings] * 16                                            # assign to all cameras
    with open("ar_codes/dp/2d.txt", "w") as file:                             # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(0x021F6608, arr.to_bytes()))
    with open("ar_codes/pt/2d.txt", "w") as file:                             # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(0x021F8AE4, arr.to_bytes()))

# HGSS
with open("data/original/binary/camera_data_hgss.bin", "rb") as data:
    data = data.read(CameraHGSS.byte_length * 17)
    with open("ar_codes/hgss/control.txt", "w") as file:                        # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(0x02206478, data))
    arr = CameraArray[CameraHGSS].from_files(io.BytesIO(data))
    buildings = next(camera for camera in arr.cameras if camera.is_2d)          # get the first 2d camera
    arr.cameras = [buildings] * 17                                              # assign to all cameras
    with open("ar_codes/hgss/2d.txt", "w") as file:                             # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(0x02206478, arr.to_bytes()))
        