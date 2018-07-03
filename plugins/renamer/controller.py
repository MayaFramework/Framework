import os
import re
# path example:
# "P:\bm2\chr\gato\out\rigging\thinHigh\out\bm2_chrout_chr_gato_out_rigging_thinHigh_default_none_out.ma " 
from Framework.lib.config.config import Config
import propierties


class Renamer(object):

    REG_EXP = '{[A-Z]*}'
    FOLDER_PATH_FORMAT = "{DISK}/{SHOW}/{GROUP}/{NAME}/{AREA}/{STEP}/{LAYER}/{PIPE}"
    FOLDER_PATH_LENGHT = len(re.findall(REG_EXP, FOLDER_PATH_FORMAT))
    FILE_NAME_FORMAT = "{SHOW}_{WORKTYPE}_{GROUP}_{NAME}_{AREA}_{STEP}_{LAYER}_{PARTITION}_{DESCRIPTION}_{PIPE}.{VERSION}.{EXTENSION}"
    FILE_NAME_LENGHT = len(re.findall(REG_EXP, FILE_NAME_FORMAT))
    
    FILE_NAME_WITHOUT_VERSION = "{SHOW}_{WORKTYPE}_{GROUP}_{NAME}_{AREA}_{STEP}_{LAYER}_{PARTITION}_{DESCRIPTION}_{PIPE}.{EXTENSION}"
    

    
    
    ATTR_WORKTYPE = "WORKTYPE"
    ATTR_DISK = "DISK"
    ATTR_SHOW = "SHOW"
    ATTR_GROUP = "GROUP"
    ATTR_NAME = "NAME"
    ATTR_AREA = "AREA"
    ATTR_STEP = "STEP"
    ATTR_LAYER= "LAYER"
    ATTR_PIPE = "PIPE"
    ATTR_LAYER = "LAYER"
    ATTR_DESCRIPTION = "DESCRIPTION"
    ATTR_EXTENSION = "EXTENSION"
    ATTR_PARTITION = "PARTITION"
    ATTR_VERSION = "VERSION"

    
    def __init__(self):
        self._config = Config.instance()

        
    def check_fields_value(self, fields_data=""):
        '''
        checks field dict matching possible values
        :param fields_data: dict
        :return (bool)
        '''
        for key, value in fields_data.iteritems():
            if key == self.ATTR_DISK and value not in propierties.ATTR_DISK_AVAILABLE:
                return False
            if key == self.ATTR_SHOW and value not in propierties.ATTR_SHOW_AVAILABLE:
                return False
            if key == self.ATTR_GROUP and value not in propierties.ATTR_GROUP_AVAILABLE:
                return False
            if key == self.ATTR_AREA and value not in propierties.ATTR_AREA_AVAILABLE:
                return False
            if key == self.ATTR_PIPE and value not in propierties.ATTR_PIPE_AVAILABEL:
                return False
        return True
    
    def get_fields_from_file_name(self, file_name):
        '''
        file_path to extract fields
        :param file_path: (str)
        '''
        
        file_name_fields = file_name.split("_")
        splitted_ext = file_name_fields[-1].split(".")
