import pip
import subprocess
print "DOWNLOADING FROM PIP"
# Installing Pyside
import sys
#%USERPROFILE%\AppData\Local\Microsoft\WindowsApps

MAIN_CODE_ROUT = "P://TOOLS/"
INTERAL_GIT= "https://github.com/MayaFramework/Framework.git"
INTERNAL_LOCAL_ROUT = "{main_rout}/Framework".format(main_rout=MAIN_CODE_ROUT)
INTERNAL_BRANCH = "bm2_production"

EXTERNAL_BM2_GIT= "https://github.com/MiguelMolledo/BM2Public.git"
EXTERNAL_BM2_LOCAL_ROUT = "{main_rout}/BM2Public".format(main_rout=MAIN_CODE_ROUT)
EXTERNAL_BRANCH = "bm2_external_pro"

EXTRAPACKAGES = {
    "shotgun": "git+git://github.com/shotgunsoftware/python-api.git"
}

PACKAGES = ['pyside', 'six', 'dropbox', 'requests',
            'urllib3', 'GitPython', EXTRAPACKAGES["shotgun"]]


subprocess.call('setx PYTHONPATH "P:\TOOLS;C:\Python27\Lib\site-packages"')
subprocess.call('setx Path "%USERPROFILE%\AppData\Local\Microsoft\WindowsApps;C:\Python27;C:\Python27\Scripts;"')

for package in PACKAGES:
    args = ["install", package]
    msg = "INSTALLING {}".format(package)
    if package in sys.modules:
        msg = "UPDATING {}".format(package)
        args.append("-U")
    print msg, args
    pip.main(args)


# Set environ file 
import os
import shutil
import getpass

python_dir = r"C:\Python27\Lib\site-packages"
file = "environ.pth"

userSetup_path = "C:/Users/{}/Documents/maya/2017/scripts".format(getpass.getuser())
path_to_add = [MAIN_CODE_ROUT, "P:/Deployment",INTERNAL_LOCAL_ROUT, EXTERNAL_BM2_LOCAL_ROUT, userSetup_path]
current_folder = os.path.dirname(__file__)
for c_path in path_to_add:
    try:
        os.makedirs(c_path)
    except Exception as e:
        pass
with open(os.path.join(python_dir,file), "w") as f:
    for c_path in path_to_add:
        f.write(c_path+"\n")

# userSetup_path = os.path.join(os.environ["MAYA_APP_DIR"], "2017", "scripts").replace("\\","/")
# shutil.copy2(os.path.join(current_folder,"userSetup.py"), userSetup_path)



#Update or Clone


sys.path.append(r"C:/Python27/Lib/site-packages")
sys.path.append(MAIN_CODE_ROUT)

os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = os.path.join(current_folder, "Git/bin/git.exe")
os.environ['GIT_SSL_NO_VERIFY'] = "1"

import git


def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def clone_repo(git_url, repo_dir, branch="master"):
    try:
        git.Repo.clone_from(git_url, repo_dir, branch=branch)
        return True
    except:
        return False


def pull_latest_changes(repo_dir):
    repo = git.Repo(repo_dir)
    repo.git.stash('save')
    o = repo.remotes.origin
    o.pull()
    return True




def load_repo(git_url, local_path, branch):
    result = None
    if not is_git_repo(local_path):
        print "Cloning project: {project}... wait a few minutes".format(project=local_path)
        result = clone_repo(git_url, local_path, branch=branch)
        if result:
            print "Finished Update process"
    else:
        print "Project exists in  {project}, pulling changes... wait a few minutes".format(project=local_path)
        result = pull_latest_changes(local_path)
        if result:
            print "Finished Update process"
    
     
load_repo(git_url=INTERAL_GIT,
          local_path=INTERNAL_LOCAL_ROUT,
          branch=INTERNAL_BRANCH)
     
load_repo(git_url=EXTERNAL_BM2_GIT,
          local_path=EXTERNAL_BM2_LOCAL_ROUT,
          branch=EXTERNAL_BRANCH)

#Copy Bats
bats_to_copy = ["Downloader.bat", "Uploader.bat", "FileExplorer.bat"]
target_copy = os.path.join(MAIN_CODE_ROUT)
for bat in bats_to_copy:
    shutil.copy2(os.path.join(current_folder, bat), target_copy)

    
