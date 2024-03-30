class Camera:
    def __init__(self, 
        distance: int,      # u32
        angle: tuple[int],  # u16 x 3
        is_2d: bool,        # u16
        perspective: int,   # u16
        near: int,          # u32
        far: int,           # u32
        label = None
    ):
        self.distance = distance
        self.angle = angle
        self.is_2d = is_2d
        self.perspective = perspective
        self.near = near
        self.far = far
        self.label = label

    @classmethod
    def from_bytes(cls, data, label = None):
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