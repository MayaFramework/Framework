from Framework.plugins.dependency_uploader.uploader_window import UploaderWindow
import maya.cmds as MC
import maya.mel as MM
import Framework.plugins.renamer.controller as renamerController;  reload(renamerController)
import os


class NoChangesDetected(Exception):
    pass


def checkSceneName(path):
    try:
        rename = renamerController.Renamer()
        folder, filename = os.path.normpath(path).replace("\\", "/").rsplit("/", 1)
        folder_fields = rename.get_fields_from_folder_path(folder)
        rename.check_fields_value(folder_fields)
        return rename.check_fields_value(folder_fields)
    except renamerController.WrongNameFormatting:
        return False


def getCorrectName(path=None):
    if not path:
        path = MC.file(q=True, sn=True)
    rename = renamerController.Renamer()
    folder, filename = os.path.normpath(path).replace("\\", "/").rsplit("/", 1)
    folder_fields = rename.get_fields_from_folder_path(folder)
    return rename.generate_complete_file_path(folder_fields)


def canSceneBeSaved():
    modified = MC.file(mf=True, q=True)
    if not modified:
        raise NoChangesDetected()
    path = MC.file(q=True, sn=True)
    nameChecked = checkSceneName(path)
    if not nameChecked:
        # name = getCorrectName(path)
        name = "TEST"
        raise renamerController.WrongName("Wrong name on scene. Scene name must be '{}'".format(name))
    return True


def save(chk=False, out=False):
    canSceneBeSaved()
    MM.eval("incrementAndSaveScene 0")
    path = MC.file(q=True, sn=True)

    widget = UploaderWindow(file_path=path)
    widget.ASK_TO_PUBLISH = False
    widget.PUBLISH_TO_CHK = chk
    widget.PUBLISH_TO_OUT = out
    widget.show()