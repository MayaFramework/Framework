
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
#     DependencyLoaderWidget().show()
#     app.exec_()
    tool = DependencyLoaderWidget()
    obj = gui_loader.get_default_container(tool, "Update All")
    obj.show()
    app.exec_()

    """
    P:bm2/seq/dip/sho/010/animation/wip/bm2_shoani_seq_dip_sho_010_animation_default_scene_wip0001.ma
    #problemas abc
    P:/bm2/seq/wtf/sho/030/layout/out/bm2_seqsho_seq_wtf_sho_030_layout_default_scene_out.ma
    
    # Problema   fur
    OUT 
    WORK/BM2/seq/dip/sho/020/lighting/out/bm2_seqsho_seq_dip_sho_020_lighting_scenery_none_out.ma
    WIP
    WORK/BM2/seq/dip/sho/020/lighting/wip/bm2_seqsho_seq_dip_sho_020_lighting_scenery_none_wip.0005.ma
    
    """
    
    
    #P:/bm2/chr/gato/cfx/thingHigh/groom/mps
    #P:/bm2/seq/wtf/sho/040/hair/mps
    
    #