import os
import re
from functools import partial

import controller
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets
from Framework.lib.metadata_lib import metadata, metadata_utils
from core import scene, folder

import maya.cmds as cmds
import temp_config
import time
reload(temp_config)
reload(gui_loader)

PROJECT_ROOT = r"P:/BM2"

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class SceneLoaderUI(form, base):

    OPENSCENE = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/open_scene.png"))
    LISTWIDGETS = ["firstLevelLW", "secondLevelLW", "thirdLevelLW", "fourthLevelLW", "fifthLevelLW", "sceneLW"]

    saved_scene = QtCore.Signal()

    def __init__(self):
        super(SceneLoaderUI, self).__init__()
        self.setupUi(self)

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
    def scene_selected(self):
        return self.__scene_selected

    @scene_selected.setter
    def scene_selected(self, value):
        self.__scene_selected = value

    def __default_state_window(self):
        self.__populate_initial_combo()

    def __connect_default_signals(self):
        self.categoryCB.activated.connect(self.__category_changed)
        self.firstLevelLW.itemClicked.connect(partial(self.__selection_changed, self.firstLevelLW))
        self.secondLevelLW.itemClicked.connect(partial(self.__selection_changed, self.secondLevelLW))
        self.thirdLevelLW.itemClicked.connect(partial(self.__selection_changed, self.thirdLevelLW))
        self.fourthLevelLW.itemClicked.connect(partial(self.__selection_changed, self.fourthLevelLW))
        self.fifthLevelLW.itemClicked.connect(partial(self.__selection_changed, self.fifthLevelLW))
        self.sceneLW.itemClicked.connect(self.__scene_selectedCB)

        self.loadSceneBT.clicked.connect(self.load_scene)
        self.saveLocalBT.clicked.connect(self.save_scene)

    def __populate_initial_combo(self):
        for path in os.listdir(PROJECT_ROOT):
            full_path = os.path.join(PROJECT_ROOT, path)
            folder_obj = folder.Folder(full_path)
            self.categoryCB.addItem(path, folder_obj)

    def __category_changed(self, index):
        folder_obj = self.categoryCB.itemData(index)
        self.final_path = folder_obj.folder_path
        children = folder_obj.children
        children_full_path = folder_obj.children_full_path
        self.__populate_lists(self.firstLevelLW, children_full_path)

    def __selection_changed(self, list_widget, item):
        item_data = item.data(QtCore.Qt.UserRole)
        if isinstance(item_data, folder.Folder):
            index = self.LISTWIDGETS.index(list_widget.objectName()) + 1
            self.__populate_lists(eval("self.{}".format(self.LISTWIDGETS[index])), item_data.children_full_path)
        elif isinstance(item_data, scene.Scene):
            print "scene"
        self.final_path = item_data.folder_path

    def __scene_selectedCB(self, scene_item):
        item_data = scene_item.data(QtCore.Qt.UserRole)
        if isinstance(item_data, scene.Scene):
            self.__refresh_ui(item_data)
            self.scene_selected = item_data

    def __refresh_ui(self, scene_item):
        self.sceneNameLB.setText(scene_item.scene_name)
        if scene_item.metadata:
            self.dateLB.setText(scene_item.metadata.modified)
            self.scene_image_pixmap.setPixmap(QtGui.QPixmap(scene_item.metadata.image))
            self.userLB.setText(scene_item.metadata.author)

    def __populate_lists(self, list_widget, paths):
        self.__clean(list_widget)
        for path in paths:
            list_item = QtWidgets.QListWidgetItem()
            if os.path.isdir(path):
                item_obj = folder.Folder(path)
                list_item.setData(QtCore.Qt.UserRole, item_obj)
                list_item.setText(item_obj.dir_name)
            elif path.endswith(".ma") or path.endswith(".mb"):
                item_obj = scene.Scene(path)
                list_item.setData(QtCore.Qt.UserRole, item_obj)
                list_item.setText(item_obj.scene_name)                
            list_widget.addItem(list_item)

    def __clean(self, list_widget):
        found = False
        for lw in self.LISTWIDGETS:
            if list_widget.objectName() != lw and not found:
                continue
            elif list_widget.objectName() != lw and found:
                list_widget.clear()
            else:
                found = True
                list_widget.clear()

    def load_scene(self):
        if self.scene_selected:
            self.scene_selected.load_scene()

    def save_scene(self):
        if self.scene_selected:
            self.scene_selected.save_scene()
            self.saved_scene.emit()

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