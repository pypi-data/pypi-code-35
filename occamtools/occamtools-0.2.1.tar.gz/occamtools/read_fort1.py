import os
from tqdm import tqdm


def _parse_bool(string):
    if string.lower() in ('yes', 'y', '1', 't', 'true'):
        return True
    elif string.lower() in ('no', 'n', '0', 'f', 'false'):
        return False
    else:
        raise ValueError(f"String not recognized as a boolean, {string}")


class Fort1:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'r') as in_file:
            self.file_contents = in_file.readlines()

    def _parse_line(self, line, index):
        if 'title' in line:
            self.title = self.file_contents[index+1].strip()
        elif 'atoms' in line:
            self.n_particles = int(self.file_contents[index+1].strip())
        elif 'cutoff' in line and 'nl' not in line:
            self.cutoff = float(self.file_contents[index+1].strip())
        elif 'nl_cutoff' in line:
            self.nl_cutoff = float(self.file_contents[index+1].strip())
        elif 'nl_size' in line:
            self.nl_size = int(self.file_contents[index+1].strip())
        elif 'time_step' in line:
            self.dt = float(self.file_contents[index+1].strip())
        elif 'number_of_steps' in line:
            self.n_time_steps = int(self.file_contents[index+1].strip())
        elif 'simulated_ensemble' in line:
            self.ensemble = self.file_contents[index+1].strip()
        elif 'angle_function' in line:
            self.angle_function = int(self.file_contents[index+1].strip())
        elif 'trj_print' in line:
            self.trj_print = int(self.file_contents[index+1].strip())
        elif 'out_print' in line:
            self.out_print = int(self.file_contents[index+1].strip())
        elif 'pbc_traj' in line:
            self.pbc_traj = _parse_bool(self.file_contents[index+1].strip())
        elif 'mean_field' in line:
            self.mean_field = self.file_contents[index+1].strip()
        elif 'num_config_acc' in line:
            self.num_config_acc = int(self.file_contents[index+1].strip())
        elif 'pot_calc_freq' in line:
            self.pot_calc_freq = int(self.file_contents[index+1].strip())
        elif 'temperature_coupl' in line:
            self.temperature_coupl = float(self.file_contents[index+1].strip())
        elif 'target_pressure' in line:
            self.target_pressure = float(self.file_contents[index+1].strip())
        elif 'pressure_coupling' in line:
            self.pressure_coupling = float(self.file_contents[index+1].strip())
        elif 'velocity_read' in line:
            self.velocity_read = _parse_bool(
                self.file_contents[index+1].strip()
            )
        elif 'target_temperature' in line:
            self.target_temperature = float(
                self.file_contents[index+1].split()[0]
            )
        elif 'collision_freq' in line:
            self.collision_frequency = float(
                self.file_contents[index+1].strip()
            )
        elif 'SCF_lattice_update' in line:
            self.density_lattice_update = int(
                self.file_contents[index+1].strip()
            )
        elif 'intra_nonbonded' in line:
            self.intra_nonbonded = _parse_bool(
                self.file_contents[index+1].strip()
            )
        elif 'adaptive' in line:
            self.adaptive = True
            next_line = self.file_contents[index+1].split()
            self.adaptive_region_start = float(next_line[0])
            self.adaptive_region_end = float(next_line[1])
            self.adaptive_transition_length = float(next_line[2])
        elif 'end' in line:
            pass
        else:
            raise ValueError(f"fort.1 line not recognized, {line}")

    def read_file(self, file_name=None, silent=False):
        if file_name is not None:
            self.file_name = file_name
            with open(self.file_name, 'r') as in_file:
                self.file_contents = in_file.readlines()
        if not silent:
            print('Loading fort.1 data from file:\n'
                  + os.path.abspath(self.file_name))

        if silent:
            enumerate_obj = enumerate(self.file_contents)
        else:
            enumerate_obj = enumerate(tqdm(self.file_contents))
        for i, line in enumerate_obj:
            if i % 2 == 0:
                self._parse_line(line, i)
