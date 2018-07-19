"""
@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com
"""

import inspect
import os, sys, json
def read_json(file_path):
    if not os.path.isfile(file_path):
        raise Exception("Not file Found on the system: %s"%file)
    with open(file_path) as f:
        d = json.load(f)
        return d

def save_json(file_path,json_data):
    json.dump(json_data,file_path)
    return True


def execute_command(command, wait = False):
    # TODO timeout, logger, return response
    import subprocess
    if wait:
        subprocess.call(command)
    else:
        subprocess.Popen(command)


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def get_subfolders(folder_path, recursive=True):
    """
    Retrieve the subfolders in a given folder.

    Args:
        folder_path (str): The path where to look for folders in.
        recursive (bool, optional): Indicates if the search must be recursive. By default is True.

    Returns:
        list of str: List of the folders that are inside the given folder.
    """
    subfolders = [folder_path]
    inmediate_folders = [
        os.path.join(folder_path, name) for name in os.listdir(folder_path)
        if (os.path.isdir(os.path.join(folder_path, name)) and (name != ".git") and (name != ".svn"))
    ]

    if recursive:
        for folder in inmediate_folders:
            subfolders += get_subfolders(folder, recursive=recursive)
    else:
        subfolders = inmediate_folders

    return subfolders



def get_image_files(folder, recursive=True):
    """
    Get all image files in a folder.

    Args:
        folder (str): Path to the folder that contains the images.

    Returns:
        list of str: List with the paths to the images.
    """
    return get_files(folder, extensions=[".png", ".jpg", ".gif"], recursive=recursive)


def get_image_file(name, folder, recursive=True):
    """
    Get an image file from a folder by a given name.

    Args:
        name (str): Name of the desired image file.
        folder (str): Path to the folder that contains the images.

    Returns:
        str: The path to the image if found, None if not found.
    """
    image_files = get_image_files(folder, recursive=recursive)

    for image_file in image_files:
        short_name = os.path.basename(os.path.splitext(name)[0])
        file_base_name = os.path.basename(os.path.splitext(image_file)[0])
        if short_name == file_base_name:
            return image_file
        
        
def get_files(folder_path, extensions=None, filters=None, recursive=True, filters_mode="OR", filters_invert=False):
    """
    Look in a given folder for files that match certain requirements.

    Args:
        folder_path (str): String with the path where to find files in.
        extensions (list of str, optional): Optional string array parameter that if given,
            filter the results by extension.
        filters (list of str, optional): Optional string array parameter that if ginven,
            filters the files that don't contain any of the filter words.
        recursive (bool, optional): Optional boolean indicating if the search must be recursive.
            Default is True.

    Returns:
        str: List that contains the found files.
    """
    subfolders = [folder_path] + get_subfolders(folder_path, recursive=recursive)
    files = []

    for folder in subfolders:
        files += get_folder_files(folder, extensions=extensions)

    # If it has filters, keeps only the files that matches them.
    if filters:
        filtered_files = []
        if not filters_invert:
            for current_file in files:
                if filters_mode == "OR":
                    for filter_word in filters:
                        if filter_word.lower() in current_file.lower():
                            filtered_files.append(current_file)
                            break
                elif filters_mode == "AND":
                    match_all_filters = True
                    for filter_word in filters:
                        if filter_word.lower() not in current_file.lower():
                            match_all_filters = False
                            break
                    if match_all_filters:
                        filtered_files.append(current_file)
        else:
            for current_file in files:
                if filters_mode == "OR":
                    match_one_filter = False
                    for filter_word in filters:
                        if filter_word.lower() in current_file.lower():
                            match_one_filter = True
                            break
                    if not match_one_filter:
                        filtered_files.append(current_file)
                elif filters_mode == "AND":
                    match_all_filters = True
                    for filter_word in filters:
                        if filter_word.lower() not in current_file.lower():
                            match_all_filters = False
                            break
                    if not match_all_filters:
                        filtered_files.append(current_file)

        files = filtered_files

    files = [os.path.normpath(os.path.abspath(file)) for file in files]

    return files

def get_folder_files(folder_path, extensions=None):
    """
    Retrieve the files under a given folder.

    Args:
        folder_path (str): The path where to look for files in.
        extensions (list of str, optional): List of extensions to filter the search.

    Returns:
        list of str: List of the files that are inside the given folder.
    """
    files = [
        os.path.join(folder_path, name) for name in os.listdir(folder_path)
        if (os.path.isfile(os.path.join(folder_path, name)))
    ]

    if extensions:
        filter_files = []
        for extension in extensions:
            filter_files += [file_path for file_path in files if (os.path.splitext(file_path)[1] == extension)]
        files = filter_files

    return files