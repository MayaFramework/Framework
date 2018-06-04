from Framework.lib.gui_loader import gui_loader
from PySide2 import QtCore, QtGui, QtWidgets
import os
import controller



form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class Saver(form, base):

    def __init__(self):
        super(Saver, self).__init__()
        self.setupUi(self)

        self.connectDefaultSignals()

    def connectDefaultSignals(self):
        self.saveBT.clicked.connect(self.normalSave)
        self.outBT.clicked.connect(self.out)
        self.chkBT.clicked.connect(self.chk)

    def save(self, out=False, chk=False):
        try:
            controller.save(out=out, chk=chk)
        except controller.NoChangesDetected or controller.renamerController.WrongName:
            self.noChangesDialog()

    def normalSave(self):
        self.save()

    def out(self):
        self.save(out=True)

    def chk(self):
        self.save(chk=True)

    def noChangesDialog(self):
        QtWidgets.QMessageBox.critical(self, "No changes detected", "You must do any change in order to save the scene. Also, check that the scene name is the correct one")