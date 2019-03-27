from mdio.xtcio import xtc_open
import numpy as np

testbox = np.array(
    [[5.94140005, 0.,         0.        ],
     [0.,         5.94140005, 0.        ],
     [0.,         0.,         5.94140005]]
    )
xtcfile = 'examples/test.xtc'
testcrds = np.array([2.837, 4.348, 2.527]) 
testi = 220

def test_opener():
    f = xtc_open(xtcfile, 'r')
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
    fin = xtc_open(xtcfile, 'r')
    fout = xtc_open('tmp.xtc', 'w')
    frame = fin.read_frame()
    while frame is not None:
        fout.write_frame(frame)
        frame = fin.read_frame()
    fin.close()
    fout.close()

    finA = xtc_open(xtcfile, 'r')
    finB = xtc_open('tmp.xtc', 'r')
    frameA = finA.read_frame()
    frameB = finB.read_frame()
    i = 0
    while frameA is not None:
        #if not np.allclose(frameA.crds, frameB.crds):
        #    print(i, frameA.crds[-1],frameB.crds[-1])
        assert np.allclose(frameA.crds, frameB.crds) is True
        frameA = finA.read_frame()
        frameB = finB.read_frame()
        i += 1
    finA.close()
    finB.close()

def test_nobox():
    xtcfile = 'examples/test_nobox.xtc'
    testi = 220

    f = xtc_open(xtcfile, 'r')
    frame = f.read_frame()
    assert np.allclose(frame.crds[0], testcrds) is True
    i = 1
    while frame is not None:
        frame = f.read_frame()
        i += 1
    assert i == testi
    f.close()

def test_selection():
    fsel = xtc_open(xtcfile, selection=range(12))
    framesel = fsel.read_frame()
    assert len(framesel.crds) == 12
    fsel.close()
