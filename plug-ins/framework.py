import sys
import os
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import cmdLoader
import importlib

kPluginCmdName = "mainLoader"

def testFunction():
    print "mainLoader"

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
    for directory, module in allPlugins2Load(path):
        print "loading {}".format(module)
        importlib.import_module("module")

# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(cmdLoader.customCmd(kPluginCmdName, loadAllPlugins))
    
# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )