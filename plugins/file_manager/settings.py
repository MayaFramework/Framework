from Framework.lib.ui.qt.QT import QtCore

class CustomSettings(QtCore.QSettings):

    def __init__(self, organization, application):
        super(CustomSettings, self).__init__(organization, application)

        for child in self.childKeys():
            setattr(self, child, self.value(child, decodeIfNeeded=False))

    def __getitem__(self, item):
        value = self.__dict__.get(item, None)
        if isinstance(value, str) or isinstance(value, unicode):
            return str(value).decode('base64','strict')
        return value

    def __setitem__(self, key, value):
        self.setValue(key, value)

    def setValue(self, key, value):
        if isinstance(value, str):
            value = value.encode('base64','strict')
        self.__dict__[key] = value
        super(CustomSettings, self).setValue(key, value)

    def value(self, key, decodeIfNeeded=True):
        if decodeIfNeeded:
            value = self.__dict__.get(key, None)
            if isinstance(value, str):
                return value.decode('base64','strict')
            return value
        else:
            return super(CustomSettings, self).value(key)

    def items(self):
        return vars(self)
