import os
from Framework.lib.gui_loader import gui_loader
from Framework.plugins.file_manager.filetypeChooser import FileTypeChooser
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.plugins.file_manager.filetypes.folder import Folder
from Framework.plugins.renamer.controller import Renamer

from Framework import get_icon_path

ICON_PATH = get_icon_path()

FOLDER = Folder(r"P:/bm2/elm/albertoElemTest/mod/high/main/chk")

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "newfileDialog.ui"))


class NewFileDialog(form, base):

    createFile = QtCore.Signal(str)

    def __init__(self, currentDir,  parent=None):
        super(NewFileDialog, self).__init__(parent=parent)
        self.setupUi(self)

        print currentDir
        self.currentDir = currentDir

        self.initUI()
        self.connectSignals()

    def initUI(self):
        self.getPreviewName()

    def connectSignals(self):
        self.descriptionLE.textChanged.connect(self.updatePreview)
        self.partitionLE.textChanged.connect(self.updatePreview)
        self.extensionLE.textChanged.connect(self.updatePreview)
        self.versionLE.textChanged.connect(self.updatePreview)

    def getPreviewName(self):
        renamer = Renamer()
        self.previewName = renamer.generate_complete_path_from_folder(  self.currentDir,
                                                                        partition="[PARTITION]",
                                                                        description="[DESCRIPTION]",
                                                                        extension="[EXTENSION]",
                                                                        version ="[VERSION]")
        self.previewLB.setText(self.previewName)

    def updatePreview(self):
        updatedFileName = self.previewName.replace("[DESCRIPTION]", self.descriptionLE.text())
        updatedFileName = updatedFileName.replace("[PARTITION]", self.partitionLE.text())
        updatedFileName = updatedFileName.replace("[EXTENSION]", self.extensionLE.text())
        updatedFileName = updatedFileName.replace("[VERSION]", self.versionLE.text())
        self.previewLB.setText(updatedFileName)

    def accept(self):
        self.createFile.emit(os.path.normpath(self.previewLB.text()))
        super(NewFileDialog, self).accept()

if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui

    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = NewFileDialog(FOLDER.local_path)
    widget.show()
    app.exec_()
