
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader
    from uploader_window import UploaderWindow
    app = QtWidgets.QApplication(sys.argv)
    widget = UploaderWindow(r"P:\BM2\loc\salaTelefonos\scn\main\main\wip\bm2_locscn_loc_salaTelefonos_scn_main_main_default_none_wip0020.ma")
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.show()
    widget.execute_analize_process()
    app.exec_()
