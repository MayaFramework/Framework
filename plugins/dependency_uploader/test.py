
if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader
    from uploader_window import UploaderWindow
#     app = QtWidgets.QApplication(sys.argv)
#     file_path = r"P:\BM2\loc\salaTelefonos\scn\main\main\wip\bm2_locscn_loc_salaTelefonos_scn_main_main_default_none_wip0020.ma"
#     widget = UploaderWindow(file_path)
#     obj = gui_loader.get_default_container(widget, "UPLOADER")
#     obj.show()
#     widget.execute_analize_process()
#     app.exec_()



    from Framework.plugins.dependency_loader.downloader import Downloader, DownloaderResponse
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui

    
    download_finished = False
    def on_download_finished():
       download_finished  = True
       print download_finished, "TERMINA JODER "


    
    downloader = Downloader()
    file_list = []
    file_list.append("P:/BM2/seq/des/sho/020/animation/out/bm2_shopre_seq_des_sho_020_animation_previscardboard2_alembic_out.abc")
    downloader.set_files_to_process(file_list)
    downloader.set_maxium_threads(10)
    downloader.on_finish_download.connect(on_download_finished, QtCore.Qt.QueuedConnection)
    downloader.start_download_process()
    
    import time
    while download_finished  == False:
        time.sleep(0.5)
        print "Downloading...."
        if download_finished:
            break
    download_finished  = False
