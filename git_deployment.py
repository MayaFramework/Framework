import git


GIT_PYTHON_GIT_EXECUTABLE = "P:/Deployment/GitPortable/App/Git/bin/git.exe"
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


def doIt():
    if not is_git_repo(REPO_DIR):
        clone_repo(PRODUCTION_REPO, REPO_DIR, branch="bm2_production")
    else:
        pull_latest_changes(REPO_DIR)