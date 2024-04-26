from pyscript import document
import json

VERSION = "v0.0.2"
DATA_PATH_META = "data/meta/payload_info_{data}.json"
DATA_PATH_NAMES = "data/meta/camera_names_{data}.json"
DATA_PATH_BINARY_ORIGINAL = "data/original/binary/camera_data_{data}.bin"
DATA_PATH_BINARY_MODIFIED = "data/modified/{mod}/binary/camera_data_{data}.bin"
DATA = ("dppt", "hgss")
MODIFICATIONS = ()

document.getElementById("version").innerHTML = VERSION
app = document.getElementById("app")

def load_data(meta, data):
    app.innerHTML = ""

def load_default_data(data):
    with open(DATA_PATH_META.format(data = data), "r") as file:
        meta = json.load(file)
    with open(DATA_PATH_BINARY_ORIGINAL.format(data = data), "rb") as file:
        binary_data = file.read()
    load_data(meta, binary_data)

def main():
    data_selector = document.createElement("select")
    for item in DATA:
        option = document.createElement("option")
        option.value = item
        option.innerHTML = f"{item} default"
        data_selector.appendChild(option)
    app.appendChild(data_selector)
    app.appendChild(document.createElement("br"))
    use_data = document.createElement("button")
    use_data.innerHTML = "Use data"
    use_data.onclick = lambda e : load_default_data(data_selector.value)
    app.appendChild(use_data)
    upload_data = document.createElement("button")
    upload_data.innerHTML = "Use data from disk..."
    app.appendChild(upload_data)
main()