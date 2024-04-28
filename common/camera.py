import typing
import json
from scripts.common import util

class Camera:
    def __init__(self, parts: dict, label: str = None):
        self.parts = parts
        self.label = label

    @staticmethod
    def read_value(value_type: str, offset: int, data: bytes) -> typing.Any:
        return int.from_bytes(data[offset : offset + util.size_of(value_type)], "little")

    @staticmethod
    def write_value(value_type: str, value, offset: int, data: bytearray):
        size = util.size_of(value_type)
        data[offset : offset + size] = value.to_bytes(size, "little")
        

    @classmethod
    def from_bytes(cls, payload_info: dict, data: bytes, label: str = None):
        return cls(
            {
                key: cls.read_value(info["type"], info["offset"], data)
                for key, info in payload_info["schema"]["parts"].items()
            },
            label
        )

    def to_bytes(self, payload_info: dict, default_values: dict) -> bytes:
        data = bytearray(payload_info["schema"]["length"])
        for key, info in payload_info["schema"]["parts"].items():
            self.write_value(
                info["type"],
                self.parts[key] if key in self.parts else default_values[key],
                info["offset"],
                data
            )
        return bytes(data)

    def __str__(self):
        return f"{self.label}\nData: {self.parts}"

    def copy(self):
        return type(self)(self.parts.copy(), self.label)

    def to_json(self) -> dict:
        return {
            "label": self.label,
            "parts": self.parts
        }
    
    @classmethod
    def from_json(cls, obj: dict):
        return cls(obj["parts"], obj["label"])

class CameraArray:
    def __init__(self, payload_info: dict, cameras: typing.Iterable[Camera]):
        self.payload_info = payload_info
        self.cameras = [*cameras]
        self.default_values = self.cameras[0].parts.copy()

    @classmethod
    def from_bytes(cls,
        payload_info: dict,
        data: typing.Iterable[bytes],
        labels: typing.Iterable[typing.Optional[str]]
    ):
        return cls(
            payload_info,
            (
                Camera.from_bytes(payload_info, b, label)
                for b, label in zip(data, labels)
            )
        )

    def to_bytes(self) -> bytes:
        return b"".join(
            camera.to_bytes(self.payload_info, self.default_values)
            for camera in self.cameras
        )

    @classmethod
    def from_files(cls, 
        metadata: typing.TextIO,
        data: typing.BinaryIO,
        labels: typing.TextIO = None
    ):
        payload_info = json.load(metadata)
        byte_length = payload_info["schema"]["length"]
        n = payload_info["count"]
        parts = (data.read(byte_length) for _ in range(n))
        if labels == None:
            return cls.from_bytes(
                payload_info,
                parts,
                (None for _ in range(n))
            )
        return cls.from_bytes(
            payload_info,
            parts,
            (label.strip() for label in labels)
        )

    def __str__(self):
        return "\n".join(f"{i}: {camera}" for i, camera in enumerate(self.cameras))

    def __getitem__(self, slice) -> Camera:
        return self.cameras[slice]

    def __setitem__(self, slice, value: Camera):
        self.cameras[slice] = value

    def is_safe_value(self, part: str, value: int):
        return value >= 0 and value < 1 << 8 * util.size_of(self.payload_info["schema"]["parts"][part]["type"])

    def set_part_safe(self, i: int, part: str, value: int):
        if self.is_safe_value(part, value):
            self[i].parts[part] = value
            return True
        return False