import maya.cmds as cmds
import sys
import os

from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.gui_loader import gui_loader
from Framework import get_environ_file, get_css_path, get_icon_path


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
        self._affectedElements = list()
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

    def has_affectedElements(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return True if self._affectedElements != [] else False

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
        if value in [self.DEFAULT_STATE, self.CHECK_PASSED, self.READY_TO_FIX, self.CHECK_FAILLED]:
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
    def output(self, value, *args):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, str):
            raise TypeError("Not Supported Type %s" % type(value))
        self._output += "{}\n".format(value)

    def setLog(self, value, *args):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """        
        if not isinstance(value, str):
            raise TypeError("Not Supported Type %s" % type(value))
        if "start" in args:
            self._output += "### {} ###\n\n".format(self.name)
        self._output += "{}\n".format(value)
        if "final" in args:
            self._output += "##########\n\n"        

    @property
    def affectedElements(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._affectedElements

    @affectedElements.setter
    def affectedElements(self, value):
        """Summary
        
        Args:
            value (TYPE): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            TypeError: Description
        """
        if not isinstance(value, list):
            raise TypeError(value)
        self._affectedElements = value

    @property
    def fixable(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        return self._fixable

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
    def __init__(self, name, check_list=[], mainFunction=None):
        """Summary
        
        Args:
            name (TYPE): Description
            check_list (list, optional): Description
        """
        super(BaseBatteryCheck, self).__init__()
        self._check_object_list = []
        self.name = name
        self.checks = check_list
        self.mainFunction = mainFunction

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
        