#         
#         if len(splitted_ext) != 3:
#             raise OldNamingConvention("Looks like this name has the old Naming convention")
        attr_pipe = ""
        attr_version = ""
        attr_extension = ""
        if len(splitted_ext) == 3:
            # for wip and files with version
            attr_pipe, attr_version, attr_extension = splitted_ext
        elif len(splitted_ext) == 2:
            # for chk and out
            attr_pipe, attr_extension = splitted_ext
            
        if len(file_name_fields)+2 != self.FILE_NAME_LENGHT:
            print ("Not enough fields found for the file name, \nCheck this structure: %s"%self.FILE_NAME_FORMAT)

            fields_data = {
                            self.ATTR_SHOW: self.ATTR_SHOW,
                            self.ATTR_WORKTYPE: self.ATTR_WORKTYPE,
                            self.ATTR_GROUP: self.ATTR_GROUP,
                            self.ATTR_NAME: self.ATTR_NAME,
                            self.ATTR_AREA: self.ATTR_AREA,
                            self.ATTR_STEP: self.ATTR_STEP,
                            self.ATTR_LAYER: self.ATTR_LAYER,
                            self.ATTR_PARTITION: self.ATTR_PARTITION,
                            self.ATTR_DESCRIPTION: self.ATTR_DESCRIPTION,
                            self.ATTR_PIPE: self.ATTR_PIPE,
                            self.ATTR_VERSION: self.ATTR_VERSION,
                            self.ATTR_EXTENSION: self.ATTR_EXTENSION
                            }
            return fields_data
        else:
            fields_data = {
                            self.ATTR_SHOW: file_name_fields[0],
                            self.ATTR_WORKTYPE: file_name_fields[1],
                            self.ATTR_GROUP: file_name_fields[2],
                            self.ATTR_NAME: file_name_fields[3],
                            self.ATTR_AREA: file_name_fields[4],
                            self.ATTR_STEP: file_name_fields[5],
                            self.ATTR_LAYER: file_name_fields[6],
                            self.ATTR_PARTITION: file_name_fields[7],
                            self.ATTR_DESCRIPTION: file_name_fields[8],
                            self.ATTR_PIPE: attr_pipe,
                            self.ATTR_VERSION: attr_version,
                            self.ATTR_EXTENSION: attr_extension
                            }
            return fields_data
        
    def generate_worktype(self):
        # TODO:  I HAVE NO FUCKING IDEA HOW TO MAKE THIS WORKS
        """
        
        [worktipe]
        (codigo concreto para los files que nos permiten hacer busquedas automatizadas en el futuro)
        
        [group] todos menos seq --------->   [group]+[area]
        
        [group] seq [area] todas menos shot ------------------> [seq name] + [area]
        
         [group] seq [area] shot ------------------> [area] + [layer 3 primeras letras]

        """
        pass
    
    def norm_path (self, file_path):
        file_path = os.path.normpath(file_path).replace("\\","/")
        return file_path
    
    def get_fields_from_folder_path(self, folder_path):
        '''
        file_path to extract fields
        :param file_path: (str)
        '''
        file_path = self.norm_path(folder_path)
        fields = file_path.rsplit("/")
        if len(fields) != self.FOLDER_PATH_LENGHT:
            raise Exception("Not enough fields found for the file name, \nCheck this structure: %s"%self.FOLDER_PATH_FORMAT)

        fields_data = {
                        self.ATTR_DISK:fields[0],
                        self.ATTR_SHOW: fields[1],
                        self.ATTR_GROUP: fields[2],
                        self.ATTR_NAME: fields[3],
                        self.ATTR_AREA: fields[4],
                        self.ATTR_STEP: fields[5],
                        self.ATTR_LAYER: fields[6],
                        self.ATTR_PIPE: fields[7]
                    }
        
        return fields_data


    def get_fields_from_file_path(self, file_path):
        folder, filename = os.path.normpath(file_path).replace("\\","/").rsplit("/",1)
        folder_fields = self.get_fields_from_folder_path(folder)
        self.check_fields_value(folder_fields)
        file_name_fields = self.get_fields_from_file_name(filename)
        self.check_fields_value(file_name_fields)
        
        if self.compare_data_fields(data_1=folder_fields, data_2=file_name_fields):
            file_name_fields.update(folder_fields)
            return file_name_fields
        
        else:
            raise WrongNameFormatting("There are different values found for the same path fields. Check its format\nFILE_NAME_FORMAT: %s\nFOLDER_FORMAT: %s"%(self.FILE_NAME_FORMAT, self.FOLDER_PATH_FORMAT))
    
    def compare_data_fields(self, data_1, data_2):
        for key,value in data_1.iteritems():
            if key in data_2 and data_2[key] != value:
                return False
        return True
    
    def generate_complete_path_from_folder(self, folder_path,partition="partition", description="description", extension="txt", version ="version"):
        fields = self.get_fields_from_folder_path(folder_path)
        fields[self.ATTR_WORKTYPE] = fields[self.ATTR_GROUP]+fields[self.ATTR_AREA]
        fields[self.ATTR_PARTITION] = partition
        fields[self.ATTR_DESCRIPTION] = description
        fields[self.ATTR_EXTENSION] = extension
        fields[self.ATTR_VERSION] = version
        return self.generate_complete_file_path(fields)
        
    def generate_complete_file_path_from_file(self, file_path, partition="", description="", extension="", version=""):
        result=True
        result_data = {}
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        file_name_fields = self.get_fields_from_file_name(basename)
        base_fields = self.get_fields_from_folder_path(dirname)
        result_data.update(file_name_fields)
        result_data.update(base_fields)
        result_data[self.ATTR_WORKTYPE] = base_fields[self.ATTR_GROUP]+base_fields[self.ATTR_AREA]
        if partition: result_data[self.ATTR_PARTITION] = partition
        if description: result_data[self.ATTR_DESCRIPTION] = description
        if extension: result_data[self.ATTR_EXTENSION] = extension
        if version: result_data[self.ATTR_VERSION] = version
        
        if result_data[self.ATTR_PARTITION] == self.ATTR_PARTITION:
            result=False
        if result_data[self.ATTR_DESCRIPTION] == self.ATTR_DESCRIPTION:
            result=False
        if result_data[self.ATTR_EXTENSION] == self.ATTR_EXTENSION:
            result=False

        return (result, self.generate_complete_file_path(result_data))

    def generate_complete_file_path(self, fields):
        '''
        format file name matching fields with the static attr FILE_NAME
        '''
        file_name = self.generate_file_name(fields)
        folder = self.generate_folder_path(fields)
        return os.path.normpath(os.path.join(folder,file_name))

    def generate_folder_path(self, fields):
        '''
        format file name matchin fields with the static attr FILE_NAME
        '''
        base_fields = {
            self.ATTR_SHOW: self._config.environ["show"]}
        
        
        base_fields.update(self.extract_folder_fields(fields))
        if not self.check_fields_value(fields):
            raise Exception("This fields are not supported, check its format: Check its format\nFILE_NAME_FORMAT: %s\nFOLDER_FORMAT: %s"%(self.FILE_NAME_FORMAT, self.FOLDER_PATH_FORMAT))
        
        file_name = self.FOLDER_PATH_FORMAT.format(**base_fields)
        result = re.findall(Renamer.REG_EXP, file_name)
        if len(result)>0:
            raise Exception("Need to specify the next values: %s" % (" ".join(result)))
        return file_name



    def generate_file_name(self, fields):
        '''
        format file name matchin fields with the static attr FILE_NAME
        '''
        base_fields = {
            self.ATTR_SHOW: self._config.environ["show"]}
        
        
        base_fields.update(self.extract_file_name_fields(fields))
        if not self.check_fields_value(fields):
            raise Exception("This fields are not supported, check its format: Check its format\nFILE_NAME_FORMAT: %s\nFOLDER_FORMAT: %s"%(self.FILE_NAME_FORMAT, self.FOLDER_PATH_FORMAT))
        
        file_name = ""
        if fields[self.ATTR_VERSION] == self.ATTR_VERSION:
            fields.pop(self.ATTR_VERSION)
            file_name = self.FILE_NAME_WITHOUT_VERSION.format(**fields)
        
        elif fields[self.ATTR_VERSION] and fields[self.ATTR_VERSION]!=self.ATTR_VERSION:
            file_name = self.FILE_NAME_FORMAT.format(**fields)

        result = re.findall(Renamer.REG_EXP, file_name)
        
        if len(result)>0:
            raise Exception("Need to specify the next values: %s" % (" ".join(result)))
        return file_name

    def extract_file_name_fields(self, fields):
        result = {}
        for key, value in fields.iteritems():
            if key in [self.ATTR_DISK, self.ATTR_GROUP, self.ATTR_NAME,
                       self.ATTR_AREA, self.ATTR_STEP, self.ATTR_LAYER,
                       self.ATTR_PARTITION, self.ATTR_DESCRIPTION, self.ATTR_PIPE,
                       self.ATTR_EXTENSION, self.ATTR_WORKTYPE]:
                result[key] = value
        return result
    
    

    def extract_folder_fields(self, fields):
        result = {}
        for key, value in fields.iteritems():
            if key in [self.ATTR_DISK,self.ATTR_SHOW, self.ATTR_GROUP, self.ATTR_NAME, self.ATTR_AREA, self.ATTR_STEP, self.ATTR_LAYER, self.ATTR_PIPE]:
                result[key] = value
        return result
    
    
