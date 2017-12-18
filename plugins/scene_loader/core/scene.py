import getpass
import os
import re
from datetime import datetime
import base64

import maya.cmds as cmds
import maya.mel as mel
from Framework.lib.metadata_lib import metadata, metadata_utils
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.logger import logger
from Framework.lib.ma_utils.reader import MaReader


class Scene(object):

    def __init__(self, scene_path=None):

        if not scene_path:
            scene_path = cmds.file(sn=True, q=True).replace("\\", "/")

        self.metadata = None
        self.local_path, self.remote_path = self.validate_scene_path(scene_path)

        self.dpx = DropboxManager("MspKxtKRUgAAAAAAAAA1OnMGBw6DOOG2Cz38E83-YJaxw7Jv2ihc2Afd-82vmZkI")

        if not os.path.exists(self.local_metadata_path):
            # We should download the metadata if exists in Dropbox
            # This method should work either with local or remote metadata
            if self.dpx.existFile(self.local_metadata_path):
                self.dpx.downloadFile(self.local_metadata_path)
                self.metadata = metadata.Metadata.generate_metadata(self.local_metadata_path)
            else:
                logger.warning("No Metadata available for {}".format(self.scene_name))
        else:
            self.metadata = metadata.Metadata.generate_metadata(self.local_metadata_path)

    def validate_scene_path(self, scene_path):
        if scene_path.startswith("P:/"):
            local_path = scene_path
            remote_path = scene_path.replace("P:/BM2/", "/work/bm2/")
        elif scene_path.startswith("/work"):
            local_path = scene_path.replace("/work", "P:/")
            remote_path = scene_path
        else:
            raise Exception
        return local_path, remote_path

    @property
    def version(self):
        if self.metadata:
            return self.metadata.scene_version
        else:
            return None

    @property
    def scene_name(self):
        return os.path.split(self.local_path)[-1]

    @property
    def scene_type(self):
        return self.local_path.split("/")[-2]

    @property
    def remote_metadata_path(self):
        scene_name = os.path.basename(self.remote_path)
        scene_folder = os.path.dirname(self.remote_path)
        return os.path.join(scene_folder, "metadata",
                        "{}.metadata".format(scene_name.rsplit(".", 1)[0])
                        ).replace("\\", '/')

    @property
    def local_metadata_path(self):
        scene_name = os.path.basename(self.local_path)
        scene_folder = os.path.dirname(self.local_path)
        return os.path.join(scene_folder, "metadata",
                        "{}.metadata".format(scene_name.rsplit(".", 1)[0])
                        ).replace("\\", '/')

    @property
    def scene_modified(self):
        return cmds.file(q=True, modified=True)

    @property
    def notes(self):
        return self.metadata.notes

    @property
    def has_old_version_naming(self):
        OLDVERSIONREGEX = "{}\d{{3}}(?=\.)".format(self.scene_type)
        return True if re.search(OLDVERSIONREGEX, self.scene_name) else False

    @property
    def dependencies(self):
        if self.metadata:
            return self.metadata.dependencies
        return None

    def get_ma_dependencies(self):
        return MaReader.get_references(self.local_path)

    def get_ma_dependencies_recursive(self):
        dependencies_list = list()
        all_references = MaReader.get_all_references(dependencies_list, self.dpx, self.local_path)
        return all_references

    def get_metadata_attribute(self, attribute):
        return self.metadata.get(attribute)

    def add_notes(self, notes):
        self.metadata.notes.insert(0, notes)
        print "saving"
        self.metadata.save_local_metadata()

    def save_scene(self, force=True, create_snapshot=False, publish=False):
        # TODO WE NEED TO RENAME FIRST WITH THE NEW VERSION
        # if not self.scene_modified:
        #     raise Exception("Nothing to save")

        if self.has_old_version_naming:
            print "IM HERE"
            cleaned_scene_name = self.clean_old_version_naming()
            cmds.file(rename=cleaned_scene_name)
            cmds.file(s=True)

        mel.eval("incrementAndSaveScene 0")
        self.local_path = cmds.file(q=True, sn=True)

        if not self.metadata:
            self.metadata = metadata.Metadata.generate_metadata_from_scene(self.local_path)
            self.metadata.image = self.generate_snapshot()
            self.metadata.notes = list()
            self.metadata.dependencies = self.get_ma_dependencies_recursive()
        else:
            self.metadata_incremental_save(create_snapshot=create_snapshot)

        self.metadata.save_local_metadata()

        self.dpx.uploadFiles([self.local_path, self.local_metadata_path])

        if publish:
            logger.info("PUBLISHING")
            self.dpx.moveFile(self.local_path, self.local_path.replace(self.scene_type, "chk"))
            self.dpx.moveFile(self.local_metadata_path, self.local_metadata_path.replace(self.scene_type, "chk"))
            self.dpx.uploadFiles([self.local_path, self.local_metadata_path])

    def open_scene(self, force_ma_dependencies=False):
        if not os.path.exists(self.local_path):
            self.download_scene()

        if force_ma_dependencies:
            logger.info("Force MA dependencies checked on. Getting MA dependencies")
            dependencies = self.get_ma_dependencies_recursive()
            for dependency in dependencies:
                if not os.path.exists(dependency):
                    if self.dpx.existFile(dependency):
                        self.dpx.downloadFile(dependency)
            logger.info("Dependencies Donwloaded")

        if self.dependencies and not force_ma_dependencies:
            for dependencies in self.dependencies:
                if not os.path.exists(dependencies):
                    if self.dpx.existFile(dependencies):
                        self.dpx.downloadFile(dependencies)
            logger.info("Dependencies Donwloaded")

        cmds.file(self.local_path, o=True, f=True)

    def download_scene(self):
        # if not os.path.exists(self.local_path):
        #     # This method should work either with local or remote metadata
        if self.dpx.existFile(self.local_path):
            self.dpx.downloadFile(self.local_path)
            logger.info("Scene downloaded!")



    def metadata_incremental_save(self, create_snapshot=False):
        self.metadata.author = getpass.getuser()
        self.metadata.modified = str(datetime.now()).split(".")[0]
        self.metadata.scene_path = cmds.file(q=True, sn=True)
        self.metadata.scene_version = self.__get_incremented_version()  # Necesitamos marcar un naming convention para las versiones
        self.metadata.dependencies = self.get_ma_dependencies_recursive()
        if create_snapshot:
            self.metadata.image = self.generate_snapshot()

    def generate_snapshot(self):
        image_path = self.local_path.replace(".ma", ".png")
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
        encoded_image = base64.b64encode(open(image_path, "rb").read())
        os.remove(image_path)
        return encoded_image

    @staticmethod
    def has_version(scene_path):
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

    def clean_old_version_naming(self):
        OLDVERSIONREGEX = "{}\d{{3}}(?=\.)".format(self.scene_type)
        current_scene_name = self.scene_name
        current_old_version = re.search(OLDVERSIONREGEX, current_scene_name).group(0)
        new_scene_name = self.local_path.replace(current_old_version, ".0001")
        return new_scene_name
