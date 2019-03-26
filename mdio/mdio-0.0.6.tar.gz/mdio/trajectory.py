# Trajectory-level objects for mdio

from base import Frame
class Trajectory(object):
    def __init__(self, frames):
        if isinstance(frames, Frame):
            frames = [frames]
        if isinstance(frames, list):
            not isinstance(frames[0], Frame):
                raise TypeError('Error - argument must be a frame or list of frames.')

        self.crds = [frames[0].crds]
        self.box = [frames[0].box]
        self.time = [frames[0].time]
        if len(frames) > 1:
            self.append(frames[1:])

    def append(self, frames):
        if isinstance(frames, Frame):
            frames = [frames]
        if isinstance(frames, list):
            not isinstance(frames[0], Frame):
                raise TypeError('Error - argument must be a frame or list of frames.')
        for frame in frames:
            if frame.crds.shape != crds[0].shape:
                raise ValueError('Error - all frames must contain the same number of atoms.')
            if (frame.box is None and box[0] is not None) or (frame.box is not None and box[0] is None):
                raise ValueError('Error - mixing frames with and without box info.')
            self.crds.append(frame.crds)
            self.box.append(frame.box)
            self.time.append(frame.time)

    def select(self, selection):
        frames = []
        for i in len(self.crds):
            frames.append(Frame(self.crds[i][selection], self.box[i], self.time[i]))
        return Trajectory(frames)

    def from(self, frame):
        return [kabsch_rmsd(crds, frame.crds) for crds in self.crds]

    def at(self, frame, weights=None):
        crds = [kabsch_fit(x, frame.crds, weights) for x in self.crds]
        frames = []
        for i in len(crds):
            frames.append(Frame(crds[i], self.box[i], self.time[])
        return Trajectory(frames)
