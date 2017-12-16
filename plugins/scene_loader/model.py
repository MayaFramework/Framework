import os
from functools import partial

import controller
import temp_config
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework import get_environ_config
from Framework.lib.gui_loader import gui_loader
from PySide2 import QtCore, QtGui, QtWidgets
from core import scene, folder
from Framework.plugins.scene_loader.gui.new_note_dialog import NewNoteDialog
from Framework.plugins.scene_loader.gui.show_notes_dialog import NotesDialog
import logging
import maya.cmds as cmds



reload(temp_config)
reload(gui_loader)

PROJECT_ROOT = "bm2"

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class SceneLoaderUI(form, base):

    SAVEICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/save_icon.png"))
    PUBLISHICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/publish_icon.png"))
    LISTWIDGETS = ["firstLevelLW", "secondLevelLW", "thirdLevelLW", "fourthLevelLW", "fifthLevelLW", "sceneLW"]

    saved_scene = QtCore.Signal()

    def __init__(self):
        super(SceneLoaderUI, self).__init__()
        self.setupUi(self)

        self._config = get_environ_config()
        # self.dpx = DropboxManager(self._config["test_dpx_token"])
        self._logger = logging.getLogger(__name__)
        self.dpx = DropboxManager("MspKxtKRUgAAAAAAAAA1OnMGBw6DOOG2Cz38E83-YJaxw7Jv2ihc2Afd-82vmZkI")

        self.__final_path = None
        self.__scene_selected = None

        self.__default_state_window()
        self.__connect_default_signals()

    @property
    def final_path(self):
        return self.__final_path

    @final_path.setter
    def final_path(self, value):
        self.__final_path = value

    @property
    def final_local_path(self):
        return self.final_path.replace("/work/", "P:/")

    @property
    def scene_selected(self):
        return self.__scene_selected

    @scene_selected.setter
    def scene_selected(self, value):
        if not isinstance(value, scene.Scene):
            raise Exception
        self.__scene_selected = value

    def __default_state_window(self):
        self.__populate_initial_combo()
        self.saveLocalBT.setIcon(self.SAVEICON)
        self.publishBT.setIcon(self.PUBLISHICON)

        self.sceneLW.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def __connect_default_signals(self):
        self.categoryCB.activated.connect(self.__category_changed)
        self.firstLevelLW.itemClicked.connect(partial(self.__selection_changed, self.firstLevelLW))
        self.secondLevelLW.itemClicked.connect(partial(self.__selection_changed, self.secondLevelLW))
        self.thirdLevelLW.itemClicked.connect(partial(self.__selection_changed, self.thirdLevelLW))
        self.fourthLevelLW.itemClicked.connect(partial(self.__selection_changed, self.fourthLevelLW))
        # self.fifthLevelLW.itemClicked.connect(partial(self.__selection_changed, self.fifthLevelLW))
        self.fifthLevelLW.itemClicked.connect(self.__fill_maya_files)
        self.sceneLW.itemClicked.connect(self.__scene_selectedCB)
        self.sceneLW.customContextMenuRequested.connect(self.__scene_context_menu)
        self.notesBT.clicked.connect(self.__show_notes)

        # self.loadSceneBT.clicked.connect(self.load_scene)
        self.saveLocalBT.clicked.connect(self.save_scene)
        self.publishBT.clicked.connect(self.publish_scene)

    def __populate_initial_combo(self):
        initial_folders = self.dpx.getFolderChildrenFromFolder(PROJECT_ROOT)
        for path in initial_folders:
            folder_obj = folder.Folder(path, self.dpx)
            self.categoryCB.addItem(path.split("/")[-1], folder_obj)

    def __category_changed(self, index):
        folder_obj = self.categoryCB.itemData(index)
        self.final_path = folder_obj.remote_path
        # children = folder_obj.children
        children_full_path = folder_obj.remote_children_folders
        self.__populate_lists(self.firstLevelLW, children_full_path)

    def __selection_changed(self, list_widget, item):
        item_data = item.data(QtCore.Qt.UserRole)
        if isinstance(item_data, folder.Folder):
            index = self.LISTWIDGETS.index(list_widget.objectName()) + 1
            self.__populate_lists(eval("self.{}".format(self.LISTWIDGETS[index])), item_data.remote_children_folders)
        elif isinstance(item_data, scene.Scene):
            print "scene"
        self.final_path = item_data.remote_path

    def __scene_selectedCB(self, scene_item):
        item_data = scene_item.data(QtCore.Qt.UserRole)
        if isinstance(item_data, scene.Scene):
            self.__refresh_ui(item_data)
            self.scene_selected = item_data

    def __refresh_ui(self, scene_item):
        self.sceneNameLB.setText(scene_item.scene_name)
        if scene_item.metadata:
            self.dateLB.setText(scene_item.metadata.modified)
            self.userLB.setText(scene_item.metadata.author)
            self.__set_scene_image(scene_item)
        else:
            self.dateLB.setText("")
            self.scene_image_pixmap.setPixmap(QtGui.QPixmap(""))
            self.userLB.setText("")

    def __set_scene_image(self, scene_item):
        ba = QtCore.QByteArray.fromBase64(str(scene_item.metadata.image))
        img = QtGui.QPixmap()
        img.loadFromData(ba)
        self.scene_image_pixmap.setPixmap(img)

    def __populate_lists(self, list_widget, paths):
        """
        Populate the given list with the following paths
        :param list_widget: str QListWidgetItem objectName
        :param paths: list Paths
        :return:
        """
        self.__clean(list_widget)
        for path in paths:
            list_item = QtWidgets.QListWidgetItem()
            list_widget.addItem(list_item)
            if path.endswith(".ma") or path.endswith(".mb"):
                item_obj = scene.Scene(path)
                list_item.setData(QtCore.Qt.UserRole, item_obj)
                # list_item.setText(item_obj.scene_name)
                scene_widget = SceneWidget(item_obj)
                list_item.setSizeHint(QtCore.QSize(0,30))
                list_widget.setItemWidget(list_item, scene_widget)
            else:
                item_obj = folder.Folder(path, self.dpx)
                list_item.setData(QtCore.Qt.UserRole, item_obj)
                list_item.setText(item_obj.dir_name)

    def __fill_maya_files(self, list_item):
        item_data = list_item.data(QtCore.Qt.UserRole)
        if isinstance(item_data, folder.Folder):
            self.__clean(self.sceneLW)
            # progress_bar = QtWidgets.QProgressDialog("Analyzing files", "Cancel", 0, len(item_data.remote_children_maya_files), self)

            for index, path in enumerate(item_data.remote_children_maya_files):
                list_item = QtWidgets.QListWidgetItem()
                self.sceneLW.addItem(list_item)
                item_obj = scene.Scene(path)
                list_item.setData(QtCore.Qt.UserRole, item_obj)
                # list_item.setText(item_obj.scene_name)
                scene_widget = SceneWidget(item_obj)
                list_item.setSizeHint(scene_widget.sizeHint())
                self.sceneLW.setItemWidget(list_item, scene_widget)
                # progress_bar.setValue(index)
                # if progress_bar.wasCanceled():
                #     break

        self.final_path = item_data.remote_path

    def __clean(self, list_widget):
        found = False
        for lw in self.LISTWIDGETS:
            lw_object = getattr(self, lw)
            if list_widget.objectName() != lw:
                if not found:
                    continue
                else:
                    lw_object.clear()
            else:
                found = True
                lw_object.clear()

    def __scene_context_menu(self, pos):
        item = self.sceneLW.itemAt(pos)
        disabled = False if item else True
        menu = self.__generate_menu(disabled)
        menu.move(self.sceneLW.mapToGlobal(pos))
        menu.exec_()

    def __generate_menu(self, disabled=False):
        menu = QtWidgets.QMenu()
        menu.addAction("Create new scene", self.__generate_new_scene)
        note = menu.addAction("Create Note", self.__add_notes)
        if disabled:
            note.setEnabled(not disabled)
        return menu

    def __add_notes(self):
        dialog = NewNoteDialog()
        accepted = dialog.exec_()
        if accepted:
            note = dialog.noteTE.toPlainText()
            if note != "":
                self.scene_selected.add_notes(note)

    def __show_notes(self):
        if self.scene_selected:
            notes = self.scene_selected.notes
            if notes != []:
                dialog = NotesDialog(notes)
                dialog.exec_()

    def __generate_new_scene(self):
        new_scene = controller.generate_new_scene(self.final_local_path)
        try: os.makedirs(self.final_local_path)
        except: pass
        cmds.file(new=True, f=True)
        cmds.file(rename="{}/{}".format(self.final_local_path, new_scene))
        cmds.file(save=True, f=True)
        new_scene = scene.Scene(cmds.file(q=True, sn=True))
        new_scene.save_scene()

    def load_scene(self):
        if self.scene_selected:
            self.scene_selected.load_scene()

    def save_scene(self):
        if self.scene_selected:
            self.scene_selected.save_scene()
            # self.saved_scene.emit()

    def publish_scene(self):
        if self.scene_selected:
            self.scene_selected.save_scene(create_snapshot=True, publish=True)
            # self.saved_scene.emit()

