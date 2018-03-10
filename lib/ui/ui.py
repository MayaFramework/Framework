'''
Created on Mar 10, 2018

@author: miguel.molledo.alvarez@gmail.com
'''

from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
def getMayaWindow():
   for w in QtWidgets.QApplication.topLevelWidgets():
       if w.objectName() == 'MayaWindow':
           return w