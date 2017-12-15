from PySide2 import QtCore, QtGui, QtWidgets
from Framework.lib.gui_loader import gui_loader
import os

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "new_note_dialog.ui"))


class NewNoteDialog(form, base):

    newNote = QtCore.Signal(str)

    def __init__(self):
        super(NewNoteDialog, self).__init__()
        self.setupUi(self)

        self.__connect_default_signals()

    def __connect_default_signals(self):
        self.acceptBT.clicked.connect(self.accept)
        self.cancelBT.clicked.connect(self.reject)

