import gadgetpy
import os

def test_valid_name():
    assert gadgetpy.utils.verifyName('test.usb0')

def test_invalid_name():
    assert not gadgetpy.utils.verifyName('test')

def test_valid_pointer(fs):
    tmpdir = "/gadgets/"
    fs.create_dir(tmpdir)
    fs.create_file('/sys/class/udc/test')
    assert gadgetpy.utils.verifyPointer(tmpdir,'test')

def test_pointer_in_use(fs):
    tmpdir = "/gadgets/"
    gadget = gadgetpy.Gadget('testGadget',tmpdir,write=False)
    fs.create_file(os.path.join(gadget.path,'UDC'),contents='test')
    fs.create_file('/sys/class/udc/test')
    assert not gadgetpy.utils.verifyPointer(str(tmpdir),'test')

def test_invalid_pointer(fs):
    tmpdir = "/gadgets/"
    fs.create_dir(tmpdir)
    fs.create_file('/sys/class/udc/test2')
    assert not gadgetpy.utils.verifyPointer(tmpdir,'test')
