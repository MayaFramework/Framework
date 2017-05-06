import os


def get_environ_file():
    return os.path.join(os.path.dirname(__file__),"environ.json")

def get_css_path():
    from .lib.gui.css import get_css_path
    return get_css_path()

def get_icon_path():
    from .icons import get_icon_path
    return get_icon_path()
