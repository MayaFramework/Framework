


"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
"""
from Framework.lib.singleton import Singleton
from Framework import get_environ_file, get_css_path, get_icon_path, get_environ_file
from Framework.lib.file import utils

import json
import sys
import os

class Config(Singleton):
    def __init__(self):
        self.__environ = {}
        self.__icon_path = ""
        base_framework_path = os.path.join(os.path.dirname(__file__),"..","..")
        # Environ
        self.environ_file = os.path.join(base_framework_path, "config", "environ.json")
        self.environ = utils.read_json(self.environ_file)
        
        # Icon Path
        self.icon_path = get_icon_path()
    
    @property
    def environ(self):
        return self.__environ
    
    @environ.setter
    def environ(self, environ_dict):
        self.__environ = environ_dict
    
    @property
    def environ_file(self):
        return self.__environ_file
    
    @environ_file.setter
    def environ_file(self, environ_file):
        self.__environ_file = environ_file
    
    
    @property
    def icon_path(self):
        return self.__icon_path
    
    @icon_path.setter
    def icon_path(self, file_path):
        if os.path.exists(file_path):
            self.__icon_path = file_path
    
    
    
if __name__ == "__main__":
    config = Config.instance()