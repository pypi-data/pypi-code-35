import numpy as np
from  mdio import rmsd
from os.path import splitext
import mdio.dcdio 
import mdio.ncio 
import mdio.xtcio 

class Frame(object):
    """
    A frame of trajectory data.
    
    """
    def __init__(self, crds, box=None, time=0.0, precision=1000, timestep = 1.0):
        crds = np.array(crds, dtype=np.float32)
        if len(crds.shape) != 2:
            raise TypeError('Error - crds must be a [N,3] array.')
        if crds.shape[1] != 3:
            raise TypeError('Error - crds must be a [N,3] array.')
        self.natoms = crds.shape[0]
        self.crds = crds
        if box is not None:
            box = np.array(box, dtype=np.float32)
            if len(box.shape) == 1 and len(box) == 6:
                tbox = np.zeros((3,3), dtype=np.float32)
                tbox[0, 0] = box[0]
                tbox[1, 0] = box[1]
                tbox[1, 1] = box[2]
                tbox[2, 0] = box[3]
                tbox[2, 1] = box[4]
                tbox[2, 2] = box[5]
                box = tbox
            elif box.shape != (3,3):
                raise ValueError('Error - unrecognised box data {}'.format(box))
        self.box = box
        self.time = float(time)
        self.precision = int(precision)
        self.timestep = timestep

    def __str__(self):
        if self.box is not None:
            return "mdio.Frame with {} atoms and box info.".format(self.natoms)
        else:
            return "mdio.Frame with {} atoms.".format(self.natoms)


# Trajectory-level objects for mdio

