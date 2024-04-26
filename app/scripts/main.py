from pyscript import document
import json
from scripts.common.camera import Camera, CameraArray
from scripts.html_tools import build_element

VERSION = "v0.0.2"
DATA_PATH_META = "data/meta/payload_info_{data}.json"
DATA_PATH_NAMES = "data/meta/camera_names_{data}.txt"
DATA_PATH_BINARY_ORIGINAL = "data/original/binary/camera_data_{data}.bin"
DATA_PATH_BINARY_MODIFIED = "data/modified/{mod}/binary/camera_data_{data}.bin"
DATA = ("dppt", "hgss")
MODIFICATIONS = ()

document.getElementById("version").innerHTML = VERSION
app = document.getElementById("app")

def load_data(camera_array):
    app.innerHTML = ""
    print(camera_array)

def load_default_data(data):
    with open(DATA_PATH_META.format(data = data), "r") as metadata, \
        open(DATA_PATH_BINARY_ORIGINAL.format(data = data), "rb") as binary_data:
        try:
            with open(DATA_PATH_NAMES.format(data = data), "r") as labels:
                camera_array = CameraArray.from_files(metadata, binary_data, labels)
        except FileNotFoundError:
            print(f"not found, {DATA_PATH_NAMES.format(data = data)}")
            camera_array = CameraArray.from_files(metadata, binary_data)
    load_data(camera_array)

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