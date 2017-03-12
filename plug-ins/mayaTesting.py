import os
import sys

def allPlugins2Load(MAYA_PLUG_IN_PATH=None):
    if not MAYA_PLUG_IN_PATH:
        MAYA_PLUG_IN_PATH == os.environ["MAYA_PLUG_IN_PATH"]
    directory_list = list()
    modules_imports = list()
    for root, dirs, files in os.walk(MAYA_PLUG_IN_PATH, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name, "mayaInit.py"))
            modules_imports.append(name + ".mayaInit")
    return directory_list, modules_imports

def loadAllPlugins():
    path = r"C:\Users\Alberto\Documents\maya\2017\plug-ins"
    directory, module =  allPlugins2Load(path)
    print module
    # for directory, module in allPlugins2Load(path):
    #     print "loading {}".format(module)
    #     importlib.import_module("module")

print loadAllPlugins()