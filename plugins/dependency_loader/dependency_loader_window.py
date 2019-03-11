
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
# "work/bm2/elm/gafasgato_test/sha/high/shading/chk/bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
CSS_PATH = get_css_path()
ICO_PATH = get_icon_path()


def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)

form_class, base_class = gui_loader.load_ui_type(os.path.join(os.path.dirname(__file__), "gui", "main.ui"))

class DependencyLoaderWidget(base_class, form_class):
    _correct_downloaded = []
    _failed_downloaded = []
    # main flags
    __STATE_POPUP_WIDGET_ON_FINISHED_PROCESS = True
    __STATE_UNATENDED_CREATE_FOLDER_PRROCESS = True
    __STATE_OVERWRITE_LOCAL_FILES = True
    __STATE_DOWNLOAD_MAIN_MA_FILE = True
    __STATE_DOWNLOAD_DEPENDENCIES = True
    __STATE_DOWNLOAD_CONTENT_FROM_FOLDERS = True
    __STATE_INTERNAL_OPEN_FILE = False
    __STATE_EXTERNAL_OPEN_FILE = True
    # Signals
    on_finish_download = QtCore.Signal()
    on_start_download = QtCore.Signal()
    openFileSignal = QtCore.Signal()

    def __init__(self, file_path="",parent=None):
        super(DependencyLoaderWidget, self).__init__(parent=parent)
        self.setupUi(self)
