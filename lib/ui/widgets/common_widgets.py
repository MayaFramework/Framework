

"""
Summary:
    This module cover a common uses of QtWidgets  
"""
import sys
import pprint
import os
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui, QtXml
from Framework.lib.types import types 
# from cmn.cmn.python.lib imporPyQt5
# from PyQt5 import QtWidgets, QtCore, Qt
from Framework import get_css_path
from Framework.lib.gui_loader import gui_loader
from Framework.lib.file import utils as file_utils
from Framework import get_environ_file, get_css_path, get_icon_path
CSS_PATH = get_css_path()
ICON_PATH = get_icon_path()
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
    _name_btn_left = 'Cancel'
    _name_btn_right = 'Continue'
    _level_supported = [ERROR_LEVEL, INFO_LEVEL, WARNING_LEVEL]

    def __init__(self, title, level='INFO', msg=None):
        super(MessageWindow, self).__init__()
        set_style_sheet(self, os.path.join(get_css_path(), "dark_style1.qss"))
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

    @property
    def name_btn_left(self):
        return self._name_btn_left

    @name_btn_left.setter
    def name_btn_left(self, value):
        if isinstance(value, (str,unicode)):
            self._name_btn_left = value
        
        self.left_btn.setText(value)
        
    @property
    def name_btn_right(self):
        return self._name_btn_right

    @name_btn_right.setter
    def name_btn_right(self, value):
        if isinstance(value, (str,unicode)):
            self._name_btn_right = value
        
        self.right_btn.setText(value)
        


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
        set_style_sheet(self, os.path.join(get_css_path(), "dark_style1.qss"))
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


class MovieLabel(QtWidgets.QWidget):

    def __init__(self, file_path, parent=None):
        super(MovieLabel, self).__init__(parent)
        self.movie = QtGui.QMovie(file_path, QtCore.QByteArray(), self)
        size = self.movie.scaledSize()
        self.setGeometry(200, 200, size.width(), size.height())
        self.movie_screen = QtWidgets.QLabel()
        self.movie_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(30)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

class FilterableWidget(object):
    
    def __init__(self, parent=None):
        super(FilterableWidget, self).__init__()
        self.is_filtered = True
        
    '''
    implement this method in the widget that inherits specifying the rules that filter
    '''
    def filtering_behaviour(self):
        pass
    
    def IsFiltered(self, filters):
        
        self.is_filtered = self.filtering_behaviour(filters)
        return self.is_filtered
    


class FilterWidget(QtWidgets.QWidget):
        
    def __init__(self, parent = None,widgets_to_filter=[]):
        super(FilterWidget,self).__init__(parent)
        self.widgets_to_filter = widgets_to_filter
        gui_loader.loadUiWidget(os.path.normpath(os.path.join(os.path.dirname(__file__),'../..','ui',"uis",'filter_widget.ui')), self)
        self.le_filter.textChanged.connect(self.filter)
        self.custom_filters = None
        self.pb_filter.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"search.png")))
        self.widget_names = {}
        
    def filter(self):
        """ provokes error C++. Use findChild instead. """
        ''' 
        print('testing C++ error')
        filters = self.le_filter.text().split('')
        '''
        filters = self.findChild(QtWidgets.QLineEdit,'le_filter').text().split(' ')
        
        if self.custom_filters:
            filters.extend(self.custom_filters)
            
        self.hide_all()
        
        for w in self.parentWidget().findChildren(FilterableWidget):
            if w.IsFiltered(filters):
                w.show()
        '''
        for w in self.widgets_to_filter:
            if w.IsFiltered(filters):
                w.show()
        '''
    def clear_filter_widget(self, clear_custom_filters = True):
        self.widgets_to_filter = {}
        if clear_custom_filters:
            self.clear_custom_filters()
        
    def hide_all(self):
        for w in self.parentWidget().findChildren(QtWidgets.QWidget):
            if isinstance(w,FilterableWidget):
                w.hide()
        '''    
        for w in self.widgets_to_filter:
            w = self.findChild(FilterableWidget, w_name)
            w.hide()
        '''
    def add_filterable_widget(self, w):
        if not self.widgets_to_filter:
            self.widgets_to_filter = []
        if isinstance(w, FilterableWidget):
            self.widgets_to_filter.append(w)
        else:
            raise Exception('Widget must inherit from FilterableWidget class!')
        
    def add_custom_filters(self, custom_filters):
        if not self.custom_filters:
            self.custom_filters = []
        if any(type(custom_filters) == string_type for string_type in (types.StringType,types.UnicodeType,types.StringTypes)):
            if not custom_filters in self.custom_filters:
                self.custom_filters.append(unicode(custom_filters))
        elif type(custom_filters) == type([]):
            self.custom_filters = list(set(self.custom_filters) | set(unicode(f) for f in custom_filters))
        
    def clear_custom_filters(self):
        self.custom_filters = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    a = MovieLabel(file_path="P:\dev\Framework\icons\gif\loading.gif")
    a.show()
    app.exec_()
# if __name__ == "__main__":
# # EXAMPLE Progress Bar
# #     import time
# #     processBar = ProgressBar(100)
# #     for x in range(0, 100):
# #         time.sleep(0.1)
# #         processBar.update()
#
#   app = QtWidgets.QApplication(sys.argv)
#   a = MessageWindow(title='Publisher Message',
#                   level='ERROR',
#                   msg='message')
#     # b = ReporterWindow(title = ' reporter', level = 'WARNING', msg='My Message to send into some ddbb ')
