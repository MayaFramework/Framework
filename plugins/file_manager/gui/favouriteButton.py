from PySide2 import QtWidgets, QtCore, QtGui
import os

from Framework import get_icon_path

ICON_PATH = get_icon_path()

class StarButton(QtWidgets.QPushButton):

    EMPTY_STAR = os.path.join(ICON_PATH, "empty_star.png")
    FILLED_STAR = os.path.join(ICON_PATH, "filled_star.png")
    favourited = QtCore.Signal()

    def __init__(self, parent=None):
        super(StarButton, self).__init__(parent=parent)

        # self.setHidden(True)
        self._favourite = False

        self.clicked.connect(self.markAsFavourite)
        self.setIcon(QtGui.QIcon())

    @property
    def favourite(self):
        return self._favourite

    @favourite.setter
    def favourite(self, value):
        self._favourite = value

    def enterEvent(self, event):
        if not self.favourite:
            self.setIcon(QtGui.QIcon(StarButton.EMPTY_STAR))
        super(StarButton, self).enterEvent(event)

    def leaveEvent(self, event):
        if not self.favourite:
            self.setIcon(QtGui.QIcon())
        super(StarButton, self).leaveEvent(event)

    def markAsFavourite(self):
        if not self.favourite:
            self.favourite = True
            # self.setHidden(False)
            self.favourited.emit()
            self.setIcon(QtGui.QIcon(StarButton.FILLED_STAR))
        else:
            self.favourite = False
            # self.setHidden(False)
            self.favourited.emit()
            self.setIcon(QtGui.QIcon(StarButton.EMPTY_STAR))