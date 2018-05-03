
"""
:author: Miguel Molledo Alvarez
:email: miguel.molledo.alvarez@gmail.com
"""
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from dependency_loader_window import DependencyLoaderWidget
    from Framework.lib.gui_loader import gui_loader
    app = QtWidgets.QApplication(sys.argv)
    file_path = r"P:\BM2\loc\salaTelefonos\scn\main\main\wip\bm2_locscn_loc_salaTelefonos_scn_main_main_default_none_wip0020.ma"
    tool = DependencyLoaderWidget(file_path)


    
    
    tool = DependencyLoaderWidget(file_path)
    # TEST 1: Download just main file
#     tool.download_dependencies=False
#     tool.download_main_file = True
#     tool.download_content_from_filtered_folders = False
#     tool.overwrite_local_files = True
# #     
#     # TEST 2: Download dependencies and not the main file 
#     tool.download_dependencies=True
#     tool.download_main_file = False
#     tool.download_content_from_filtered_folders = True
#     tool.overwrite_local_files = True
# 
# #     
#     # TEST 3: Download dependencies and everything
#     tool.download_dependencies=True
#     tool.download_main_file = True
#     tool.download_content_from_filtered_folders = True
#     tool.overwrite_local_files = True
# 
#     
#     # TEST 4: Unatended process
#     #with or without asking to create folders
#     tool.state_unatended_create_folder_process = True
#     
#     # with popup once its finished
#     
#     tool.state_popup_widget_on_finish = True


    
    obj = gui_loader.get_default_container(tool, "Update All")
    obj.show()
#     tool.execute_update_process()

#     #TEST 4: Download extra files
    extra_files = [file_path, r"P:\BM2\loc\salaTelefonos\scn\main\main\wip\bm2_locscn_loc_salaTelefonos_scn_main_main_default_none_wip100.ma"]
    tool.execute_update_process(extra_files)
    app.exec_()
    
    