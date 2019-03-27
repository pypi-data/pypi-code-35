from mdio.dcdio import dcd_open
import numpy as np

dcdfile = 'examples/test.dcd'
testcrds = np.array([28.37, 43.48, 25.27])
testbox = np.array([[59.414,  0.,     0.   ],
     [ 0.,    59.414,  0.,   ],
     [ 0.,     0.,    59.414]], dtype=np.float32)
testi = 220

def test_opener():
    f = dcd_open(dcdfile, 'r')
    frame = f.read_frame()
    assert np.allclose(frame.crds[0], testcrds) is True
    assert np.allclose(frame.box, testbox) is True
    i = 1
    while frame is not None:
        frame = f.read_frame()
        i += 1
    assert i == testi
    f.close()

def test_consistency():
    fin = dcd_open(dcdfile, 'r')
    fout = dcd_open('tmp.dcd', 'w')
    frame = fin.read_frame()
    while frame is not None:
        fout.write_frame(frame)
        frame = fin.read_frame()
    fin.close()
    fout.close()

    finA = dcd_open(dcdfile, 'r')
    finB = dcd_open('tmp.dcd', 'r')
    frameA = finA.read_frame()
    frameB = finB.read_frame()
    while frameA is not None:
        assert np.allclose(frameA.crds, frameB.crds) is True
        frameA = finA.read_frame()
        frameB = finB.read_frame()
    finA.close()
    finB.close()

def test_nobox():
    dcdfile = 'examples/test_nobox.dcd'

    f = dcd_open(dcdfile, 'r')
    frame = f.read_frame()
    assert np.allclose(frame.crds[0], testcrds) is True
    i = 1
    while frame is not None:
        frame = f.read_frame()
        i += 1
    assert i == testi

    f.close()

def test_selection():
    fsel = dcd_open(dcdfile, selection=range(12))
    framesel = fsel.read_frame()
    assert len(framesel.crds) == 12
    fsel.close()
