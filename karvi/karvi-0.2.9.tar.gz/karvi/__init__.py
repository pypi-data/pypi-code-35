name = "karvi"
__version__ = "0.2.9"


def get_templates_dir():
    import os

    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/")
    return templates_dir


def get_version():
    import subprocess

    try:
        git_hash = subprocess.check_output(["git", "describe", "--tags"])
        git_hash = git_hash.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        git_hash = None

    if git_hash and (git_hash != __version__):
        git_hash = git_hash.split("-", 3)
        version = "{}.dev{}".format(git_hash[0], git_hash[1])
    else:
        version = __version__

    return version
