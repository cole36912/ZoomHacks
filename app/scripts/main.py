from pyscript import document, window
import js
import json
from scripts.common.camera import Camera, CameraArray
from scripts.common import util
from scripts.html_util import build_element, make_action_link, bytes_to_buffer, buffer_to_bytes
from scripts.data_contexts import DATA_CONTEXTS, UIntContext, HexContext
import io

VERSION = "v0.0.8"
DATA_PATH_META = "data/meta/payload_info_{data}.json"
DATA_PATH_NAMES = "data/meta/camera_names_{data}.txt"
DATA_PATH_BINARY_ORIGINAL = "data/original/binary/camera_data_{data}.bin"
DATA_PATH_BINARY_MODIFIED = "data/modified/{mod}/binary/camera_data_{data}.bin"
DATA = ("dppt", "hgss")
MODIFICATIONS = ()

document.getElementById("version").innerHTML = VERSION

class App:
    app = document.getElementById("app")
    camera_array: CameraArray = None

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
            size = cls.camera_array.payload_info["schema"]["parts"][key]["size"]
            row = (
                cls.context_of(key)(value, size),
                UIntContext(value, size),
                HexContext(value, size)
            )
            for context in row:
                context.row = row
            contextual_values[key] = row
        def save_values():
            camera.label = label.value
            if not all(
                value.is_valid()
                for row in contextual_values.values()
                for value in row
            ):
                return window.alert("Fix invalid values")
            for key in camera.parts:
                camera.parts[key] = contextual_values[key][1].get_value()
            return True
        cls.render_nodes(
            build_element("h3", f"Camera {i}"),
            build_element("label",
                "Label: ",
                props = {
                    "for": "label"
                }
            ),
            label := build_element("input",
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
                    ),
                    props = {"className": "table"}
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
                        "Save",
                        props = {
                            "onclick": lambda e : save_values() and cls.show_cameras()
                        }
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
    def generate_ar_codes(cls):
        cls.render_nodes(
            build_element("table",
                build_element("tr",
                    build_element("td",
                        make_action_link("Back", lambda e : cls.show_cameras())
                    )
                ),
                props = {"className": "menu_bar"}
            ),
            *(
                build_element("details",
                    build_element("summary", key),
                    build_element("code", props = {
                        "innerHTML": util.generate_pretty_ar_code(
                            int(address, 16),
                            cls.camera_array.to_bytes(),
                            "<br>"
                        )
                    })
                )
                for key, address in cls.camera_array.payload_info["addresses"].items()
            )
        )

    @classmethod
    def copy_camera(cls, source: int):
        targets = window.prompt("Enter target indices separated by commas or \"*\" for all")
        if targets == None:
            return
        n = len(cls.camera_array.cameras)
        if targets == "*":
            targets = {*range(n)}
        else:
            try:
                targets = {int(i) for i in targets.split(",")}
                assert all(i < n for i in targets)
            except (ValueError, AssertionError):
                return window.alert("One or more values were invalid")
        targets -= {source}
        for target in targets:
            cls.camera_array[target] = cls.camera_array[source].copy()
        cls.show_cameras()

    @classmethod
    def swap_camera(cls, source: int):
        target = window.prompt("Enter target index")
        if target == None:
            return
        n = len(cls.camera_array.cameras)
        try:
            target = int(target)
            assert target < n
        except (ValueError, AssertionError):
            return window.alert("Invalid index")
        temp = cls.camera_array[source]
        cls.camera_array[source] = cls.camera_array[target]
        cls.camera_array[target] = temp
        cls.show_cameras()

    @classmethod
    def import_camera(cls, i: int):
        build_element("input", props = {
            "type": "file",
            "accept": ".json",
            "onchange": lambda event : 
                event.target.files.item(0).text().then(
                    lambda text : (
                        cls.camera_array.__setitem__(i, 
                            Camera.from_json(json.loads(text))
                        ), 
                        cls.show_cameras()
                    )
                )
        }).click()

    @classmethod
    def export_camera(cls, i: int):
        build_element("a", props = {
            "href": window.URL.createObjectURL(
                js.Blob.new((
                    json.dumps(cls.camera_array[i].to_json()),
                ))
            ),
            "download": "camera.json"
        }).click()

    @classmethod
    def export_array_data(cls):
        build_element("a", props = {
            "href": window.URL.createObjectURL(
                js.Blob.new((
                    bytes_to_buffer(cls.camera_array.to_bytes()),
                ))
            ),
            "download": "camera_data.bin"
        }).click()

    @classmethod
    def export_array_names(cls):
        build_element("a", props = {
            "href": window.URL.createObjectURL(
                js.Blob.new((
                    f"{camera.label}\n"
                    for camera in cls.camera_array.cameras
                ))
            ),
            "download": "camera_names.txt"
        }).click()

    @classmethod
    def show_cameras(cls):
        cls.render_nodes(
            build_element("table",
                build_element("tr",
                    build_element("td",
                        make_action_link("Close", lambda e : cls.main())
                    ),
                    build_element("td",
                        make_action_link("Batch Action...", lambda e : cls.batch_action())
                    ),
                    build_element("td",
                        make_action_link("Generate AR Codes", lambda e : cls.generate_ar_codes())
                    ),
                    build_element("td",
                        make_action_link("Export data to file...", lambda e : cls.export_array_data())
                    ),
                    build_element("td",
                        make_action_link("Export names to file...", lambda e : cls.export_array_names())
                    )
                ),
                props = {"className": "menu_bar"}
            ),
            build_element("table",
                *(
                    build_element("tr",
                        build_element("td", i, props = {"className": "id_col"}),
                        build_element("td", camera.label),
                        build_element("td", make_action_link("Edit...", (lambda x : lambda e : cls.edit_camera(x))(i))),
                        build_element("td", make_action_link("Copy...", (lambda x : lambda e : cls.copy_camera(x))(i))),
                        build_element("td", make_action_link("Swap...", (lambda x : lambda e : cls.swap_camera(x))(i))),
                        build_element("td", make_action_link("Import from file...", (lambda x : lambda e : cls.import_camera(x))(i))),
                        build_element("td", make_action_link("Export to file...", (lambda x : lambda e : cls.export_camera(x))(i))),
                    )
                    for i, camera in enumerate(cls.camera_array.cameras)
                ),
                props = {"className": "table"}
            )
        )

    @classmethod
    def batch_action(cls):
        def execute():
            if not targets_input.validity.valid:
                return window.alert("Invalid targets")
            if not value_input.validity.valid:
                return window.alert("Invalid value")
            targets = targets_input.value
            part = part_select.value
            op = op_select.value
            if op == "mult":
                op_val = float(value_input.value)
            else:
                try:
                    op_val = int(value_input.value)
                except ValueError:
                    return window.alert("Integer required for selected operation")
            n = len(cls.camera_array.cameras)
            if targets == "*":
                targets = (*range(n),)
            else:
                targets = (*(int(i) for i in targets.split(",")),)
            if op == "set":
                values = [op_val for _ in targets]
            else:
                values = [cls.camera_array[i].parts[part] for i in targets]
                if op == "add":
                    for i in range(len(values)):
                        values[i] += op_val
                elif op == "mult":
                    for i in range(len(values)):
                        values[i] = round(values[i] * op_val)
                elif op == "or":
                    for i in range(len(values)):
                        values[i] |= op_val
                else:
                    raise Exception(op)
            if not all(
                cls.camera_array.is_safe_value(part, value)
                for value in values
            ):
                return window.alert("Resulting values were invalid")
            for i, value in zip(targets, values):
                cls.camera_array[i].parts[part] = value
            return True
        cls.render_nodes(
            build_element("div",
                build_element("table",
                    build_element("tr",
                        build_element("td", "Target rows:"),
                        build_element("td",
                            targets_input := build_element("input", props = {
                                "type": "text",
                                "value": "*",
                                "pattern": (
                                    v := util.re_nat_lt(len(cls.camera_array.cameras)),
                                    f"^ *\\* *| *{v}(?: *, *{v})* *$"
                                )[1],
                                "required": True
                            })
                        )
                    ),
                    build_element("tr",
                        build_element("td", "Property:"),
                        build_element("td",
                            part_select := build_element("select", *(
                                build_element("option",
                                    part,
                                    props = {"value": part}
                                )
                                for part in cls.camera_array.payload_info["schema"]["parts"]
                            ))
                        )
                    ),
                    build_element("tr",
                        build_element("td", "Operation:"),
                        build_element("td",
                            op_select := build_element("select", *(
                                build_element("option",
                                    desc,
                                    props = {"value": op}
                                )
                                for op, desc in (
                                    ("set", "Set value"),
                                    ("add", "Add value"),
                                    ("mult", "Multiply value"),
                                    ("or", "Bitwise OR")
                                )
                            ))
                        )
                    ),
                    build_element("tr",
                        build_element("td", "Value (Base 10 integer):"),
                        build_element("td",
                            value_input := build_element("input", props = {
                                "type": "text",
                                "value": "2731713",
                                "pattern": "^ *[0-9]*\\.?[0-9]* *$",
                                "required": True
                            })
                        )
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
                        "Execute",
                        props = {
                            "onclick": lambda e : execute() and cls.show_cameras()
                        }
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
    def load_file_data(cls, data):
        def process_files(event):
            target = event.target
            def select(binary_index, labels):
                target.files.item(binary_index).arrayBuffer().then(lambda buffer : (
                    setattr(
                        cls,
                        "camera_array",
                        CameraArray.from_files(
                            metadata := open(DATA_PATH_META.format(data = data), "r"),
                            io.BytesIO(buffer_to_bytes(buffer)),
                            labels
                        )
                    ),
                    metadata.close(),
                    labels != None and labels.close(),
                    cls.show_cameras()
                ))

            labels_index = None
            if target.files.length == 1:
                binary_index = 0
            else:
                for i in range(target.files.length):
                    ext = target.files.item(i).name.rsplit(".", maxsplit = 1)[-1]
                    if ext == "txt":
                        labels_index = i
                    elif ext == "bin":
                        binary_index = i
            if labels_index == None:
                try:
                    select(binary_index, open(DATA_PATH_NAMES.format(data = data), "r"))
                except FileNotFoundError:
                    print(f"not found, {DATA_PATH_NAMES.format(data = data)}")
                    select(binary_index, None)
            else:
                target.files.item(labels_index).text().then(lambda text : (
                    select(binary_index, io.StringIO(text))
                ))
            
        build_element("input", props = {
            "type": "file",
            "accept": ".bin,.txt",
            "onchange": lambda event : process_files(event),
            "multiple": True
        }).click()

    @classmethod
    def render_nodes(cls, *nodes):
        cls.app.replaceChildren(*nodes)

    @classmethod
    def main(cls):
        cls.render_nodes(
            build_element("table",
                build_element("tr",
                    build_element("td",
                        data_selector := build_element("select", *(
                            build_element("option",
                                f"{item} default",
                                props = {"value": item}
                            )
                            for item in DATA
                        ))
                    ),
                    build_element("td",
                        build_element("button",
                            "Use data",
                            props = {
                                "onclick": lambda e : cls.load_default_data(data_selector.value)
                            }
                        )
                    )
                ),
                build_element("tr",
                    build_element("td",
                        payload_selector := build_element("select", *(
                            build_element("option",
                                item,
                                props = {"value": item}
                            )
                            for item in DATA
                        ))
                    ),
                    build_element("td",
                        build_element("button",
                            "Import data...",
                            props = {
                                "onclick": lambda e : cls.load_file_data(payload_selector.value)
                            }
                        )
                    )
                )
            )
        )
App.main()