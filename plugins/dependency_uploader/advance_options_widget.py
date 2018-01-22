'''
Created on Dec 13, 2017

@author: Miguel
'''
import os
import sys
from Framework.lib import ui
from Framework.lib.gui_loader import gui_loader
from uploader import Uploader
from uploader_exceptions import *
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework import get_environ_file, get_css_path, get_icon_path
CSS_PATH = get_css_path()
ICON_PATH = get_icon_path()



class AdvanceOptionsWidget(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(AdvanceOptionsWidget, self).__init__(parent=parent)
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "publish_advance_options.ui"), self)
        ui.apply_resource_style(self)
        self._chk_state = False
        self._out_state = False
        
    def closeEvent(self, event):
        self.update_properties()
        event.accept()
    def update_properties(self):
        self._chk_state = self.chk_check_box.checkState() == QtCore.Qt.Checked
        self._out_state = self.out_check_box.checkState() == QtCore.Qt.Checked
    @property
    def chk_state(self):
        return self._chk_state
    
    @property
    def out_state(self):
        return self._out_state
    
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget  = AdvanceOptionsWidget()
    widget.show()
    app.exec_()
    print widget.chk_state
    print widget.out_state