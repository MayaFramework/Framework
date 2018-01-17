
"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
"""
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from dependency_loader_window import DependencyLoaderWidget
    from Framework.lib.gui_loader import gui_loader
    app = QtWidgets.QApplication(sys.argv)
#     DependencyLoaderWidget().show()
#     app.exec_()
    file_path = r"P:\BM2\loc\salaTelefonos\scn\main\main\wip\bm2_locscn_loc_salaTelefonos_scn_main_main_default_none_wip0020.ma"
    tool = DependencyLoaderWidget(file_path)
    obj = gui_loader.get_default_container(tool, "Update All")
    obj.show()
    tool.execute_update_process()
    app.exec_()