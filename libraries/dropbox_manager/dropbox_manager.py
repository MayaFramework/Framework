"""
author = ["miguel.molledo.alvarez@gmail.com"]


EXAMPLE:

dpx = DropboxManager(token="Yomp-8XE2CoAAAAAAAAAuQsiUXNm1_Fo4BbispgGAoV8-0NvNw2E3YgwoLH1pZBX")

TO UPLOAD FILES
dpx.uploadFile(r"s:/project/test/audiotest.m4v")
or
dpx.uploadFiles(["s:/project/test/audiotest.m4v", "s:/project/test/fileTest.txt"])


TO DOWNLOAD FILES
dpx.getFile("project/audiotest.m4v") 
or 
dpx.downloadFile("c:/project/audiotest.m4v")

or 
dpx.downloadFiles(["s:/project/test/audiotest.m4v", "s:/project/test/fileTest.txt"])


"""




import dropbox 
import sys
import os
import pprint
import shutil
# token = "Yomp-8XE2CoAAAAAAAAAuQsiUXNm1_Fo4BbispgGAoV8-0NvNw2E3YgwoLH1pZBX"
class DropboxManager(object):
	__client = None
	__dpx = None
	__base_path = None
	def __init__(self, token, work_path = "c:/dmb2/"):
		self.__client = dropbox.client.DropboxClient(token)
		self.__dpx = dropbox.dropbox.Dropbox(token)

	def uploadFile(self, local_file):
		if not local_file.startswith(self.__base_path):
			raise Exception("Wrong repository")

		dropbox_path = dropbox.client.format_path(resource_path.split(self.__base_path,1)[1])
		with open(local_file, 'rb') as my_file:
			self.__client.put_file(dropbox_path, my_file)

	def downloadFile(self, dropbox_path):
		if dropbox_path.startswith(self.__base_path):
			target = dropbox_path
			dropbox_path = dropbox.client.format_path(dropbox_path.split(self.__base_path,1)[1])
		else:
			target = os.path.join(self.__base_path, dropbox_path)
			dropbox_path = dropbox.client.format_path(dropbox_path)

		self.__dpx.files_download_to_file(target, dropbox_path)
		return True

	def uploadFiles(self, files):
		for file in files:
			self.uploadFile(self.normpath(file))

	def downloadFiles(self, files):
		for file in files:
			self.getFile(self.normpath(file))

	def normpath(self, path):
		return os.path.normpath(path).replace("\\", "/")


# TODO IN THIS class
# def getChildrenFromFolder():
# 	return list




# TODO in another class like sequencer loader
# # functions
# 	def getAssetList(type = "CHAR, ELEM, FX, ", filetype = 'chrg'):
# 		return dict {"CHAR": {
# 							"alias": "blabla",
# 							"filetype": "chrg" }
# 		}}








