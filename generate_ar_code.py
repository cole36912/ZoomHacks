import json
from common.camera_codec import CameraArray
import common.util as util
import io

with open("data/camera_data.bin", "rb") as data:
    data = data.read(24 * 16)
    with open("ar_codes/control.txt", "w") as file:
        file.write(util.generate_pretty_ar_code(0x021F6608, data))
    arr = CameraArray.from_files(io.BytesIO(data))
    buildings = next(camera for camera in arr.cameras if camera.is_2d)
    arr.cameras = [buildings] * 16
    with open("ar_codes/2d.txt", "w") as file:
        file.write(util.generate_pretty_ar_code(0x021F6608, arr.to_bytes()))
        