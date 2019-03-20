import zipfile
import os
import tempfile
import udp_filetransfer

def package_directory(dpath:str):
    """
    Packages a directory int oa zipfile and returns the zip name.
    """
    with tempfile.NamedTemporaryFile(delete=False) as pkf:
        with zipfile.ZipFile(pkf, "w", zipfile.ZIP_DEFLATED) as pkg:
            for root, dirs, files in os.walk(dpath):
                r_dir = os.path.relpath(root, dpath)
                for f in files:
                    pkg.write(os.path.join(r_dir, f))
    return pkf.name

def distribute(path:str):
    """
    Package and distribute a task.
    """
    if os.path.isdir(path):
        path = package_directory(path)
    distributor = udp_filetransfer.ChunkSender(path)
    distributor.run()
