from pyscript import document

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