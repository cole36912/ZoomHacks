import typing
import json

class Camera:
    def __init__(self, payload_info: dict, parts: dict, label: str = None):
        self.payload_info = payload_info
        self.parts = parts
        self.label = label

    @staticmethod
    def read_value(value_type: str, offset: int, data: bytes) -> typing.Any:
        if value_type in ("int16", "uint16"):
            return int.from_bytes(data[offset : offset + 2], "little")
        if value_type in ("int32", "uint32"):
            return int.from_bytes(data[offset : offset + 4], "little")
        raise ValueError(value_type)

    @staticmethod
    def write_value(value_type: str, value, offset: int, data: bytearray):
        if value_type in ("int16", "uint16"):
            data[offset : offset + 2] = value.to_bytes(2, "little")
            return
        if value_type in ("int32", "uint32"):
            data[offset : offset + 4] = value.to_bytes(4, "little")
            return
        raise ValueError(value_type)
        

    @classmethod
    def from_bytes(cls, payload_info: dict, data: bytes, label: str = None):
        return cls(
            payload_info,
            {
                key: cls.read_value(info["type"], info["offset"], data)
                for key, info in payload_info["schema"]["parts"].items()
            },
            label
        )

    def to_bytes(self) -> bytes:
        data = bytearray(length = self.payload_info["schema"]["length"])
        for key, info in self.payload_info["schema"]["parts"].items():
            self.write_value(info["type"], self.parts[key], info["offset"], data)
        return bytes(data)

    def __str__(self):
        return f"{self.label}\nMeta: {self.payload_info}\nData: {self.parts}"

class CameraArray:
    def __init__(self, cameras: typing.Iterable[Camera]):
        self.cameras = [*cameras]

    @classmethod
    def from_bytes(cls,
        payload_info: dict,
        data: typing.Iterable[bytes],
        labels: typing.Iterable[typing.Optional[str]]
    ):
        return cls(
            Camera.from_bytes(payload_info, b, label)
            for b, label in zip(data, labels)
        )

    def to_bytes(self) -> bytes:
        return b"".join(camera.to_bytes() for camera in self.cameras)

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