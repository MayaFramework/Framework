import os
from Framework.lib.gui_loader import gui_loader
from Framework.lib.shotgun.shotgunInit import ShotgunInit
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui


from Framework import get_icon_path

ICON_PATH = get_icon_path()



form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "signinDialog.ui"))


class SignInDialog(form, base):

    def __init__(self, parent=None):
        super(SignInDialog, self).__init__(parent=parent)
        self.setupUi(self)

        self.sg = ShotgunInit()

        self.userName = None
        self.password = None

    def accept(self):
        if self.authenticateUser():
            self.login = self.usernameLE.text()
            self.userName = self.getRealName(self.login)
            self.password = self.passwordLE.text()
            super(SignInDialog, self).accept()
        else:
            return False

    def authenticateUser(self):
        userName = self.usernameLE.text()
        password = self.passwordLE.text()
        user = self.sg.getUser(userName)
        if user:
            return user.authenticate(password)
        return False

    def getRealName(self, login):
        user = self.sg.getUser(login)
        return user.getField("name")
