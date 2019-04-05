import os
import numpy as np
from tqdm import tqdm


def _are_floats(*args):
    are_floats = True
    try:
        for f in args:
            float(f)
    except TypeError:
        are_floats = False
    except ValueError:
        are_floats = False
    return are_floats


class Xyz:
    def __init__(self, file_name):
        self.file_name = file_name
        self.velocities = False

    def _allocate_arrays(self):
        self.type = np.zeros(self.n_particles)
        self.time = np.zeros(self.n_time_steps_)
        self.x = np.zeros(shape=(self.n_time_steps_, self.n_particles))
        self.y = np.zeros(shape=(self.n_time_steps_, self.n_particles))
        self.z = np.zeros(shape=(self.n_time_steps_, self.n_particles))
        if self.velocities:
            self.vx = np.zeros(shape=(self.n_time_steps_, self.n_particles))
            self.vy = np.zeros(shape=(self.n_time_steps_, self.n_particles))
            self.vz = np.zeros(shape=(self.n_time_steps_, self.n_particles))

    def _parse_comment_first(self, line):
        line = line.split()
        recognized = True
        self.box = [None, None, None]
        if len(line) == 4:
            if not _are_floats(*tuple(line)):
                recognized = False
            else:
                self.time[0] = float(line[0])
                self.box = [float(line[1]), float(line[2]), float(line[3])]
        elif len(line) == 3:
            recognized = False
            if _are_floats(*tuple(line)):
                self.box = [float(line[0]), float(line[1]), float(line[2])]
        else:
            recognized = False
        if self.box[0] is not None:
            self.box = np.array(self.box)
        self.comment_format_known = recognized

    def _parse_types(self, in_file):
        in_file.seek(0)  # Reset position to the start of the file
        self.type_dict = {}
        ind = 0
        for _ in range(2):
            line = in_file.readline()
        for i in range(self.n_particles):
            line = in_file.readline().split()
            t = line[0]
            if t not in self.type_dict:
                self.type_dict[t] = ind
                ind += 1
            self.type[i] = self.type_dict[t]

    def read_file(self, file_name=None, save=True, silent=False):
        if file_name is not None:
            self.file_name = file_name
        if not silent:
            print('Loading fort.8 data from file:\n'
                  + os.path.abspath(self.file_name))

        # Go through the file initally and just count the number of lines.
        with open(self.file_name, 'r') as in_file:
            self.num_lines = sum(1 for line in in_file)

        with open(self.file_name, 'r') as in_file:
            for _ in range(3):
                line = in_file.readline()
            if len(line.split()) == 7:
                self.velocities = True
            in_file.seek(0)

            self.n_particles = int(in_file.readline())
            self.n_time_steps_ = self.num_lines // self.n_particles
            self._allocate_arrays()
            line = in_file.readline()
            self._parse_comment_first(line)
            self._parse_types(in_file)

            in_file.seek(0)
            if silent:
                range_obj = range(self.n_time_steps_)
            else:
                range_obj = tqdm(range(self.n_time_steps_))

            for time_step in range_obj:
                for _ in range(2):
                    line = in_file.readline()
                if self.comment_format_known:
                    self.time[time_step] = float(line.split()[0])
                for i in range(self.n_particles):
                    line = in_file.readline().split()
                    self.x[time_step, i] = float(line[1])
                    self.y[time_step, i] = float(line[2])
                    self.z[time_step, i] = float(line[3])

                    if self.velocities:
                        self.vx[time_step, i] = float(line[4])
                        self.vy[time_step, i] = float(line[5])
                        self.vz[time_step, i] = float(line[6])
