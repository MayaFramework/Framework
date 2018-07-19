import os
import sys
from Framework.lib.file import utils

def get_base_framework_path():
    return os.path.dirname(__file__)

def get_environ_file():
    return os.path.join(os.path.dirname(__file__),"config","environ.json")

def get_environ_config():
    return utils.read_json(get_environ_file())

def get_css_path():
    from .lib.ui.css import get_css_path
    return get_css_path()

def get_icon_path():
    from .icons import get_icon_path
    return get_icon_path()

def get_uis_path():
	from .lib.ui.uis import get_uis_path
	return get_uis_path()
    
    
    
if __name__ == "__main__":
    pass