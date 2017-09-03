import os
import re

import controller
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets
from Framework.lib.metadata_lib import metadata, metadata_utils
from core import scene

import maya.cmds as cmds
import temp_config
import time
reload(temp_config)
reload(gui_loader)

PROJECT_ROOT = r"P:/"

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class SceneLoaderUI(form, base):

    OPENSCENE = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/open_scene.png"))

    def __init__(self):
        super(SceneLoaderUI, self).__init__()
        self.setupUi(self)
        # self.proyect_tree = controller.generate_paths_info(PROJECT_ROOT)['P:/BM2']# temp_config.PROJECT_TEMP['P:/BM2']# 
        self.__root = "P:/BM2"
        self.__category = None
        self.__first_level = None
        self.__second_level = None
        self.__third_level = None
        self.__fourth_level = None
        self._path = None
        self.proyect_tree = controller.generate_paths_info2(self.__root) # temp_config.PROJECT_TEMP['P:/BM2']# 
        self.__current_tab = None
        # self.myProcess = FoldersTree()
        # self.myProcess.start()

        self.__default_window_state()
        self.__connect_default_signals()
        
    def __default_window_state(self):
        self.categoryCB.addItems(sorted(self.proyect_tree))
        self.__set_icons()

    def __set_icons(self):
        self.loadSceneBT.setIcon(self.OPENSCENE)

    def __connect_default_signals(self):
        self.categoryCB.currentIndexChanged[str].connect(self.__category_change)
        self.firstLevelLW.itemClicked.connect(self.__first_level_changed)
        self.secondLevelLW.itemClicked.connect(self.__second_level_changed)
        self.thirdLevelLW.itemClicked.connect(self.__third_level_changed)
        self.fourthLevelLW.itemClicked.connect(self.__fourth_level_changed)
        self.scenesTW.currentChanged.connect(self.__scene_type_changed)
        self.loadSceneBT.clicked.connect(self.__load_scene)
        self.saveLocalBT.clicked.connect(self.__save_local)
        # self.myProcess.finished.connect(self.__thread_finished)

    # def __thread_finished(self):
    #     self.all_paths = self.myProcess.project_tree
    #     print "SE FINI"

    def __category_change(self, category):
        self.__category = category
        self._path = os.path.join(self.__root, category)
        self.__reset_lists()
        self.firstLevelLW.addItems(sorted(controller.generate_paths_info2(self._path)))

    def __first_level_changed(self, list_item):
        # current_keys = sorted(self.proyect_tree[self.__category][list_item.text()].keys())
        self.__first_level = list_item.text()
        self._path = os.path.join(self.__root, self.__category, self.__first_level)
        self.secondLevelLW.clear()
        self.thirdLevelLW.clear()
        self.fourthLevelLW.clear()
        self.secondLevelLW.addItems(sorted(controller.generate_paths_info2(self._path)))
        self.firstLevelBT.setText(list_item.text())

    def __second_level_changed(self, list_item):
        # current_keys = sorted(self.proyect_tree[self.__category][self.__first_level][list_item.text()].keys())
        self.__second_level = list_item.text()
        self.thirdLevelLW.clear()
        self.fourthLevelLW.clear()
        self._path = os.path.join(  self.__root, self.__category, 
                                    self.__first_level, self.__second_level)
        self.thirdLevelLW.addItems(sorted(controller.generate_paths_info2(self._path)))
        self.secondLevelBT.setText(list_item.text())

    def __third_level_changed(self, list_item):
        # current_keys = sorted(self.proyect_tree[self.__category][self.__first_level]
        #                                        [self.__second_level][list_item.text()].keys())
        self.__third_level = list_item.text()
        self._path = os.path.join(  self.__root, self.__category, 
                                    self.__first_level, self.__second_level, self.__third_level)        
        self.fourthLevelLW.clear()
        self.fourthLevelLW.addItems(sorted(controller.generate_paths_info2(self._path)))
        self.thirdLevelBT.setText(list_item.text())

    def __fourth_level_changed(self, list_item):
        self.__fourth_level = list_item.text()
        self._path = os.path.join(  self.__root, self.__category, self.__first_level, 
                                    self.__second_level, self.__third_level, self.__fourth_level)   
        self.fourthLevelBT.setText(list_item.text())
        self.scenes_dictionary = controller.generate_paths_info(self._path).get(self.__fourth_level)
        self.__populate_scenes(self.scenes_dictionary)

    def __scene_type_changed(self, tab_index):
        self.__current_tab = self.scenesTW.tabText(tab_index)

    def __populate_scenes(self, scenes_tree):
        self.__delete_tabs()
        if scenes_tree:
            for folder, scenes in scenes_tree.iteritems():
                scenes_list_widget = QtWidgets.QListWidget()
                scenes_list_widget.itemClicked.connect(self.__scene_selected)
                all_scenes = sorted([item for item in scenes.keys() if item.endswith(".ma")], reverse=True)
                for scene in all_scenes:
                    print self.__current_tab
                    scene_path =  os.path.join(self._path, scene)
                    list_item = SceneItem(scene_path)
                    scenes_list_widget.addItem(list_item)
                self.scenesTW.addTab(scenes_list_widget, folder)

    def __delete_tabs(self):
        while self.scenesTW.count() != 0:
            tab = self.scenesTW.currentIndex()
            self.scenesTW.removeTab(tab)

    def __scene_selected(self, scene_item):
        print scene_item.scene_obj.scene_path
        print scene_item.scene_obj.metadata_path

        # metadata = scene_item.metadata
        # print metadata
        # if metadata:
        #     self.metadata_object = metadata
        #     self.__refresh_scene_info(self.metadata)
        # metadata_object = self.__generate_metadata_path_from_selection(scene.text().split(".")[0])
        # if metadata_object:
        #     self.metadata_object = metadata_object
        #     self.__refresh_scene_info(self.metadata_object)
        # print os.path.join(self.__current_path, self.__current_tab, scene.text())

    def __generate_metadata_path_from_selection(self, scene):
        metadata_file = os.path.join(self._path, self.__current_tab, "metadata" , "{}.metadata".format(scene))
        return metadata_utils.make_metadata_from_local(metadata_file)

    def __refresh_scene_info(self, metadata_object):
        self.sceneNameLB.setText(metadata_object.scene_name)
        self.userLB.setText(metadata_object.author)
        self.dateLB.setText(metadata_object.modified)
        pixmap = metadata_object.image if metadata_object.image else None
        self.scene_image_pixmap.setPixmap(QtGui.QPixmap(pixmap))

    def __set_scene_snapshot(self, metadata_object):
        image_path = metadata_object.scene_path.replace(".ma", ".png")
        controller.generate_snapshot(image_path)
        return image_path

    def __reset_lists(self):
        self.firstLevelLW.clear()
        self.secondLevelLW.clear()
        self.thirdLevelLW.clear()
        self.fourthLevelLW.clear()

    def __load_scene(self):
        if getattr(self, "metadata_object"):
            cmds.file(self.metadata_object.scene_path, o=True, f=True)

    def __save_local(self):
        current_m_object = metadata_utils.make_metadata_from_local(metadata_utils.generate_metadata_path(cmds.file(sn=True, q=True)))
        m_object, m_object_path = metadata_utils.generate_metadata_from_scene()
        if not current_m_object.image:
            image_path = self.__set_scene_snapshot(m_object)
            m_object.image = image_path
        else:
            m_object.image = current_m_object.image
        m_object.save_local_metadata()
        self.__refresh_scene_info(m_object)


    def generate_scene_name(self):
        if len(dep) > 3:
            short_dep = dep[:3]
        else:
            short_dep = dep
        scene = "bm2_{}{}_{}_{}_{}_{}_{}_default_none_{}{}".format(self.__second_level, short_dep, self.__category, self.__first_level, 
                                                                self.__second_level, self.__third_level, self.__fourth_level, self.__current_tab, "001")
        return scene



class FoldersTree(QtCore.QThread):
        def __init__(self, parent = None):
            super(FoldersTree, self).__init__()

        def run(self):
            self.project_tree = controller.generate_paths_info(PROJECT_ROOT)
    

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