import os
import re
from Framework.lib.gui_loader import gui_loader
reload(gui_loader)
from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets

TEMPPATH = r"C:\Users\Alberto\Documents\P\bm2"


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))




class SceneLoaderUI(form, base):

    def __init__(self):
        super(SceneLoaderUI, self).__init__()
        self.setupUi(self)