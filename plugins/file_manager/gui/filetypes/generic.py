from PySide2 import QtCore, QtGui, QtWidgets
import os
from Framework.lib.gui_loader import gui_loader


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "ui", "generic.ui"))


class GenericWidget(form, base):

    def __init__(self, fileObj, icon=None, parent=None):
        super(GenericWidget, self).__init__(parent)
        self.setupUi(self)

        self._supportedType = None
        self._icon = icon
        self.fileObj = fileObj

        self.initUI()


    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    # @property
    # def supportedType(self):
    #     if not self._supportedType:
    #         raise ValueError("You must spicify at least one supported type for {}".format(self.__class__.__name__))
    #     return self._supportedType
    #
    # @supportedType.setter
    # def supportedType(self, value):
    #     self._supportedType = value

    def initUI(self):
        # This method could be override in some cases
        self.nameLB.setText(self.fileObj.name)
        self.iconLB.setPixmap(QtGui.QPixmap(self.icon))