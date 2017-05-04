import sys
import os
# sys.path.append(r"D:\Miguel\Programming\project\bm2")
from Framework.lib.gui_loader import gui_loader
from Framework import icons
from PySide import QtCore, QtGui
from Framework.lib.ma_utils.reader import MaReader
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.gui import css
import time
import threading


CSS_PATH = css.get_css_path()
ICO_PATH = icons.get_icon_path()
# TESTING
#  D:\Miguel\Programming\project\bm2\tests\bm2_shocam_seq_tst_sot_0010_camera_default_scene_wip001.ma

ui_file = os.path.join(os.path.dirname(__file__), "gui", "main.ui")
form, base = gui_loader.loadUiType(ui_file)


def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)




# class ExampleThread(QtCore.QThread):
#     def run(self):
#         count = 0
#         print count


class DependencyLoaderWidget(form, QtGui.QDialog):
    dropboxManager = None
    _correct_downloaded = []
    _failed_downloaded = []
    _processed_list = []
    _current_thread_count = 0
    def __init__(self):
        super(DependencyLoaderWidget, self).__init__()
        self.setupUi(self)
        setStyleSheet(self, os.path.join(CSS_PATH, 'dark_style.css'))
        self.exec_()


    def termina(self):
        print "termina"

    def reset_state(self):
        # Objects
        self._ma_list = []
        self._correct_downloaded = []
        self._failed_downloaded = []

        # Ui Objects
        self.dependency_list.clear()
        return True

    def get_dependencies(self, path):
        try:
            if not path.endswith(".ma"):
                return None

            maReader = MaReader()
            dependencies = maReader.get_references(path)
            return dependencies
        except Exception as e:
            print e
            return False

    def get_file_depend_dependencies(self, file):
        dependencies = self.get_dependencies(file)
        if not dependencies:
            return False

        current_files = []
        for key, values in dependencies.iteritems():
            if key in self._processed_list:
                continue
            current_files.append(key)
            # Create Ui Element
            listItem = QtGui.QListWidgetItem(key)
            listItem.setIcon(QtGui.QIcon(
                os.path.join(ICO_PATH, "question.png")))
            QtGui.qApp.processEvents()
            self.dependency_list.addItem(listItem)
            self._processed_list.append(key)

        for my_file in current_files:
            if self.is_available_thread(timeout=60*60):
                self._current_thread_count += 1
                t = threading.Thread(target = self.execute_download, args=(my_file,))
                t.start()

    def is_available_thread(self, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self._current_thread_count < 3:
                return True
            time.sleep(period)
        return False
    def execute_download(self,file):
        start= time.time()
        try:
            item = self.get_item(file)
            if not item:
                return
            # logic   
            result = self.download_file(file, item)
            if result:
                self._correct_downloaded.append(file)
                if file.endswith(".ma"):
                    self.get_file_depend_dependencies(file)
            else:
                self._failed_downloaded.append(file)
            
        except Exception as e:
            print e  
        finally:
            self._current_thread_count -=1
            print "Thread Acabado: %s"%file
            print " Time:",(time.time()-start)

    def download_file(self, file, item):
        try:
            if not self.dropboxManager:
                self.dropboxManager = DropboxManager(
                    token="MspKxtKRUgAAAAAAAAAHPJW-Ckdm7XX_jX-sZt7RyGfIC7a7egwG-JqtxVNzOSJZ")

            item.setIcon(QtGui.QIcon(
                os.path.join(ICO_PATH, "downloading.png")))
            QtGui.qApp.processEvents()
            if self.dropboxManager.downloadFile(file):
                item.setIcon(QtGui.QIcon(
                    os.path.join(ICO_PATH, "checked.png")))
                return True
            else:
                item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "error.png")))
                return False

        except Exception as e:
            item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "error.png")))
            print e
            return False
        finally:
            QtGui.qApp.processEvents()


    def get_item(self,file):
        result = self.dependency_list.findItems(file ,QtCore.Qt.MatchExactly)
        if result:
            result = result[0]
        return result

    @QtCore.Slot()
    def on_update_btn_clicked(self):
        start = time.time()
        path = os.path.normpath(self.path.text()).replace("\\", "/")
        if not path or not path.endswith(".ma"):
            raise Exception("Specify a ma file!")

        self.reset_state()
        result = self.get_file_depend_dependencies(path)
        print "TERMINA TODO: ", time.time() - start

app = QtGui.QApplication(sys.argv)
DependencyLoaderWidget()
