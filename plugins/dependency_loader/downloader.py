

"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
"""
import copy
import os, sys
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.config.config import Config
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.ui.qt_thread import CustomQThread
from Framework.lib.ma_utils.reader import MaReader
import time
import datetime
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
        if file_path and isinstance(file_path, (str, unicode)):
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
    
    #filters
    FILTER_ERROR_PATHS = ['.mayaSwatches']
    NONEXISTENT_PATH = ["<UDIM>", "###"]
    
    #signals
    on_finish_download = QtCore.Signal()
    on_start_download = QtCore.Signal()
    on_file_start_download = QtCore.Signal(DownloaderResponse)
    on_file_finish_download = QtCore.Signal(DownloaderResponse)
    STATE_OVERWRITE_LOCAL_FILES = True
    STATE_DOWNLOAD_DEPENDENCIES = True
    STATE_DOWNLOAD_CONTENT_FROM_FOLDERS = True
    
    #checks
    CHECK_FILE_SIZE = True
    CHECK_MODIFIED_DATE = False
    
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
        self._thrash_threads = []
        self._current_thread_count = 0
        self._maximum_threads = 10
        self._processed_file_list = []
        self._threads_processed = 0
    
    def set_overwrite_mode(self, value=True):
        if isinstance(value, bool):
            self.STATE_OVERWRITE_LOCAL_FILES = value

    def set_download_dependency_mode(self,  value=True):
        if isinstance(value, bool):
            self.STATE_DOWNLOAD_DEPENDENCIES = value

    def set_download_filtered_folder(self,  value=True):
        if isinstance(value, bool):
            self.STATE_DOWNLOAD_CONTENT_FROM_FOLDERS = value

    def set_maxium_threads(self, maximum):
        if isinstance(maximum, int):
            self._maximum_threads = maximum

    def set_files_to_process(self, file_list):
        self._file_list = [self._dpx.getTargetPath(x) for x in file_list]
    
    @property
    def processed_file_list(self):
        return self._processed_file_list

    @processed_file_list.setter
    def processed_file_list(self, file_list):
        self._processed_file_list = file_list
        
    
    
    @property
    def processed_folder_list(self):
        return self._folders_processed

    @processed_folder_list.setter
    def processed_folder_list(self, file_list):
        self._folders_processed = file_list
        
    
    
    def start_download_process(self):
        self.set_default_state()
        self.on_start_download.emit()
        self.download_files(self._file_list)

    def is_loadable(self, file_path):
        for c_filter in self.FILTER_ERROR_PATHS:
            if c_filter in file_path:
                return False
        return True
            
        
        
    def download_files(self, file_list=[]):
        """
        Check for each file if it has been processed or not.
        IF its not, add a new Thread and execute the list of threads
        """
        
        if not file_list:
            file_list = self._file_list
            if not self._file_list:
                raise Exception("Not file list defined")
        # for each file list check if its a maya file and get its dependencies
        aux_file_list = copy.deepcopy(file_list)
        tmp_file_list = copy.deepcopy(file_list)
        for f in tmp_file_list:
            print f
            if not self.is_loadable(f):
                self._processed_file_list.append(f)
                continue
            t_path = self._dpx.getTargetPath(f)
            if t_path in self._processed_file_list:
                aux_file_list.remove(t_path)
                continue
#             TO DEBUG CHILDREN FILE PATHS
#             else:
#                 print "t_path: {t_path} not in this list {processed}".format(t_path = t_path,
#                                                                              processed = str(self._processed_file_list))
                        
            self._processed_file_list.append(t_path)
            cThread = CustomQThread(func=self.download_file, file_path=t_path)
            cThread.on_finishing.connect(self.on_finished_download_file, QtCore.Qt.QueuedConnection)
            cThread.file_path = t_path
            if not self.thread_exist(cThread):
                self._threads.append(cThread)

        
        for thread in self._threads:
            if thread.file_path in aux_file_list and self.is_available_thread(timeout=60*60):
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
        response.file_path = file_path
        # some paths are not found in dropbox because maya format some routs
        # to indicate a sequence of images, etc... 
        
        if [x for x in self.NONEXISTENT_PATH if x in file_path]:
            response.state = DownloaderResponse.SUCCESS_STATE
        else:
            response.state = result
        

            
        self._current_thread_count -=1
        self.on_file_finish_download.emit(response)
        new_files = []
        if response.state == DownloaderResponse.ERROR_STATE:
            self._threads_processed += 1
            # if fails before return check if its in the filter rules and
            # get files
            if self.is_file_in_filter_rules(file_path):
                folder = file_path.rsplit("/",1)[0]
                if not folder in self._folders_processed:
                    children = self.get_children_from_folder(folder)
                    if children:
                        if not folder in self._folders_processed:
                            self._folders_processed.append(folder)
                            new_files.extend(children)
            if new_files:
                self.download_files(list(set(new_files)))
                
            if self.is_process_finished():
                self.on_finish_download.emit()

            return
        elif response.state == DownloaderResponse.SUCCESS_STATE:
            if self.CHECK_FILE_SIZE and os.path.exists(file_path):
                file_path_mtd = self._dpx.getFileMetadata(file_path)
                local_size = 0
                try:
                    local_size = os.path.getsize(file_path)
                except Exception as e:
                    print e, "problem getting the size of file: %s"%(file_path)
                if local_size and not int(local_size) == int(file_path_mtd.size):
                    response.state = DownloaderResponse.ERROR_STATE
                    response.message = "Download success but different size from the local content"
                    
#                 print file_path, local_size, file_path_mtd.size
        
        
        # Now check for new possible files pulling from this one
        # calculating dependencies
        if self.STATE_DOWNLOAD_DEPENDENCIES:
            dependencies = self.get_file_dependencies(file_path)
            if dependencies:
                new_files.extend(dependencies)
                
        if self.STATE_DOWNLOAD_CONTENT_FROM_FOLDERS:
            # check filter folders
            if self.is_file_in_filter_rules(file_path):
                folder = file_path.rsplit("/",1)[0]
                if not folder in self._folders_processed:
                    children = self.get_children_from_folder(folder)
                    if children:
                        if not folder in self._folders_processed:
                            self._folders_processed.append(folder)
                            new_files.extend(children)
        if new_files:
            self.download_files(list(set(new_files)))
            
        # check if its the last thread to process
        self._threads_processed += 1
        if self.is_process_finished():
            self.on_finish_download.emit()

    def set_default_state(self):
        self._folders_processed = []
        self._processed_file_list = []
        self._threads = []
        self._current_thread_count = 0
        self._threads_processed = 0
        self._total_threads_to_process = 0

    def is_process_finished(self):
        if self._threads_processed == len(self._threads):
            return True
        
        print self._threads_processed, len(self._threads)
        return False

    def download_file(self, file_path):
        '''
        Download file and parse the result in a tuple of 3 elements
        :param file_path: str
        
        return:
            tuple:  False/True (bool)
                    file_path (str)
                    dropboxManager response (object)
        '''

        # TODO: set only readable when download finished and if exists in local
        # and the permission its just readable change it to editable
        # TODO: Add format error to regroup them into more understandable messages
        
        response = DownloaderResponse()
        response.message =  "Downloading: %s " % file_path
        response.state = DownloaderResponse.IN_PROGRESS
        response.file_path = file_path
        self.on_file_start_download.emit(response)
        response = "ERROR"
        if self.CHECK_MODIFIED_DATE and os.path.exists(file_path):
            
            try:
                file_path_metadata= self._dpx.getFileMetadata(file_path)
            except Exception as e:
                print e
                return (DownloaderResponse.ERROR_STATE, file_path, e)
            local_datetime = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            dropbox_datetime = file_path_metadata.client_modified
            print local_datetime, dropbox_datetime, file_path
            if local_datetime and dropbox_datetime:
                if local_datetime > dropbox_datetime:
                    return (DownloaderResponse.SUCCESS_STATE, file_path, "Remote file older than local")
        
        try:
            if not os.path.exists(file_path):
                response = self._dpx.downloadFile(file_path)
            else:
                if self.STATE_OVERWRITE_LOCAL_FILES:
                    response = self._dpx.downloadFile(file_path)
                else:
                    return(DownloaderResponse.SUCCESS_STATE, file_path, "Not overwritten")

            if response:
                return (DownloaderResponse.SUCCESS_STATE, file_path, response)
            else:
                return (DownloaderResponse.ERROR_STATE, file_path, "")
        except Exception as e:
            return  (DownloaderResponse.ERROR_STATE, file_path, e)

    def get_file_dependencies(self, file_path):
        try:
            if self.is_ma_file(file_path):
                dependencies = MaReader.get_references(file_path)
                if dependencies: 
                    return [self._dpx.getTargetPath(x) for x in dependencies]
            else:
                return []
        except Exception as e:
            print e
            return []
    def is_ma_file(self, file_path):
        if file_path.endswith(".ma"):
            return True
        else:
            return False
   
    
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
        children = self._dpx.getAllChildren(folder)
        return [self._dpx.getTargetPath(x.path_display) for x in children]

        