import os

from gadgetpy import MassStorage, Gadget

def test_MassStorage_create(tmpdir):
    gadget = Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    # if there is anything in the UDC file, the gadget is considered mounted
    tmpdir.join('testGadget','UDC').write('')
    tmpdir.mkdir('testGadget/functions')
    tmpdir.mkdir('testGadget/configs')
    massstorage = MassStorage('usb0')
    gadget.addFunction(massstorage)
    tmpdir.mkdir('testGadget/functions/mass_storage.usb0/lun.0')
    gadget.write()
    gadgetPath = tmpdir.join('testGadget')
    assert gadgetPath.join('functions',massstorage.name,'lun.0','cdrom').read().strip() == "0"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','nofua').read().strip() == "0"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','removable').read().strip() == "0"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','ro').read().strip() == "0"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','file').read().strip() == ""

def test_massstorage_write(tmpdir):
    gadget = Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    # if there is anything in the UDC file, the gadget is considered mounted
    tmpdir.join('testGadget','UDC').write('')
    tmpdir.mkdir('testGadget/functions')
    tmpdir.mkdir('testGadget/configs')
    massstorage = MassStorage('usb0')
    massstorage.image = '/tmp/test/thisisanimage.img'
    massstorage.cdrom = True
    massstorage.readOnly = True
    gadget.addFunction(massstorage)
    tmpdir.mkdir('testGadget/functions/mass_storage.usb0/lun.0')
    gadget.write()
    gadgetPath = tmpdir.join('testGadget')
    assert gadgetPath.join('functions',massstorage.name,'lun.0','cdrom').read().strip() == "1"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','nofua').read().strip() == "0"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','removable').read().strip() == "0"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','ro').read().strip() == "1"
    assert gadgetPath.join('functions',massstorage.name,'lun.0','file').read().strip() == "/tmp/test/thisisanimage.img"
