from common.codec.camera_dppt import CameraDPPt
from common.codec.camera_hgss import CameraHGSS
import json

def test_binary_decode_and_encode_dppt():
    with open("data/camera_data_dppt.bin", "rb") as data:
        for _ in range(16):
            bytes_initial = data.read(24)
            camera = CameraDPPt.from_bytes(bytes_initial)
            bytes_final = camera.to_bytes()
            assert bytes_final == bytes_initial

def test_json_decode_and_encode_dppt():
    with open("data/camera_data_dppt.bin", "rb") as data:
        for _ in range(16):
            json_initial = json.dumps(
                CameraDPPt.from_bytes(data.read(24)).to_json()
            )
            json_final = json.dumps(
                CameraDPPt.from_json(
                    json.loads(json_initial)
                ).to_json()
            )
            assert json_final == json_initial

def test_binary_decode_and_encode_hgss():
    with open("data/camera_data_hgss.bin", "rb") as data:
        for _ in range(17):
            bytes_initial = data.read(36)
            camera = CameraHGSS.from_bytes(bytes_initial)
            bytes_final = camera.to_bytes()
            assert bytes_final == bytes_initial