"""
@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com
"""

import sys
import os
import subprocess
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ma_utils.reader import MaReader
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework import get_environ_file, get_css_path, get_icon_path, get_environ_config
from Framework.lib.file import utils as f_util
from Framework.lib.ui.widgets.common_widgets import MessageWindow
import DATA
import time
import threading
from Framework.lib.ui.qt_thread import CustomQThread
#=========================================================================
# TODO: Separate Logic from the UI, this is a fucking shit
#=========================================================================
# "work/bm2/elm/gafasgato_test/sha/high/shading/chk/bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
CSS_PATH = get_css_path()
ICO_PATH = get_icon_path()


# ui_file = os.path.join(os.path.dirname(__file__), "gui", "main.ui")
# form, base = gui_loader.load_ui_type(ui_file)


def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)


class DependencyLoaderWidget(QtWidgets.QDialog):
    dropboxManager = None
    _correct_downloaded = []
    _failed_downloaded = []
    _processed_list = []
    _current_thread_count = 0
    _threads = []
    def __init__(self):
        super(DependencyLoaderWidget, self).__init__()
#         self.setupUi(self)
        self._config = get_environ_config()
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "main.ui"), self)
        setStyleSheet(self, os.path.join(CSS_PATH, 'dark_style1.qss'))
        self.dropboxManager = DropboxManager(token=self._config["dpx_token"])
        self.__icons()
        self.context_menu_list()
        # Loading Text and Movie
        
        self.set_loading_gif(self.loading_label)
        self.downloading_text.setText("Downloading...")
        self.set_loading_visible(True)

    def __icons(self):
        self.downloading_ico_path=os.path.join(ICO_PATH, "downloading.png")
        self.question_ico_path=os.path.join(ICO_PATH, "question.png")
        self.checked_ico_path=os.path.join(ICO_PATH, "checked.png")
        self.error_ico_path=os.path.join(ICO_PATH, "error.png")


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

        clipboard = QtWidgets.QApplication.clipboard()
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
        """
        P:\bm2\chr\test\test\shading\thinHigh\out\test.ma
        """
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
            cThread = CustomQThread(func=self.download_file, file_path=key)
            cThread.on_finishing.connect(self.on_finished_download_file, QtCore.Qt.QueuedConnection)
            cThread.file_path = key
            self._threads.append(cThread)
            
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
                            cThread = CustomQThread(func=self.download_file, file_path=child)
                            cThread.on_finishing.connect(self.on_finished_download_file, QtCore.Qt.QueuedConnection)
                            cThread.file_path = child
                            self._threads.append(cThread)

        for c_thread in self._threads:
            if self.is_available_thread(timeout=60*60):
                self._current_thread_count += 1
                self.on_starting_download_file(c_thread.file_path)
                c_thread.start()

    def add_item_in_list(self, key):
        if key.startswith("P:bm2"):
            print "VERGA"
        listItem = QtWidgets.QListWidgetItem(key)
        listItem.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "question.png")))
        self.dependency_list.addItem(listItem)
        QtWidgets.QApplication.processEvents()

    def is_available_thread(self, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self._current_thread_count <= self.thread_spinBox.value():
                return True
            QtWidgets.QApplication.processEvents()
            time.sleep(period)
        return False


#     def execute_download(self, my_file):
#         result = self.download_file(file, item)

#     def execute_download(self, my_file):
# #         time = time.time()
#         try:
#             item = self.get_item(my_file)
#             if not item:
#                 return
#             # logic
#             result = self.download_file(my_file, item)
#             if result:
#                 self._correct_downloaded.append(my_file)
#                 if my_file.endswith(".ma"):
#                     self.get_file_depndencies(my_file)
#             else:
#                 self._failed_downloaded.append(my_file)
# 
#         except Exception as e:
#             print e
#         finally:
#             self._current_thread_count -= 1
#             if self._current_thread_count == 0:
#                 self.set_loading_visible(False)
# #             print "Thread Acabado: %s" % file
# #             print " Time:", (time.time()-start)


    def download_file(self, file_path):
        '''
        Download file and parse the result in a tuple of 3 elements
        :param file_path: str
        
        return:
            tuple:  False/True (bool)
                    file_path (str)
                    dropboxManager response (object)
        '''
        response = None
        print "Downloading: %s" % file_path
        try:
            response = self.dropboxManager.downloadFile(file_path)
            if response:
                return (True, file_path, response)
            else:
                return (False, file_path, response)
        except Exception as e:
            return  (False, file_path, e)


    def on_starting_download_file(self, my_file):
        print "start Thread"
        item = self.get_item(my_file)
        if not item:
            return
        item.setIcon(QtGui.QIcon(self.downloading_ico_path))
        QtWidgets.QApplication.processEvents()

    def on_finished_download_file(self, tuple_response):
        result, file_path, dpx_response = tuple_response
        item = self.get_item(file_path)
        print result, file_path, dpx_response
        if not item:
            return
        if result:
            item.setIcon(QtGui.QIcon(self.checked_ico_path))
        else:
            item.setIcon(QtGui.QIcon(self.error_ico_path))
        self._current_thread_count -=1
        QtWidgets.QApplication.processEvents()




#     def download_file(self, file, item):
#         try:
#             item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "downloading.png")))
#             QtWidgets.QApplication.processEvents()
#             response = 
#             if response:
#                 item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "checked.png")))
#                 return (True, response)
#             else:
#                 item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "error.png")))
#                 return (False, response)
# 
#         except Exception as e:
#             item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH, "error.png")))
#             print e
#             return (False, e)
#         finally:
#             QtWidgets.QApplication.processEvents()


        


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
        current_path_file = self.dropboxManager.getTargetPath(self.get_current_text())
        if not os.path.exists(current_path_file):
            self.dropboxManager.downloadFile(current_path_file)
        self.create_default_folders_on_target(current_path_file)
        self.get_file_depndencies(current_path_file)

    def create_default_folders_on_target(self, file_path):
#       folders_list = ",".join(["wip","mps","out","ref","chk"])
        folders_list = ",".join(DATA.WORKING_FOLDERS)
        window = MessageWindow("Create Starter Folders","Warning",
                      msg="Do you want to create previous folders on the target"+\
                            "Path:\n %s \n FOLDERS: %s" % (file_path, folders_list))

        if window.get_response():
            folder = file_path.rsplit("/",2)[0]
            for working_folder in DATA.WORKING_FOLDERS:
                self.create_path_rout(folder +'/'+ working_folder)

    def create_path_rout(self,path_rout):
        if not os.path.exists(path_rout):
            os.makedirs(path_rout)


    @QtCore.Slot()
    def on_open_btn_clicked(self):
        maya_path = self.get_maya_exe_path()
        command = '"{0}" -file "{1}"'.format(maya_path,
                                             str(self.dropboxManager.getTargetPath(self.get_current_text())))
        f_util.execute_command(command)

    def set_loading_gif(self, label):

        movie = QtGui.QMovie(os.path.join(ICO_PATH, "gif", "loading.gif"))
        print os.path.join(ICO_PATH, "gif", "loading.gif")
#         movie.setCacheMode(QtGui.QMovie.CacheAll)
        label.setMovie(movie)
        movie.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    from Framework.lib.gui_loader import gui_loader
#     DependencyLoaderWidget().show()
#     app.exec_()
    obj = gui_loader.get_default_container(DependencyLoaderWidget(), "Update All")
    obj.exec_()