class SceneItem(QtWidgets.QListWidgetItem):

    def __init__(self, scene_path):
        super(SceneItem, self).__init__()
        self.scene_path = scene_path
        self.scene_obj = scene.Scene(scene_path)

        self.__default_state_window()

    @property
    def metadata(self):
        return self.scene_obj.metadata

    @property
    def name(self):
        return self.scene_obj.scene_name

    def __default_state_window(self):
        self.setText(self.scene_obj.scene_name)


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "scene_widget.ui")) 

       
class SceneWidget(form, base):

    OPENICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/open_icon.png"))
    DOWNLOAD = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/download_icon.png"))

    def __init__(self, scene_obj):
        super(SceneWidget, self).__init__()
        self.setupUi(self)
        self.scene_obj = scene_obj

        self.__default_state_window()
        self.__connect_default_signals()

    @property
    def metadata(self):
        return self.scene_obj.metadata

    def __default_state_window(self):
        self.sceneLB.setText(self.scene_obj.scene_name)
        self.openBT.setIcon(self.OPENICON)
        self.downloadBT.setIcon(self.DOWNLOAD)
        if self.metadata:
            self.__set_image()

    def __connect_default_signals(self):
        self.openBT.clicked.connect(self.open_scene)
        self.downloadBT.clicked.connect(self.download_scene)

    def __set_image(self):
        ba = QtCore.QByteArray.fromBase64(str(self.metadata.image))
        img = QtGui.QPixmap()
        img.loadFromData(ba)
        self.iconLB.setPixmap(img)

    def open_scene(self):
        self.scene_obj.open_scene()

    def download_scene(self):
        self.scene_obj.download_scene()

    def mousePressEvent(self, event):
        super(SceneWidget, self).mousePressEvent(event)
        # print "test"