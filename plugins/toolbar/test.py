'''
Created on Oct 21, 2018

@author: Miguel
'''



if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    from Framework.plugins.toolbar import baseIcon, model, controller
    reload(baseIcon)
    reload(controller)
    reload(model)
    ui = model.ToolsLauncherUI()
    ui.show()
    app.exec_()