class WrongNameFormatting(Exception):
    pass


class WrongName(Exception):
    pass


class OldNamingConvention(Exception):
    pass
    

RENAMER_EXCEPTIONS = [WrongNameFormatting, WrongName, OldNamingConvention]

    
if __name__ == "__main__":
    rename = Renamer()
    file_path = r"P:\bm2\seq\tst\sho\300\scncmp\chk\bm2_seqsho_seq_tst_sho_300_scncmp_default_none_chk.ma"
    folder, filename = os.path.normpath(file_path).replace("\\","/").rsplit("/",1)
    wrong_path = r""
    import pprint

    
    folder_fields = rename.get_fields_from_folder_path(folder)
    print "FOLDER_FIELDS"
    pprint.pprint(folder_fields)
    
    
    file_name_fields = rename.get_fields_from_file_name(filename)
    print "FILENAME_FIELDS"
    pprint.pprint(file_name_fields)

    fields = rename.get_fields_from_file_path(file_path)
    print "FILE_PATH_FIELDS"
    pprint.pprint(fields)
    print "CHECKING FILEDS VALUE FORMAT: %s"%file_path
    print rename.check_fields_value(fields)
    
    print "CREATING A PATH FROM FIELDS"
    print rename.generate_complete_file_path(fields)
    print "CREATING A FILE_NAME FROM FIELDS"
    print rename.generate_file_name(fields)
    
    print "CREATING A FOLDER PATH FROM FIELDS"
    print rename.generate_folder_path(fields)
    
    
    print "GENERATE COMPLETE PATH FROM FOLDER"
    print rename.generate_complete_path_from_folder(folder,
                                                    partition="[PARTITION]",
                                                    description="[DESCRIPTION]",
                                                    extension="[EXTENSION]",
                                                    version ="[VERSION]")
    
    
    
    
    print "GENERATE COMPLETE PATH FROM FILEPATH"
    file_path = r"P:\bm2\seq\tst\sho\300\scncmp\chk\bm2_seqsho_seq_tst_sho_300_scncmp_default_none_chk.001.ma"
    partition = ""
    description=""
    extension=""
    version=""
    print rename.generate_complete_file_path_from_file(file_path, partition, description, extension, version)
    file_path = r"P:\bm2\seq\tst\sho\300\scncmp\chk\cncmp_default_none_chk"
    partition = ""
    description=""
    extension=""
    version="002"
    print "GENERATE COMPLETE PATH FROM FILEPATH"
    print rename.generate_complete_file_path_from_file(file_path, partition, description, extension, version)
    file_path = r"P:\bm2\seq\tst\sho\300\scncmp\chk\bm2_seqsho_seq_tst_sho_300_scncmp_default_none_chk.001.ma"
    partition = ""
    description="medueleunhuevo"
    extension="peneduro"
    version="002"
    print "GENERATE COMPLETE PATH FROM FILEPATH"
    print rename.generate_complete_file_path_from_file(file_path, partition, description, extension, version)
    
    
    '''    
    

    print "CREATING A FILE NAME FROM A ROUT"
    print ""
    
    
    '''
    
    
