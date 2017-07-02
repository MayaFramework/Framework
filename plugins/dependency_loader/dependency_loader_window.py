import sys
import os
import subprocess
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ma_utils.reader import MaReader
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework import get_environ_file, get_css_path, get_icon_path
from Framework.lib.file import utils as f_util
from Framework.lib.ui.widgets.common_widgets import MessageWindow
import DATA
import time
import threading

#=========================================================================
# TODO: Separate Logic from the UI
#=========================================================================
# "C:\Users\Miguel\Downloads\bm2_shoscn_seq_tst_sot_0300_scncmp_default_scene_out.ma"
CSS_PATH = get_css_path()
ICO_PATH = get_icon_path()


ui_file = os.path.join(os.path.dirname(__file__), "gui", "main.ui")
form, base = gui_loader.load_ui_type(ui_file)


def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)


class DependencyLoaderWidget(form, QtWidgets.QDialog):
    dropboxManager = None
    _correct_downloaded = []
    _failed_downloaded = []
    _processed_list = []
    _current_thread_count = 0

    def __init__(self):
        super(DependencyLoaderWidget, self).__init__()
        self.setupUi(self)
        setStyleSheet(self, os.path.join(CSS_PATH, 'dark_style1.qss'))
        self.context_menu_list()
        self.dropboxManager = DropboxManager(
            token="MspKxtKRUgAAAAAAAAAHPJW-Ckdm7XX_jX-sZt7RyGfIC7a7egwG-JqtxVNzOSJZ")
        # Loading Text and Movie
        self.set_loading_gif(self.loading_label)
        self.downloading_text.setText("Downloading...")
        self.set_loading_visible(False)

    def context_menu_list(self):
        self.dependency_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # Context Menu
        # Copy Action
        copy_action = QtWidgets.QAction("Copy rout", self)
        copy_action.triggered.connect(self.copy_selected_rout)
        self.dependency_list.addAction(copy_action)

    def get_maya_exe_path(self):
        custom_environ_dict = f_util.read_json(get_environ_file())

        if "maya_exe" in custom_environ_dict:
            return custom_environ_dict["maya_exe"]

    def copy_selected_rout(self):
        selected_item = self.dependency_list.selectedItems()
        if not selected_item:
            raise Exception("Select a row!")

        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(selected_item[0].text())

    def reset_state(self):
        # Objects
        self._correct_downloaded = []
        self._failed_downloaded = []
        self._processed_list = []
        # Ui Objects
        self.dependency_list.clear()
        self.downloading_text.setText("")
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

    def get_file_depndencies(self, file):
        dependencies = self.get_dependencies(file)
        if not dependencies:
            return False

        current_files = []
        for key, values in dependencies.iteritems():
            key = self.dropboxManager.getTargetPath(key)
            if key in self._processed_list:
                continue
            current_files.append(key)
            # Create Ui Element
            self.add_item_in_list(key)
            self._processed_list.append(key)

            if "/mps/" in key:
                folder = key.rsplit("/", 1)[0]
                children = self.dropboxManager.getChildrenFromFolder(folder)
                if children:
                    for child in children:
                        child = self.dropboxManager.getTargetPath(child)
                        if child not in self._processed_list:
                            self.add_item_in_list(child)
                            current_files.append(child)
                            self._processed_list.append(child)

        for my_file in current_files:
            if self.is_available_thread(timeout=60*60):
                self._current_thread_count += 1
                t = threading.Thread(
                    target=self.execute_download, args=(my_file,))
                t.start()

    def add_item_in_list(self, key):
        listItem = QtWidgets.QListWidgetItem(key)
        listItem.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "question.png")))
        self.dependency_list.addItem(listItem)
        QtWidgets.QApplication.processEvents()

    def is_available_thread(self, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self._current_thread_count <= self.thread_spinBox.value():
                return True
            time.sleep(period)
        return False

    def execute_download(self, file):
        start = time.time()
        try:
            item = self.get_item(file)
            if not item:
                return
            # logic
            result = self.download_file(file, item)
            if result:
                self._correct_downloaded.append(file)
                if file.endswith(".ma"):
                    self.get_file_depndencies(file)
            else:
                self._failed_downloaded.append(file)

        except Exception as e:
            print e
        finally:
            self._current_thread_count -= 1
            if self._current_thread_count == 0:
                self.set_loading_visible(False)
            print "Thread Acabado: %s" % file
            print " Time:", (time.time()-start)

    def download_file(self, file, item):
        try:
            if not self.dropboxManager:
                self.dropboxManager = DropboxManager(
                    token="MspKxtKRUgAAAAAAAAAHPJW-Ckdm7XX_jX-sZt7RyGfIC7a7egwG-JqtxVNzOSJZ")

            item.setIcon(QtGui.QIcon(
                os.path.join(ICO_PATH, "downloading.png")))
            QtWidgets.QApplication.processEvents()
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
            QtWidgets.QApplication.processEvents()

    def set_loading_visible(self, visible_state):
        self.loading_label.setVisible(visible_state)
        self.downloading_text.setVisible(visible_state)

    def get_item(self, file):
        result = self.dependency_list.findItems(file, QtCore.Qt.MatchExactly)
        if result:
            result = result[0]
        return result

    def get_current_text(self):
        path = os.path.normpath(self.path.text()).replace("\\", "/")
        if not path or not path.endswith(".ma"):
            raise Exception("Specify a ma file!")
        return path

    @QtCore.Slot()
    def on_update_btn_clicked(self):
        self.set_loading_visible(True)
        self.reset_state()
        self.create_default_folders_on_target(self.get_current_text())
        self.get_file_depndencies(self.get_current_text())

    def create_default_folders_on_target(self, file_path):
#       folders_list = ",".join(["wip","mps","out","ref","chk"])
        folders_list = ",".join(DATA.WORKING_FOLDERS)
        window = MessageWindow("Create Starter Folders","Warning",
                      msg="Do you want to create previous folders on the target"+\
                            "Path:\n %s \n FOLDERS: %s" % (file_path, folders_list))

        if window.get_response():
            folder = file_path.rsplit("/",1)[0]
            for working_folder in DATA.WORKING_FOLDERS:
                self.create_path_rout(folder +'/'+ working_folder)

    def create_path_rout(self,path_rout):
        if not os.path.exists(path_rout):
            os.makedirs(path_rout)


    @QtCore.Slot()
    def on_open_btn_clicked(self):
        maya_path = self.get_maya_exe_path()
        command = '"{0}" -file "{1}"'.format(maya_path,
                                             self.get_current_text())
        f_util.execute_command(command)

    def set_loading_gif(self, label):

        movie = QtGui.QMovie(os.path.join(ICO_PATH, "gif", "loading.gif"))
        movie.setCacheMode(QtGui.QMovie.CacheAll)
        label.setMovie(movie)
        movie.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    from Framework.lib.gui_loader import gui_loader
    obj = gui_loader.get_default_container(DependencyLoaderWidget(), "Update All")
    obj.exec_()
