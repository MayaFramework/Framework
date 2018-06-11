from generic import GenericWidget
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
import os
from Framework import get_icon_path


ICON_PATH = get_icon_path()


class UnknownWidget(GenericWidget):

    ICON = os.path.join(ICON_PATH, "unknown-file.png")

    def __init__(self, folderObj, icon=ICON, parent=None):
        super(UnknownWidget, self).__init__(folderObj, icon=icon, parent=parent)





