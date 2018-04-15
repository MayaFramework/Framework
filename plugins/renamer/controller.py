import os
import re
# path example:
# "P:\bm2\chr\gato\out\rigging\thinHigh\out\bm2_chrout_chr_gato_out_rigging_thinHigh_default_none_out.ma " 
from Framework.lib.config.config import Config
import propierties
class Renamer(object):
    FILE_PATH_FORMAT = "{disk}/{show}/{group}/{name}/{area}/{step}/{layer}/{pipe}/{filename}"
    FILE_NAME = "{show}_{worktype}_{group}_{name}_{area}_{step}_{layer}_{partition}_{description}_{pipe}.{extension}"
    WORK_TYPE = ""
    REG_EXP = '{[a-z]*}'


    

    ATTR_DISK = "disk"
    ATTR_SHOW = "show"
    ATTR_GROUP = "group"
    ATTR_NAME = "name"
    ATTR_AREA = "area"
    ATTR_STEP = "step"
    ATTR_LAYER= "layer"
    ATTR_PIPE = "pipe"
    ATTR_LAYER = "layer"
    ATTR_DESCRIPTION = "description"
    ATTR_EXTENSION = "extension"


    
    def __init__(self):
        self._config = Config.instance()


    def check_file_path_format(self, file_path):
        file_name_fields = self.get_fields_from_file_name(file_path)
        self.check_fields_value(file_name_fields)
        file_path_fields = self.get_fields_from_file_path(file_path)
        self.check_fields_value(file_path_fields)
        
        if file_name_fields[self.ATTR_SHOW] != file_path_fields[self.ATTR_SHOW]:
            return False

        if file_name_fields[self.ATTR_GROUP] != file_path_fields[self.ATTR_GROUP]:
            return False
        
        if file_name_fields[self.ATTR_NAME] != file_path_fields[self.ATTR_NAME]:
            return False
        
        if file_name_fields[self.ATTR_NAME] != file_path_fields[self.ATTR_NAME]:
            return False
        
        if file_name_fields[self.ATTR_AREA] != file_path_fields[self.ATTR_AREA]:
            return False
        
        
        if file_name_fields[self.ATTR_STEP] != file_path_fields[self.ATTR_STEP]:
            return False
        
        
        if file_name_fields[self.ATTR_AREA] != file_path_fields[self.ATTR_AREA]:
            return False
        
        if file_name_fields[self.ATTR_LAYER] !=  file_path_fields[self.ATTR_LAYER]:
            return False
        
        return True
        
    
    def check_fields_value(self, fields_data=""):
        '''
        checks field dict matching possible values
        :param fields_data: dict
        :return (bool)
        '''
        for key, value in fields_data:
            if key == self.ATTR_DISK and key not in propierties.ATTR_DISK_AVAILABLE:
                return False
            if key == self.ATTR_SHOW and key not in propierties.ATTR_SHOW_AVAILABLE:
                return False
            if key == self.ATTR_GROUP and key not in propierties.ATTR_GROUP_AVAILABLE:
                return False
            if key == self.ATTR_AREA and key not in propierties.ATTR_AREA_AVAILABLE:
                return False
            if key == self.ATTR_PIPE and key not in propierties.ATTR_PIPE_AVAILABEL:
                return False
        return True
    
    def get_fields_from_file_name(self, file_name):
        '''
        file_path to extract fields
        :param file_path: (str)
        '''
        
        file_name_fields = file_name.split("_")
        extension = file_name_fields[-1].replace(".","")
        fields_data = {
                        self.ATTR_SHOW: file_name_fields[0],
                        self.WORK_TYPE: file_name_fields[1],
                        self.ATTR_GROUP: fields[2],
                        self.ATTR_NAME: fields[3],
                        self.ATTR_AREA: fields[4],
                        self.ATTR_STEP: fields[5],
                        self.ATTR_LAYER: fields[6],
                        self.ATTR_PARTITION: file_name_fields[7],
                        self.ATTR_DESCRIPTION: [8],
                        self.ATTR_PIPE: fields[9],
                        self.ATTR_EXTENSION: extension
                        }
        return fields_data
    
    def get_fields_from_file_path(self, file_path):
        '''
        file_path to extract fields
        :param file_path: (str)
        '''
        file_path = os.path.normpath(file_path)
        fields = file_path.rsplit("\\")

        file_name_fields = fields[8].split("_")
        extension = file_name_fields[-1].replace(".","")
        fields_data = {
                        self.ATTR_DISK:fields[0],
                        self.ATTR_SHOW: fields[1],
                        self.ATTR_GROUP: fields[2],
                        self.ATTR_NAME: fields[3],
                        self.ATTR_AREA: fields[4],
                        self.ATTR_STEP: fields[5],
                        self.ATTR_LAYER: fields[6],
                        self.ATTR_PIPE: fields[7],
                        self.ATTR_FILENAME: fields[8],
                        self.WORK_TYPE: file_name_fields[1],
                        self.ATTR_PARTITION: file_name_fields[-4],
                        self.ATTR_DESCRIPTION: [-3],
                        self.ATTR_EXTENSION: extension
                        }
        return fields_data

    
    def generete_complete_file_path(self, fields):
        '''
        format file name matchin fields with the static attr FILE_NAME
        '''
        base_fields = {
            self.ATTR_DISK: self._confing.environ[self.ATTR_DISK],
            self.SHOW: self._config.environ[self.SHOW]}
        base_fields.update(fields)

        file_name = self.generate_file_name(base_fields)

        base_fields.update({self.ATTR_FILENAME: file_name})

        file_path = self.FILE_PATH_FORMAT.format(base_fields)
        result = re.findall(self.REG_EXP, file_path)
        if len(result)>0:
            raise Exception("Need to specify the next values: %s" % (" ".join(result)))
        return file_path

    def generate_file_name(self, fields):
        '''
        format file name matchin fields with the static attr FILE_NAME
        '''
        base_fields = {
            self.SHOW: self._config.environ[self.SHOW]}
        base_fields.update(fields)

        file_name = Renamer.FILE_NAME.format(fields)
        result = re.findall(Renamer.REG_EXP, file_name)
        if len(result)>0:
            raise Exception("Need to specify the next values: %s" % (" ".join(result)))
        return file_name



if __name__ == "__main__":
    file_path = r"P:\bm2\chr\gato\out\rigging\thinHigh\out\bm2_chrout_chr_gato_out_rigging_thinHigh_default_none_out.ma"
    fields = {
        Renamer.ATTR_ASSET: "",
            
        }
    rename = Renamer()
    print rename.generateCompleteFilePath(**fields)
    
