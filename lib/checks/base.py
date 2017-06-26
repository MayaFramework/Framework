"""Summary

Attributes:
    checker_widget (TYPE): Description
    general_batery_check (TYPE): Description
    GENERAL_CHECKS_BATTERY (TYPE): Description
    IMAGE_PATH (TYPE): Description
    maya_widget (TYPE): Description
"""
import sys
import os

from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.gui_loader import gui_loader
from simple.cmn import image
from Framework import get_environ_file, get_css_path, get_icon_path
IMAGE_PATH = get_icon_path()
'''
TODO:
comment everything :D
Change Ui Imports
'''


class BaseCheck(object):
    """Summary
    
    Attributes:
        CHECK_FAILLED (int): Description
        CHECK_PASSED (int): Description
        DEFAULT_STATE (int): Description
        READY_TO_FIX (int): Description
        state (TYPE): Description
    """
    def __init__(self):
        """Summary
        """
        super(BaseCheck, self).__init__()
        self._name = ""
        self._description = None
        self._fixable = False
        self._selectable = False
        self._output = ""
        self.CHECK_FAILLED = -1
        self.DEFAULT_STATE = 0
        self.CHECK_PASSED = 1
        self.READY_TO_FIX = 2
        self._state = self.DEFAULT_STATE

    # MAIN FUNCTIONS
    def execute(self):
        """Summary
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: Description
        """
        raise Exception("Method Not implemented from the class inherited")

    def fix(self):
        """Summary
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: Description
        """
        raise Exception("Method Not implemented from the class inherited")

    def select_in_scene(self):
        """Summary
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: Description
        """
        raise Exception("Method Not implemented from the class inherited")

    def is_fixable(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return True if self._fixable == True else False

    def is_selectable(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return True if self._selectable == True else False

    #Properties
    @property
    def state(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._state
    @state.setter
    def state(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        if value in [self.DEFAULT_STATE, self.CHECK_PASSED, self.READY_TO_FIX]:
            self._state = value

    @property
    def name(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._name

    @name.setter
    def name(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, str) and not isinstance(value, unicode):
            raise TypeError("Not Supported Type %s" % type(value))
        self._name = value


    @property
    def description(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._description

    @description.setter
    def description(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, str) and not isinstance(value, unicode):
            raise TypeError("Not Supported Type %s" % type(value))
        self._description = value

    @property
    def output(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._output

    @output.setter
    def output(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, str) and not isinstance(value, str):
            raise TypeError("Not Supported Type %s" % type(value))
        self._output = value

    @property
    def selectable(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._selectable

    @selectable.setter
    def selectable(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, bool):
            raise TypeError(value)
        self._selectable = value == True

    @property
    def fixable(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._selectable

    @fixable.setter
    def fixable(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, bool):
            raise TypeError(value)
        self._fixable = value == True

    def reset_state(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.state = self.DEFAULT_STATE
        return self.state




class BaseBatteryCheck(object):
    """Summary
    
    Attributes:
        checks (TYPE): Description
        name (TYPE): Description
    """
    def __init__(self, name, check_list=[]):
        """Summary
        
        Args:
            name (TYPE): Description
            check_list (list, optional): Description
        """
        super(BaseBatteryCheck, self).__init__()
        self._check_object_list = []
        self.name = name
        self.checks = check_list

    # Main Functions
    def execute_all(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        for check in self.checks:
            if check.state == check.CHECK_PASSED:
                continue
            check.execute()

    def fix_all(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        checks = self.checks
        for check in checks:
            if check.state == check.READY_TO_FIX:
                check.fix()

    def execute_and_fix_all(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.execute_all()
        self.fix_all()

    def reset_all(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        for check in self.checks:
            check.reset_state()



    def add_check(self, check):
        """Summary
        
        Args:
            check (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(check, BaseCheck):
            raise TypeError(check)
        self._check_object_list.append(check)

    def add_checks(self, check_list):
        """Summary
        
        Args:
            check_list (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        for check in check_list:
            self.add_check(check)


    @property
    def checks(self):
        """Summary
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: Description
        """
        if len(self._check_object_list) > 0:
            return self._check_object_list
        else:
            raise Exception("Not checks Defined")

    @checks.setter
    def checks(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not value:
            raise TypeError("Not Supported Type: %s" % value)
        if isinstance(value,list) or isinstance(value, dict):
            self.add_checks(value)
        else:
            self.add_check(value)

    @property
    def name(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._name

    @name.setter
    def name(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, str) and not isinstance(value, unicode):
            raise TypeError("Not Supported Type: %s" % value)
        self._name = value





row, base_row = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "check_row.ui"))


class BaseRowCheck(row, base_row):
    """Summary
    
    Attributes:
        controller (TYPE): Description
        icon_path (TYPE): Description
    """
    icon_path = {
        -1: os.path.join(IMAGE_PATH,  "general", "ic_highlight_off_white_24dp_2x.png"),
        0: os.path.join(IMAGE_PATH, "general", "ic_warning_white_24dp_2x.png"),
        1: os.path.join(IMAGE_PATH, "general", "ic_check_circle_white_24dp_2x.png"),
        2: os.path.join(IMAGE_PATH, "general", "ic_build_white_24dp_1x.png")
    }

    def __init__(self, controller=None):
        """Summary
        
        Args:
            controller (None, optional): Description
        
        Raises:
            Exception: Description
        """
        super(BaseRowCheck, self).__init__()
        self.setupUi(self)
        if not isinstance(controller, BaseCheck):
            raise Exception("Not supported Type of controller")
        self.controller = controller
        self._init_widget()

    def _init_widget(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.name_lab.setText(str(self.controller.name))
        self.name_lab.setToolTip(str(self.controller.name))
        self.description_lab.setText(str(self.controller.description))
        self.description_lab.setToolTip(str(self.controller.description))

        self.update_check_state()

        self.pass_btn.setIcon(QtGui.QIcon(os.path.join(
            IMAGE_PATH, "general", "ic_exit_to_app_white_24dp_1x.png")))
        self.fix_btn.setIcon(QtGui.QIcon(os.path.join(
            IMAGE_PATH, "general", "ic_build_white_24dp_1x.png")))
        self.copy_btn.setIcon(QtGui.QIcon(os.path.join(
            IMAGE_PATH, "general", "ic_content_copy_white_24dp_1x.png")))
        self.select_btn.setIcon(QtGui.QIcon(os.path.join(
            IMAGE_PATH, "general", "ic_tab_unselected_white_24dp_1x.png")))

    def update_check_state(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.state_lab.setPixmap(self.icon_path[self.controller.state])
        QtWidgets.QApplication.processEvents()

    def reset_state(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.controller.reset_state()

    def state(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self.controller.state

    @QtCore.Slot()
    def on_pass_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.controller.execute()
        self.update_check_state()

    @QtCore.Slot()
    def on_fix_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: Description
        """
        if self.controller.is_fixable():
            self.controller.fix()
            self.update_check_state()
        else:
            raise Exception("This check is not fixable")

    @QtCore.Slot()
    def on_copy_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        output = self.controller.get_output()
        if output:
            print output  # USES PYTHON LOGGER
        else:
            print "There arent any output"

    @QtCore.Slot()
    def on_select_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        
        Raises:
            Exception: Description
        """
        if self.controller.is_selectable():
            self.controller.select_in_scene()
        else:
            raise Exception(
                "There are not any available elements to select defined")


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "battery_check_container.ui"))


class BaseChecksWidget(form, base):
    """Summary
    
    Attributes:
        battery_checker_list (TYPE): Description
        rows (list): Description
    """
    def __init__(self, battery_checker_list):
        """Summary
        
        Args:
            battery_checker_list (TYPE): Description
        """
        super(BaseChecksWidget, self).__init__()
        self.setupUi(self)
        self.rows = []
        self.battery_checker_list = battery_checker_list
        self._init_batteries()
    def _init_batteries(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        line = QtWidgets.QFrame()
        line.setGeometry(QtCore.QRect(320, 150, 118, 3)

)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        for battery in self.battery_checker_list:
            if not isinstance(battery, BaseBatteryCheck):
                raise Exception(
                    "This Battery: %s is not from a base class supported" % type(battery))

            # Creating Layout Ui for each battery and appending rows widgets
            battery_layout = QtWidgets.QVBoxLayout()
            battery_layout.addWidget(line)
            battery_label = QtWidgets.QLabel(battery.name)
            battery_layout.addWidget(battery_label)
            for check in battery.checks:
                row_widget = BaseRowCheck(check)
                battery_layout.addWidget(row_widget)
                self.rows.append(row_widget)
            self.check_layout.addLayout(battery_layout)

    def update_battery_rows(self, battery):
        """Summary
        
        Args:
            battery (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        for check in battery.checks:
            for row in self.rows:
                if not row.controller == check:
                    continue
                row.update_check_state()

    @QtCore.Slot()
    def on_passAll_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        for battery in self.battery_checker_list:
            battery.execute_all()
            self.update_battery_rows(battery)

    @QtCore.Slot()
    def on_fixAll_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        for battery in self.battery_checker_list:
            battery.fix_all()
            self.update_battery_rows(battery)

    @QtCore.Slot()
    def on_passFixAll_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        for battery in self.battery_checker_list:
            battery.execute_and_fix_all()
            self.update_battery_rows(battery)

    @QtCore.Slot()
    def on_resetAll_btn_clicked(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        for battery in self.battery_checker_list:
            battery.reset_all()
            self.update_battery_rows(battery)







# EXAMPLE PLUGIN
class CleanPlugins(BaseCheck):
    """Summary
    
    Attributes:
        description (str): Description
        fixable (bool): Description
        name (str): Description
        output (TYPE): Description
        selectable (bool): Description
        state (TYPE): Description
    """
    def __init__(self):
        """Summary
        """
        super(CleanPlugins, self).__init__()
        self.name = "Clean Plugins"
        self.description = "Clean every plugin not supported"

    def execute(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        # Update State
        # Reset output
        # Start Check process

        # Update Result
        # update output
        # update fix state (its fixable just once it has tried to pass the check)
        # Update data to select if its possible throught the Ui
        print "Starting CHECK: %s" % self.name
        self.state = self.CHECK_PASSED
        self.selectable = False
        self.fixable = False
        self.output = "Check: %s PASSED" % self.name
        return True

class CheckSceneName(BaseCheck):
    """Summary
    
    Attributes:
        description (str): Description
        fixable (bool): Description
        name (str): Description
        output (str): Description
        selectable (bool): Description
        state (TYPE): Description
        TRAPI (int): Description
    """
    TRAPI = 0

    def __init__(self):
        """Summary
        """
        super(CheckSceneName, self).__init__()
        self.name = "Check Name Convention"
        self.description = "This check makes blablablabalbal aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
    def execute(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        print "Starting Check CHECK: %s" % self.name


        self.selectable = False

        if self.TRAPI == 0:
            self.fixable = True
            self.state = self.READY_TO_FIX
            self.output = "SOMETHING WAS WRONG ON CHECKSCENE NAME"
            print self.output
            return False
        if self.TRAPI == 1:
            self.fixable = False
            self.state = self.CHECK_PASSED
            self.output = "Check: %s PASSED" % self.name
            return True

    def fix(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        print "Starting Fix %s"%self.name
        self.TRAPI = 1
        self.execute()



if __name__ == "__main__":

    QtWidgets.QApplication(sys.argv)
    # # EXAMPLE BATTERY
    GENERAL_CHECKS_BATTERY = [CleanPlugins(), CheckSceneName()]

    general_batery_check = BaseBatteryCheck("General Checks",GENERAL_CHECKS_BATTERY)

    checker_widget = BaseChecksWidget([general_batery_check])

    maya_widget = gui_loader.get_maya_container(checker_widget)
    maya_widget.exec_()
