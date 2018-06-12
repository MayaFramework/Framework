'''
Created on Jul 2, 2017
@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com
'''
import os
import sys
from Framework.lib import ui
from Framework.lib.gui_loader import gui_loader
from custom_row_widget import NewRowPrompt
from advance_options_widget import AdvanceOptionsWidget
from uploader_background_widget import UploaderBackgroundWidget
from uploader import Uploader
from uploader_exceptions import *
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework import get_environ_file, get_css_path, get_icon_path
from Framework.lib.ui.widgets import tree_widget, common_widgets
from exceptions import *
import threading
import time
from shutil import copyfile
CSS_PATH = get_css_path()
ICON_PATH = get_icon_path()

'''
:Example 
    work/bm2/elm/gafasgato_test/sha/high/shading/chk/bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma
    
    template path :
    {project}_{worktype}_{group}_{name}_{area}_{step}_{layer}_{partition}_{description}_{pipe}_.{ext}

:TODO
- Order list by icons state not by name
- Check name convention and fix the maya file

'''


class UploaderWindow(QtWidgets.QDialog):
    timeout = 60*60
    TOOL_NAME = "UPLOADER"
    CURRENT_AREA_WORK_PATH = " "
    
    PUBLISH_TO_CHK = False
    PUBLISH_TO_OUT = False
    ASK_TO_PUBLISH = True
    def __init__(self, parent=None, file_path=""):
        super(UploaderWindow, self).__init__(parent=parent)
        self.setWindowTitle(self.TOOL_NAME)
        self.current_threads = 0
        self.maximum_threads = 4
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "gui", "main.ui"), self)
        ui.apply_resource_style(self)
