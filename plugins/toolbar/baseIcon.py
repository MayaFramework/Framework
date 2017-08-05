import os
import random

from Framework.lib.ui.qt.QT import QtCore, QtGui, QtWidgets
from toolbar_config import colors

print "TEST"

class Button(QtWidgets.QPushButton):

    button_clicked = QtCore.Signal()
    button_released = QtCore.Signal()
    button_pressed = QtCore.Signal()

    HEIGHT = 70

    def __init__(self):
        super(Button, self).__init__()
        self._name = ""
        self._icon = None
        self._clicked_command = None
        self._pressed_command = None
        self._release_command = None
        self.__pressed = False
        self.setAutoRepeat(True)
        self.clicked.connect(self.__handle_click)
        self.button_clicked.connect(self.__clickedButton)
        self.button_released.connect(self.__releasedButton)
        self.button_pressed.connect(self.__pressedButton)
        self.setFixedHeight(self.HEIGHT)
        self.__setStyleSheet()
        # self.setFixedWidth(self.HEIGHT)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, button_name):
        self._name = button_name
        self.setText("  {}".format(self._name))

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, button_icon):
        self._icon = button_icon
        self.setIconSize(QtCore.QSize(32, 32))
        self.setIcon(QtGui.QIcon(self._icon))

    @property
    def clicked_command(self):
        return self._clicked_command

    @clicked_command.setter
    def clicked_command(self, button_clicked_command):
        self._clicked_command = button_clicked_command

    @property
    def pressed_command(self):
        return self._pressed_command

    @pressed_command.setter
    def pressed_command(self, button_pressed_command):
        self._pressed_command = button_pressed_command

    @property
    def release_command(self):
        return self._release_command

    @release_command.setter
    def release_command(self, button_release_command):
        self._release_command = button_release_command

    def __handle_click(self):
        if self.isDown():
            self.button_pressed.emit()
        elif not self.__pressed:
            self.button_clicked.emit()
        else:
            self.button_released.emit()

    def __clickedButton(self):
        if not self.clicked_command:
            raise Exception("Clicked Command not implemented")        
        self.clicked_command()

    def __releasedButton(self):
        def restore_state():
            self.setAutoRepeat(True)
            self.__pressed = False
        restore_state()
        if not self.release_command:
            raise Exception("Release Command not implemented")
        self._release_command()

    def __pressedButton(self):
        def restore_state():
            self.setAutoRepeat(False)
            self.__pressed = True
        restore_state()
        if not self.pressed_command:
            raise Exception("Pressed Command not implemented")
        self._pressed_command()
        
    def __setStyleSheet(self):
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        self.setFont(bold_font)
        # default_stylesheet = "border:0px; background-color:transparent; padding-left: 10px; text-align: left" # border-left-color:#2196F3" 
        # stylesheet = colors.COLORS.get(random.randint(0, len(colors.COLORS.keys())-1))
        # self.setStyleSheet(STYLESHEET)

    # def enterEvent(self, event):
    #     stylesheet = "border: 5px; border-left-style: solid; border-left-color: #2196F3;background-color:transparent; padding-left: 10px; text-align: left"
    #     self.setStyleSheet(stylesheet)
    #     super(Button, self).enterEvent(event)

    # def leaveEvent(self, event):
    #     stylesheet = "border:0px; background-color:transparent; padding-left: 10px; text-align: left"
    #     self.setStyleSheet(stylesheet)
    #     super(Button, self).leaveEvent(event)        

class TestButton(Button):

    def __init__(self):
        super(TestButton, self).__init__()
        self.name = "Checks"
        self.icon = os.path.join(os.path.dirname(__file__), "gui", "icons", "checks.png")
        self.clicked_command = self.click        
        self.pressed_command = self.pressed
        self.release_command = self.released

    def click(self):
        from Framework.lib.new_checks import model, checks_configuration, baseCheck
        ui = model.ChecksUIWidget()
        ui.show()
    
    def pressed(self):
        print "PRESSED"

    def released(self):
        print "RELEASED"
