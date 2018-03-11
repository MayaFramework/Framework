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

        # self.fileExtensionCB.addItems(NewFileDialog.getExtensions())
        self.fileExtensionCB.addItems([".ma"])

    @property
    def selectedExtension(self):
        return self._selectedExtension

    @selectedExtension.setter
    def selectedExtension(self, value):
        self._selectedExtension = value

    def accept(self):
        self.selectedExtension = self.fileExtensionCB.currentText()
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