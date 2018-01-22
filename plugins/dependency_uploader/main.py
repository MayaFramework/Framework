
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader
    from uploader_window import UploaderWindow
    app = QtWidgets.QApplication(sys.argv)
    widget = UploaderWindow()
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.show()
    app.exec_()
