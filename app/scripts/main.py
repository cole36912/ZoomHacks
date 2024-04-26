from pyscript import document
import json
from scripts.common.camera import Camera, CameraArray
from scripts.html_tools import build_element, make_action_link

VERSION = "v0.0.3"
DATA_PATH_META = "data/meta/payload_info_{data}.json"
DATA_PATH_NAMES = "data/meta/camera_names_{data}.txt"
DATA_PATH_BINARY_ORIGINAL = "data/original/binary/camera_data_{data}.bin"
DATA_PATH_BINARY_MODIFIED = "data/modified/{mod}/binary/camera_data_{data}.bin"
DATA = ("dppt", "hgss")
MODIFICATIONS = ()

document.getElementById("version").innerHTML = VERSION
app = document.getElementById("app")
camera_array = None

def edit_camera(i: int):
    global camera_array
    camera = camera_array.cameras[i]
    app.replaceChildren(
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
                )
                for key, value in camera.parts.items()
            )
        )
    )

def show_cameras():
    global camera_array
    app.replaceChildren(
        build_element("table", *(
            build_element("tr",
                build_element("td", i, props = {"className": "id_col"}),
                build_element("td", camera.label),
                build_element("td", make_action_link("Edit...", lambda e : edit_camera(i))),
                build_element("td", make_action_link("Copy..")),
                build_element("td", make_action_link("Swap..")),
                build_element("td", make_action_link("Import from file..")),
                build_element("td", make_action_link("Export to file..")),
            )
            for i, camera in enumerate(camera_array.cameras)
        ))
    )
    print(camera_array)

def load_default_data(data):
    global camera_array
    with open(DATA_PATH_META.format(data = data), "r") as metadata, \
        open(DATA_PATH_BINARY_ORIGINAL.format(data = data), "rb") as binary_data:
        try:
            with open(DATA_PATH_NAMES.format(data = data), "r") as labels:
                camera_array = CameraArray.from_files(metadata, binary_data, labels)
        except FileNotFoundError:
            print(f"not found, {DATA_PATH_NAMES.format(data = data)}")
            camera_array = CameraArray.from_files(metadata, binary_data)
    show_cameras()

def main():
    app.replaceChildren(
        data_selector := build_element("select", *(
            build_element("option",
                f"{item} default",
                props = {
                    "value": item
                }
            )
            for item in DATA
        )),
        build_element("br"),
        build_element("button",
            "Use data",
            props = {
                "onclick": lambda e : load_default_data(data_selector.value)
            }
        ),
        build_element("button",
            "Use data from disk..."
        )
    )
main()