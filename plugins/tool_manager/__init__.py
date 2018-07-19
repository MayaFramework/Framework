import Framework
from Framework.lib.file import utils
import importlib
import inspect
import pprint
import json
import sys
import os
import importlib
from Framework.lib.config.config import Config 
def get_ext_tools():
    tools = []
    for ext_fold in Config.instance().environ["external_plugins"]:
        possible_folder = os.path.join(os.path.dirname(Framework.get_base_framework_path()), ext_fold)
        if os.path.exists(possible_folder):        
            base_import = ext_fold.replace("/",".")
            tools.extend(get_tools(base_import, possible_folder))
    return tools
        
        
def get_internal_tools():
    tools = []
    for ext_fold in Config.instance().environ["internal_plugins"]:
        possible_folder = os.path.join(os.path.dirname(Framework.get_base_framework_path()), ext_fold)
        if os.path.exists(possible_folder):        
            base_import = ext_fold.replace("/",".")
            tools.extend(get_tools(base_import, possible_folder))
    return tools
def get_tools(base_import, folder_path):
    tools = []

#     current_folder = os.path.dirname(os.path.dirname(__file__))
    tool_candidates = utils.get_subfolders(folder_path)

    for tool_candidate in tool_candidates:
        tool_info_file = os.path.join(tool_candidate, "info.json")
        if os.path.exists(tool_info_file):
            with open(tool_info_file) as tool_info_f:
                tool_info = json.load(tool_info_f)
                module_path = tool_candidate.replace(folder_path, "")
                tool_module = os.path.basename(tool_candidate)
                
                module_import = base_import
                module_import += ".".join(module_path.split(os.path.sep))
                #module_import += "import tool_def"
                #module_import += ".tool_def"

                mod = importlib.import_module(module_import)

                tool_info["definition"] = mod.tool_def()
                tool_info["path"] = tool_candidate

                tools.append(tool_info)

    return tools

def get_tools_from_folder_list(folder_list):
    result = []
    for folder in folder_list:
        result.extend(get_tools(folder))
    return result

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))

