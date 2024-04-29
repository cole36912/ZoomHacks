from pyscript import document
import js

def build_element(tag, *children, props = {}):
    ret = document.createElement(tag)
    ret.replaceChildren(*children)
    for key, val in props.items():
        setattr(ret, key, val)
    return ret

def build_element_from_html(tag, html, props = {}):
    ret = document.createElement(tag)
    ret.innerHTML = html
    for key, val in props.items():
        setattr(ret, key, val)
    return ret

def clean_errors():
    for element in document.querySelectorAll("body > .py-error"):
        element.remove()

def make_action_link(text, action = lambda e : None):
    return build_element("a",
        text,
        props = {
            "href": "javascript:void",
            "onclick": action
        }
    )

def bytes_to_buffer(b: bytes):
    buffer = js.ArrayBuffer.new(len(b))
    view = js.DataView.new(buffer)
    for i, x in enumerate(b):
        view.setUint8(i, x)
    return buffer

def buffer_to_bytes(buffer) -> bytes:
    view = js.DataView.new(buffer)
    return bytes((view.getUint8(i) for i in range(view.byteLength)))