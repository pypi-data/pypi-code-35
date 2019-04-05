import mdio
from mdio import Frame, Trajectory
import numpy as np

data = np.random.rand(13,56,3)

def test_frame_init():
    f = Frame(data[0])

def test_traj_init_from_frame():
    t = Trajectory(Frame(data[0]))

def test_traj_init_from_frames():
    frames = [Frame(x) for x in data]
    t = Trajectory(frames)

def test_traj_init_from_array():
    t1 = Trajectory(data[0])
    t2 = Trajectory(data)

