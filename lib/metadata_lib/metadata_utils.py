import getpass
import json
import os
from datetime import datetime

import maya.cmds as cmds
import metadata


def make_metadata_from_local(metadata_file):
    if not is_metadata_file(metadata_file):
        raise Exception("{} must be a valid Metadata File".format(os.path.basename(metadata_file)))
    with open(metadata_file) as json_data:
        metadata_data = json.load(json_data)
    return metadata.MetadataLocal(metadata_data)


def is_metadata_file(metadata_file):
    return os.path.splitext(metadata_file)[1] == ".metadata"


def generate_metadata_from_scene(save=True):
    maya_metadata = {
        "author" : getpass.getuser(),
        "modified": str(datetime.now()).split(".")[0],
        "scene_path": cmds.file(sn=True, q=True),
        "scene_version": "001", # Necesitamos marcar un naming convention para las versiones
        "dependencies": ["Caca", "Culo", "Pedo", "Pis"]
    }
    local_metadata = metadata.MetadataLocal(maya_metadata)
    if save:
        metadata_file = local_metadata.save_local_metadata()
        return local_metadata, metadata_file
    return local_metadata, None


def open_maya_file(metadata_file):
    metadata_data = make_metadata_from_local(metadata_file)
    cmds.file(os.path.normpath(metadata_data.scene_path))
