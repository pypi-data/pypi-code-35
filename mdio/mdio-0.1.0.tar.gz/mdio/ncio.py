from netCDF4 import Dataset
import numpy as np
import mdio.base 

class NCFileReader(object):
    def __init__(self, filename, selection=None):
        self.filename = filename
        self.selection = selection
        self.root = Dataset(filename, 'r')
        if self.root.Conventions != "AMBER":
            raise TypeError("Error - this does not appear" 
                             " to be an Amber netcdf file.")
        self.coordinates = self.root['/coordinates']
        self.time = self.root['/time']
        self.index = -1
        self.nframes = len(self.coordinates)
        self.periodic = 'cell_spatial' in self.root.dimensions
        if self.periodic:
            self.cell_lengths = self.root['/cell_lengths']
            self.cell_angles = self.root['/cell_angles']
            
    def read_frame(self, selection=None):
        if selection is None:
            selection = self.selection
        self.index += 1
        if self.index >= self.nframes:
            return None
        if self.periodic:
            box = la2v(self.cell_lengths[self.index], 
                       self.cell_angles[self.index])
        else:
            box = None
        crds = self.coordinates[self.index]
        if selection is not None:
            crds = crds[selection]
        frame = mdio.base.Frame(crds, 
                      box=box, 
                      time=self.time[self.index])
        return frame
    
    def read(self, selection=None):
        frames = []
        frame = self.read_frame(selection=selection)
        while frame is not None:
            frames.append(frame)
            frame = self.read_frame(selection=selection)
        return mdio.base.Trajectory(frames)

    def close(self):
        self.root.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
        
class NCFileWriter(object):
    def __init__(self, filename):
        self.filename = filename
        self.index = -1
        self.root = Dataset(filename, 'w', format="NETCDF3_64BIT_OFFSET")
        self.root.set_fill_off()
        
        self.root.Conventions = "AMBER"
        self.root.ConventionVersion = "1.0"
        self.root.program = "mdio"
        self.root.programVersion = "0.0.2"
        self.root.title = "CREATED by mdio.ncio"
        
        self.root.createDimension("frame", None)
        self.root.createDimension("spatial", 3)
        
        self.spatial = self.root.createVariable("spatial", "S1", ("spatial",))
        self.spatial[0] = "x"
        self.spatial[1] = "y"
        self.spatial[2] = "z"

        self.time = self.root.createVariable("time", "f4", ("frame",))
        self.time.units = "picoseconds"
        
        self.periodic = False

    def set_coordinates(self, natoms):
        self.root.createDimension("atom", natoms)
        self.coordinates = self.root.createVariable("coordinates", "f4", 
                                                    ("frame", "atom", "spatial"))
        self.coordinates.units = "angstrom"
        
    def set_periodic(self):
        if 'cell_spatial' in self.root.dimensions:
            return
        self.root.createDimension("cell_spatial", 3)
        self.root.createDimension("cell_angular", 3)
        self.root.createDimension("label", 5)
        
        self.cell_angular = self.root.createVariable("cell_angular", "S1", 
                                                     ("cell_spatial", "label"))
        self.cell_spatial = self.root.createVariable("cell_spatial", "S1", 
                                                     ("cell_spatial",))
                
        self.cell_angular[0] = "alpha"
        self.cell_angular[1] = "beta"
        self.cell_angular[2] = "gamma"

        self.cell_spatial[0] = "a"
        self.cell_spatial[1] = "b"
        self.cell_spatial[2] = "c"

        self.cell_lengths = self.root.createVariable("cell_lengths", "f4", 
                                                     ("frame", "cell_spatial"))
        self.cell_lengths.units = "angstrom"

        self.cell_angles = self.root.createVariable("cell_angles", "f4", 
                                                    ("frame", "cell_angular"))
        self.cell_angles.units = "degree"
        
        self.periodic = True
        
    def write_frame(self, frame):
        self.index += 1
        self.time[self.index] = frame.time
        if self.index == 0:
            self.set_coordinates(frame.natoms)
            if frame.box is not None:
                self.set_periodic()

        self.coordinates[self.index] = frame.crds
        if frame.box is None and self.periodic:
            raise ValueError('Error: frame contains no box data.')
        if frame.box is not None and not self.periodic:
            raise ValueError('Error: frame contains unexpected box data.')
        if self.periodic:
            l, a = v2la(frame.box)
            self.cell_lengths[self.index] = l
            self.cell_angles[self.index] = a
        
    def write(self, trajectory):
        for i in range(len(trajectory)):
            self.write_frame(trajectory.frame(i))

    def close(self):
        self.root.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

def la2v(lengths, angles):
    alpha = angles[0] * np.pi / 180
    beta = angles[1] * np.pi / 180
    gamma = angles[2] * np.pi / 180

    a = np.array([lengths[0], 0.0, 0.0])
    b = np.array([lengths[1]*np.cos(gamma), lengths[1]*np.sin(gamma), 0.0])
    cx = lengths[2]*np.cos(beta)
    cy = lengths[2]*(np.cos(alpha) - np.cos(beta)*np.cos(gamma)) / np.sin(gamma)
    cz = np.sqrt(lengths[2]*lengths[2] - cx*cx - cy*cy)
    c = np.array([cx,cy,cz])

    v = np.array((a,b,c))
    # Make sure that all vector components that are _almost_ 0 are set exactly
    # to 0
    tol = 1e-6
    v[np.logical_and(v>-tol, v<tol)] = 0.0

    return v

def v2la(vectors):
    a = vectors[0]
    b = vectors[1]
    c = vectors[2]

    a_length = np.sqrt(np.sum(a*a))
    b_length = np.sqrt(np.sum(b*b))
    c_length = np.sqrt(np.sum(c*c))

    alpha = np.arccos(np.dot(b, c) / (b_length * c_length))
    beta = np.arccos(np.dot(c, a) / (c_length * a_length))
    gamma = np.arccos(np.dot(a, b) / (a_length * b_length))

    alpha = alpha * 180.0 / np.pi
    beta = beta * 180.0 / np.pi
    gamma = gamma * 180.0 / np.pi

    return [a_length, b_length, c_length], [alpha, beta, gamma]

def nc_open(filename, mode='r', selection=None):
    """
    Open an Amber netcdf trajectory file.
    """
    if not mode in ["r", "w"]:
        raise ValueError('Error: mode must be "r" or "w".')
    if mode == 'r':
        return NCFileReader(filename, selection=selection)
    else:
        return NCFileWriter(filename)
