import sys
import os
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui, QtXml
# from cmn.cmn.python.lib.ui.QT import  QtCore, QtWidgets, QtGui, QtXml
from Framework import get_css_path, get_environ_file, get_icon_path, get_uis_path




IMAGE_PATH = get_icon_path()
UIS_PATH = get_uis_path()
CSS_PATH = get_css_path()
try:
    import pyside2uic as uic
except:
#     from Framework.lib import pysideuic as uic
    import pysideuic as uic

# print uic
import xml.etree.ElementTree as xml
from cStringIO import StringIO


def load_ui_type(uiFile):
    """Summary

    Args:
        uiFile (TYPE): Description

    Returns:
        TYPE: Description
    """

    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        # Fetch the base_class and form class based on their type in the xml
        # from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtWidgets.%s' % widget_class)
    return form_class, base_class

'''
#===============================================================================
# This Maya shit must be defined within a maya function or it crash executing it from outsite
#===============================================================================

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMaya as OpenMaya
import maya.mel
from PySide2.QtCore import QEvent, QMimeData, QModelIndex, QObject, QPersistentModelIndex, QSize, Qt, QPoint, QItemSelectionModel, QThread, Signal, Slot
from PySide2.QtGui import QCursor, QDrag, QIcon, QPen, QColor, QPainter, QKeySequence
from PySide2.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QBoxLayout, QMenu, QMenuBar, QSizePolicy, QToolTip
from PySide2.QtWidgets import QWidget, QLayoutItem, QAbstractItemView, QTreeView, QPushButton
import maya.cmds as cmds
class Container(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    """
    This class implements the dockable render setup window. 
    """

    # Constants
    # MAYA-66674: Make default size a user preference
    width = (cmds.optionVar(query='workspacesWidePanelInitialWidth')) * 0.75
    STARTING_SIZE = QtCore.QSize(width, 600)
    PREFERRED_SIZE = QtCore.QSize(width, 420)
    MINIMUM_SIZE = QtCore.QSize((width * 0.95), 220)

    def __init__(self, initialWidget, title="Tool"):
        # The class MayaQWidgetDockableMixin retrieves the right parent (i.e. Maya Main Window)
        super(RenderSetupWindow, self).__init__(parent=None)
        self.preferredSize = self.PREFERRED_SIZE

        self.setWindowTitle(title)

        # create a frame that other windows can dock into.
        self.dockingFrame = QMainWindow(self)
        self.dockingFrame.layout().setContentsMargins(0,0,0,0)
        self.dockingFrame.setWindowFlags(Qt.Widget)
        self.dockingFrame.setDockOptions(QMainWindow.AnimatedDocks)

        self.centralWidget = initialWidget(self)
        self.centralWidget.layout().setContentsMargins(0,0,0,0)
        self.dockingFrame.setCentralWidget(self.centralWidget)

        # Adds the tree view to the window's layouts
        # the renderSetupView is set to be stretchy, while the other widgets are not
        layout = QVBoxLayout(self)
        layout.addWidget(self.dockingFrame, 0)
        self.setLayout(layout)
        
    def setSizeHint(self, size):
        self.preferredSize = size

    def sizeHint(self):
        return self.preferredSize

    def minimumSizeHint(self):
        return self.MINIMUM_SIZE

    def dispose(self):
        self.centralWidget.dispose()

    def show(self, *args, **kwargs):
        # Override MayaQWidgetDockableMixin.show() method
        # to resolve menu parenting issues for templates
        # MAYA-73418
        super(RenderSetupWindow, self).show(*args, **kwargs)
'''


def get_default_container(widget, name='APP NAME', style=True, simple_bar=True):
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Framework: [Miguel Molledo, Alberto Sierra]")
    # dialog.SetSizeContraint()
    main_layout = QtWidgets.QVBoxLayout()
    main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
    if simple_bar:
        # Add a bar
        widget_with_bar = SimpleBar(name, widget)
        main_layout.addWidget(widget_with_bar)
    else:
        main_layout.addWidget(widget)
    dialog.setLayout(main_layout)
    # Set Style
    css_file = os.path.join(CSS_PATH, "dark_style1.qss")
    if style:
        with open(css_file, 'r') as style_file:
            dialog.setStyleSheet(style_file.read())

    return dialog

form, base = load_ui_type(os.path.join(UIS_PATH, "simple_bar.ui"))


class SimpleBar(form, base):

    def __init__(self, name, widget):
        super(SimpleBar, self).__init__()
        self.setupUi(self)
        # with open(r"C:\project\dev\cmn\cmn\python\lib\ui\uis\stylesheet.css") as file:
        #   self.setStyleSheet(file.read())
        self.__init_icons()
        self.name.setText(str(name))
        self.set_style()
        self.widget_layout.addWidget(widget)

    def __init_icons(self):
        # Warning
        icon = QtGui.QIcon(os.path.join(IMAGE_PATH,"warning.png"))
        self.report_btn.setIcon(icon)
        # question
        icon = QtGui.QIcon(os.path.join(IMAGE_PATH,"question.png"))
        self.help_btn.setIcon(icon)

        pixmap = QtGui.QPixmap(os.path.join(IMAGE_PATH,"miguel.png"))
        self.icon.setPixmap(pixmap)
    def set_style(self):
        self.setStyleSheet(
            "QToolButton#report_btn,#help_btn{ background-color: rgba(0,0,0,1);border-width: 0px;}")
