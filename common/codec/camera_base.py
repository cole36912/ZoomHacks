import typing
from common.util import BracketFunction

class CameraBase:
    def __init__(self, label = None):
        self.label = label

    @classmethod
    def from_bytes(cls, data: bytes, label: str = None):
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        raise NotImplementedError()

@BracketFunction
def CameraArray(CameraType: type):
    class ReturnClass:
        def __init__(self, cameras: typing.Iterable[CameraType]):
            self.cameras = [*cameras]

        @classmethod
        def from_bytes(cls, 
            data: typing.Iterable[bytes],
            labels: typing.Iterable[typing.Optional[str]]
        ):
            return cls(
                CameraType.from_bytes(b, label)
                for b, label in zip(data, labels)
            )

        def to_bytes(self) -> bytes:
            return b"".join(camera.to_bytes() for camera in self.cameras)

        @classmethod
        def from_files(cls, 
            data: typing.BinaryIO,
            labels: typing.TextIO = None,
            n: int = 16
        ):
            parts = (data.read(CameraType.byte_length) for _ in range(n))
            if labels == None:
                return cls.from_bytes(
                    parts,
                    (None for _ in range(n))
                )
            return cls.from_bytes(
                parts,
                (label.strip() for label in labels)
            )

        @classmethod
        def from_json(cls, obj):
            return cls(CameraType.from_json(child) for child in obj)

        def to_json(self) -> list[CameraType]:
            return [camera.to_json() for camera in self.cameras]
    return ReturnClass