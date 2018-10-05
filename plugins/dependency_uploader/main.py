
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader
    from uploader_window import UploaderWindow
    app = QtWidgets.QApplication(sys.argv)
    widget = UploaderWindow()
    widget.ASK_TO_PUBLISH = True
    widget.PUBLISH_TO_CHK = True
    widget.PUBLISH_TO_OUT = True
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.show()
    app.exec_()


"""
P:\bm2\seq\tst\sho\300\scncmp\wip\bm2_seqsho_seq_tst_sho_300_scncmp_default_none_wip.0007.ma
"""