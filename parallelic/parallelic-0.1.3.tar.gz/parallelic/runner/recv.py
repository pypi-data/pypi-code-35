import zipfile
import udp_filetransfer
import tempfile
import os

def unpack_package(pkpath:str):
    outpath = tempfile.mkdtemp()
    with zipfile.ZipFile(pkpath) as pkg:
        pkg.extractall(outpath)
    return outpath

def receive():
    task = udp_filetransfer.receive()
    if zipfile.is_zipfile(task):
        task = unpack_package(task)
    return task

        