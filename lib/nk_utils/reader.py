# encoding: utf-8
"""
Created on 24 ene. 2019

:author: Raquel Jarillo Pellón
:email: rachel.1991.15@gmail.com
"""

import sys

import os
import pprint
import re
from Framework.lib.dropbox_manager.manager import DropboxManager

REG_EXPRESSION = "(\"P:/.*);"


class NkReader(object):

    @staticmethod
    def has_dependencies(nk_file):
        with open(nk_file) as file:
            lines = file.readlines()
            for line in lines:
                match_result = re.findall(REG_EXPRESSION, line)
                if match_result:
                    return True
        return False
    
    @staticmethod
    def get_references(nk_file):
        #TODO:
        pass
    
    @staticmethod
    def get_all_references(dependencies_list, db_instance, path):
        
        #TODO: review
        
        dependencies = NkReader.get_references(path)
        if dependencies:
            for dp in dependencies.keys():
                if not dp in dependencies_list:
                    dependencies_list.append(dp)
                if dp.endswith(".nk"):
                    if not os.path.exists(dp):
                        db_instance.downloadFile(dp)
                        NkReader.get_all_references(dependencies_list, db_instance, dp)
        return dependencies_list
        
        