import pip
print "DOWNLOADING FROM PIP"
# Installing Pyside
import sys

PRODUCTION_REPO = "https://github.com/MayaFramework/Framework.git"
REPO_DIR = "P:/TOOLS/Framework"

PACKAGES = ['pyside', 'six', 'dropbox', 'requests', 'urllib3', 'GitPython']

for package in PACKAGES:
    args = ["install", package]
    msg = "INSTALLING {}".format(package)
    if package in sys.modules:
        msg = "UPDATING {}".format(package)
        args.append("-U")
    print msg
    pip.main(args)


# Set environ file 
import os
import shutil
import getpass

python_dir = r"C:\Python27\Lib\site-packages"
file = "environ.pth"
path_to_add = [r"P:/TOOLS/", "P:/Deployment"]
try:
    for path in path_to_add:
        os.makedirs(path)
except:
    pass
with open(os.path.join(python_dir,file), "w") as f:
    for path in path_to_add:
        f.write(path+"\n")

userSetup_path = "C:/Users/{}/Documents/maya/2017/scripts".format(getpass.getuser())

current_folder = os.path.dirname(__file__)

# userSetup_path = os.path.join(os.environ["MAYA_APP_DIR"], "2017", "scripts").replace("\\","/")
shutil.copy2("P:/Deployment/userSetup.py", userSetup_path)



#Update or Clone

import git
sys.path.append(r"C:/Python27/Lib/site-packages")
sys.path.append(r"P:/TOOLS")

os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "P:/Deployment/Git/bin/git.exe"
os.environ['GIT_SSL_NO_VERIFY'] = "1"




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
    o = repo.remotes.origin
    o.pull()


if not is_git_repo(REPO_DIR):
    clone_repo(PRODUCTION_REPO, REPO_DIR, branch="bm2_production")
else:
    pull_latest_changes(REPO_DIR)
    
    
    
    
#Copy Bats
bats_to_copy = ["Downloader.bat", "Uploader.bat"]
target_copy = os.path.join(REPO_DIR, "..")
for bat in bats_to_copy:
    shutil.copy2(os.path.join(current_folder, "resources", bat), target_copy)

    