import json
from common.camera_codec import CameraArray
import common.util as util
import io

with open("data/camera_data.bin", "rb") as data:
    data = data.read(24 * 16)
    with open("ar_codes/control.txt", "w") as file:                     # code for default values, should have no effect
        file.write(util.generate_pretty_ar_code(0x021F6608, data))
    arr = CameraArray.from_files(io.BytesIO(data))
    buildings = next(camera for camera in arr.cameras if camera.is_2d)  # get the first (and only) 2d camera
    arr.cameras = [buildings] * 16                                      # assign to all cameras
    with open("ar_codes/2d.txt", "w") as file:                          # code to make all cameras the same as the building camera
        file.write(util.generate_pretty_ar_code(0x021F6608, arr.to_bytes()))
        