from Framework.lib.file import utils
import importlib
import inspect
import pprint
import json
import sys
import os
import importlib
from Framework.lib.config.config import Config 

def get_tools():
    tools = []

    current_folder = os.path.dirname(os.path.dirname(__file__))
    tool_candidates = utils.get_subfolders(current_folder)

    for tool_candidate in tool_candidates:
        tool_info_file = os.path.join(tool_candidate, "info.json")
        if os.path.exists(tool_info_file):
            with open(tool_info_file) as tool_info_f:
                tool_info = json.load(tool_info_f)
                module_path = tool_candidate.replace(current_folder, "")
                tool_module = os.path.basename(tool_candidate)
                
                module_import = "Framework.plugins"
                module_import += ".".join(module_path.split(os.path.sep))
                #module_import += "import tool_def"
                #module_import += ".tool_def"

                mod = importlib.import_module(module_import)

                tool_info["definition"] = mod.tool_def()
                tool_info["path"] = tool_candidate

                tools.append(tool_info)

    return tools


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))

