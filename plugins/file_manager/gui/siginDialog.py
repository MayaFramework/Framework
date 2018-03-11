import os
from Framework.lib.gui_loader import gui_loader
from Framework.lib.shotgun.shotgunInit import ShotgunInit
from PySide2 import QtCore, QtGui, QtWidgets


from Framework import get_icon_path

ICON_PATH = get_icon_path()



form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "signinDialog.ui"))


class SignInDialog(form, base):

    def __init__(self, parent=None):
        super(SignInDialog, self).__init__(parent=parent)
        self.setupUi(self)

        self.userName = None
        self.password = None

    def accept(self):
        if self.authenticateUser():
            self.userName = self.usernameLE.text()
            self.password = self.passwordLE.text()
            super(SignInDialog, self).accept()
        else:
            return False

    def authenticateUser(self):
        userName = self.usernameLE.text()
        password = self.passwordLE.text()
        sg = ShotgunInit()
        user = sg.getUser(userName)
        if user:
            return user.authenticate(password)
        return False


