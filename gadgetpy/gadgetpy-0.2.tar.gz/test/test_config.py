import os
from gadgetpy import MassStorage, Gadget, Config

def test_config_create(tmpdir):
    Config('c.1')

def test_config_add(tmpdir):
    gadget = Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    tmpdir.join('testGadget','UDC').write('')
    tmpdir.mkdir('testGadget/functions')
    tmpdir.mkdir('testGadget/configs')
    massstorage = MassStorage('usb0')
    config = Config('c.1')
    config.addFunction(massstorage)
    gadget.addFunction(massstorage)
    tmpdir.mkdir('testGadget/functions/mass_storage.usb0/lun.0')
    gadget.addConfig(config)
    gadget.write()
    gadgetPath = tmpdir.join('testGadget')
    assert gadgetPath.join('configs','c.1',massstorage.name,'lun.0','cdrom').read().strip() == "0"
    assert gadgetPath.join('configs','c.1',massstorage.name,'lun.0','nofua').read().strip() == "0"
    assert gadgetPath.join('configs','c.1',massstorage.name,'lun.0','removable').read().strip() == "0"
    assert gadgetPath.join('configs','c.1',massstorage.name,'lun.0','ro').read().strip() == "0"
    assert gadgetPath.join('configs','c.1',massstorage.name,'lun.0','file').read().strip() == ""