class Trajectory(object):
    """
    A series of Frames.
    """
    def __init__(self, data):
        if isinstance(data, Frame):
            frames = [data]
        elif isinstance(data, list):
            if not isinstance(data[0], Frame):
                raise TypeError('Error - argument must be a frame or list of frames.')
            frames = data
        elif isinstance(data, np.ndarray):
            s = data.shape
            if len(s) < 2 or len(s) > 3:
                raise TypeError('Error - argument must be a [natoms, 3] or [nframes, natoms, 3] array')
            if s[-1] != 3:
                raise TypeError('Error - argument must be a [natoms, 3] or [nframes, natoms, 3] array')
            if len(s) == 2:
                data = [data]
            frames = [Frame(x) for x in data] 
        else:
            raise TypeError('Error - unsupported data type for initialisation.')

        self.crds = np.array([frames[0].crds])
        self.natoms = len(self.crds[0])
        self.box = np.array([frames[0].box])
        self.time = [frames[0].time]
        if len(frames) > 1:
            self.append(frames[1:])

    def __str__(self):
        if self.box[0] is None:
            return "mdio.Trajectory with {} frames, and {} atoms.".format(len(self.crds), self.natoms)
        else:
            return "mdio.Trajectory with {} frames, {} atoms and box info.".format(len(self.crds), self.natoms)

    def __len__(self):
        """
        Length of the trajectory.
        """
        return len(self.crds)

    def __getitem__(self, key):
        """
        Returns a Frame or sub-Trajectory.
        """
        crds = self.crds[key]
        box = self.box[key]
        time = self.time[key]
        if isinstance(key, int):
            return Frame(crds, box, time)
        else:
            return Trajectory([Frame(crds[i], box[i], time[i]) for i in range(len(crds))])

    def __add__(self, other):
        if not isinstance(other, Trajectory):
            raise NotImplementedError('Error - can only add a Trajectory to a Trajectory.')
        result = Trajectory(self.frames())
        result.append(other.frames())
        return result

    def __iadd__(self, other):
        if not isinstance(other, Trajectory):
            raise NotImplementedError('Error - can only add a Trajectory to a Trajectory.')
        self.append(other.frames())
        return self

    def append(self, frames):
        """
        Append exra frames to a Trajectory.
        """
        if isinstance(frames, Frame):
            frames = [frames]
        if isinstance(frames, list):
            if not isinstance(frames[0], Frame):
                raise TypeError('Error - argument must be a frame or list of frames.')
        crds = []
        box = []
        for frame in frames:
            if frame.crds.shape != self.crds[0].shape:
                raise ValueError('Error - all frames must contain the same number of atoms.')
            if (frame.box is None and self.box[0] is not None) or (frame.box is not None and self.box[0] is None):
                raise ValueError('Error - mixing frames with and without box info.')
            crds.append(frame.crds)
            box.append(frame.box)
            self.time.append(frame.time)

        self.crds = np.vstack((self.crds, crds))
        if self.box[0] is None:
            self.box = np.concatenate((self.box, box))
        else:
            self.box = np.vstack((self.box, box))

    def frame(self, index):
        return Frame(self.crds[index], self.box[index], self.time[index])
 
    def frames(self):
        return [self.frame(i) for i in range(len(self))]

    def select(self, selection):
        """
        Create a new Trajectory from selected atoms.
        """
        frames = []
        for i in range(len(self.crds)):
            frames.append(Frame(self.crds[i][selection], self.box[i], self.time[i]))
        return Trajectory(frames)

    def rmsd_from(self, frame):
        """
        The RMSD of each Frame from a reference Frame.
        """
        if isinstance(frame, Trajectory):
            frame = frame.frame(0)
        elif not isinstance(frame, Frame):
            raise TypeError('Error - argument must be a Frame or Trajectory')

        if frame.crds.shape != self.crds[0].shape:
            return ValueError("Error - reference structure has {} atoms but trajectory has {} atoms.".format(frame.crds.shape[0], self.crds.shape[0]))
        return [rmsd.kabsch_rmsd(crds, frame.crds, translate=True) for crds in self.crds]

    def fitted_to(self, frame, weights=None):
        """
        Returns a copy of the trajectory least-squares fitted to the reference.
        """
        if isinstance(frame, Trajectory):
            frame = frame.frame(0)
        elif not isinstance(frame, Frame):
            raise TypeError('Error - argument must be a Frame or Trajectory')

        if frame.crds.shape != self.crds[0].shape:
            return ValueError("Error - reference structure has {} atoms but trajectory has {} atoms.".format(frame.crds.shape[0], self.crds.shape[0]))

        crds = [rmsd.kabsch_fit(x, frame.crds, weights) for x in self.crds]
        frames = []
        for i in range(len(crds)):
            frames.append(Frame(crds[i], None, self.time[i]))
        return Trajectory(frames)

    def packed_around(self, centre_atom_index):
        """
        Pack the coordinates in a trajectory into the periodic box.
        """
        if self.box[0] is None:
            return self
        frames = []
        for i in range(len(self.crds)):
            A = self.box[i].T
            B = np.linalg.inv(A)
            box_centre = np.matmul(A, [0.5, 0.5, 0.5])
            dv = box_centre - self.crds[i][centre_atom_index]
            r = self.crds[i] + dv
            f = np.matmul(B, r.T)
            g = f - np.floor(f)
            t = np.matmul(A, g)
            crds = t.T - dv
            frames.append(Frame(crds, self.box[i], self.time[i]))
        return Trajectory(frames)

    def save(self, filename):
        ext = splitext(filename)[1]
        if ext in [".nc", ".ncdf"]:
            opener = mdio.ncio.nc_open
        elif ext in [".dcd"]:
            opener = mdio.dcdio.dcd_open
        elif ext in [".xtc"]:
            opener = mdio.xtcio.xtc_open
        else:
            raise TypeError('Error - unrecognised file extension ({})'.format(ext))
        with opener(filename, "w") as f:
            f.write(self)

def load(filename, selection=None):
    """
    Format-detecting file loader
    """
    openers = [mdio.ncio.nc_open, mdio.dcdio.dcd_open, mdio.xtcio.xtc_open]

    for opener in openers:
        try:
            with opener(filename, selection=selection) as f:
                t = f.read()
            success = True
        except:
            success = False
        if success:
            break
    if not success:
        raise TypeError('Error - {} does not have a recognised file format'.format(filename))
    return t

def mdopen(filename, mode="r", selection=None):
    """
    Format-agnostic open routines.
    """
    openers = [mdio.ncio.nc_open, mdio.dcdio.dcd_open, mdio.xtcio.xtc_open]

    if not mode in ["r", "w"]:
        raise ValueError('Error - mode must be "r" or "w"')

    if mode == "r":
        for opener in openers:
            try:
                with opener(filename, selection=selection) as f:
                    frame = f.read_frame()
                success = True
            except:
                success = False
            if success:
                return opener(filename, selection=selection)
        if not success:
            raise TypeError('Error - {} does not have a recognised file format'.format(filename))

    else:
        ext = splitext(filename)[1]
        if ext in [".nc", ".ncdf"]:
            opener = mdio.ncio.nc_open
        elif ext in [".dcd"]:
            opener = mdio.dcdio.dcd_open
        elif ext in [".xtc"]:
            opener = mdio.xtcio.xtc_open
        else:
            raise TypeError('Error - unrecognised file extension ({})'.format(ext))
        return opener(filename, "w")

