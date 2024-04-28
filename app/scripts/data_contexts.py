from scripts.html_util import build_element

class DataContext:
    def __init__(self, value, size: int):
        self.element = self.create_element(value, size)
        self.element.onkeyup = self.update_row
        self.element.onchange = self.update_row
        self.size = size

    def is_valid(self) -> bool:
        return self.element.validity.valid

    def update_row(self, event):
        if self.is_valid():
            value = self.get_value()
            for context in self.row:
                if context is not self:
                    context.set_value(value)

    @staticmethod
    def create_element(value, size: int):
        return build_element("input", props = {"value": value})

    def get_value(self):
        return self.element.value

    def set_value(self, value):
        self.element.value = value

class IntContext(DataContext):
    @staticmethod
    def create_element(value: int, size: int):
        return build_element("input", props = {
            "type": "number",
            "value": value,
            "max": (1 << 8 * size - 1) - 1,
            "min": -(1 << 8 * size - 1),
            "required": True
        })

    def get_value(self) -> int:
        return int(self.element.value)

class UIntContext(IntContext):
    @staticmethod
    def create_element(value: int, size: int):
        return build_element("input", props = {
            "type": "number",
            "value": value,
            "max": (1 << 8 * size) - 1,
            "min": 0,
            "required": True
        })

class HexContext(DataContext):
    def __init__(self, value, size: int):
        super().__init__(value, size)
        self.element.onchange = self.captialize

    def captialize(self, event):
        self.element.value = self.element.value.upper()
        
    @staticmethod
    def create_element(value: int, size: int):
        return build_element("input", props = {
            "type": "text",
            "value": f"{{:0{2 * size}X}}".format(value),
            "pattern": f"^[0-9a-fA-F]{{{2 * size}}}$"
        })

    def get_value(self) -> int:
        return int(self.element.value, 16)
    
    def set_value(self, value):
        self.element.value = f"{{:0{2 * self.size}X}}".format(value)

class FloatContext(DataContext):
    @staticmethod
    def create_element(value: int, size: int):
        return build_element("input", props = {
            "type": "number",
            "value": round(value / 4096, 4),
            "max": (1 << 8 * size - 12) - 2e-4,
            "min": 0,
            "step": 1e-4,
            "required": True
        })

    def get_value(self) -> int:
        return round(float(self.element.value) * 4096)

    def set_value(self, value: int):
        self.element.value = round(value / 4096, 4)

class AngleContext(DataContext):
    @staticmethod
    def create_element(value: int, size: int):
        return build_element("input", props = {
            "type": "number",
            "value": round(value * 90 / 0x4000, 3),
            "max": 360 - 3e-3,
            "min": 0,
            "step": 1e-3,
            "required": True
        })

    def get_value(self) -> int:
        return round(float(self.element.value) * 0x4000 / 90)

    def set_value(self, value: int):
        self.element.value = round(value * 90 / 0x4000, 3)

class BooleanContext(DataContext):
    @staticmethod
    def create_element(value: int, size: int):
        return build_element("input", props = {
            "type": "checkbox",
            "checked": bool(value)
        })

    def get_value(self) -> int:
        return int(self.element.checked)

    def set_value(self, value: int):
        self.element.checked = bool(value)


DATA_CONTEXTS = {
    "int": IntContext,
    "hex": HexContext,
    "float": FloatContext,
    "angle": AngleContext,
    "bool": BooleanContext
}