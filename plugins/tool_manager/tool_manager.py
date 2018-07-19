import inspect
import pprint
import sys
import os
import Framework
from Framework.lib import ui
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.ui.widgets import common_widgets
from Framework.lib.config.config import Config
from Framework import get_environ_file, get_css_path, get_icon_path
from Framework.plugins import tool_manager
from Framework.lib.file import utils as file_utils
from Framework.lib.ui.ui import getMayaWindow

config = Config.instance()
CSS_PATH = get_css_path()
ICON_PATH = get_icon_path()

class ToolManager(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super(ToolManager,self).__init__(parent=parent)
        ui.apply_resource_style(self)
        self.setObjectName("tool_manager")
        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("BM2 Tool Manager")

        # Allows maximize and minimize
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.mainWiget = ToolManagerMainWidget(parent=self)

        self.layout().addWidget(self.mainWiget)
        self.layout().setContentsMargins(2, 2, 2, 2)
        
        self.show()

class ToolManagerMainWidget(QtWidgets.QWidget):

    def __init__(self,parent = None):
        super(ToolManagerMainWidget, self).__init__()
        self._config = config
        self._tools = []
        self._scripts = []
        self._waiting_refresh = False
        self.initUI()

    @property
    def current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    @property
    def current_folder(self):
        return os.path.dirname(self.current_file)

    def initUI(self):
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "ui", "tool_manager.ui"), self)
        ui.apply_resource_style(self)

        # Significant controls
        self.tm_paint_timer = QtCore.QTimer()
        self.tm_paint_timer.setSingleShot(True)
        self.tm_paint_timer.setInterval(1000)

        self.filter_widget = common_widgets.FilterWidget(parent=self)
 
        self.filter_widget_image = QtGui.QIcon(os.path.join(ICON_PATH,"search.png"))
        self.filter_widget.pb_filter.setIcon(self.filter_widget_image)
        self.filter_layout.addWidget(self.filter_widget)

        
        self._tools = None

        # Signals
        self.refresh_btn.clicked.connect(self.schedule_refresh)
        self.filter_widget.pb_filter.clicked.connect(self.schedule_refresh)
        self.filter_widget.add_custom_filters(['tool','script'])
        self.tools_btn.clicked.connect(self.on_pb_filter_tools_clicked)
        self.scripts_btn.clicked.connect(self.on_pb_filter_scripts_clicked)
        self.refresh_btn.setIcon(QtGui.QIcon(os.path.join(ICON_PATH,"essential","repeat.png")))

        self.tm_paint_timer.timeout.connect(self.fill_tools_list)


        # Compile tools and scripts info
        self.schedule_refresh()
        self.filter_widget.setParent(self)
        
        self.show()

    def on_pb_filter_tools_clicked(self):
        self.filter_widget.clear_custom_filters()
        self.filter_widget.add_custom_filters('tool')
        self.filter_widget.filter()
    
    def on_pb_filter_scripts_clicked(self):
        self.filter_widget.clear_custom_filters()
        self.filter_widget.add_custom_filters('script')
        self.filter_widget.filter()
        
    def schedule_refresh(self):
        self.clear_tools()
        self.tm_paint_timer.stop()
        self.tm_paint_timer.start()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    '''
        to be run only once at the beginning with a delay
    '''

    def fill_tools_list(self):

        ext_tools = tool_manager.get_ext_tools()
        int_tools = tool_manager.get_internal_tools()
        
        
        self._tools = ext_tools + int_tools
        for tool in self._tools:
            tool_widget = ToolManagerToolWidget(self,tool)
            self.vl_tools_list.addWidget(tool_widget)
        
        self.filter_widget.filter()
        
        QtWidgets.QApplication.restoreOverrideCursor()

    def clear_tools(self):
        self.filter_widget.clear_filter_widget(clear_custom_filters=False)
        ui.clear_layout(self, self.vl_tools_list)
        '''
        for i in reversed(range(self.vl_tools_list.count())):
            item = self.vl_tools_list.takeAt(0)
            if item:
                w = item.widget()
                if w:
                    w.setParent(None)
                    w.deleteLater()
        '''

