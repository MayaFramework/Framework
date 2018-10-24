from Framework.plugins.dependency_uploader.uploader_window import UploaderWindow
try:
    import maya.cmds as MC
    import maya.mel as MM
except:
    print "Trying to import maya modules from outside of maya environment"
import Framework.plugins.renamer.controller as renamerController;  reload(renamerController)
import os
import sys

class NoChangesDetected(Exception):
    pass


def checkSceneName(path):
    try:
        rename = renamerController.Renamer()
        fields = rename.get_fields_from_file_path(path)
        return rename.check_fields_value(fields)
        # folder, filename = os.path.normpath(path).replace("\\", "/").rsplit("/", 1)
        # folder_fields = rename.get_fields_from_folder_path(folder)
        # rename.check_fields_value(folder_fields)
        # return rename.check_fields_value(folder_fields)
    except renamerController.WrongNameFormatting:
        return False


def getCorrectName(path=None):
    if not path:
        path = MC.file(q=True, sn=True)
    rename = renamerController.Renamer()
    folder, filename = os.path.normpath(path).replace("\\", "/").rsplit("/", 1)

    try:
        filename_fields = rename.get_fields_from_file_name(filename)
    except renamerController.OldNamingConvention:
        filename_fields = dict()

    return rename.generate_complete_path_from_folder(folder,
                                                     partition=filename_fields.get("partition", "default"),
                                                     description=filename_fields.get("description", "none"),
                                                     extension=filename_fields.get("extension", "ma"),
                                                     version =filename_fields.get("version", "[VERSION]")
                                                     )


def canSceneBeSaved():
    modified = MC.file(mf=True, q=True)
    if not modified:
        raise NoChangesDetected()
    path = MC.file(q=True, sn=True)
    nameChecked = checkSceneName(path)
    if not nameChecked:
        name = getCorrectName(path)
        raise renamerController.WrongName("Wrong name on scene. Scene name must be '{}'".format(name))
    return True


def save(chk=False, out=False):
    canSceneBeSaved()
    MM.eval("incrementAndSaveScene 0")
    path = MC.file(q=True, sn=True)
    execute_sub_process(file_path=path, chk=chk, out=out)
#     widget = UploaderWindow(file_path=path)
#     widget.ASK_TO_PUBLISH = False
#     widget.PUBLISH_TO_CHK = chk
#     widget.PUBLISH_TO_OUT = out
#     widget.show()
#     widget.execute_upload_process()


def execute_sub_process(file_path, chk=False, out=False):
    import subprocess
    from Framework.lib.config.config import Config 
#     python_file_route = "C:\Users\Miguel\AppData\Roaming\BM2_TMPORAL_FILES\saver_tmp_file.py"
    python_file_route = os.path.join(os.getenv('APPDATA'), Config.instance().environ["bm2_tmp_files_folder"], "tmp_file_python.py")
    python_code = u"""
from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets
from Framework.plugins.dependency_uploader.uploader_window import UploaderWindow
import sys
app = QtWidgets.QApplication(sys.argv)
widget = UploaderWindow(file_path=r'{file_path}')
widget.ASK_TO_PUBLISH = {ask}
widget.PUBLISH_TO_CHK = {chk}
widget.PUBLISH_TO_OUT = {out}
widget.execute_upload_process()
app.exec_()
    """.format(ask=False, chk=chk, out=out, file_path=file_path)
    if not os.path.exists(os.path.dirname(python_file_route)):
        os.makedirs(os.path.dirname(python_file_route))
    with open(python_file_route, "w+") as my_file:
        my_file.write(python_code)
    subprocess.Popen(['python', python_file_route])


if __name__ == "__main__":

    
    import time
    for x in range(0,10):
        print "waiting.."
        time.sleep(1)
    









