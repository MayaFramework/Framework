import sys
import os
import git

sys.path.append(r"C:/Python27/Lib/site-packages")
sys.path.append(r"P:/TOOLS")

# initialize playblaster
import maya.cmds as cmds
import Framework.plugins.playblaster.playblasterUI as playblasterUI
import Framework.plugins.playblaster.playblasterUI as check
import Framework.plugins.playblaster.playblasterUI as playblasterAnimUtils

cmds.evalDeferred('playblasterValues=check.checkWindowAtStartMaya()',lowestPriority=True)

# end playblaster


# start aTools

if not cmds.about(batch=True):

    # launch aTools_Animation_Bar
    cmds.evalDeferred("from aTools.animTools.animBar import animBarUI; animBarUI.show('launch')")

# end aTools


os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = "P:/Deployment/Git/bin/git.exe"
os.environ['GIT_SSL_NO_VERIFY'] = "1"

PRODUCTION_REPO = "https://github.com/MayaFramework/Framework.git"
REPO_DIR = "P:/TOOLS/Framework"




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
    print ("Finished Clone process")
else:
    pull_latest_changes(REPO_DIR)
    print ("Finished Clone process")