#         self.setupUi(self)
        self.uploader = Uploader()
        self._init_widget()
        if file_path:
            self.path_line_edit.setText(file_path)
        
    def _init_widget(self):
        self.upload_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "upload.png")))
        self.analize_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "search.png")))
        self.add_row_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "add_color.png")))
        self.check_name_convention_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH, "fix.png")))
        
        self.ico_path_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"file_add.png")))
        self.clear_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"eraser.png")))
        self.warning_leyend.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"warning.png")))
        self.question_leyend.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"question.png")))
        self.error_leyend.setPixmap(QtGui.QPixmap(os.path.join(ICON_PATH,"error.png")))
        
        self.set_actions_menu_for_inspection_tree()
        self.inspection_tree.resizeColumnToContents(1)
        self.inspection_tree.resizeColumnToContents(0)
        
        #TODO
        self.check_name_convention_btn.hide()

    @QtCore.Slot()
    def on_ico_path_btn_clicked(self):
        file_selected = QtWidgets.QFileDialog.getOpenFileNames(self, ("Open File"), "P:/bm2", ("Objects (*.ma )"))[0]
        if not file_selected:
            raise Exception("Not Path Found")
        self.path_line_edit.setText(file_selected[0])

    @QtCore.Slot()
    def on_analize_btn_clicked(self):
        self.execute_analize_process()

    @QtCore.Slot()
    def on_upload_btn_clicked(self):
        self.execute_upload_process()
        
    def execute_analize_process(self):
        file_path = self.get_file_path()
        if not file_path.endswith(".ma"):
            raise Exception("Not File Ma file extension")
        self.fill_tree_widget(file_path)
        
    def execute_upload_process(self):
        #check files and confirmation from the user
        main_file = self.uploader.dpx.getTargetPath(self.get_file_path())
        files_to_upload = self.find_tree_selection()
        files_to_upload.append(main_file)
        files_text = "\n".join(files_to_upload)
        message = "You are going to upload these files, do you agree?\n %s " % files_text
        prompt = common_widgets.MessageWindow(title="CONFIRMATION",msg=message)
        prompt.exec_()
        if not prompt.get_response():
            return
        # get chk and out options

        chk = None
        out = None
        if self.ASK_TO_PUBLISH:
            chk, out = self.publish_assistance_widget(main_file)
            
        
        self.uploader_background_widget = UploaderBackgroundWidget(file_path_list=files_to_upload,
                                                                   max_threads=self.threads_spin_box.value())

        self.uploader_background_widget.show()
        self.uploader_background_widget.execute_upload_process()

        if chk or self.PUBLISH_TO_CHK:
            self.publish_file_to_chk(main_file)
        
        if out or self.PUBLISH_TO_OUT:
            self.publish_file_to_out(main_file)


    def publish_file_to_chk(self, file_path):
        current_level = file_path.split("/")[-2]
        # replace location
        new_file = file_path.replace("/{0}/".format(current_level),"/chk/")
        # replace versions
        new_file = self.clean_version_from_file_path(new_file)
        # P:/bm2/seq/tst/sho/650/scncmp/wip/bm2_seqsho_seq_tst_sho_650_scncmp_default_none_wip.0005.ma
        #replace file name
        base_path, file_name = file_path.rsplit("/",1)
        
        name, extension = new_file.split(".")
    
        file_name_fields = name.split("_")
        #replace location in the file name
        file_name_fields[-1] = "chk"
        file_name = "_".join(file_name_fields)
        
        new_file = file_name+ ".{extension}".format(extension=extension)
        
        new_file_dpx = self.uploader_background_widget.uploader.dpx.getDropboxPath(new_file)
        self.uploader_background_widget.upload_custom_file(file_path=file_path, target_path=new_file_dpx)
        
        copyfile(file_path,new_file)
            
    def publish_file_to_out(self, file_path):
        current_level = file_path.split("/")[-2]
        # replace location
        new_file = file_path.replace("/{0}/".format(current_level),"/out/")
        # replace versions
        new_file = self.clean_version_from_file_path(new_file)
        # P:/bm2/seq/tst/sho/650/scncmp/wip/bm2_seqsho_seq_tst_sho_650_scncmp_default_none_wip.0005.ma
        #replace file name
        base_path, file_name = file_path.rsplit("/",1)
        
        name, extension = new_file.split(".")
    
        file_name_fields = name.split("_")
        #replace location in the file name
        file_name_fields[-1] = "out"
        file_name = "_".join(file_name_fields)
        
        new_file = file_name+ ".{extension}".format(extension=extension)
        
        new_file_dpx = self.uploader_background_widget.uploader.dpx.getDropboxPath(new_file)
        self.uploader_background_widget.upload_custom_file(file_path=file_path, target_path=new_file_dpx)
        copyfile(file_path, new_file)

    def clean_version_from_file_path(self, file_path):
        fields = file_path.split(".")
        return fields[0] + "." + fields[2]
        

    def publish_assistance_widget(self, main_file):
        current_level = main_file.split("/")[-2]
        advance_options_widget = AdvanceOptionsWidget()
        advance_options_widget.exec_()
        chk = advance_options_widget.chk_state
        out = advance_options_widget.out_state
        return chk,out
    
    def insert_new_file(self, file_path):
    
        #check if currently exists in the list
        if self.inspection_tree.findItems(file_path, QtCore.Qt.MatchExactly, 0):
            return
        tree_item = QtWidgets.QTreeWidgetItem(self.inspection_tree)
        tree_item.setText(0, file_path)
        tree_item.setCheckState(0, QtCore.Qt.Checked)
        if file_path.startswith(self.CURRENT_AREA_WORK_PATH):
            tree_item.setIcon(0, QtGui.QIcon(os.path.join(ICON_PATH,"file_add.png")))
        else:
            tree_item.setIcon(0, QtGui.QIcon(os.path.join(ICON_PATH,"warning.png")))

        self.inspection_tree.addTopLevelItem(tree_item)

    @QtCore.Slot()
    def on_add_row_btn_clicked(self):
        new_row = NewRowPrompt()
        new_row.exec_()
        file_list = new_row.get_file_path()
        if not file_list:
            return
            
        for file_path in file_list:
            self.insert_new_file(self.uploader.dpx.normpath(file_path))
        self.resize_tree_widget()

    def resize_tree_widget(self):
        self.inspection_tree.resizeColumnToContents(1)
        self.inspection_tree.resizeColumnToContents(0)
        self.inspection_tree.header().setResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.inspection_tree.header().setResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.inspection_tree.header().setResizeMode(1,QtWidgets.QHeaderView.Fixed)

    @QtCore.Slot(str)
    def on_path_line_edit_textChanged(self, file_path):
        if not os.path.exists(file_path):
            self.ico_path_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"error.png")))
            return

        if file_path.endswith('.ma'):
            self.ico_path_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"maya_icon.png")))
        else:
            self.ico_path_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"file.png")))


    @QtCore.Slot()
    def on_clear_btn_clicked(self):
        self.inspection_tree.clear()
        self.path_line_edit.setText("")

    @QtCore.Slot()
    def on_check_name_convention_btn_clicked(self):
        path = self.get_file_path()
        print self.uploader.dpx.getDropboxPath(path)
        self.check_name_convention(path)
    def check_name_convention(self, file_path):
        '''
        :Example 
        work/bm2/elm/gafasgato_test/sha/high/shading/chk/bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma
        
        template path :
        {project}_{worktype}_{group}_{name}_{area}_{step}_{layer}_{partition}_{description}_{pipe}_.{ext}
        '''
        file_path = "work/bm2/elm/gafasgato_test/sha/high/shading/chk/bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
        print file_path
        #=======================================================================
        # base_path
        #=======================================================================
        fields = os.path.dirname(file_path).split("/")
        project = fields[1]
        group = fields[2]
        name = fields[3]
        area = fields[4]
        step = fields[5]
        layer = fields[6]
        pipe = fields[7]
        partition = ''
        description = ''
        worktype = group+area
        print project, group, name, area, step, layer, pipe, partition, description, worktype
        print '_'.join([project,worktype, group, name, area, step, layer, pipe])
        #=======================================================================
        # file_name
        #=======================================================================
        file_name = os.path.basename(file_path).split("_")
        project = ''
        worktype = ''
        group = ''
        name = ''
        area = ''
        step = ''
        layer = ''
        partition = ''
        description = ''
        pipe = ''



    def get_file_path(self):
        file_path = self.path_line_edit.text()
        while file_path.startswith(" ") or file_path.endswith(" "):
            file_path = file_path.replace(" ", "")
        if not file_path:
            raise Exception("Nothing defined in the file path box")
        if not os.path.exists(file_path):
            raise Exception("Not file path found on local disk: %s " % file_path)
        file_path = self.uploader.dpx.normpath(file_path)
        self.path_line_edit.setText(file_path)
        self.CURRENT_AREA_WORK_PATH = file_path.split("/")[-3]
        self.work_area_label.setText(self.CURRENT_AREA_WORK_PATH)
        return self.uploader.dpx.normpath(file_path)

    def fill_tree_widget(self, file_path):
        dependencies_dict = self.uploader.get_dependencies(file_path)
        if not dependencies_dict:
            raise MaDepdencyException("Downloading: %s"%file_path)
        data = []
        # process filtered keys
        for dependency in dependencies_dict[self.uploader.FILTERED_KEY]:
            row_dict = {}
            dependency = self.uploader.dpx.normpath(dependency)
            # first column will be the path to upload
            row_dict[0] = {"text": str(dependency),
                           "icon": os.path.join(ICON_PATH, "file_add.png"),
                           "checked": 2}
            row_dict[1] = {
                        "text": dependency.rsplit("/")[-3],
                        "icon": os.path.join(ICON_PATH, "marker.png"),
                        "checked": None
            }
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
                row_dict[1] = {
                                "text": dependency.rsplit("/")[-3],
                                "icon":  os.path.join(ICON_PATH, "marker.png"),
                                "checked": None
                    }
            else:
                tmp_ico = os.path.join(ICON_PATH, "question.png")
                row_dict[0] = {"text": str(dependency),
                               "icon": tmp_ico,
                               "checked": None}
                row_dict[1] = {
                                "text": dependency.rsplit("/")[-3],
                                "icon":  os.path.join(ICON_PATH, "marker.png"),
                                "checked": None
                    }
            data.append({"value":row_dict})





        headers = ["Files","Work Area"]
        self.inspection_tree.clear()
        self.inspection_tree.setColumnCount(len(headers))
        self.inspection_tree.setHeaderLabels(headers)
        tree_widget.recursive_advance_tree(self.inspection_tree, data)
        
        
        self.resize_tree_widget()
        # make possible to add custom routes in case of the tool doesnt recognize all the work routs
