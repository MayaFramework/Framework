import os
import re

import controller
from baseIcon import Button
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets
from toolbar_config import toolbar_config

reload(toolbar_config)

TOOLBAR_CFG_DATA = controller.toolbar_cfg_data()
COLOR = TOOLBAR_CFG_DATA.get("accent_color")
def widget_stylesheet(color):
    style = ""  + \
        "QPushButton"  + \
        "{" + \
        "background-color: transparent;" + \
        "border: 0px;" + \
        "border-width: 0px;" + \
        "padding: 20px;" + \
        "text-align: left" + \
    "}" + \
    "QPushButton:hover" + \
    "{" + \
        "border: 5px;" + \
        "border-left-style: solid;" + \
        "border-left-color: {};".format(color) + \
        "background-color:transparent;" + \
        "padding-left: 15px;" + \
        "text-align: left" + \
    "}" +\
    "QLabel" + \
    "{" + \
        "color: {};".format(color) + \
    "}" +\
    "QWidget#mainForm{" + \
	"background-color: rgb(0, 30, 48);" + \
    "color: {};".format(color) + \
    "}"
    return style


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class ToolsLauncherUI(form, base):

    def __init__(self):
        super(ToolsLauncherUI, self).__init__()
        self.setupUi(self)
        self.populateButtons()
        self.__default_state_window()
        self.__connect_default_signals()

    def populateButtons(self):
        all_buttons = toolbar_config.TOOLS
        for button in all_buttons:
            button.setStyleSheet(widget_stylesheet(COLOR))
            self.flow_layout.addWidget(button)
        spacer = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.flow_layout.addItem(spacer)            

    def __connect_default_signals(self):
        self.configBT.clicked.connect(self.__set_accent_color)

    def __default_state_window(self):
        picture = os.path.join(controller._config_path(), TOOLBAR_CFG_DATA.get("user_picture"))
        self.__set_user_picture(picture)
        self.usernameLB.setText(controller.current_user())
        self.setStyleSheet(widget_stylesheet(COLOR))
    
    def __set_user_picture(self, picture):
        pixmap = QtGui.QIcon(picture)
        self.usernameIcon.setIconSize(QtCore.QSize(80, 80))
        self.usernameIcon.setIcon(pixmap)

    def __set_accent_color(self):
        dialog = QtWidgets.QColorDialog()
        dialog.colorSelected.connect(self.__change_accent_color)
        dialog.exec_()

    def __change_accent_color(self, color):
        hex_color = str(color.name())
        self.setStyleSheet(widget_stylesheet(hex_color))
        for button in toolbar_config.TOOLS:
            button.setStyleSheet(widget_stylesheet(hex_color))
        toolbar_data = controller.toolbar_cfg_data()
        toolbar_data["accent_color"] = hex_color
        controller.save_toolbar_cfg_data(toolbar_data)


# EXAMPLE!!!

# from Framework.plugins.toolbar import baseIcon, model, controller
# reload(baseIcon)
# reload(controller)
# reload(model)
# ui = model.ToolsLauncherUI()
# ui.show()