def __repo_hash__():
    """Retrieve git hash of the repo that produced the package."""
    import json
    import os
    # Locate directory of __init__.py, where we know repo_hash.json resides.
    with open(os.path.join(os.path.dirname(__file__),'repo_hash.json')) as file:
        data = json.load(file)
        return data["repo_hash"]

def __editable_dist__(dist='pypackage'):
    """Is distribution an editable install?"""
    import os
    import sys
    for path_item in sys.path:
        egg_link = os.path.join(path_item, dist + '.egg-link')
        if os.path.isfile(egg_link):
            return True
    return False

def git_repository_hash():
    """Retrieve repository hash."""
    import os
    import subprocess

    # Check if pypackage was installed with 'python setup.py develop'
    # or with pip install dist/pypackage-*-py3-none-any.whl.
    if __editable_dist__():
        # In the first case, the hash of the repo needs to be obtained
        # constantly from the repo.
        here = os.path.abspath(os.path.dirname(__file__))
        os.chdir(here)
        label = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
        return label.decode("utf-8")
    else:
        # In the second case, the version is obtained during the building
        # of the wheel package and doesn't change once installed.
        # Get git hash from repo_hash.json.
        return __repo_hash__()

from .version import __version__
