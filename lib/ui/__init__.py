


from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui


def apply_resource_style(ui_object):
    from Framework.lib.ui.resources import resources_rc
    f = QtCore.QFile(":qdarkstyle/rc/style.qss")
    if f.exists():
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
        stylesheet = ts.readAll()
        ui_object.setStyleSheet(stylesheet)
        
        
    
def clear_layout(self_obj, layout):
    self_obj.qt_object = layout
    for i in reversed(range(self_obj.qt_object.count())):
        item = layout.takeAt(0)
        if item:
            w = item.widget()
        if w:
            #self.clear_layout(w.layout())
            w.setParent(None)
            w.deleteLater()