import os
from functools import partial
import maya.cmds as cmds

from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui

import baseCheck
import checks_configuration


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class ChecksUIWidget(form, base):
    """Summary
    
    Attributes:
        battery_checker_list (TYPE): Description
        rows (list): Description
    """
    CHECKNAMEICON = QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/name_tag.png"))
    DESCRIPTIONICON = QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/description.png"))
    LOGICON = QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/log.png"))
    RUNICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/run.png"))
    FIXICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/fix.png"))    

    def __init__(self, battery_checker_list=None):
        """Summary
        
        Args:
            battery_checker_list (TYPE): Description
        """
        super(ChecksUIWidget, self).__init__()
        self.setupUi(self)
        self.__defaultStateWindow()
        self.__connectDefaultSignals()
        self.__addTabs()
    
    def __connectDefaultSignals(self):
        self.runallBT.clicked.connect(self.runAll)
        self.fixallBT.clicked.connect(self.fixAll)

    def __defaultStateWindow(self):
        self.nametag_icon.setPixmap(self.CHECKNAMEICON)
        self.description_icon.setPixmap(self.DESCRIPTIONICON)
        self.log_icon.setPixmap(self.LOGICON)
        self.runallBT.setIcon(self.RUNICON)
        self.fixallBT.setIcon(self.FIXICON)

    def __addTabs(self):
        batteriesChecks = checks_configuration.ALLBATTERIES
        for battery in batteriesChecks:
            scrollArea = QtWidgets.QScrollArea()
            scrollArea.setWidgetResizable(True)
            scrollWidget = QtWidgets.QWidget()
            scrollLayout = QtWidgets.QVBoxLayout()
            scrollLayout.setSpacing(0)
            scrollLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            scrollLayout.setContentsMargins(0,0,0,0)
            for check in battery.checks:
                checkWidget = CheckWidget(check, self)                
                scrollLayout.addWidget(checkWidget)
            spacer = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            scrollLayout.addItem(spacer)
            scrollWidget.setLayout(scrollLayout)
            scrollArea.setWidget(scrollWidget)
            self.checksTab.addTab(scrollArea, battery.name)    

    def runAll(self):
        currentWidget = self.checksTab.currentWidget()
        for widget in currentWidget.findChildren(CheckWidget):
            if widget.checkObject.state == widget.checkObject.CHECK_PASSED:
                continue
            widget.runCheck()

    def fixAll(self):
        currentWidget = self.checksTab.currentWidget()
        for widget in currentWidget.findChildren(CheckWidget):
            if widget.checkObject.state == widget.checkObject.CHECK_PASSED or not widget.checkObject.fixable:
                continue
            widget.fixCheck()


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "check_widget.ui"))


class CheckWidget(form, base):

    STATES = {
       -1          : "border:1px outset; border-color: #880E4F; border-radius: 2px; background-color:#E91E63",
        0          : "border:1px outset; border-color: #0D47A1; border-radius: 2px; background-color:#2196F3",
        1          : "border:1px outset; border-color: #1B5E20; border-radius: 2px; background-color:#4CAF50",
        2          : "border:1px outset; border-color: #E65100; border-radius: 2px; background-color:#FF9800",
        "disabled" : "border:1px outset; border-color: #212121; border-radius: 2px; background-color:#9E9E9E"
    }
    RUNICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/run.png"))
    FIXICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/fix.png"))
    SELECTICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "gui/icons/select.png"))

    def __init__(self, checkObject, mainUI):
        super(CheckWidget, self).__init__()
        self.setupUi(self)
        if not isinstance(checkObject, baseCheck.BaseCheck):
            raise Exception("Unsupported check Object")
        self.checkObject = checkObject
        self.mainUI = mainUI
        self.name_lab.setText(str(self.checkObject.name))
        self.name_lab.setToolTip(str(self.checkObject.name))
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setWidgetState()
        self.__connectDefaultSignals()
        self.__setIcons()
        self.__setFont()

    def __setIcons(self):
        self.runBT.setIcon(self.RUNICON)
        self.fixBT.setIcon(self.FIXICON)
        self.selBT.setIcon(self.SELECTICON)

    def __setFont(self):
        font = QtGui.QFont()
        font.setBold(True)
        self.name_lab.setFont(font)

    def __connectDefaultSignals(self):
        self.runBT.clicked.connect(self.runCheck)
        self.fixBT.clicked.connect(self.fixCheck)
        self.selBT.clicked.connect(self.selectAssets)

    def setWidgetState(self):
        self.mainUI.logTE.setText(self.checkObject.output)
        self.fixBT.setEnabled(self.checkObject.fixable)
        affectedElems_bool = True if self.checkObject.affectedElements != [] else False
        self.selBT.setEnabled(affectedElems_bool)
        if self.checkObject.disable:
            self.setStyleSheet(self.STATES["disabled"])
        else:
            self.setStyleSheet(self.STATES[self.checkObject.state])

    def runCheck(self):
        self.__refreshUI()
        self.checkObject.execute()
        self.setWidgetState()

    def fixCheck(self):
        self.__refreshUI()
        self.checkObject.fix()
        self.setWidgetState()

    def selectAssets(self):
        self.__refreshUI()
        if self.checkObject.affectedElements:
            cmds.select(self.checkObject.affectedElements)

    def enterEvent(self, event):
        super(CheckWidget, self).enterEvent(event)

    def leaveEvent(self, event):
        super(CheckWidget, self).enterEvent(event)                 

    def mousePressEvent(self, event):
        '''re-implemented to suppress Right-Clicks from selecting items.'''
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                if self.checkObject.state == self.checkObject.DEFAULT_STATE:
                    self.checkObject.disable = not self.checkObject.disable
                    if self.checkObject.disable:
                        self.setStyleSheet(self.STATES["disabled"])
                        self.runBT.setEnabled(False)
                    else:
                        self.setStyleSheet(self.STATES[self.checkObject.state])
                        self.runBT.setEnabled(True)
            else:
                if not self.checkObject.disable:
                    self.__refreshUI() 
        super(CheckWidget, self).mousePressEvent(event)        

    def __refreshUI(self):
        self.mainUI.nameLB.setText(self.checkObject.name)
        self.mainUI.descriptionTE.setText(self.checkObject.description)
        self.mainUI.logTE.setText(self.checkObject.output)        
