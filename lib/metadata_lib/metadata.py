import os
import json
import metadata_utils

import getpass
from datetime import datetime


class BaseMetadata(object):
    def __init__(self):
        self.author = None
        self.modified = None
        self.scene_path = None
        self.scene_version = None
        self.dependencies = None
        self.image = None

    def __getitem__(self, value):
        return self.__dict__[value]    

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __len__(self):
        return len(self.__dict__)

    @property
    def metadata(self):
        return vars(self)

    @metadata.setter
    def metadata(self, value):
        if not isinstance(value, dict):
            raise TypeError("Metadata must be a dict")
        for k,v in value.iteritems():
            self.__dict__[k] = v

    @property
    def scene_folder(self):
        return os.path.dirname(self.scene_path)

    @property
    def scene_name(self):
        return os.path.basename(self.scene_path).rsplit(".", 1)[0]

    def keys(self):
        return self.__dict__.keys()

    def get(self, key):
        return self.__dict__.get(key, None)

    def remove(self, key):
        self.__dict__.pop(key, None)
        return vars(self)

    def save_metadata(self, path):
        raise Exception("INHERETED METHOD")


class Metadata(BaseMetadata):
    def __init__(self, metadata=None):
        super(Metadata, self).__init__()
        # if metadata:
        #     if not isinstance(metadata, dict):
        #         raise TypeError("Metadata should be a dict")
        self.metadata = metadata

    def save_metadata(self, path):
        if not os.path.isdir(path):
            raise Exception("Path should be a dir")
        metadata_path = os.path.join(path, "{}.metadata".format(self.scene_name))
        with open(metadata_path, 'w') as outfile:
            json.dump(self.metadata, outfile, indent=4)
        return metadata_path

    def save_local_metadata(self):
        metadata_folder = os.path.join(self.scene_folder, "metadata")
        if not os.path.isdir(metadata_folder):
            os.mkdir(metadata_folder)
        metadata_file = self.save_metadata(metadata_folder)
        return metadata_file

    def save_dropbox_metadata(self, local_metadata_path, dpx_instance=None):
        dpx_instance.uploadFile(local_metadata_path)

    @classmethod
    def generate_metadata(cls, metadata_path):
        metadata_data = None
        if os.path.isfile(metadata_path):
            with open(metadata_path) as json_data:
                metadata_data = json.load(json_data)
        return cls(metadata_data)

    @classmethod
    def generate_metadata_from_scene(cls, scene_path, save=True):
        maya_metadata = {
            "author" : getpass.getuser(),
            "modified": str(datetime.now()).split(".")[0],
            "scene_path": scene_path,
            "scene_version": scene_path.split(".")[1], # Necesitamos marcar un naming convention para las versiones
            "dependencies": []
        }
        local_metadata = cls(maya_metadata)
        if save:
            local_metadata.save_local_metadata()
        return local_metadata