#         self.inspection_tree.resizeColumnToContents(1)
#         self.inspection_tree.resizeColumnToContents(0)
#         self.inspection_tree.header().setResizeMode(QtWidgets.QHeaderView.ResizeToContents)
#         self.inspection_tree.header().setResizeMode(0,QtWidgets.QHeaderView.Stretch)
#         self.inspection_tree.header().setResizeMode(1,QtWidgets.QHeaderView.Fixed)
# #         
#         self.inspection_tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
#         self.inspection_tree.header().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
#         self.inspection_tree.header().setSectionResizeMode(1,QtWidgets.QHeaderView.Fixed)
# #         
        self.inspection_tree.setColumnWidth(1, 100)


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
        if not "Files" in tree_info:
            return aux_list
        for path, value in tree_info["Files"].iteritems():
            # TODO Here check how to get the value from CheckState to after return the state
            if (value["CheckState"] == 2) and os.path.exists(path):
                aux_list.append(str(path))
        return aux_list


    def set_actions_menu_for_inspection_tree(self):
#         menu = QtWidgets.QMenu(self)
#         quitAction = menu.addAction("Quit")
#         action = menu.exec_(self.mapToGlobal(event.pos()))
        self.inspection_tree.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        remove_action = QtWidgets.QAction(self)
        remove_action.setText("Remove Files")
        remove_action.triggered.connect(self.remove_row_from_inspection_tree)
        self.inspection_tree.addAction(remove_action)
        
        copy_action = QtWidgets.QAction(self)
        copy_action.setText("Copy Files")
        copy_action.triggered.connect(self.copy_files_from_inspection_tree)
        self.inspection_tree.addAction(copy_action)
        
        
        select_action = QtWidgets.QAction(self)
        select_action.setText("Check Files Selected")
        select_action.triggered.connect(self.check_selected_items_from_inspection_tree)
        self.inspection_tree.addAction(select_action)
        
    def copy_files_from_inspection_tree(self):
        selected_items = self.inspection_tree.selectedItems()
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Cliboard)
        result = []
        for item in selected_items:
            result.append(item.text(0))
        if len(result)==1:
            text = result[0]
        elif len(result) > 1:
            text = "; ".join(result)
        cb.setText(text, mode=cb.Cliboard)
        
    def check_selected_items_from_inspection_tree(self):

        selected_items = self.inspection_tree.selectedItems()
        for item in selected_items:
            if item.checkState(0) == QtCore.Qt.Checked:
                item.setCheckState(0,QtCore.Qt.Unchecked)
            else:
                item.setCheckState(0,QtCore.Qt.Checked)

    def remove_row_from_inspection_tree(self):
        print "REMOVING"
        selected_items = self.inspection_tree.selectedItems()
        for item in selected_items:
            print item.text(0)
            self.inspection_tree.takeTopLevelItem(self.inspection_tree.indexOfTopLevelItem(item))
 

    def get_item(self, name):
        """
        Finds the specified name into the tree widget
        """
        result = self.inspection_tree.findItems(name, QtCore.Qt.MatchExactly)
        if result:
            result = result[0]
        return result





if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader

    app = QtWidgets.QApplication(sys.argv)
    widget = UploaderWindow()
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.show()
    app.exec_()

