import os


TEMPPATH = r"C:\Users\Alberto\Documents\P\bm2"


def generate_paths_info(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    paths_dict = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], paths_dict)
        parent[folders[-1]] = subdir
    return paths_dict