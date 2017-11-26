import pip
print "DOWNLOADING FROM PIP"
# Installing Pyside
package_name='pyside'
pip.main(['install', package_name])
# 
package_name='six'
pip.main(['install', package_name])
# 

package_name='dropbox'
pip.main(['install', package_name, "-U"])
# 
package_name='requests'
pip.main(['install', package_name])
# 
package_name='urllib3'
pip.main(['install', package_name])
# 




# Set environ file 
import os
python_dir = r"C:\Python27\Lib\site-packages"
file = "environ.pth"
path_to_add = [r"P:/TOOLS"]
try:
    os.makedirs("P:/TOOLS/")
except:
    pass
with open(os.path.join(python_dir,file), "w") as f:
    for path in path_to_add:
        f.write(path)

import time
import os
import dropbox
import time
import threading
class updater(object):
    def __init__(self):
        self._thread_count = 0
        self.update()

    def update(self):
        token = "5e9ZZ9cN4roAAAAAAAACdfeZo9IR2Bs2HbA-9AFgcwFYd0d7Iur5gY9So6Z5Rw_i"
        self.dpx_d = dropbox.dropbox.Dropbox(token)
        result =  self.dpx_d.files_list_folder("/TOOLS/", recursive=True)
        for x in result.entries:
            splited = x.path_display.rsplit(".",1)
            if len(splited) >1:
                if self.is_available_thread(60*60):
                    self._thread_count += 1
                    t = threading.Thread(target = self.execute_download, args=(x.path_display,))
                    t.start()



    def execute_download(self,file):
        folder = file.rsplit("/", 1)[0]
        try:
            print "CREANDO FOLDER: %s"%folder
            os.makedirs("P:/"+folder)
        except Exception as e:
            print "Warning: %s" % e
        try:
            print "Downloading: %s"%file
            self.dpx_d.files_download_to_file("P:/"+file,file)
            print "Downloading FINISHED"
        except Exception as e:
            print e
            print "Something was wrong with: %s"%file
        finally:
            self._thread_count -=1

    def is_available_thread(self,timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if self._thread_count <= 20:
                return True
            time.sleep(period)
        return False


print "Downloading Framework "
updater()
