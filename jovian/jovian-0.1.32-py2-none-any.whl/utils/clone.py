import os
from requests import get
from jovian.utils.constants import API_URL
from jovian._version import __version__
from jovian.utils.logger import log
from jovian.utils.rcfile import set_notebook_slug, get_rcdata, rcfile_exists


def _u(path):
    """Make a URL from the path"""
    return API_URL + path


def _msg(res):
    try:
        data = res.json()
        if 'errors' in data and len(data['errors'] > 0):
            return data['errors'][0]['message']
        if 'message' in data:
            return data['message']
        if 'msg' in data:
            return data['msg']
    except:
        if res.text:
            return res.text
        return 'Something went wrong'


def _pretty(res):
    """Make a human readable output from an HTML response"""
    return '(HTTP ' + str(res.status_code) + ') ' + _msg(res)


def _h(fresh):
    """Create a header to provide library metadata"""
    return {"x-jovian-source": "library",
            "x-jovian-library-version": __version__,
            "x-jovian-command": "clone" if fresh else "pull"}


def get_gist(slug, fresh):
    """Download a gist"""
    res = get(url=_u('/gist/' + slug), headers=_h(fresh))
    if res.status_code == 200:
        return res.json()['data']
    raise Exception('Failed to retrieve Gist: ' + _pretty(res))


def clone(slug, fresh=True):
    """Download the files for a gist"""
    # Download gist metadata
    log('Fetching ' + slug + "..")
    gist = get_gist(slug, fresh)
    title = gist['title']

    # If fresh clone, create directory
    if fresh:
        if os.path.exists(title):
            i = 1
            while os.path.exists(title + '-' + str(i)):
                i += 1
            title = title + '-' + str(i)
        if not os.path.exists(title):
            os.makedirs(title)
        os.chdir(title)

    # Download the files
    log('Downloading files..')
    for f in gist['files']:
        with open(f['filename'], 'wb') as fp:
            fp.write(get(f['rawUrl']).content)

        # Create .jovianrc for a fresh clone
        if fresh and f['filename'].endswith('.ipynb'):
            set_notebook_slug(f['filename'], slug)

    # Print success message and instructions (TODO)
    if fresh:
        log('Cloned successfully to ' + title)
    else:
        log('Files dowloaded successfully in current directory')


RCFILE_NOTFOUND = "Could not detect '.jovianrc' file. Make sure you are running 'jovian pull' inside a directory cloned with 'jovian clone'."


def pull(slug=None):
    """Get the latest files associated with the current gist"""
    # If a slug is provided, just use that
    if slug:
        clone(slug, fresh=False)
        return

    # Check if .jovianrc exists
    if not rcfile_exists():
        log(RCFILE_NOTFOUND, error=True)
        return

    # Get list of notebooks
    nbs = get_rcdata()['notebooks']
    for fname in nbs:
        # Get the latest files for each notebook
        clone(nbs[fname]['slug'], fresh=False)
