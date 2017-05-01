import sys,os
# sys.path.append(r"D:\Miguel\Programming\project\bm2")
from Framework.lib.gui_loader import gui_loader
from Framework import icons
from PySide import QtCore,QtGui
ui_file = os.path.join(os.path.dirname(__file__), "gui", "main.ui")
ICO_PATH = icons.get_icon_path()
from Framework.lib.ma_utils.reader import MaReader 
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.gui import css
CSS_PATH = css.get_css_path()
import time
# TESTING 
#  D:\Miguel\Programming\project\bm2\tests\bm2_shocam_seq_tst_sot_0010_camera_default_scene_wip001.ma
   
form,base = gui_loader.loadUiType(ui_file)
def setStyleSheet(uiClass, cssFile):
    file = open(cssFile).read()
    uiClass.setStyleSheet(file)

class DependencyLoaderWidget(form,QtGui.QDialog):
	dropboxManager = None
	def __init__(self):
		super(DependencyLoaderWidget, self).__init__()
		self.setupUi(self)
		setStyleSheet(self, os.path.join(CSS_PATH,'dark_style.css'))
		self.exec_()


	def get_dependencies(self, path):
		if not path.endswith(".ma"):
			return None

		maReader = MaReader()
		dependencies = maReader.get_references(path)
		return dependencies


	def get_file(self,file):
		dependencies = self.get_dependencies(file)
		if not dependencies:
			return False

		self.dependency_list.clear()
		for key,values in dependencies.iteritems():
			listItem = QtGui.QListWidgetItem(key)
			listItem.setIcon(QtGui.QIcon(os.path.join(ICO_PATH,"question.png")))
			QtGui.qApp.processEvents()
			self.dependency_list.addItem(listItem)
			
		count = self.dependency_list.count()
		for x in xrange(0,count):
			item = self.dependency_list.item(x)
			try:

				item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH,"downloading.png")))
				QtGui.qApp.processEvents()
				result = self.update_file(item.text())
				if result:
					item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH,"checked.png")))
				else:
					item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH,"error.png")))
			except Exception as e:
				item.setIcon(QtGui.QIcon(os.path.join(ICO_PATH,"error.png")))
				print e
			finally:
				QtGui.qApp.processEvents()

			# self.update_file(item.text())

	def update_file(self,file):
		if not self.dropboxManager:
			self.dropboxManager = DropboxManager(token="MspKxtKRUgAAAAAAAAAHPJW-Ckdm7XX_jX-sZt7RyGfIC7a7egwG-JqtxVNzOSJZ")
		if self.dropboxManager.downloadFile(file):
			return True

	@QtCore.Slot()
	def on_update_btn_clicked(self):
		path = os.path.normpath(self.path.text()).replace("\\","/")
		if not path or not path.endswith(".ma"):
			raise Exception("Specify a ma file!")
		print path
		result = self.get_file(path)
		print result




app = QtGui.QApplication(sys.argv)
DependencyLoaderWidget()
