import getpass
import os
from datetime import datetime

import maya.cmds as cmds
import maya.mel as mel
from Framework.lib.metadata_lib import metadata, metadata_utils


class Scene(object):

    def __init__(self, scene_path=None):
        if not scene_path:
            scene_path = cmds.file(sn=True, q=True).replace("\\", "/")
        self.scene_path = scene_path
        self.metadata = metadata.MetadataLocal.generate_metadata(self.metadata_path)
    
    @property
    def version(self):
        if self.metadata:
            return self.metadata.scene_version
        else:
            return None

    @property
    def scene_name(self):
        return os.path.split(self.scene_path)[-1] 

    @property
    def metadata_path(self):
        scene_name = os.path.basename(self.scene_path)
        scene_folder = os.path.dirname(self.scene_path)
        return os.path.join(scene_folder, "metadata", 
                        "{}.metadata".format(scene_name.rsplit(".", 1)[0])
                        ).replace("\\", '/')

    @property
    def scene_modified(self):
        return cmds.file(q=True, modified=True)

    @property
    def notes(self):
        return self.metadata.notes

    def add_notes(self, notes):
        self.metadata.notes = notes
        self.metadata.save_local_metadata()

    def save_scene(self, force=True, create_snapshot=False):
        # TODO WE NEED TO RENAME FIRST WITH THE NEW VERSION
        if not self.scene_modified:
            raise Exception("Nothing to save")
        mel.eval("incrementAndSaveScene 0")
        self.scene_path = cmds.file(q=True, sn=True)
        if not self.metadata:
            self.metadata = metadata.MetadataLocal.generate_metadata_from_scene(self.scene_path)
            self.metadata.image = self.generate_snapshot()   
        else:
            self.incremental_save(create_snapshot=create_snapshot)
        self.metadata.save_local_metadata()

    def load_scene(self):
        cmds.file(self.scene_path, o=True, f=True)

    def incremental_save(self, create_snapshot=False):
        self.metadata.author = getpass.getuser()
        self.metadata.modified = str(datetime.now()).split(".")[0]
        self.metadata.scene_path = cmds.file(q=True, sn=True)
        self.metadata.scene_version = self.__get_incremented_version()  # Necesitamos marcar un naming convention para las versiones
        self.metadata.dependencies = ["Caca", "Culo", "Pedo", "Pis"]
        if create_snapshot:
            self.metadata.image = self.generate_snapshot()        

    def generate_snapshot(self):
        image_path = self.scene_path.replace(".ma", ".png")
        cmds.playblast( frame=1,
                        format="image",
                        completeFilename="{}".format(image_path),
                        sequenceTime=0,
                        clearCache=1,
                        viewer=0,
                        offScreen=True,
                        fp=0,
                        percent=100,
                        compression="png",
                        quality=100,
                        widthHeight=(240,175),
                        showOrnaments=False )
        return image_path        

    @staticmethod
    def has_version(scene_path):
        # TODO IMPROVE WITH REGEX
        scene_splitted = scene_path.split(".")
        if len(scene_splitted) == 2:
            return False
        elif len(scene_splitted) == 3:
            return True

    def __get_incremented_version(self):
        # TODO IMPROVE WITH REGEX
        new_scene_path = cmds.file(q=True, sn=True)
        version_number = new_scene_path.split(".")[1]
        return version_number
