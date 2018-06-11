from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui

class PathButton(QtWidgets.QPushButton):

    def __init__(self, folderObj, parent=None):
        super(PathButton, self).__init__(parent)

        self.folderObj = folderObj

        self.setFlat(True)
        self.setText("{} >".format(folderObj.name))