class ToolManagerToolWidget(common_widgets.FilterableWidget, QtWidgets.QWidget):
    def __init__(self, parent, tool):
        super(ToolManagerToolWidget, self).__init__(parent)

        self._config = config
        self._tool = tool
        self._tool_instance = None
        self.initUI()
        
    def filtering_behaviour(self, filters):
        
        keep = False
            
        for filter in filters:
            if (filter in self._tool["code"] or filter in self._tool["category"] or filter in self._tool["name"]):
                keep = True
                break
            
        return keep
        
    @property
    def current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    @property
    def current_folder(self):
        return os.path.dirname(self.current_file)

    def initUI(self):
        # Load UI file
        current_file = self.current_file
        current_folder = self.current_folder
        gui_loader.loadUiWidget(os.path.join(os.path.dirname(__file__), "ui", "tool_manager_tool.ui"), self)
        # Significant controls
        self.pb_run = gui_loader.get_child(self, "pb_run")

        # Signals
        self.pb_run.clicked.connect(self.run)

        self.fill_tool_info()
        
        self.show()

    def fill_tool_info(self):
        self.lbl_icon = gui_loader.get_child(self, "lbl_icon")
        self.lbl_category = gui_loader.get_child(self, "lbl_category")
        self.lbl_name = gui_loader.get_child(self, "lbl_name")

        self.lbl_category.setText(self._tool["category"])
        self.lbl_name.setText(self._tool["name"])

        self.lbl_icon_image =QtGui.QPixmap(file_utils.get_image_file(self._tool["icon"], self._tool["path"]))
        self.lbl_icon.setPixmap(self.lbl_icon_image)

    def run(self):
        
      
        self.tool = self._tool["definition"]()
        maya_window = getMayaWindow()
        self._tool_instance = gui_loader.get_default_container(self.tool, self._tool["name"], parent=maya_window)
        self._tool_instance.setWindowFlags(QtCore.Qt.Window)
        ui.apply_resource_style(self._tool_instance)
        self.move_tool_to_cursor_position(self._tool_instance)
        self._tool_instance.show()

        

    def move_tool_to_cursor_position(self, tool_instance):
        cursor_pos = QtGui.QCursor.pos()
        tool_instance_frame_geometry = tool_instance.frameGeometry()
        
        def fit_tool_inside_screen(tool_widget, screen_widget = None):
            X_OFFSET = 40
            Y_OFFSET = 60
            if not screen_widget:
                screen_widget = QtWidgets.QDesktopWidget()
                
                (desktop_width, desktop_height) = screen_widget.width(), screen_widget.height()
        
            right_limit = cursor_pos.x() + tool_widget.width()/2
            left_limit = cursor_pos.x() - tool_widget.width()/2
            
            tool_center_x = cursor_pos.x()
            tool_center_y = cursor_pos.y()
            if right_limit > desktop_width:
                tool_center_x = desktop_width - tool_widget.width()/2 - X_OFFSET
            elif left_limit < 0:
                tool_center_x = tool_widget.width()/2 + X_OFFSET
                
            upper_limit = cursor_pos.y() - tool_widget.height()/2
            bottom_limit = cursor_pos.y() + tool_widget.height()/2
            
            if upper_limit < 0:
                tool_center_y = tool_widget.height()/2 + Y_OFFSET
            elif bottom_limit > desktop_height:
                tool_center_y = desktop_height - tool_widget.height()/2 - Y_OFFSET
                 
            return QtCore.QPoint(tool_center_x, tool_center_y)
         
        tool_pos = fit_tool_inside_screen(tool_instance_frame_geometry)
        tool_instance_frame_geometry.moveCenter(tool_pos)

        tool_instance.setGeometry(tool_instance_frame_geometry)
            
def run(tab_position=False):
    import os
    app = QtWidgets.QApplication(sys.argv)
#     from Framework.lib.ui.ui import getMayaWindow
#     maya_window = getMayaWindow()
    obj = gui_loader.get_default_container(ToolManager(), "Update All", parent=None)
    obj.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
    
    
    