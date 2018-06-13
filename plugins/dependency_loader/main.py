
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
    tool = DependencyLoaderWidget()
    obj = gui_loader.get_default_container(tool, "Update All")
    obj.show()
    app.exec_()
    
    """
    P:bm2/seq/dip/sho/010/animation/wip/bm2_shoani_seq_dip_sho_010_animation_default_scene_wip0001.ma
    """