import typing

class Camera:
    def __init__(self, 
        distance: int,                  # u32
        angle: typing.Iterable[int],    # u16 x 3
        is_2d: bool,                    # u16
        perspective: int,               # u16
        near: int,                      # u32
        far: int,                       # u32
        label = None
    ):
        self.distance = distance
        self.angle = (*(angle),)
        self.is_2d = is_2d
        self.perspective = perspective
        self.near = near
        self.far = far
        self.label = label

    @classmethod
    def from_bytes(cls, data: bytes, label: str = None):
        return cls(
            distance = int.from_bytes(data[: 4], "little"),
            angle = (*(
                int.from_bytes(data[i : i + 2], "little")
                for i in range(4, 10, 2)
            ),),
            is_2d = bool(int.from_bytes(data[12 : 14], "little")),
            perspective = int.from_bytes(data[14 : 16], "little"),
            near = int.from_bytes(data[16 : 20], "little"),
            far = int.from_bytes(data[20 : 24], "little"),
            label = label
        )

    def to_bytes(self):
        return b"".join((
            self.distance.to_bytes(4, "little"),
            *(
                self.angle[i].to_bytes(2, "little")
                for i in range(3)
            ),
            b"\0\0",
            b"\1\0" if self.is_2d else b"\0\0",
            self.perspective.to_bytes(2, "little"),
            self.near.to_bytes(4, "little"),
            self.far.to_bytes(4, "little")
        ))

    @classmethod
    def from_json(cls, obj):
        return cls(
            distance = obj["distance"],
            angle = (*obj["angle"],),
            is_2d = obj["is_2d"],
            perspective = obj["perspective"],
            near = obj["near"],
            far = obj["far"],
            label = obj["name"]
        )

    def to_json(self):
        return {
            "name": self.label,
            "distance": self.distance,
            "angle": [*self.angle],
            "is_2d": self.is_2d,
            "perspective": self.perspective,
            "near": self.near,
            "far": self.far
        }

class CameraArray:
    def __init__(self, cameras: typing.Iterable[Camera]):
        self.cameras = [*cameras]

    @classmethod
    def from_bytes(cls, 
        data: typing.Iterable[bytes],
        labels: typing.Iterable[typing.Optional[str]]
    ):
        return cls(
            Camera.from_bytes(b, label)
            for b, label in zip(data, labels)
        )

    def to_bytes(self):
        return b"".join(camera.to_bytes() for camera in self.cameras)

    @classmethod
    def from_files(cls, 
        data: typing.BinaryIO,
        labels: typing.TextIO = None,
        n: int = 16
    ):
        if labels == None:
            labels = (None,) * n
        else:
            labels = (*(labels.readline().strip() for _ in range(n)),)
        data = (*(data.read(24) for _ in range(n)),)
        return cls.from_bytes(data, labels)

    @classmethod
    def from_json(cls, obj):
        return cls(Camera.from_json(child) for child in obj)

    def to_json(self):
        return [camera.to_json() for camera in self.cameras]