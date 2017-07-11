

"""
Summary:
	This module cover a common uses of QtWidgets  
"""
import sys
import pprint
import os
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui, QtXml
# from cmn.cmn.python.lib import PyQt5
# from PyQt5 import QtWidgets, QtCore, Qt
from Framework import get_css_path
def set_style_sheet(Qt_object, css_file):
	with open(css_file, 'r') as style_file:
		Qt_object.setStyleSheet(style_file.read())

class MessageWindow(QtWidgets.QDialog):
    """
    A Common message window to wait for a user response

    Initialize and wait for a response.
    Ask the response by calling the method (get_response)
    	get_response:
    		True: if it have pressed the right button (Continue)
    		False: if it have pressed the left button (Cancel)
    Attributes:
        name_btn_left (str): name of the left btn
        name_btn_right (str): name of the right btn
        _level_supported (lsit): of levels supported to format the window
        text (QtWidgets.QPlainText): an optional container to put a huge msg
		title(str): Main short msg
		level (Str): A specific level to format the information 
		msg (str): String to fill the container info

    """
    ERROR_LEVEL = "ERROR"
    WARNING_LEVEL = "WARNING"
    INFO_LEVEL = "INFO"
    name_btn_left = 'Cancel'
    name_btn_right = 'Continue'
    _level_supported = [ERROR_LEVEL, INFO_LEVEL, WARNING_LEVEL]

    def __init__(self, title, level='INFO', msg=None):
        super(MessageWindow, self).__init__()
        set_style_sheet(self,os.path.join(get_css_path(),"dark_style1.qss"))
        self._state = False
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.horizontal_layout_btns = QtWidgets.QHBoxLayout()
        self.label_layout = QtWidgets.QHBoxLayout()

        title_font = QtGui.QFont()
        title_font.setPointSize(11)
        self.title_label = QtWidgets.QLabel()
        self.title_label.setText(title)
        self.title_label.setFont(title_font)

        level_font = QtGui.QFont()
        level_font.setPointSize(11)
        level_font.setBold(True)
        self.level_label = QtWidgets.QLabel()
        self.level_label.setFont(level_font)
        self.level_label.setText(level.upper())
        self.set_lvl_color(self.level_label, level)
        self.label_layout.addWidget(self.title_label)
        self.label_layout.addWidget(self.level_label)

        self.right_btn = QtWidgets.QPushButton()
        self.right_btn.setMinimumHeight(30)
        self.right_btn.setMinimumWidth(100)
        self.right_btn.setText(self.name_btn_right)
        self.right_btn.clicked.connect(self.on_right_btn)

        self.left_btn = QtWidgets.QPushButton()
        self.left_btn.setMinimumHeight(30)
        self.left_btn.setMinimumWidth(100)
        self.left_btn.setText(self.name_btn_left)
        self.left_btn.clicked.connect(self.on_left_btn)

        self.vertical_layout.addLayout(self.label_layout)

        if msg:
            self.text = QtWidgets.QTextEdit()
            self.text.setPlainText(msg)
            self.vertical_layout.addWidget(self.text)
            self.text.setReadOnly(True)

        self.horizontal_layout_btns.addWidget(self.left_btn)
        self.horizontal_layout_btns.addWidget(self.right_btn)

        self.vertical_layout.addLayout(self.horizontal_layout_btns)

        self.resize(100, 10)
        self.exec_()

    def set_lvl_color(self, label, lvl):
        sample = QtGui.QPalette()
        color = self.get_color_lvl(lvl)
        sample.setColor(QtGui.QPalette.WindowText, color)
        label.setPalette(sample)

    def get_color_lvl(self, lvl):
        if not lvl.upper() in self._level_supported:
            raise Exception("Level not supported")
        if lvl.upper() == 'ERROR':
            return QtGui.QColor(128, 21, 21)
        elif lvl.upper() == 'INFO':
            return QtGui.QColor(7.1, 21.6, 32.2)
        elif lvl.upper() == 'WARNING':
            return QtGui.QColor(212, 196, 106)

    def get_response(self):
        return self._state

    def on_right_btn(self):
        self._state = True
        self.close()

    def on_left_btn(self):
        self._state = False
        self.close()


class ReporterWindow(MessageWindow):
    """
    Class which inherites from Message window to change the btn actions

    
    Attributes:
        name_btn_left (str): String with the left name
        name_btn_right (str): String with the right name
	
    """
    def __init__(self, title, level='ERROR', msg=None):
        self.name_btn_left = 'Copy Information'
        self.name_btn_right = 'Send Information'
        super(ReporterWindow, self).__init__(title, level, msg)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)

    def on_left_btn(self):
        """
        This btn copy the information from the text container into the cliboard.
        
        Returns:
            TYPE: Description
        """
        try:
            if self.text:
                cliboard = QtWidgets.QApplication.clipboard()
                cliboard.setText(self.text.toPlainText())
            else:
                pass
        except:
            print "Not Text Found to copy on the cliboard"

    def on_right_btn(self):
        """
        A method overloaded which manages the way of sending informations
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: IN PROGRES

        TODO:
	        # It could be an option to send into the ddbb
	        # It could be another option to send the information by email
        """
        raise Exception("IN-PROGRESS")


class ProgressBar(QtWidgets.QProgressBar):
    """
    Re imeplementation of Progress Bar 
    
    Attributes:
        maximum (int): maximum value where the progress bar ends
        value (int): current value
    """
    def __init__(self, max=None):
        super(ProgressBar, self).__init__()
        set_style_sheet(self,os.path.join(get_css_path(),"dark_style1.qss"))
        self.value = 0
        if max:
            self.setMax(max)
        self.show()

    def setMax(self, value):
        self.maximum = max
        self.setMaximum(value)

    def update(self):
        if self.value == self.getMax() or self.value > self.getMax():
            self.close()
            return
        self.value += 1
        self.setValue(self.value)
        QtWidgets.qApp.processEvents()

    def getMax(self):
        return self.maximum

if __name__ == "__main__":
# EXAMPLE Progress Bar
# 	import time
# 	processBar = ProgressBar(100)
# 	for x in range(0, 100):
# 		time.sleep(0.1)
# 		processBar.update()

	app = QtWidgets.QApplication(sys.argv)
	a = MessageWindow(title='Publisher Message',
					level='ERROR',
					msg='message')
    # b = ReporterWindow(title = ' reporter', level = 'WARNING', msg='My Message to send into some ddbb ')