#         gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "main.ui"), self)
        setStyleSheet(self, os.path.join(CSS_PATH, 'dark_style1.qss'))
        if file_path:
            self.path.setText(file_path)
        self._config = Config.instance()
        self.downloader = Downloader()
        # <<<<
        #file_path_mps = 'P:\\BM2\\seq\\bat\\sho\\030\\lighting\\out\\mps\\bm2_seqsho_seq_bat_sho_030_lighting_default_none_out.%04d.exr'
        #file_path_mps = 'P:\\BM2\\seq\\des\\scn\\establishing001\\main\\mps\\bm2_seqsho_seq_bat_sho_030_footage_alta_dpx_out.%04d.dpx'
        file_path_mps = 'P:\\BM2\\seq\\bat\\sho\\030\\animation\\wip\\out\\footage\\bm2_seqsho_seq_bat_sho_030_footage_alta_dpx_out.%04d.dpx'
        file_path_zip = 'P:\\BM2\\seq\\bat\\sho\\030\\footage\\out\\bm2_seqsho_seq_bat_sho_030_footage_alta_dpx_out\\bm2_seqsho_seq_bat_sho_030_footage_alta_dpx_out.%04d.dpx'
    
        files_to_download_ = self.downloader.check_file_path_to_download(file_path=file_path_mps)
        print 'file_path_mps RESULT:'
        print files_to_download_
        
        files_to_download_ = self.downloader.check_file_path_to_download(file_path=file_path_zip)
        print 'file_path_zip RESULT:'
        print files_to_download_
        
        # >>>>
        self._init_widgets()
        self._failed_downloaded = []
        self._correct_downloaded = []

    @property
    def download_dependencies(self):
        return self.__STATE_DOWNLOAD_DEPENDENCIES
    
    @download_dependencies.setter
    def download_dependencies(self, value):
        if isinstance(value, bool):
            self.__STATE_DOWNLOAD_DEPENDENCIES = value
            self.download_ma_file.setChecked(value)
            self.downloader.set_download_dependency_mode(self.__STATE_DOWNLOAD_DEPENDENCIES)

    @property
    def download_content_from_filtered_folders(self):
        return self.__STATE_DOWNLOAD_CONTENT_FROM_FOLDERS
    
    @download_content_from_filtered_folders.setter
    def download_content_from_filtered_folders(self, value):
        if isinstance(value, bool):
            self.__STATE_DOWNLOAD_CONTENT_FROM_FOLDERS = value
            self.download_ma_file.setChecked(value)
            self.downloader.set_download_filtered_folder(value)

    @property
    def download_main_file(self):
        return self.__STATE_DOWNLOAD_MAIN_MA_FILE
    
    @download_main_file.setter
    def download_main_file(self, value):
        if isinstance(value, bool):
            self.__STATE_DOWNLOAD_MAIN_MA_FILE = value
            self.download_ma_file.setChecked(value)
    @property
    def state_unatended_create_folder_process(self):
        return self.__STATE_UNATENDED_CREATE_FOLDER_PRROCESS
    
    @state_unatended_create_folder_process.setter
    def state_unatended_create_folder_process(self, value):
        if isinstance(value, bool):
            self.__STATE_UNATENDED_CREATE_FOLDER_PRROCESS = value


    @property
    def state_popup_widget_on_finish(self):
        return self.__STATE_POPUP_WIDGET_ON_FINISHED_PROCESS
    
    @state_popup_widget_on_finish.setter
    def state_popup_widget_on_finish(self, value):
        if isinstance(value, bool):
            self.__STATE_POPUP_WIDGET_ON_FINISHED_PROCESS = value

    @property
    def overwrite_local_files(self):
        return self.__STATE_OVERWRITE_LOCAL_FILES
    
    @overwrite_local_files.setter
    def overwrite_local_files(self, value):
        if isinstance(value, bool):
            self.__STATE_OVERWRITE_LOCAL_FILES = value
            self.overwrite_chk_box.setChecked(value)
            self.downloader.set_overwrite_mode(value)
    
    
    @property
    def external_open_file(self):
        return self.__STATE_EXTERNAL_OPEN_FILE
    
    @external_open_file.setter
    def external_open_file(self, value):
        if isinstance(value, bool):
            self.__STATE_EXTERNAL_OPEN_FILE = value
    
    
    @property
    def internal_open_file(self):
        return self.__STATE_INTERNAL_OPEN_FILE
    
    @internal_open_file.setter
    def internal_open_file(self, value):
        if isinstance(value, bool):
            self.__STATE_INTERNAL_OPEN_FILE = value


    def _init_widgets(self):
        self.__init_icons()
        self._context_menu_list()
        self._init_log_state()
        self._init_signals()
        self._update_advance_options()
        
    def _update_advance_options(self):
        self.advance_options_widget.setVisible(False)
        self.download_main_file = self.__STATE_DOWNLOAD_MAIN_MA_FILE
        self.overwrite_local_files = self.__STATE_OVERWRITE_LOCAL_FILES
        self.download_dependencies = self.__STATE_DOWNLOAD_DEPENDENCIES
        self.download_content_from_filtered_folders = self.__STATE_DOWNLOAD_CONTENT_FROM_FOLDERS
        
        
    def _init_signals(self):
        #setting downloader signals
        self.downloader.on_file_finish_download.connect(self._on_file_finish_download, QtCore.Qt.QueuedConnection)
        self.downloader.on_file_start_download.connect(self._on_file_start_download, QtCore.Qt.QueuedConnection)
        self.downloader.on_finish_download.connect(self._on_finish_download, QtCore.Qt.QueuedConnection)
        self.downloader.on_start_download.connect(self._on_start_download, QtCore.Qt.QueuedConnection)


    def _init_log_state(self):
        #Log States
        self.set_log_visible(False)
        self.log_btn.setIcon(QtGui.QIcon(self.list_ico_path))
        self.log_text = ""
        # Loading Text and Movie
        self.set_loading_gif(False)

        
    def __init_icons(self):
        self.downloading_ico_path=os.path.join(ICO_PATH, "downloading.png")
        self.question_ico_path=os.path.join(ICO_PATH, "question.png")
        self.checked_ico_path=os.path.join(ICO_PATH, "checked.png")
        self.error_ico_path=os.path.join(ICO_PATH, "error.png")
        self.list_ico_path=os.path.join(ICO_PATH, "list.png")
        
        self.file_ma_ico_path=os.path.join(ICO_PATH, "maya_icon.png")
        self.file_nk_ico_path=os.path.join(ICO_PATH, "nuke_icon.png")
        


    def _context_menu_list(self):
        self.dependency_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # Context Menu
        # Copy Action
        copy_action = QtWidgets.QAction("Copy rout", self)
        copy_action.triggered.connect(self.copy_selected_rout)
        self.dependency_list.addAction(copy_action)



    def set_log_visible(self, state=True):
        self.log_widget.setVisible(state)
        

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
        elif state == DownloaderResponse.IN_PROGRESS:
            self.log_text += "\nDownloading:  {0}".format(file_path)
        self.log_text_widget.setPlainText(self.log_text)
        
        
    def clean_flags(self):
        pass
        
    def _on_file_finish_download(self, downloaderResponse):
        self.add_log(file_path=downloaderResponse.file_path, message=downloaderResponse.message, state=downloaderResponse.state)
        self.update_item(downloaderResponse.file_path, state=downloaderResponse.state)
        if downloaderResponse.state == DownloaderResponse.ERROR_STATE:
            self._failed_downloaded.append(downloaderResponse)
        else:
            self._correct_downloaded.append(downloaderResponse)
            
    def _on_file_start_download(self, downloaderResponse):
        self.add_item_in_list(downloaderResponse.file_path, state= downloaderResponse.state)
        self.add_log(file_path=downloaderResponse.file_path, message=downloaderResponse.message, state=downloaderResponse.state)
        
    def _on_finish_download(self):
        # update GIF
        self.set_loading_gif(False)        
        if self.state_popup_widget_on_finish:
            if self._failed_downloaded:
                level = MessageWindow.ERROR_LEVEL
                files = "\n ".join([obj.file_path for obj in self._failed_downloaded])
                msg = "Something was wrong downloading some files :'( , check  these files in the output panel. %s " % (files)
                left_text = "Close"
                right_text = "Retry"
            else:
                level = MessageWindow.INFO_LEVEL
                msg = "Process finished, apparently no errors found. :D"
                left_text =  "Close"
                right_text = "Continue"
            window = MessageWindow("Donwloader Process finished",level,msg=msg)
            window.name_btn_left = left_text
            window.name_btn_right = right_text
            window.exec_()
            if self._failed_downloaded:
                if window.get_response():
                    # means its the right click so retry the failled files
                    self.retry_download_process()
                    return
            
        if self.external_open_file:
            self.open_file()

        if self.internal_open_file:
            self.openFileSignal.emit()
            
        self.clean_flags()
        self.on_finish_download.emit()




    def _on_start_download(self):
        self._failed_downloaded = []
        self._correct_downloaded = []
        self.set_loading_gif(True)
        self.on_start_download.emit()

    def retry_download_process(self):
        self.dependency_list.clear()
        self.set_log_visible(True)
        if not self._failed_downloaded:
            return
        folder_processed = self.downloader.processed_folder_list
        self.downloader.set_default_state()
        self.downloader.set_files_to_process([obj.file_path for obj in self._failed_downloaded])
        self.downloader.processed_folder_list = folder_processed
        self.downloader.processed_file_list = self._correct_downloaded
        self.downloader.set_maxium_threads(self.thread_spinBox.value())
        self._failed_downloaded = []
        self._correct_downloaded = []
        self.downloader.download_files()


    
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
        if self.get_item(key):
            return 
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

    def clean_empty_characters(self, file_path):
        return file_path.replace(" ", "")
    
    def clean_quation_marks(self, file_path):
        return file_path.replace('\"','')
        

    def get_current_text(self):
        file_path = os.path.normpath(self.path.text()).replace("\\", "/")
        if not file_path or not file_path.endswith(".ma") or not file_path.endswith(".nk"):
            raise Exception("Specify a ma or nk file!")
        return file_path

    @QtCore.Slot()
    def on_update_btn_clicked(self):
        self.STATE_EXTERNAL_OPEN_FILE = True
        self.execute_update_process()

    def execute_download_file(self, download_file):
        file_list = [download_file]
        

        
        self.dependency_list.clear()
        self.log_text_widget.clear()
        self.set_log_visible(True)
        QtWidgets.QApplication.processEvents()
        self.downloader.set_files_to_process(file_list)
        self.create_default_folders_on_target(download_file)
        self.downloader.start_download_process()
        


    def execute_update_process(self,  extra_files_to_download=[]):
        """
        Set The loading gif visible
        Downloads the path if the current doesnt exist in local disk
        Calculates file_dependencies
        """
        
        file_list = []
        
        if extra_files_to_download:
            file_list.extend(extra_files_to_download)
        
        try:
            current_file_path = self.get_current_text()
        except:
            current_file_path = ""

        if current_file_path:
            if  not os.path.exists(current_file_path):
                file_path = self.downloader._dpx.getTargetPath(current_file_path)
                if file not in file_list:
                    file_list.append(file_path)
                self.create_default_folders_on_target(file_path)
            else:
                if self.download_main_file:
                    file_path = self.downloader._dpx.getTargetPath(current_file_path)
                    if file_path not in file_list:
                        file_list.append(file_path)
                    self.create_default_folders_on_target(file_path)

            if self.download_dependencies:
                if current_file_path:
                    dependencies = self.downloader.get_file_dependencies(current_file_path)
                    if dependencies:
                        file_list.extend(self.downloader.get_file_dependencies(file_path))
            
        self.dependency_list.clear()
        self.log_text_widget.clear()
        self.set_log_visible(True)
        self.downloader.set_files_to_process(file_list)
        self.downloader.set_maxium_threads(self.thread_spinBox.value())
        QtWidgets.QApplication.processEvents()
        self.downloader.start_download_process()

    def create_default_folders_on_target(self, file_path):
        """
        Creates default folders on the target path
        """
        if not self.state_unatended_create_folder_process:
            folders_list = ",".join(DATA.WORKING_FOLDERS)
            window = MessageWindow("Create Starter Folders","Warning",
                          msg="Do you want to create previous folders on the target"+\
                                "Path:\n %s \n FOLDERS: %s" % (file_path, folders_list))
    
            if window.get_response():
                folder = file_path.rsplit("/",2)[0]
                for working_folder in DATA.WORKING_FOLDERS:
                    self.create_path_rout(folder +'/'+ working_folder)
        else:
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
    def on_download_file_btn_clicked(self):
        try:
            current_file_path = self.get_current_text()
        except Exception as e:
            print e
            return

        if  not os.path.exists(current_file_path):
            current_file_path = self.downloader._dpx.getTargetPath(current_file_path)
        self.download_dependencies = False
        self.execute_download_file(current_file_path)
        
            
    @QtCore.Slot()
    def on_advance_options_btn_clicked(self):
        self.advance_options_widget.setVisible(self.advance_options_widget.isHidden())
    
    
    @QtCore.Slot(bool)
    def on_overwrite_chk_box_clicked(self, checked):
        self.overwrite_local_files = checked
    
    
    @QtCore.Slot(bool)
    def on_download_ma_file_clicked(self, checked):
        self.download_dependencies = checked
    
    
    @QtCore.Slot(str)
    def on_path_textChanged(self, file_path):
        file_path = self.clean_quation_marks(file_path)
        file_path = self.clean_empty_characters(file_path)
        self.path.setText(file_path)
    
    def open_file(self):
        maya_path = self._config.environ["maya_exe"]
        current_path = self.get_current_text()
        command = '"{0}" -file "{1}"'.format(maya_path,current_path)
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
