import os
from Framework.lib.gui_loader import gui_loader
from Framework.plugins.file_manager.filetypeChooser import FileTypeChooser
from PySide2 import QtCore, QtGui, QtWidgets


from Framework import get_icon_path

ICON_PATH = get_icon_path()


NOTALLOWEDEXTENSIONS = [".mb"]


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "newfileDialog.ui"))


class NewFileDialog(form, base):

    def __init__(self, parent=None):
        super(NewFileDialog, self).__init__(parent=parent)
        self.setupUi(self)

        self._selectedExtension = None
        self._fileName = str()
        self.newFile = None
        self.newWidget= None

        # self.fileExtensionCB.addItems(NewFileDialog.getExtensions())
        self.fileExtensionCB.currentIndexChanged[str].connect(self._extensionChanged)
        self.fileExtensionCB.addItems([".ma"])

    @property
    def selectedExtension(self):
        return self._selectedExtension

    @selectedExtension.setter
    def selectedExtension(self, value):
        self._selectedExtension = value

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self, value):
        self._fileName = value

    def _extensionChanged(self, extension):
        obj = FileTypeChooser.getClassByExtension(extension)
        restrictedFileName = getattr(obj, "restrictedFileName")
        self.filenameLE.setDisabled(restrictedFileName)
        if restrictedFileName:
            newObj = obj.generateFileName(os.path.normpath(self.parent().currentFolder.local_path).replace("\\", "/"))
            self.filenameLE.setText(newObj)

    def accept(self):
        self.selectedExtension = self.fileExtensionCB.currentText()
        self.fileName = self.filenameLE.text()
        obj, widget = FileTypeChooser.getClassByExtension(self.selectedExtension, includeWidget=True)
        fileName = os.path.join(self.parent().currentFolder.local_path, self.fileName)
        self.newFile = obj.generateNewFile(scene_path=fileName)
        self.newWidget = widget(self.newFile)
        super(NewFileDialog, self).accept()

    @staticmethod
    def getExtensions():
        extensions = list()
        for value in FileTypeChooser.FILETYPECLASSES.values():
            for extension in value["extensions"]:
                if extension in NOTALLOWEDEXTENSIONS:
                    continue
                extensions.append(extension)
        return extensions