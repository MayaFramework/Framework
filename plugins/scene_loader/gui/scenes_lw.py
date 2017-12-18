from PySide2 import QtWidgets, QtCore, QtGui

class BackgroundList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(BackgroundList, self).__init__(parent)
    #     self.viewport().installEventFilter(self)
    #
    # def eventFilter(self, widget, event):
    #     if event.type() == QtCore.QEvent.Paint:
    #         if self.count() == 0:
    #             p = QtGui.QPainter()
    #             p.begin(widget)
    #             font = QtGui.QFont()
    #             font.setPointSize(25)
    #             p.setFont(font)
    #             p.setPen(QtGui.QPen(QtGui.QColor("#BDBDBD")))
    #             p.drawText(self.rect(), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, "EMPTY")
    #             p.end()
    #     return super(BackgroundList, self).eventFilter(widget, event)