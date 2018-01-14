
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader
    from uploader_window import UploaderWindow
    app = QtWidgets.QApplication(sys.argv)
    widget = UploaderWindow()
#     widget = UploaderBackgroundWidget([r"P:\\bm2\\elm\\gafasGato_TEST\\sha\\high\\shading\\chk\\bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"], 2)
#     widget.execute_upload_process()
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.show()
    app.exec_()
