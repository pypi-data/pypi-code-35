import os
import gadgetpy
from pytest import raises

# Notes
# Some files are auto-created by configfs, but since we aren't in a
# real configfs mount when testing, we have to fake creating these
# files, so the default for write in Gadget has to be false for these
# tests not to error out when creating the instance.

# TODO: if someone can find a better work-around, I'm open to options
# I'd rather have this work correctly

def test_valid_base_path():
    gadget = gadgetpy.Gadget('testGadget','/test/path/',write=False)
    assert gadget.path=='/test/path/testGadget'

def test_fail_on_existing(tmpdir):
    tmpdir.mkdir('testGadget')
    with raises(gadgetpy.GadgetExists):
        testGadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)

def test_path_gets_created(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    assert os.path.isdir(gadget.path)

def test_blocks_write_on_mount(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    # if there is anything in the UDC file, the gadget is considered mounted
    tmpdir.join('testGadget','UDC').write('abcd')
    with raises(gadgetpy.GadgetMounted):
        gadget.write()

def test_files_get_written(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    tmpdir.join('testGadget','UDC').write('')
    gadget.write()
    gadgetPath = tmpdir.join('testGadget')
    stringPath = gadgetPath.join('strings','0x409')
    assert stringPath.check(dir=1)
    assert gadgetPath.join('idVendor').read() == "0x1d6b"
    assert gadgetPath.join('idProduct').read() == "0x0104"
    assert gadgetPath.join('bcdDevice').read() == "0x0100"
    assert gadgetPath.join('bcdUSB').read() == "0x0200"
    assert stringPath.join('serialnumber').read() == "fedcba9876543210"
    assert stringPath.join('manufacturer').read() == "Lorium Ipsum"
    assert stringPath.join('product').read() == "Python Gadget"

def test_deactivate(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    tmpdir.join('testGadget','UDC').write('')
    gadget.write()
    tmpdir.join('testGadget','UDC').write('abcd')
    gadget.deactivate()
    assert tmpdir.join('testGadget','UDC').read().isspace()

def test_change_strings(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    tmpdir.join('testGadget','UDC').write('')
    gadget.write()
    gadget.product = "Test Gadget"
    gadget.manufacturer = "PyTest"
    gadget.idVendor = "0xdead"
    gadget.idProduct = "0xbeef"
    gadget.write()
    gadgetPath = tmpdir.join('testGadget')
    stringPath = gadgetPath.join('strings','0x409')
    assert gadgetPath.join('idVendor').read() == "0xdead"
    assert gadgetPath.join('idProduct').read() == "0xbeef"
    assert gadgetPath.join('bcdDevice').read() == "0x0100"
    assert gadgetPath.join('bcdUSB').read() == "0x0200"
    assert stringPath.join('serialnumber').read() == "fedcba9876543210"
    assert stringPath.join('manufacturer').read() == "PyTest"
    assert stringPath.join('product').read() == "Test Gadget"

def test_exists(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    assert gadget.exists()

def test_mounted(tmpdir):
    gadget = gadgetpy.Gadget('testGadget',str(tmpdir),write=False)
    gadget.buildPaths()
    tmpdir.join('testGadget','UDC').write('')
    assert not gadget.isMounted()
    tmpdir.join('testGadget','UDC').write('abcd')
    assert gadget.isMounted()
