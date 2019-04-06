from sys import platform
from os import stat,chmod
from os.path import join,expanduser
from setuptools.command.install import install

#修改project_name即可打包，其他地方不用修改
project_name = "kdui2py"

class install_cmd(install):
    def run(self):
        install.run(self)
        try :
            if platform =="win32" :
                    script_file =  join(self._get_desktop_folder(),project_name + '.bat')
                    with open(script_file, "w") as f:
                        f.write("@echo off\r\nstart " + project_name + ".exe")
            elif platform == "linux":
                    script_file =  join(self._get_desktop_folder(),project_name + '.sh')
                    with open(script_file, "w") as f:
                        f.write("#!/bin/sh\n" + project_name)
                        st = stat(script_file)
                        chmod(script_file, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            print("can not create start script." + str(e))
    def _get_desktop_folder(self):
        import subprocess
        try:
            return subprocess.check_output(['xdg-user-dir',
                                            'DESKTOP']).decode('utf-8').strip()
        except Exception:
            return join(expanduser('~'), 'Desktop')   
