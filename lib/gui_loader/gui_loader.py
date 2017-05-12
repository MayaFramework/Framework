import sys
import os
import PySide
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui, QtXml
# from cmn.cmn.python.lib.ui.QT import  QtCore, QtWidgets, QtGui, QtXml
from Framework import get_css_path, get_environ_file, get_icon_path, get_uis_path

IMAGE_PATH = get_icon_path()
UIS_PATH = get_uis_path()
CSS_PATH = get_css_path()
try:
    import pyside2uic as uic
except:
    from Framework.lib import pysideuic as uic

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



def get_maya_container(widget, name='APP NAME',style=True, simple_bar=True):
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Framework: [Miguel/Alberto]")
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
