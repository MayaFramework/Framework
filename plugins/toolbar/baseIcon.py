from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui

class toolbarIcon(QtWidgets.QPushButton):

    _name = ""
    _extraOptions = False
    _icon = ""

    _SIZE = QtCore.QSize(32, 32)

    def __init__(self):
        super(toolbarIcon, self).__init__()
        self.setSize(_SIZE)
        self.clicked.connect(self.run)
    
    @property
    def extraOptions(self):
        return self._extraOptions

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    def run(self):
        """
        Overloaded function
        """
        pass

class newIcon(toolbarIcon):

    _name = "Save Incremental"
    _extraOptions = False
    _icon = "ICONPATH"

    def __init__(self):
        super(newIcon, self).__init__()
        if self.extraOptions:
            self.__createPullDown()

    def run(self):
        print "JHOOOODER"

    def __createIcon(self):
        iconPath = self.icon
        print iconPath
        #TODO Crear el icono, y meterlo en el Toolbar

    def __createPullDown(self):
        pass