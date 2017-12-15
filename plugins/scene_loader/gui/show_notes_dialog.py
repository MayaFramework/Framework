from PySide2 import QtCore, QtGui, QtWidgets
from Framework.lib.gui_loader import gui_loader
import os

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "notes_dialog.ui"))


class NotesDialog(form, base):

    def __init__(self, notes):
        super(NotesDialog, self).__init__()
        self.setupUi(self)

        self.closeBT.clicked.connect(self.close)

        for note in notes:
            self.notesLW.addItem(note)
