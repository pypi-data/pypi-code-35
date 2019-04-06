import mdio
import numpy as np

ncfile = 'examples/test.nc'
dcdfile = 'examples/test.dcd'
testcrds = np.array([28.37, 43.48, 25.27])
testbox = np.array([[59.414,  0.,     0.   ],
     [ 0.,    59.414,  0.,   ],
     [ 0.,     0.,    59.414]], dtype=np.float32)
testi = 219

def test_loader():
    t = mdio.load(ncfile)
    assert np.allclose(t.crds[0,0], testcrds) is True
    assert np.allclose(t[0].box, testbox) is True
    assert len(t) == testi

def test_opener():
    fin = mdio.mdopen(ncfile)
    fout = mdio.mdopen('tmp.dcd', 'w')
    frame = fin.read_frame()
    while frame is not None:
        fout.write_frame(frame)
        frame = fin.read_frame()
    fin.close()
    fout.close()

def test_consistency():
    finA = mdio.mdopen(ncfile, 'r')
    finB = mdio.mdopen('tmp.dcd', 'r')
    frameA = finA.read_frame()
    frameB = finB.read_frame()
    while frameA is not None:
        assert np.allclose(frameA.crds, frameB.crds) is True
        frameA = finA.read_frame()
        frameB = finB.read_frame()
    finA.close()
    finB.close()

def test_multiopen():
    t = mdio.load([ncfile, dcdfile])
    assert len(t) == 438
