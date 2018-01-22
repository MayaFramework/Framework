import maya.api.OpenMaya as om


def info(message):
    om.MGlobal.displayInfo(message)


def warning(message):
    om.MGlobal.displayWarning(message)


def error(message):
    om.MGlobal.displayError(message)
