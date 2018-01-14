

"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
"""

from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.config.config import Config
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.ui.qt_thread import CustomQThread
from Framework.lib.ma_utils.reader import MaReader
import time
import DATA as D_DATA
class DownloaderResponse(object):
    SUCCESS_STATE = 2
    IN_PROGRESS = 1
    ERROR_STATE = 0
    AVAILABLE_STATES = [SUCCESS_STATE, IN_PROGRESS, ERROR_STATE]
    def __init__(self):
        super(DownloaderResponse, self).__init__()
        self.__file_path = ""
        self.__message = ""
        self.__state = 1
        
    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path):
        if file_path and isinstance(file_path, (str, tuple)):
            self.__file_path = file_path
        else:
            raise Exception("Not supported data: FilePath: %s" % type(file_path))
    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
#         if message and isinstance(message, (str, tuple)):
        self.__message = message
#         else:
#             raise Exception("Not supported data: Message: %s" % type(message))
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        if isinstance(state, int) and state in self.AVAILABLE_STATES:
            self.__state = state
        else:
            raise Exception("Not supported data: State: %s" % type(state))
        
    

class Downloader(QtCore.QObject):
    
    on_finish_download = QtCore.Signal()
    on_start_download = QtCore.Signal()
    on_file_start_download = QtCore.Signal(DownloaderResponse)
    on_file_finish_download = QtCore.Signal(DownloaderResponse)
    def __init__(self, file_list=[]):
        super(Downloader, self).__init__()
        if isinstance(file_list, list):
            self._file_list = file_list
        #Filter rules to download all its children
        filter_folders = D_DATA.FILTER_FOLDERS
        self._config = Config.instance()
        dpx_token = self._config.environ["dpx_token"]
        self._dpx = DropboxManager.instance()
        self._threads = []
        self._current_thread_count = 0
        self._maximum_threads = 10
    def set_maxium_threads(self, maximum):
        if isinstance(maximum, int):
            self._maximum_threads = maximum

    def set_files_to_process(self, file_list):
        self._file_list = [self._dpx.getTargetPath(x) for x in file_list]
    
    
    def start_download_process(self):
        self._processed_file_list = []
        self._threads = []
        self._current_thread_count = 0
        self.on_start_download.emit()
        self.download_files(self._file_list)
        
    def download_files(self, file_list=[]):
        """
        Check for each file if it has been processed or not.
        IF its not, add a new Thread and execute the list of threads
        """
        
        if not file_list:
            raise Exception("Not file list defined")
        # for each file list check if its a maya file and get its dependencies
        for f in file_list:
            t_path = self._dpx.getTargetPath(f)
            if t_path in self._processed_file_list:
                file_list.remove(f)
                continue
            self._processed_file_list.append(t_path)
            cThread = CustomQThread(func=self.download_file, file_path=t_path)
            cThread.on_finishing.connect(self.on_finished_download_file, QtCore.Qt.QueuedConnection)
            cThread.file_path = f
            if not self.thread_exist(cThread):
                self._threads.append(cThread)

        
        for thread in self._threads:
            if thread.file_path in file_list and self.is_available_thread(timeout=60*60):
                self._current_thread_count +=1
                thread.start()
            

    def thread_exist(self, thread):
        for thd in self._threads:
            if thread.file_path == thd.file_path:
                return True
        return False
    
    def is_available_thread(self, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self._current_thread_count <= self._maximum_threads:
                return True
            QtWidgets.QApplication.processEvents()
            time.sleep(period)
        return False
    
    def on_finished_download_file(self, tuple_response):
        """
        emit response with the following object DownloaderResponse
        Calculate new dependencies
        Check if its in the filter list and in that case download every file within the folder 
        """
        result, file_path, dpx_response = tuple_response
        response = DownloaderResponse()
        response.message = dpx_response
        response.state = result
        response.file_path = file_path
        self._current_thread_count -=1
        self.on_file_finish_download.emit(response)
        if response.state == DownloaderResponse.ERROR_STATE:
            return
        # Now check for new possible files pulling from this one
        new_files = []
        # calculating dependencies
        dependencies = self.get_file_dependencies(file_path)
        if dependencies:
            new_files.extend(new_files)
        # check filter folders
        if self.is_file_in_filter_rules(file_path):
            folder = file_path.rsplit("/",1)[0]
            children = self.get_children_from_folder(folder)
            if children:
                new_files.extend(children)
        if new_files:
            self.download_files(list(set(new_files)))
    def download_file(self, file_path):
        '''
        Download file and parse the result in a tuple of 3 elements
        :param file_path: str
        
        return:
            tuple:  False/True (bool)
                    file_path (str)
                    dropboxManager response (object)
        '''
        
        response = DownloaderResponse()
        response.message =  "Downloading: %s " % file_path
        response.state = DownloaderResponse.IN_PROGRESS
        response.file_path = file_path
        self.on_file_start_download.emit(response)
        response = "ERROR"
        print "Downloading: %s" % file_path
        try:
            response = self._dpx.downloadFile(file_path)
            if response:
                return (DownloaderResponse.SUCCESS_STATE, file_path, response)
            else:
                return (DownloaderResponse.ERROR_STATE, file_path, "")
        except Exception as e:
            return  (DownloaderResponse.ERROR_STATE, file_path, e)

    def get_file_dependencies(self, file_path):
        try:
            if not self.is_ma_file(file_path):
                return {}
            dependencies = MaReader.get_references(file_path)
            if dependencies: 
                return [x for x in dependencies]
        except Exception as e:
            print e
            return {}
    def is_ma_file(self, file_path):
        if file_path.endswith(".ma"):
            return None
   
    
    def is_file_in_filter_rules(self, file_path):
        """
        Check if the path fits with the filters
        In that case downlaod the children from that path
        """
        for f_filter in D_DATA.FILTER_FOLDERS:
            if f_filter in file_path:
                return True
        return False
    
    def get_children_from_folder(self, folder):
        """
        return every children from the folder formated
        """
        children = self._dpx.getChildrenFromFolder(folder)
        return [self._dpx.getTargetPath(x) for x in children]
    
    
    
    
    
    
    
    
    
    
    
        
        