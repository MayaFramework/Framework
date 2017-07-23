"""
Module to manage tree widgets faster.

author: miguel.molledo

"""

import sys 
import os
import pprint

from Framework.lib.ui.qt.QT import QtGui, QtWidgets, QtCore
from Framework import get_icon_path
ICO_PATH = get_icon_path()

def tree_widget(headers, elements=[], tree=None,  elements_checked = 0, children_checked = 0):
    """
    NOTE: 
    KIND OF DEPRECATED BETTER USE FILL_TREE
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



def fill_tree(tree, data, headers):
    tree.setColumnCount(len(headers))
    tree.setHeaderLabels(headers)
    recursive_advance_tree(tree, data)

def recursive_tree(tree, data):
    '''
    Works for one header and with this kind of dictionaries
        data_example = [
        {"value":"rig",
         "checked":1,
         "children":[
             {"value":"geo",
              "checked":2,
              "children":[]
              },
             {"value":"expr",
              "checked":2,
              "children":[]
              }
             ]
         },
        {"value":"controller",
         "checked":1,
         "children":[
             {"value":"bones",
              "checked":2,
              "children":[]
              },
             {"value":"references",
              "checked":2,
              "children":[]
              }
             ]
         }
        ]
    '''
#     row = len(data.keys())
    column = 0
    for row, value_info in enumerate(data):
        tree_item = QtWidgets.QTreeWidgetItem(tree)
#         tree_item = tree.topLevelItem(row)
        tree_item.setText(0,value_info["value"])
        if "checked" in value_info:
            tree_item.setCheckState(column, get_qt_check_state(value_info["checked"]))
        if "children" in value_info:
            if isinstance(value_info["children"],list) and value_info["children"]:
                recursive_tree(tree_item, value_info["children"])
        if isinstance(tree, QtWidgets.QTreeWidget):
            tree.addTopLevelItem(tree_item)
        elif isinstance(tree, QtWidgets.QTreeWidgetItem):
            tree.addChild(tree_item)
    return tree


def recursive_advance_tree(tree, data):
    '''
        {"value":{
            0:{"checked": None,
               "icon": spackage_ico_path,
               "value":"RIG"},
            1:{"checked": 2,
               "icon": download_ico_path,
               "text":"Load msg"},

            2:{"checked": 2,
               "icon": update_ico_path,
               "text":"text message"},

            3:{"checked": 2,
               "icon": upload_ico_path,
               "text":"text message"}
            },
    '''
#     row = len(data.keys())
    for row, value_info in enumerate(data):
        tree_item = QtWidgets.QTreeWidgetItem(tree)
#         tree_item = tree.topLevelItem(row)
        if isinstance(value_info["value"], str):
            tree_item.setText(0,value_info["value"])
        elif isinstance(value_info["value"], dict):
            for column, column_info in value_info["value"].iteritems():
                # Set text
                if "text" in column_info:
                    tree_item.setText(column, column_info["text"])
                # Set check box if exists
                if "checked" in column_info:
                    if isinstance(column_info["checked"], int):
                        tree_item.setCheckState(column, get_qt_check_state(column_info["checked"]))
                # Set icon
                if "icon" in column_info:
                    if os.path.exists(column_info["icon"]):
                        tree_item.setIcon(column, (QtGui.QIcon(column_info["icon"])))
            if "children" in value_info:
                if isinstance(value_info["children"],list) and value_info["children"]:
                    recursive_advance_tree(tree_item, value_info["children"])
        tree_item.setExpanded(True)
        if isinstance(tree, QtWidgets.QTreeWidget):
            tree.addTopLevelItem(tree_item)
        elif isinstance(tree, QtWidgets.QTreeWidgetItem):
            tree.addChild(tree_item)
    return tree

# def get_number_state_from_qt_state



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
    Assign color into the item

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



if __name__ == "__main__":
    download_ico_path =  os.path.join(ICO_PATH,"downloading.png")
    upload_ico_path = os.path.join(ICO_PATH, "warning.png")
    update_ico_path = os.path.join(ICO_PATH, "miguel.png")
    component_ico_path = os.path.join(ICO_PATH, "question.png")
    spackage_ico_path = os.path.join(ICO_PATH, "question.png")
    app = QtWidgets.QApplication(sys.argv)
    data_example = [
        {"value":{
            0:{"checked": None,
               "icon": spackage_ico_path,
               "text":"RIG"},
            1:{"checked": 2,
               "icon": download_ico_path,
               "text":"Load msg"},

            2:{"checked": 2,
               "icon": update_ico_path,
               "text":"text message"},

            3:{"checked": 2,
               "icon": upload_ico_path,
               "text":"text message"}
            },
#          "checked":1,
         "children":[
             {"value":{
                0:{"checked": None,
                   "icon": spackage_ico_path,
                   "text":"MDL"},
                1:{"checked": 2,
                   "icon": download_ico_path,
                   "text":"Load msg"},
    
                2:{"checked": 2,
                   "icon": update_ico_path,
                   "text":"Update msg"},
    
                3:{"checked": None,
                   "icon": upload_ico_path,
                   "text":"Publish msg"}
                },
            "children":[
                    {"value":{
                        0:{"checked": None,
                           "icon": component_ico_path,
                           "text":"GEO"},
                        1:{"checked": 2,
                           "icon": download_ico_path,
                           "text":"Load msg"},
            
                        2:{"checked": 2,
                           "icon": update_ico_path,
                           "text":"Update msg"},
            
                        3:{"checked": None,
                           "icon": upload_ico_path,
                           "text":"Publish msg"}
                                      }}
                ]
              },
             {"value":{
                0:{"checked": None,
                   "icon": spackage_ico_path,
                   "text":"SHD"},
                1:{"checked": 2,
                   "icon": download_ico_path,
                   "text":"Load msg"},
    
                2:{"checked": 2,
                   "icon": update_ico_path,
                   "text":"Update msg"},
    
                3:{"checked": None,
                   "icon": upload_ico_path,
                   "text":"Publish msg"}
                },
            "children":[{"value":{
                        0:{"checked": None,
                           "icon": component_ico_path,
                           "text":"EXPRESSIONS"},
                        1:{"checked": 2,
                           "icon": download_ico_path,
                           "text":"Load msg"},

                        2:{"checked": 2,
                           "icon": update_ico_path,
                           "text":"Update msg"},
            
                        3:{"checked": None,
                           "icon": upload_ico_path,
                           "text":"Publish msg"}
                        },
                    "children":[
                        
                            ]
              }
                
                ]
              },
                     ]
            }]
    tree = QtWidgets.QTreeWidget()
    fill_tree(tree, data_example, headers=["Inspection", "Load", "Update", "Publish"])
    print get_elements_checked(tree)
    tree.show()
    app.exec_()
