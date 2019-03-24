

import sys
import os

# Do some cross-platform importing. This module does not support
# cygwin. 
# On linux, the system first looks for Gtk via PyGObject.
# If that is not found, then it tries to get Qt. If neither are
# found, then an error is thrown. Ill try to support more formats
# in the future, but as of now, I am operating under the premise
# that everyone that would be using this on linux is using either
# a GTK or a Qt based desktop.
# On OSX, I use PyObjC to access the system clipboard. I will consider
# adding fallback support to use pb(copy|paste) as a backup.
# On windows, use the win32clipboard module. If that's not found, then
# no dice.

platform_backend = None

backends = {
    'gtk': None,
    'qt': None,
    'apple': None,
    'win': None
}

if sys.platform == 'linux':
    # Get current desktop
    current_desktop = os.environ.get('XDG_CURRENT_DESKTOP')
    if current_desktop in ['MATE', 'GNOME', 'X-Cinnamon', 'LXDE', 'XFCE', 'Unity']:
        # USE GTK AS BACKEND
        platform_backend = 'gtk'
        from .gtkbackend import GtkBackend
        backends['gtk'] = GtkBackend
    elif current_desktop in ['LXQt', 'KDE', ]:
        # USE QT AS BACKEND
        platform_backend = 'qt'
        from .qtbackend import QtBackend
        backends['qt'] = QtBackend
    else:
        raise RuntimeError('Not using a GTK or Qt-based Desktop')

elif sys.platform == 'darwin':
    try:
        # Try getting PyObjC
        from AppKit import NSPasteboard, NSStringPboardType
        from PIL import ImageGrab as PilImageGrab

        platform_backend = 'apple'
    except ModuleNotFoundError:
        raise RuntimeError("You need PyObjC if you are running on mac")

elif sys.platform == 'win32':
    try:
        platform_backend = 'win'
        from .winbackend import WindowsBackend
        backends['win'] = WindowsBackend
    except ModuleNotFoundError:
        raise RuntimeError("You need pywin32 to run on windows")
else:
    raise RuntimeError('Your platform is not supported')

