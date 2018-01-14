
"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
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
from Framework.lib.config.config import Config
from downloader import Downloader, DownloaderResponse
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
    def __init__(self, file_path=""):
        super(DependencyLoaderWidget, self).__init__()
#         self.setupUi(self)
        self._config = Config.instance()
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "main.ui"), self)
        setStyleSheet(self, os.path.join(CSS_PATH, 'dark_style1.qss'))
#         self.dropboxManager = DropboxManager(token=self._config["dpx_token"])
        self.__init_icons()
        self.context_menu_list()
        #Log States
        self.set_log_visible(False)
        self.log_btn.setIcon(QtGui.QIcon(self.list_ico_path))
        self.log_text = ""
        # Loading Text and Movie
        self.set_loading_gif(False)

        
        
        if file_path:
            self.path.setText(file_path)

        #setting Downloaderf
        self.downloader = Downloader()
        #setting downloader signals
        self.downloader.on_file_finish_download.connect(self.on_file_finish_download, QtCore.Qt.QueuedConnection)
        self.downloader.on_file_start_download.connect(self.on_file_start_download, QtCore.Qt.QueuedConnection)
        self.downloader.on_finish_download.connect(self.on_finish_download, QtCore.Qt.QueuedConnection)
        self.downloader.on_start_download.connect(self.on_start_download, QtCore.Qt.QueuedConnection)
    def set_log_visible(self, state=True):
        self.log_widget.setVisible(state)
        
    def __init_icons(self):
        self.downloading_ico_path=os.path.join(ICO_PATH, "downloading.png")
        self.question_ico_path=os.path.join(ICO_PATH, "question.png")
        self.checked_ico_path=os.path.join(ICO_PATH, "checked.png")
        self.error_ico_path=os.path.join(ICO_PATH, "error.png")
        self.list_ico_path=os.path.join(ICO_PATH, "list.png")



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
        # Ui Objects
        self.dependency_list.clear()
        self.downloading_text.setText("")
        return True

    def add_log(self, file_path, message, state):
        if state == DownloaderResponse.ERROR_STATE:
            self.log_text+= '\n{0}: \n   response:  ERROR [{1}]'.format(file_path, str(message))
        elif state == DownloaderResponse.SUCCESS_STATE:
            self.log_text+= '\n{0}: \n   response:  {1}'.format(file_path, str("SUCCES"))

        self.log_text_widget.setPlainText(self.log_text)
        
        
    def on_file_finish_download(self, downloaderResponse):
        self.add_log(file_path=downloaderResponse.file_path, message=downloaderResponse.message, state=downloaderResponse.state)
        self.update_item(downloaderResponse.file_path, state=downloaderResponse.state)

    def on_file_start_download(self, downloaderResponse):
        self.add_item_in_list(downloaderResponse.file_path, state= downloaderResponse.state)
        self.add_log(file_path=downloaderResponse.file_path, message=downloaderResponse.message, state=downloaderResponse.state)
        
    def on_finish_download(self):
        self.set_loading_gif(False)

    def on_start_download(self):
        self.set_loading_gif(True)      
        

    
    def get_icon(self, state):
        if state == DownloaderResponse.SUCCESS_STATE:
            return QtGui.QIcon(self.checked_ico_path)
        if state == DownloaderResponse.IN_PROGRESS:
            return QtGui.QIcon(self.downloading_ico_path)
        if state == DownloaderResponse.ERROR_STATE:
            return QtGui.QIcon(self.error_ico_path)

    def update_item(self, file_path, state):
        item = self.get_item(file_path)
        if not item:
            return
        icon = self.get_icon(state)
        item.setIcon(icon)
        QtWidgets.QApplication.processEvents()

    def add_item_in_list(self, key, state):
        """
        Add item into the qListWidget
        """
        if key.startswith("P:bm2"):
            print "WRONG"
        listItem = QtWidgets.QListWidgetItem(key)
        listItem.setIcon(self.get_icon(state))
        self.dependency_list.addItem(listItem)
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
        self.execute_update_process()

    def execute_update_process(self):
        """
        Set The loading gif visible
        Downloads the path if the current doesnt exist in local disk
        Calculates file_dependencies
        """
        file_list = []
#         file_path = self.get_current_text()
        file_path = r"P:\BM2\seq\tst\sho\700\scncmp\wip\bm2_shoscn_seq_tst_sho_700_scncmp_animationPrep_Dalia_wip.ma"
        file_path = self.downloader._dpx.getTargetPath(file_path)
        file_list.append(file_path)
        self.log_text_widget.clear()
        self.create_default_folders_on_target(file_path)
        self.set_log_visible(True)
        self.downloader.set_files_to_process(file_list)
        self.downloader.set_maxium_threads(self.thread_spinBox.value())
        self.downloader.start_download_process()

    def create_default_folders_on_target(self, file_path):
        """
        Creates default folders on the target path
        """
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
    def on_log_btn_clicked(self):
        self.set_log_visible(self.log_widget.isHidden())
    
    
    @QtCore.Slot()
    def on_open_btn_clicked(self):
        maya_path = self.get_maya_exe_path()
        command = '"{0}" -file "{1}"'.format(maya_path,
                                             str(self.dropboxManager.getTargetPath(self.get_current_text())))
        f_util.execute_command(command)

    def set_loading_gif(self,  state=True, label=""):
        self.set_loading_visible(state)
        if not state:
            return
        self.downloading_text.setText("Downloading...")
        movie = QtGui.QMovie(os.path.join(ICO_PATH, "gif", "loading.gif"))
        self.loading_label.setMovie(movie)
        movie.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    from Framework.lib.gui_loader import gui_loader
#     DependencyLoaderWidget().show()
#     app.exec_()
    obj = gui_loader.get_default_container(DependencyLoaderWidget(), "Update All")
    obj.exec_()
