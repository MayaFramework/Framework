'''
Created on Jul 2, 2017

@author: Miguel
'''
import os
import sys
from Framework.lib.gui_loader import gui_loader
from Framework.plugins.uploader.uploader import Uploader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework import get_environ_file, get_css_path, get_icon_path
import threading
import time
CSS_PATH = get_css_path()
ICO_PATH = get_icon_path()
ui_file = os.path.join(os.path.dirname(__file__), "gui", "main.ui")
form, base = gui_loader.load_ui_type(ui_file)

def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)


class UploaderWindow(form, QtWidgets.QDialog):
    timeout = 60*60
    def __init__(self):
        super(UploaderWindow, self).__init__()
        self.current_threads = 0
        self.maximum_threads = 4
        setStyleSheet(self,os.path.join(CSS_PATH,"dark_style1.qss"))
        self.setupUi(self)
        self.exec_()

        self.uploader = Uploader()
    def fill_tree_widget(self):
        dependencies = self.uploader.get_dependencies()
        #TODO: Transform the dictionary here into our recursive dictionary format

        # now execute and fill the tree

        # make possible to add custom routs in case of the tool doesnt recognize all the work routs
        pass

    def find_tree_selection(self):
        # access to the tree and find every children checked to add it into the list to upload
        pass

    def upload(self):
        files = self.find_tree_selection()
        if not files:
            return True
        for file in files:
            if self.is_available_thread(self.timeout):
            # check dependency_loader_window line 150
                self.current_threads +=1
                t = threading.Thread(target = self.upload_file, args = (file, ))
                t.start()
        # once we have recovered the list of files to upload execute the upload process
        pass

    def is_available_thread(self, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self.current_threads <= self.maximum_threads():
                return True
            time.sleep(period)
        return False


    def upload_file(self, file):
        item = self.get_item(file)
        if not item:
            return
        try:
            item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "downloading.png")))
            QtWidgets.QApplication.processEvents()
            state = self.uploader.upload_file(file)
            if state:
                item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "checked.png")))
            else:
                item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "error.png")))

        except Exception as e:
            item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "error.png")))
            print e
        finally:
            QtWidgets.QApplication.processEvents()
            self.current_thread -=1

    def get_item(self, name):
        """
        Fints the specified name into the tree widget
        """
        result = self.inspection_tree.findItems(name, QtCore.Qt.MatchExactly)
        if result:
            result = result[0]
        return result

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UploaderWindow()
