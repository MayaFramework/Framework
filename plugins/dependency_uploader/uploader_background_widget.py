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
import threading
import time
from Framework.lib.ui.qt_thread import CustomQThread

class UploaderBackgroundWidget(QtWidgets.QDialog):

    def __init__(self, file_path_list, max_threads=1):
        super(UploaderBackgroundWidget,self).__init__()
        if not isinstance(file_path_list, list) or not (len(file_path_list)>0):
            raise UploadException("Not enough file_path defined on the list to upload")

        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "uploader_background_widget.ui"), self)
        ui.apply_resource_style(self)
        self._file_path_list = list(set(file_path_list)) # Deleting repetitions
        self.maximum_threads = max_threads
        self.thread_spinBox.setValue(self.maximum_threads)
        self.timeout = 60*60
        self.uploader = Uploader()
        self.current_threads = 0
        self._threads = []
        self._chk_state = False
        self._out_state = False
        #BORRAR ESTO
        self.log_text = ''
        self._icons()
        
    def _icons(self):
        self.downloading_ico_path=os.path.join(ICON_PATH, "downloading.png")
        self.question_ico_path=os.path.join(ICON_PATH, "question.png")
        self.checked_ico_path=os.path.join(ICON_PATH, "checked.png")
        self.error_ico_path=os.path.join(ICON_PATH, "error.png")


        
    @property
    def chk_state(self):
        return self._chk_state
    
    @property
    def out_state(self):
        return self._out_state
    
    @chk_state.setter
    def chk_state(self, value):
        self._chk_state =  bool(value)
    
    @out_state.setter
    def out_state(self, value):
        self._out_state = bool(value)
    
    def add_item_in_list(self, list_widget, key, ):
        listItem = QtWidgets.QListWidgetItem(key)
        listItem.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "question.png")))
        self.dependency_list.addItem(listItem)
        QtWidgets.QApplication.processEvents()

    def fill_list_widget(self):
        for file_path in self._file_path_list:
            self.add_item_in_list(self.dependency_list, file_path)

    def get_item(self, file):
        result = self.dependency_list.findItems(file, QtCore.Qt.MatchExactly)
        if result:
            result = result[0]
        return result

    def upload(self):

        if not self._file_path_list:
            return True
        for filename in self._file_path_list:
            cThread = CustomQThread(self.upload_file, file_path=filename)
            cThread.file_path = filename
            cThread.on_finishing.connect(self.on_finished_download_file, QtCore.Qt.QueuedConnection)
            self._threads.append(cThread)
        for c_thread in self._threads:
            if self.is_available_thread(self.timeout):
                self.current_threads +=1
                c_thread.start()


    def is_available_thread(self, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self.current_threads <= self.maximum_threads:
                return True
            QtWidgets.QApplication.processEvents()

            time.sleep(period)
        return False

    def update_logger(self, file_path, message):
        # niapa arreglar el tema de QThreads
        self.log_text+= '\n{0}: \n   response:  {1}'.format(file_path, message)
        self.log_text_widget.setPlainText(self.log_text)

    def upload_file(self, file_path):

        response = None
        print "Uploading: %s" % file_path
        try:
            response = self.uploader.upload_file(file_path)
            if response:
                return (True, file_path, response)
            else:
                return (False, file_path, response)
        except Exception as e:
            return  (False, file_path, e)
    def on_finished_download_file(self, tuple_response):
        result, file_path, dpx_response = tuple_response
        item = self.get_item(file_path)
        print result, file_path, dpx_response
        if not item:
            return
        if result:
            item.setIcon(QtGui.QIcon(self.checked_ico_path))
            self.update_logger(file_path, "SUCCESS")
        else:
            item.setIcon(QtGui.QIcon(self.error_ico_path))
            self.update_logger(file_path, str(dpx_response))
        self.current_threads -=1
        QtWidgets.QApplication.processEvents()


    def on_starting_download_file(self, file_path):
        print "start Thread"
        item = self.get_item(file_path)
        if not item:
            return
        item.setIcon(QtGui.QIcon(self.downloading_ico_path))
        QtWidgets.QApplication.processEvents()

    def execute_upload_process(self):
        self.fill_list_widget()
        self.upload()


