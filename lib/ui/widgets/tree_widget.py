"""
Module to manage tree widgets faster.

author: [miguel.molledo@summus.es]

"""

import sys 
import pprint

from cmn.cmn.python.lib.ui.QT import QtWidgets, QtCore, Qt

def tree_widget(headers, elements=[], tree=None,  elements_checked = 0, children_checked = 0):
    """
    Method to fill a tree widget or create a new one with the headers and elements defined
    
    Args:
        tree (None, optional): QtWidget.QTreeWidget If its passed as argument it uses the parameter
        if its not create a new tree widget and return it at the end of the method 
        headers (list, str): with this flag creates the header/s with a string one header with a list 'N' headers
        elements (list, dict):
            list: it works with a list of elements or a list of lists do not support list or strings shuffled'
            In this case the order matters to insert them.
                Example:
                    [['Element1','Element2','Element3'],['Element1','Element2','Element3']]
                    or 
                    ['Element1','Element2','Element3']
            dict: It works having as a key argument the name of the columns where it inserts the data and within the corresponding data.
                example:
                    {
                        "ColumnName-1": ['Element1','Element2','Element3'],
                        or/and
                        "ColumnName-2": {
                                        "Element_02" : ["elemenet01","elemenet01","elemenet01","elemenet01"]
                                        }
                    }
        elements_checked (bool, optional): It generates a check box for each main element on the state defined (0,1,2)
        children_checked (int, optional): It generates a check box for each sub element on the state defined (0,1,2)
    
    Returns:
        TYPE: Description
    
    Raises:
        Exception: Description
    """
    # Check tree type

    if isinstance(tree, QtWidgets.QTreeWidget):
        tree = tree
    else:
        tree = QtWidgets.QTreeWidget()

        # Check Header Type
    if isinstance(headers, str):
        tree.setColumnCount(1)
        tree.setHeaderLabels(headers)
    elif isinstance(headers, list):
        tree.setColumnCount(len(headers))
        tree.setHeaderLabels(headers)
    else:
        raise Exception("Not supported type for headers try using Str or list")


    # Check element type
    # To work with lists
    if isinstance(elements, list):
        for column in range(0,len(headers)):
            element = elements[column]
            if isinstance(element, list):
                for row, element_child in enumerate(element):
                    tree_item = tree.topLevelItem(row)
                    if not tree_item:
                        tree_item = QtWidgets.QTreeWidgetItem(tree)
                    tree_item.setText(column, element_child)
                    if elements_checked:
                        tree_item.setCheckState(column, get_qt_check_state(elements_checked))
                    tree.addTopLevelItem(tree_item)

            elif (isinstance(element, str) or isinstance(element, unicode)):
                tree_item = QtWidgets.QTreeWidgetItem(tree)
                tree_item.setText(0, element)
                tree.addTopLevelItem(tree_item)
    # To work with Dictionary
    elif isinstance(elements, dict):

        for key,values in elements.iteritems():
            if not key in headers: continue
            column = headers.index(key)
            if isinstance(values,list):
                for row,key_c in enumerate(values):
                    tree_item = tree.topLevelItem(row)
                    if not tree_item:
                        tree_item = QtWidgets.QTreeWidgetItem(tree)
                    tree_item.setText(column, key_c)
                    if elements_checked:
                        tree_item.setCheckState(column, get_qt_check_state(elements_checked))
                    tree.addTopLevelItem(tree_item)
            elif isinstance(values,dict):
                row = 0
                for key_c, values_c in values.iteritems():
                    tree_item = tree.topLevelItem(row)
                    if not tree_item:
                        tree_item = QtWidgets.QTreeWidgetItem(tree)
                    tree_item.setText(column,key_c)
                    if elements_checked:
                        tree_item.setCheckState(column, get_qt_check_state(elements_checked))
                    if isinstance(values_c,list):
                        for row_c,child in enumerate(values_c):
                            child_item = tree_item.child(row_c)
                            if not child_item:
                                child_item = QtWidgets.QTreeWidgetItem(tree_item)
                            child_item.setText(column,child)

                            if children_checked:
                                child_item.setCheckState(column,get_qt_check_state(children_checked))
                            tree_item.addChild(child_item)
                    tree.addTopLevelItem(tree_item)
                    row+=1
    return tree


def get_qt_check_state(state):
    if state == 0:
        return QtCore.Qt.Unchecked
    elif state == 1:
        return QtCore.Qt.PartiallyChecked
    elif state == 2:
        return QtCore.Qt.Checked


def get_elements_checked(tree):
    """
    Check every element of the tree and returns within a dictionary
    
    Args:
        tree (QtWidgets.QTreewidget): Widget to check the state of their elements
    
    Returns:
        dict: dictionary with the keys of the elements 
    
    Raises:
        Exception: Description
    """
    column_count = tree.columnCount()
    if not column_count > 0 :
        raise Exception ("Not enough columns on this tree ")
    aux_dict = {}
    row_count = tree.topLevelItemCount()
    for column in range(0, column_count):
        name_column = tree.headerItem().text(column)
        aux_dict[name_column] = {}
        for row in range(0,row_count):
            item_widget = tree.topLevelItem(row)
            aux_dict[name_column][item_widget.text(column)] = {}
            aux_dict[name_column][item_widget.text(column)]['CheckState'] = item_widget.checkState(column)
            children_count = item_widget.childCount()
            if not children_count:
                continue
            aux_dict[name_column][item_widget.text(column)]['Children'] = {}

            for child_row in range(0,children_count):
                child_item = item_widget.child(child_row)
                child_text = child_item.text(column)
                child_state = child_item.checkState(column)
                aux_dict[name_column][item_widget.text(column)]['Children'][child_text] = child_state
    return aux_dict

