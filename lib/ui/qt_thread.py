
"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
"""

from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.gui_loader import gui_loader
import sys, time
class CustomQThread(QtCore.QThread):
    on_starting = QtCore.Signal(str)
    on_finishing = QtCore.Signal(object)

    def __init__(self, func,*args, **kwargs):
        super(CustomQThread, self).__init__(parent=None)
        self._func = func
        self._kwargs = kwargs
        self._args  = args
        self._thread_name = 'CustomQThread'
    
    @property
    def thread_name(self):
        return self._thread_name
    
    @thread_name.setter
    def thread_name(self, value):
        self._thread_name = value

    def run(self):
        self.on_starting.emit(self.thread_name)
        response = self._func(*self._args,**self._kwargs)
        self.on_finishing.emit(response)

if __name__ == "__main__":
    class MainProgram():
        def __init__(self, parent=None):
            self.threads = []
    
            self.addWorker(CustomQThread(self.test_func, file_path=r"P:/bm2/chr\/test/test/shading/thinHigh/out/test.ma", target_path=r"/work/bm2/chr/test/test/shading/thinHigh/out/test.ma"))
    
        def test_func(self, file_path, target_path):
            print self
            print file_path, target_path
            return file_path
            class my_return_test(object):
                def __init__(self):
                    super(my_return_test, self).__init__()
                    self._response = "MY RESPONSE"
            return my_return_test()
    
        def addWorker(self, worker):
            worker.on_starting.connect(self.printMessage, QtCore.Qt.QueuedConnection)
            worker.on_finishing.connect(self.get_response, QtCore.Qt.QueuedConnection)
    
            self.threads.append(worker)
    
        def startWorkers(self):
            for worker in self.threads:
                worker.start()
                # no wait, no finished. you start the threads and leave.
    
        def workersFinished(self):
            if all(worker.isFinished() for worker in self.threads):
                # wait until all the threads finished
                QtCore.QCoreApplication.instance().quit()
        @QtCore.Slot(object)
        def get_response(self, response):
            print response, type(response)
    
        @QtCore.Slot(str)
        def printMessage(self, message):
            print message
    #         sys.stdout.write(text+'\n')
    #         sys.stdout.flush()
    app = QtCore.QCoreApplication(sys.argv)
    m = MainProgram()
    m.startWorkers()
    sys.exit(app.exec_())
    