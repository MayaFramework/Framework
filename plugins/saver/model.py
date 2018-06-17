from Framework.lib.gui_loader import gui_loader
from PySide2 import QtCore, QtGui, QtWidgets
import os
import controller
from Framework.plugins.renamer.model import RenamerUI
import maya.cmds as MC



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
        except (controller.NoChangesDetected,
                controller.renamerController.WrongName,
                controller.renamerController.WrongNameFormatting,
                controller.renamerController.OldNamingConvention) as e:
            if isinstance(e, controller.NoChangesDetected):
                self.noChangesDialog()
            else:
                self.wrongNameDialog()
            # elif isinstance(e, controller.renamerController.OldNamingConvention):
            #     self.oldNamingConvention()
            # else:
            #     self.wrongNameDialog()

    def normalSave(self):
        self.save()

    def out(self):
        self.save(out=True)

    def chk(self):
        self.save(chk=True)

    def oldNamingConvention(self):
        name = controller.getCorrectName()
        QtWidgets.QMessageBox.critical(self, "OldNamingConvention", "It looks like the scene name is using the old naming convention. Please rename it to:<br><br><b>{}<br><br>DON'T FORGET TO CHANGE [VERSION] WITH THE CURRENT VERSION</b>".format(name))

    def wrongNameDialog(self):
        QtWidgets.QMessageBox.critical(self, "WrongName", "It looks like the scene name is wrong.<br>Renamer will be opened automatically. Please, rename it and then re-open this tool.")
        sceneName = os.path.normpath(MC.file(q=True, sn=True)).replace("\\", "/")
        self.dialog = RenamerUI(sceneName)
        self.dialog.show()

    def noChangesDialog(self):
        QtWidgets.QMessageBox.critical(self, "No changes detected", "You must do any change in order to save the scene")