def set_color_by_state(tree,color_dict = dict):
    """
    Set the colors of the elements depending of the state
    it uses a method which accepts as argument another method to be
    executed once fine a checkbox
    
    Args:
        tree (QtWidgets.QTreeWidget): A tree to check the states and colorize them 
        color_dict (dict, optional): a dictionary to change the color type. it only accepts
        a base color
            example:
                color_dict = {0:'gray',1:'yellow',2:'blue'} 
    
    Returns:
        TYPE: Description
    """
    def colorize(tree_item, column, state):
        """Summary
        
        Args:
            tree_item (QtWidgets.QTreeWidget): Description
            column (int): Description
            state (0,1,2): 
                0: unchecked
                1: middlechecked
                2: checked
        
        Returns:
            TYPE: Description
        """
        if state == 0:
            if color_dict:
                color = color_dict[0]
            else:
                color = 'red'
        elif state == 1:
            if color_dict:
                color = color_dict[1]
            else:
                color = 'blue'
        else:
            if color_dict:
                color = color_dict[2]
            else:
                color = 'green'
        set_color_tree_item(tree_item,column, color)
    on_check_state_execute(tree,colorize)



def set_color_tree_item(item,column,color):
    """
    Asign color into the item
    
    Args:
        item (QtWidgets.QTreewidgetItem): Qt Item to colorize
        column (int): Description
        color (str): one of the colors supported 

    Returns:
        bool: True
    
    Raises:
        Exception: Description
    """
    colors = ['red','blue','black','green','gray','yellow','white','red' ]
    if not color.lower() in colors:
        raise Exception('Color not supported')
    if not isinstance(item, QtWidgets.QTreeWidgetItem):
        raise Exception("Item type not supported try with a QTreeWidgetItem")
    eval('item.setForeground(column,QtCore.Qt.%s)' % color.lower())
    return True

def on_check_state_execute(tree,method):
    """
    This method finds a checkbox item and execute the method then.
    Always this method its called with the next parameteres
        method(QTreewidgetItem, column, state = 0,1,2)
    
    Args:
        tree (qtreeWidgetItem): Qt Item
        method (function): Method to call once it have found a check
    
    Returns:
        TYPE: Description
    
    Raises:
        Exception: Not enough columns
    """
    column_count = tree.columnCount()
    if not column_count > 0 :
        raise Exception ("Not enough columns on this tree ")
    row_count = tree.topLevelItemCount()
    for column in range(0, column_count):
        for row in range(0,row_count):
            item_widget = tree.topLevelItem(row)
            if item_widget.checkState(column):
                method(item_widget,column,item_widget.checkState(column))
            children_count = item_widget.childCount()
            if not children_count:
                continue
            for child_row in range(0,children_count):
                child_item = item_widget.child(child_row)
                method(child_item, column, child_item.checkState(column))

# # ---------------------------------------------
# # Example1
# app = QtWidgets.QApplication(sys.argv)

# column1 = ['element.1.1', 'element.1.2', 'element.1.3']
# column2 = ['element.2.1', 'element.2.2', 'element.2.3']
# column3 = ['element.3.1', 'element.3.2', 'element.3.3']
# column4 = ['element.4.1', 'element.4.2', 'element.4.3']
# headers = ['People', 'Guys', 'Penis']


# data = [column1,column2, column3, column4]

# my_tree = tree_widget(headers=headers, elements=data, elements_checked=1)

# my_tree.show()
# app.exec_()


# ---------------------------------------------
# # Example 2
# # #Working with list of list or a simple list always computes the quantity of rows related with the header count
# app = QtWidgets.QApplication(sys.argv)

# column1 = ['element.1.1', 'element.1.2', 'element.1.3']
# column2 = ['element.2.1', 'element.2.2', 'element.2.3']
# column3 = ['element.3.1', 'element.3.2', 'element.3.3']
# column4 = ['element.4.1', 'element.4.2', 'element.4.3']
# headers = ['People', 'Guys', 'Penis']
# prefix = ['A','B','C','D','E','F']
# data = {}
# data['Guys'] = {}
# data['Guys'] = column1
# data['People'] = {}
# for x in column2:
#     data['People'][x] = [x+i for i in prefix]
# data['Penis'] = {}

# for x in column2:
#     data['Penis'][x] = [x+i for i in prefix]
# my_tree = tree_widget(headers=headers, elements=data, children_checked=1)
# checkes_options = get_elements_checked(my_tree)
# import os
# file = r"C:\Users\mmolledo\Downloads\test_01\UI\stylesheet.css"
# with open(os.path.normpath(file)) as file:
#     my_tree.setStyleSheet(file.read())

# my_tree.show()
# app.exec_()
# my_tree.show()

# TEMPLATE UIS
# from cmn.cmn.python.lib.ui import ui_loader
# print dir(ui_loader)
# container = ui_loader.get_maya_container(my_tree, name = "Example Name Tree Tool")
# container.show()

# app.exec_()
# # # # ---------------------------------------------
# # # Example 3
# app = QtWidgets.QApplication(sys.argv)

# headers= ['LOGG']
# data = {}
# data['LOGG'] = {
#                         "SEQ.0001":['Checkout','Publish','CheckIn'],
#                         "SEQ.0950":['Checkout','Publish','CheckIn']
# }
# color_dict = {0:'gray',1:'yellow',2:'blue',}
# my_tree = tree_widget(headers=headers, elements=data, elements_checked=1, children_checked=0)
# set_color_by_state(my_tree,color_dict)

# my_tree.show()
# app.exec_()

