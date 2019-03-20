import getpass
import socket
import re
from subprocess import Popen, PIPE
from PyQt5.QtCore import QObject


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    def set_record_path(self, record_path):
        """Set record path then create dotlup dir."""
        self._model.record_path = record_path
        self._model.create_dotlup_dir()

    def change_interval(self, interval):
        """Change recording interval."""
        self._model.record_interval = interval

    def _handle_various_xprop(self, active_window):
        """Handle various xprop formats."""
        active_window_str = active_window
        if type(active_window) is bytes:
            active_window_str = active_window.decode()

        window_id = active_window_str.split()[-1]
        # handle XFCE xprop format
        if window_id == "0x0":
            window_id = active_window_str.split()[-2].strip(",")

        return window_id

    def get_focused_window_id(self):
        """Return focused windows id."""
        active_window_proc = Popen(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=PIPE
        )
        active_window, err = active_window_proc.communicate()
        focused_window_id = self._handle_various_xprop(active_window)
        return focused_window_id

    def get_focused_window(self):
        """Get current focused window title.

        window_name_dirty value is  b\'WM_NAME(STRING) = "WINDOW TITLE"\n'.
        WINDOW TITLE will be parsed using regex and returned as string.
        new line at the end of file needed as it's git convention.
        """
        focused_window_id = self.get_focused_window_id()
        window_name_proc = Popen(
            ["xprop", "-id", focused_window_id, "WM_NAME"], stdout=PIPE
        )
        window_name_dirty, err = window_name_proc.communicate()
        focused_window = re.findall(r"\"(.+?)\"", window_name_dirty.decode())
        return "{}\n".format("".join(focused_window))

    def get_public_ip(self):
        """Return public ip address by connecting to google DNS."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            public_ip, _ = s.getsockname()
            s.close()
        except Exception:
            public_ip = "Not connected"
        return public_ip

    def get_all_windows(self):
        """Get all windows title.

        wmctrl result is 0x03800004  0 machine user - WINDOW TITLE.
        WINDOW TITLE will be taken and returned as string.
        """
        all_windows = ""
        all_windows_proc = Popen(["wmctrl", "-l"], stdout=PIPE)
        all_windows_dirty, err = all_windows_proc.communicate()
        for line in all_windows_dirty.splitlines():
            windows_name = line.split(None, 3)[-1].decode()
            all_windows += "{}\n".format(windows_name)
        return all_windows

    def get_auth_info(self):
        """Get auth information."""
        auth_info = ""
        username = getpass.getuser()
        machine = socket.gethostname()
        ip = self.get_public_ip()
        for data in [username, machine, ip]:
            auth_info += "{}\n".format(data)
        return auth_info
