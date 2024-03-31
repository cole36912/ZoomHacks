import typing
from common.codec.camera_gen4_base import CameraGenIVBase

class CameraHGSS(CameraGenIVBase):
    byte_length = 36

    def __init__(self, 
        distance: int,                  # u32
        angle: typing.Iterable[int],    # u16 x 3
        is_2d: bool,                    # u16
        perspective: int,               # u16
        near: int,                      # u32
        far: int,                       # u32
        unk_0: int,                     # 32
        unk_1_0: int,                   # 16
        unk_1_1: int,                   # s16
        unk_2_0: int,                   # 16
        unk_2_1: int,                   # s16
        label: str = None,
        base: CameraGenIVBase = None
    ):
        super().__init__(
            distance = distance,
            angle = angle,
            is_2d = is_2d,
            perspective = perspective,
            near = near,
            far = far,
            label = label
        )
        self.unk_0 = unk_0
        self.unk_1_0 = unk_1_0
        self.unk_1_1 = unk_1_1
        self.unk_2_0 = unk_2_0
        self.unk_2_1 = unk_2_1

    @classmethod
    def from_bytes(cls, data: bytes, label: str = None):
        return super().from_bytes(
            data,
            label,
            unk_0 = int.from_bytes(data[24 : 28], "little"),
            unk_1_0 = int.from_bytes(data[28 : 30], "little"),
            unk_1_1 = int.from_bytes(data[30 : 32], "little"),
            unk_2_0 = int.from_bytes(data[32 : 34], "little"),
            unk_2_1 = int.from_bytes(data[34 : 36], "little")
        )

    def to_bytes(self):
        return b"".join((
            super().to_bytes(),
            self.unk_0.to_bytes(4, "little"),
            self.unk_1_0.to_bytes(2, "little"),
            self.unk_1_1.to_bytes(2, "little"),
            self.unk_2_0.to_bytes(2, "little"),
            self.unk_2_1.to_bytes(2, "little")
        ))