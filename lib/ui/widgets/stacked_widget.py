"""Summary
"""
import sys
import os
import pprint
from cmn.cmn.python.lib.ui.QT import QtWidgets, QtCore, Qt
from cmn.cmn.python.lib.ui import ui_loader

from cmn.cmn.python.lib import ui
UIS_PATH = ui.get_uis_path()
form, base = ui_loader.load_ui_type(
    os.path.join(UIS_PATH, "stacked_widget.ui"))


class StackedWidgetChild(QtWidgets.QDialog):
    """
    Class that must be inherited for the widgets of stackedWidget.
    This class defines a methods that must be implemented to fit with the
    StackedWidget Structure
    """
    def __init__(self):
        super(StackedWidgetChild, self).__init__()

    def get_state(self):
        raise Exception(
            "This method must be reimplemented to return the current state of the widget")



class StackedWidget(form, base):
    """
    This Widget works to have different layers with the same two buttons
    Updating the current state allows to pass to the next widget.
    """
    _widgets_added = []

    def __init__(self):
        """Summary
        """
        super(StackedWidget, self).__init__()
        self.setupUi(self)
        self.state = False
        self.total_widgets_count = 0
        # self.update_btns_state()
        self.left_btn.setHidden(True)

    def add_widget(self, widget):
        """
        add the widget into the list appending the element 
        Args:
            widget (QtWidget/QtDialog): Widget to add into the list

        """
        self.stackedWidget.addWidget(widget)
        self.total_widgets_count = self.stackedWidget.count()

    def insert_widget(self, idx, widget):
        """
        Inserts the widget in to the index position

        Args:
            idx (int): position to insert
            widget (QtWidget/QtDialog): Window to insert
        """
        self.stackedWidget.insertWidget(idx, widget)
        self.total_widgets_count = self.stackedWidget.count()

    def move_forward(self):
        """

        Change current widget with the next index if this exists.


        Raises:
            Exception: There arent more widgets in that direction
        """
        current_widgets_count = self.stackedWidget.count()
        if not current_widgets_count:
            raise Exception("there are no more widgets to pass")

        current_index = self.stackedWidget.currentIndex()
        if current_index == current_widgets_count - 1:
            # TODO change for finish process
            raise Exception("There are not more widgets forward")

        if self.state == True:
            self.stackedWidget.setCurrentIndex(
                self.stackedWidget.currentIndex()+1)
            self.reset_state()
            self.update_btns_state()
            return True
        else:
            return False

    def move_backward(self):
        """
        Change current widget with the next index if this exists.


        Raises:
            Exception: There arent more widgets in that direction
        """
        current_widgets_count = self.stackedWidget.count()
        if not current_widgets_count:
            raise Exception("there are no more widgets to pass")

        current_index = self.stackedWidget.currentIndex()
        if current_index == 0:
            raise Exception("There are no more widgets backward")

        self.reset_state()
        self.stackedWidget.setCurrentIndex(current_index-1)
        self.update_btns_state()

    def update_btns_state(self):
        """
        Update the buttons visibility 
        """
        self.left_btn.setHidden(False)
        self.right_btn.setHidden(False)
        current_idx = self.stackedWidget.currentIndex()
        maximum_widgets = self.stackedWidget.count()
        if current_idx == 0:  # First View
            self.left_btn.hide()
        if current_idx == maximum_widgets-1:  # Last view
            self.right_btn.hide()

        else:
            pass

    def get_current_state(self):
        """
        returns current state

        Returns:
            bool: state to pass or not the widget forward or backward
        """
        return self.state

    def set_state(self, state):
        """
        update the state with the new value.
        This falg is used to pass forward or backward

        Args:
            state (bool): True/False

        Raises:
            TypeError: Not supported Type must be a bool type
        """
        if not isinstance(state, bool):
            raise TypeError("Not supported type: %s " % type(state))
        self.state = state

    def reset_state(self):
        """
        reset the state to false
        """
        self.state = False

    def current_widget(self):
        """

        Returns:
            QtWidget: returns the current widget
        """
        return self.stackedWidget.currentWidget()

    @QtCore.Slot()
    def on_left_btn_clicked(self):
        """
        Move backward, in order to avoid future
        issues when this class is inherited it must overload
        this function to check the state of the current widget

        In the widget added before must be defined a function
        get state to know in what current state its found
        """
        widget = self.current_widget()
        self.set_state(widget.get_state())
        self.move_backward()

    @QtCore.Slot()
    def on_right_btn_clicked(self):
        """
        Move forward, in order to avoid future
        issues when this class is inherited it must overload
        this function to check the state of the current widget

        In the widget added before must be defined a function
        get state to know in what current state its found
        """
        widget = self.current_widget()
        self.set_state(widget.get_state())
        self.move_forward()


# EXAMPLE
'''
class ElementPublisher(StackedWidget):

    def __init__(self):
        super(ElementPublisher, self).__init__()
        # Widgets List
        widget_list = [ElementChecksWidget, ElementPublishWidget]
        for x, widget in enumerate(widget_list):
            self.insert_widget(x, widget())
            # TODO ORder by window element widget 

    def on_left_btn_clicked(self):
        widget = self.current_widget()
        widget_state = widget.get_state()
        if widget_state:
            super(ElementPublisher,self).on_left_btn_clicked()


    def on_right_btn_clicked(self):
        widget = self.current_widget()
        widget_state = widget.get_state()
        if widget_state:
            super(ElementPublisher,self).on_right_btn_clicked()



form, base = ui_loader.load_ui_type(os.path.join(UIS_PATH,"element_publish_widget.ui"))

class ElementChecksWidget(form, QtWidgets.QDialog):

    def __init__(self):
        super(ElementChecksWidget, self).__init__()
        self.setupUi(self)

    def get_state(self):
        return True if self.state.isChecked() else False


form, base = ui_loader.load_ui_type(os.path.join(UIS_PATH,"battery_checks_widget.ui"))
class ElementPublishWidget(form, QtWidgets.QDialog):

    def __init__(self):
        super(ElementPublishWidget, self).__init__()
        self.setupUi(self)

    def get_state(self):
        return True if self.state.isChecked() else False


app = QtWidgets.QApplication(sys.argv)
element_publisher_container = ui_loader.get_maya_container(ElementPublisher(), name = "Elements Publisher",style=True)
element_publisher_container.exec_()

'''
