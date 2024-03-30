from common.camera_codec import Camera
import json

def test_binary_decode_and_encode():
    with open("data/camera_data.bin", "rb") as data:
        for _ in range(16):
            bytes_initial = data.read(24)
            camera = Camera.from_bytes(bytes_initial)
            bytes_final = camera.to_bytes()
            assert bytes_final == bytes_initial

def test_json_decode_and_encode():
    with open("data/camera_data.bin", "rb") as data:
        for _ in range(16):
            json_initial = json.dumps(
                Camera.from_bytes(data.read(24)).to_json()
            )
            json_final = json.dumps(
                Camera.from_json(
                    json.loads(json_initial)
                ).to_json()
            )
            assert json_final == json_initial