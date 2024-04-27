from pyscript import document
import json
from scripts.common.camera import Camera, CameraArray
from scripts.html_util import build_element, make_action_link
from scripts.data_contexts import DATA_CONTEXTS, UIntContext, HexContext

VERSION = "v0.0.4"
DATA_PATH_META = "data/meta/payload_info_{data}.json"
DATA_PATH_NAMES = "data/meta/camera_names_{data}.txt"
DATA_PATH_BINARY_ORIGINAL = "data/original/binary/camera_data_{data}.bin"
DATA_PATH_BINARY_MODIFIED = "data/modified/{mod}/binary/camera_data_{data}.bin"
DATA = ("dppt", "hgss")
MODIFICATIONS = ()

document.getElementById("version").innerHTML = VERSION

class App:
    app = document.getElementById("app")
    camera_array = None

    @classmethod
    def size_of(cls, key):
        value_type = cls.camera_array.payload_info["schema"]["parts"][key]["type"]
        if value_type in ("int16", "uint16"):
            return 2
        if value_type in ("int32", "uint32"):
            return 4

    @classmethod
    def context_of(cls, key):
        part = cls.camera_array.payload_info["schema"]["parts"][key]
        if "context" in part:
            return DATA_CONTEXTS[part["context"]]
        return UIntContext
    
    @classmethod
    def edit_camera(cls, i: int):
        camera = cls.camera_array.cameras[i]
        contextual_values = {}
        for key, value in camera.parts.items():
            size = cls.size_of(key)
            row = (
                cls.context_of(key)(value, size),
                UIntContext(value, size),
                HexContext(value, size)
            )
            for context in row:
                context.row = row
            contextual_values[key] = row
        cls.render_nodes(
            build_element("h3", f"Camera {i}"),
            build_element("label",
                "Label: ",
                props = {
                    "for": "label"
                }
            ),
            build_element("input",
                props = {
                    "id": "label",
                    "type": "text",
                    "value": camera.label
                }
            ),
            build_element("br"),
            build_element("br"),
            build_element("div",
                build_element("table",
                    build_element("tr",
                        build_element("th", "Property"),
                        build_element("th", "Contextual Value"),
                        build_element("th", "Base 10 Value"),
                        build_element("th", "Hexadecimal Value")
                    ),
                    *(  
                        build_element("tr",
                            build_element("td", key),
                            *(
                                build_element("td", contextual_value.element)
                                for contextual_value in contextual_values[key]
                            )
                        )
                        for key in camera.parts
                    )
                ),
                build_element("br"),
                build_element("div",
                    build_element("button",
                        "Cancel",
                        props = {
                            "onclick": lambda e : cls.show_cameras()
                        }
                    ),
                    build_element("button",
                        "Save"
                    ),
                    props = {
                        "style": "text-align: right;",
                    }
                ),
                props = {
                    "style": "display: inline-block;"
                }
            )
        )

    @classmethod
    def show_cameras(cls):
        cls.render_nodes(
            build_element("table", *(
                build_element("tr",
                    build_element("td", i, props = {"className": "id_col"}),
                    build_element("td", camera.label),
                    build_element("td", make_action_link("Edit...", (lambda x : lambda e : cls.edit_camera(x))(i))),
                    build_element("td", make_action_link("Copy..")),
                    build_element("td", make_action_link("Swap..")),
                    build_element("td", 
                        make_action_link("Import from file..")
                    ),
                    build_element("td", make_action_link("Export to file..")),
                )
                for i, camera in enumerate(cls.camera_array.cameras)
            ))
        )
        print(cls.camera_array)

    @classmethod
    def load_default_data(cls, data):
        with open(DATA_PATH_META.format(data = data), "r") as metadata, \
            open(DATA_PATH_BINARY_ORIGINAL.format(data = data), "rb") as binary_data:
            try:
                with open(DATA_PATH_NAMES.format(data = data), "r") as labels:
                    cls.camera_array = CameraArray.from_files(metadata, binary_data, labels)
            except FileNotFoundError:
                print(f"not found, {DATA_PATH_NAMES.format(data = data)}")
                cls.camera_array = CameraArray.from_files(metadata, binary_data)
        cls.show_cameras()

    @classmethod
    def render_nodes(cls, *nodes):
        cls.app.replaceChildren(*nodes)

    @classmethod
    def main(cls):
        cls.render_nodes(
            data_selector := build_element("select", *(
                build_element("option",
                    f"{item} default",
                    props = {
                        "value": item
                    }
                )
                for item in DATA
            )),
            build_element("button",
                "Use data",
                props = {
                    "onclick": lambda e : cls.load_default_data(data_selector.value)
                }
            ),
            build_element("br"),
            build_element("button",
                "Use data from disk..."
            )
        )
App.main()