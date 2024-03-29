from common.camera_codec import Camera

def test_decode_and_encode():
    with open("data/camera_data.bin", "rb") as data:
        for _ in range(16):
            bytes_initial = data.read(24)
            camera = Camera.from_bytes(bytes_initial)
            bytes_final = camera.to_bytes()
            assert bytes_final == bytes_initial