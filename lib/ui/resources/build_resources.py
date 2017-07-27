"""
@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com
"""
import inspect
import os
from subprocess import check_output

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def build_res(res_path, res_name):
    print "Building Resource: %s" % res_name
    out = check_output(
        [
            "C:/Python27/Lib/site-packages/PySide/pyside-rcc",
            r"%s/%s.qrc" % (res_path, res_name)
        ]
    )

    amended_out = out.replace("from PySide import", "from Framework.lib.ui.qt.QT import")

    resources_file = os.path.abspath(os.path.join(get_current_folder(), "resources_rc.py"))
    print resources_file
    with open(resources_file, "w") as f:
        f.write(amended_out)


if __name__ == "__main__":
    sources_path = get_current_folder()
    build_res(sources_path, 'style')
