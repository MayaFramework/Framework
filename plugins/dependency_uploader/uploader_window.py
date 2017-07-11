'''
Created on Jul 2, 2017

@author: Miguel
'''
import os
import sys
from Framework.lib.gui_loader import gui_loader
from uploader import Uploader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework import get_environ_file, get_css_path, get_icon_path
from Framework.lib.ui.widgets import tree_widget, common_widgets
from exceptions import *
import threading
import time
CSS_PATH = get_css_path()
ICON_PATH = get_icon_path()



def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)


class UploaderWindow(QtWidgets.QDialog):
    timeout = 60*60
    TOOL_NAME = "UPLOADER"
    def __init__(self):
        super(UploaderWindow, self).__init__()
        self.setWindowTitle(self.TOOL_NAME)
        self.current_threads = 0
        self.maximum_threads = 4
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "main.ui"), self)
        setStyleSheet(self,os.path.join(CSS_PATH,"dark_style1.qss"))
#         self.setupUi(self)
        self.uploader = Uploader()
        self._init_widget()
        
    def _init_widget(self):
        self.icon_path.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"file.png")))
        self.upload_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "upload.png")))
        self.analize_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "search.png")))
        self.add_row_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "add_color.png")))
        file_path = self.get_file_path()
        if file_path.endswith(".ma"):
            self.fill_tree_widget(file_path)

    @QtCore.Slot()
    def on_analize_btn_clicked(self):
        
        print self.find_tree_selection()


    @QtCore.Slot()
    def on_add_row_btn_clicked(self):
        new_row = NewRowPrompt()
        new_row.exec_()
        file_path = new_row.get_file_path()
        if not file_path:
            return
        
        tree_item = QtWidgets.QTreeWidgetItem(self.inspection_tree)
        tree_item.setText(0, file_path)
        tree_item.setCheckState(0, QtCore.Qt.Checked)
        tree_item.setIcon(0, QtGui.QIcon(os.path.join(ICON_PATH,"file_add.png")))
        self.inspection_tree.addTopLevelItem(tree_item)

    @QtCore.Slot(str)
    def on_path_line_edit_textChanged(self, file_path):
        if file_path.endswith('.ma'):
            self.icon_path.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"maya_icon.png")))
        else:
            self.icon_path.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"file.png")))

    def get_file_path(self):
        file_path = self.path_line_edit.text()
        if not file_path:
            raise Exception("Nothing defined in the file path box")
        return file_path

    def fill_tree_widget(self, file_path):

        dependencies_dict = self.uploader.get_dependencies(file_path)
        if not dependencies_dict:
            raise MaDepdencyException("Downloading: %s"%file_path)
        data = []
        # process filtered keys
        for dependency in dependencies_dict[self.uploader.FILTERED_KEY]:
            row_dict = {}
            # first column will be the path to upload
            row_dict[0] = {"text": str(dependency),
                           "icon": os.path.join(ICON_PATH, "file_add.png"),
                           "checked": 2}
            data.append({"value":row_dict})

        # processing not filtered key
        for dependency in dependencies_dict[self.uploader.NOT_FILTERED_KEY]:
            row_dict = {}
            # first column will be the path to upload
            if os.path.exists(dependency):
                tmp_ico = os.path.join(ICON_PATH, "warning.png")
                row_dict[0] = {"text": str(dependency),
                               "icon": tmp_ico,
                               "checked": 0}
            else:
                tmp_ico = os.path.join(ICON_PATH, "question.png")
                row_dict[0] = {"text": str(dependency),
                               "icon": tmp_ico,
                               "checked": None}
            data.append({"value":row_dict})





        headers = ["Files"]
        self.inspection_tree.clear()
        self.inspection_tree.setColumnCount(len(headers))
        self.inspection_tree.setHeaderLabels(headers)
        tree_widget.recursive_advance_tree(self.inspection_tree, data)
        # make possible to add custom routs in case of the tool doesnt recognize all the work routs
        

    def find_tree_selection(self):
        # access to the tree and find every children checked to add it into the list to upload
        """
        {u'Files': {u'P:/BM2/elm/gafasGato/sha/high/shading/mps/bm2_elmsha_elm_gafasGato_sha_high_shading_cuero_Diffuse_mps.tx':
                        {'CheckState': PySide.QtCore.Qt.CheckState.Unchecked},
             u'P:/BM2/elm/gafasGato/sha/high/shading/mps/bm2_elmsha_elm_gafasGato_sha_high_shading_cuero_Normal_mps.tx':
                             {'CheckState': PySide.QtCore.Qt.CheckState.Unchecked},
        """
        tree_info = tree_widget.get_elements_checked(self.inspection_tree)
        aux_list = []
        for path, value in tree_info["Files"].iteritems():
            # TODO Here check how to get the value from CheckState to after return the state
            if isinstance(value["CheckState"], QtCore.Qt.CheckState) and os.path.exists(path):
                aux_list.append(str(path))
        return aux_list


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
            item.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "downloading.png")))
            QtWidgets.QApplication.processEvents()
            state = self.uploader.upload_file(file)
            if state:
                item.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "checked.png")))
            else:
                item.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "error.png")))

        except Exception as e:
            item.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "error.png")))
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



class NewRowPrompt(QtWidgets.QDialog):
    
    def __init__(self):
        super(NewRowPrompt, self).__init__()
        setStyleSheet(self,os.path.join(CSS_PATH,"dark_style1.qss"))
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "add_row_widget.ui"), self)

        self.ico_file_path.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH, "error.png")))

    @QtCore.Slot(str)
    def on_file_path_lineEdit_textChanged(self, file_path):
        if os.path.exists(file_path):
            self.ico_file_path.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"checked.png")))
        else:
            self.ico_file_path.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"error.png")))

    @QtCore.Slot()
    def on_save_btn_clicked(self):
        file_path = self.file_path_lineEdit.text()
        if not os.path.exists(file_path):
            window = common_widgets.MessageWindow(title="Checking File Path",
                                         level=common_widgets.MessageWindow.ERROR_LEVEL,
                                         msg ="This file path doesn't exists: %s\n press CANCEL to modify the path otherwise it will close this view" % file_path)

            if window.get_response():
                self.close()
            else:
                return
        self.close()

    def get_file_path(self):
        file_path =self.file_path_lineEdit.text()
        if not os.path.exists(file_path):
            return ""
        else:
            return file_path



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = UploaderWindow()
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.exec_()

