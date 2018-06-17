import os

import controller as renamerController
import maya.cmds as MC
from Framework.lib.ui.qt.QT import QtCompat, QtCore, QtGui, QtWidgets


class RenamerUI(QtWidgets.QWidget):

    PARTITION = "default"
    DESCRIPTION = "none"
    EXTENSION = "ma"
    VERSION = "0001"

    def __init__(self, scenePath=None, parent=None):
        super(RenamerUI, self).__init__(parent=parent)

        uiFile = os.path.join(os.path.dirname(__file__), "gui", "renamer.ui")
        QtCompat.loadUi(uiFile, self)

        self.scenePath = scenePath
        if not scenePath:
            self.scenePath = MC.file(sn=True, q=True)
        self.previewName = None

        self.renamer = renamerController.Renamer()

        self.connectSignals()
        self.startChecking()

    def startChecking(self):

        self.currentSceneLB.setText(self.scenePath)

        success = self.checkName()
        self.isValidLB.setText(str(success))
        if not success:
            self.userArea.setEnabled(True)
            self.renameBT.setEnabled(True)
            self.getPreviewName()

    def checkName(self):
        try:
            fields = self.renamer.get_fields_from_file_path(self.scenePath)
            success = self.renamer.check_fields_value(fields)
            return success
        except Exception:
            return False

    def connectSignals(self):
        self.descriptionLE.textChanged.connect(self.updatePreview)
        self.partitionLE.textChanged.connect(self.updatePreview)
        self.extensionLE.textChanged.connect(self.updatePreview)
        self.versionLE.textChanged.connect(self.updatePreview)
        self.defaultOptionsBT.clicked.connect(self.setDefaultOptions)
        self.renameBT.clicked.connect(self.renameIt)

    def setDefaultOptions(self):
        self.descriptionLE.setText(RenamerUI.DESCRIPTION)
        self.partitionLE.setText(RenamerUI.PARTITION)
        self.extensionLE.setText(RenamerUI.EXTENSION)
        self.versionLE.setText(RenamerUI.VERSION)

    def getPreviewName(self):
        self.previewName = self.renamer.generate_complete_path_from_folder( os.path.dirname(self.scenePath),
                                                                            partition="[PARTITION]",
                                                                            description="[DESCRIPTION]",
                                                                            extension="[EXTENSION]",
                                                                            version ="[VERSION]")
        self.fixedSceneNameLB.setText(self.previewName)

    def updatePreview(self):
        updatedFileName = self.previewName.replace("[DESCRIPTION]", self.descriptionLE.text())
        updatedFileName = updatedFileName.replace("[PARTITION]", self.partitionLE.text())
        updatedFileName = updatedFileName.replace("[EXTENSION]", self.extensionLE.text())
        updatedFileName = updatedFileName.replace("[VERSION]", self.versionLE.text())
        self.fixedSceneNameLB.setText(updatedFileName)

    def renameIt(self):
        fixedScene = os.path.normpath(self.fixedSceneNameLB.text())
        print "saving with name {}".format(fixedScene)
        MC.file(rename=fixedScene)
        # MC.file(save=True, force=True)
        self.close()
        

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = RenamerUI()
    widget.show()
    app.exec_()
