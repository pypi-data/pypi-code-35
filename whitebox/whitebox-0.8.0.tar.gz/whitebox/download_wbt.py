import os, sys, platform
import zipfile
import tarfile
import shutil
import urllib.request
import pkg_resources


def download_wbt():
    '''
    Download WhiteboxTools pre-complied binary for first-time use
    '''
    # print("Your operating system: {}".format(platform.system()))
    package_name = "whitebox"
    # Get package directory
    pkg_dir = os.path.dirname(pkg_resources.resource_filename(package_name, 'whitebox_tools.py'))
    exe_dir = os.path.join(pkg_dir, "WBT")                 # Get directory of WhiteboxTools executable file
    work_dir = os.path.join(pkg_dir, "testdata")           # Set working directory

    try:

        if not os.path.exists(exe_dir):  # Download WhiteboxTools executable file if non-existent
            print("Downloading WhiteboxTools pre-compiled binary for first time use ...")
            if platform.system() == "Windows":
                url = "https://www.uoguelph.ca/~hydrogeo/WhiteboxTools/WhiteboxTools_win_amd64.zip"
            elif platform.system() == "Darwin":
                url = "https://www.uoguelph.ca/~hydrogeo/WhiteboxTools/WhiteboxTools_darwin_amd64.zip"
            elif platform.system() == "Linux":
                url = "https://www.uoguelph.ca/~hydrogeo/WhiteboxTools/WhiteboxTools_linux_amd64.tar.xz"
            else:
                print("WhiteboxTools is not yet supported on {}!".format(platform.system()))
                exit()

            zip_name = os.path.join(pkg_dir, os.path.basename(url))         # Get WhiteboxTools zip file name
            urllib.request.urlretrieve(url, zip_name)   # Download WhiteboxTools
            zip_ext = os.path.splitext(zip_name)[1]     # Get downloaded zip file extension

            print("Decompressing {} ...".format(os.path.basename(url)))
            if zip_ext == ".zip":       # Decompress Windows/Mac OS zip file
                with zipfile.ZipFile(zip_name, "r") as zip_ref:
                    zip_ref.extractall(pkg_dir)
            else:                       # Decompress Linux tar file
                with tarfile.open(zip_name, "r") as tar_ref:
                    tar_ref.extractall(pkg_dir)
            print("WhiteboxTools package directory: {}".format(pkg_dir))

            exe_ext = ""    # file extension for MacOS/Linux
            if platform.system() == 'Windows':
                exe_ext = '.exe'
            exe_name = "whitebox_tools{}".format(exe_ext)
            exe_path = os.path.join(exe_dir, exe_name)

            if platform.system() != "Windows":   # grant executable permission
                os.system("chmod 755 " + exe_path)

            exe_path_new = os.path.join(pkg_dir, exe_name)
            shutil.copy(exe_path, exe_path_new)

        if not os.path.exists(work_dir):
            print("Downloading testdata ...")
            os.mkdir(work_dir)
            dem_url = "https://github.com/jblindsay/whitebox-tools/raw/master/testdata/DEM.tif"
            dep_url = "https://github.com/jblindsay/whitebox-tools/raw/master/testdata/DEM.dep"
            urllib.request.urlretrieve(dem_url, os.path.join(work_dir, "DEM.tif"))
            urllib.request.urlretrieve(dep_url, os.path.join(work_dir, "DEM.dep"))

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
