import mdio
from mdio import Frame, Trajectory
import numpy as np

data = np.random.rand(13,56,3)

def test_frame_init():
    f = Frame(data[0])

def test_frame_select():
    selection = range(5)
    f = Frame(data[0])
    fs = f.select(selection)
    assert fs.crds.shape[0] == 5

def test_frame_rmsd_from():
    f = Frame(data[0])
    f2 = Frame(data[0])
    f2.crds[:, 0] = f.crds[:, 1]
    f2.crds[:, 1] = f.crds[:, 2]
    f2.crds[:, 2] = f.crds[:, 0]
    assert f.rmsd_from(f2) < 0.01

def test_frame_fitted_to():
    f = Frame(data[0])
    f2 = Frame(data[0])
    f2.crds[:, 0] = f.crds[:, 1]
    f2.crds[:, 1] = f.crds[:, 2]
    f2.crds[:, 2] = f.crds[:, 0]
    f3 = f.fitted_to(f2)
    assert np.allclose(f3.crds, f2.crds)

def test_frame_packed_around():
    crds = data[0]
    extent = crds.max(axis=0) - crds.min(axis=0)
    extent = extent + 1.0
    box = np.array([[extent[0], 0, 0], [0, extent[1], 0], [0, 0, extent[2]]])
    crds[0] = crds.mean(axis=0)
    f = Frame(crds, box)
    f2 = f.packed_around(0)
    assert  np.allclose(f2.crds, f.crds)
    assert f2.rmsd_from(f) < 0.01
    f.crds[0] = 0.0
    f2 = f.packed_around(0)
    assert not np.allclose(f2.crds, f.crds)

def test_traj_init_from_frame():
    t = Trajectory(Frame(data[0]))

def test_traj_init_from_frames():
    frames = [Frame(x) for x in data]
    t = Trajectory(frames)

def test_traj_init_from_array():
    t1 = Trajectory(data[0])
    t2 = Trajectory(data)

