import os
from toolbar_config import toolbar_config
reload(toolbar_config)
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class ToolsLauncherUI(form, base):

    def __init__(self):
        super(ToolsLauncherUI, self).__init__()
        self.setupUi(self)
        self.populateButtons()

    def populateButtons(self):
        all_buttons = toolbar_config.TOOLS
        for button in all_buttons:
            self.flow_layout.addWidget(button)
        # self.scrollContainer.setLayout(main_layout)
