import os
import sys
from Framework.lib import ui
from Framework.lib.gui_loader import gui_loader
from uploader import Uploader
from uploader_exceptions import *
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework import get_environ_file, get_css_path, get_icon_path
from Framework.lib.ui.widgets import tree_widget, common_widgets

CSS_PATH = get_css_path()
ICON_PATH = get_icon_path()

class NewRowPrompt(QtWidgets.QDialog):
    
    def __init__(self):
        super(NewRowPrompt, self).__init__()
        ui.apply_resource_style(self)
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "add_row_widget.ui"), self)

        self.add_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"error.png")))

    @QtCore.Slot(str)
    def on_file_path_lineEdit_textChanged(self, file_path):
        if os.path.exists(file_path):
            self.add_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"checked.png")))
        else:
            self.add_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"error.png")))

    @QtCore.Slot()
    def on_add_btn_clicked(self):
        file_selected = QtWidgets.QFileDialog.getOpenFileNames(self, ("Open File"), "P:/bm2")[0]
        if not file_selected:
            raise Exception("Not Path Found")
        self.file_path_lineEdit.setText(file_selected[0])
        
    @QtCore.Slot()
    def on_save_btn_clicked(self):
        file_path = self.file_path_lineEdit.text()
        if not os.path.exists(file_path):
            window = common_widgets.MessageWindow(title="Checking File Path",
                                         level=common_widgets.MessageWindow.ERROR_LEVEL,
                                         msg ="This file path doesn't exists: %s\n press CANCEL to modify the path otherwise it will close this view" % file_path)

            if window.get_response():
                self.close()
            else:
                return
        self.close()

    def get_file_path(self):
        file_path =self.file_path_lineEdit.text()
        while file_path.startswith(" ") or file_path.endswith(" "):
            file_path = file_path.replace(" ", "")
        if not os.path.exists(file_path):
            return None
        else:
            return file_path