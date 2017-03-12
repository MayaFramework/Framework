import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

class customCmd(OpenMayaMPx.MPxCommand):
    def __init__(self, pluginName, pluginFunction):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.pluginName = pluginName
        self.pluginFunction = pluginFunction

    def doIt(self,argList):
        self.pluginFunction()
        
