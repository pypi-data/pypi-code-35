
import numpy as np
from occamtools.generate_fort5 import (_write_box, _write_n_particles,
                                       _write_molecule)
from occamtools.fort5_to_xyz import _ensure_inside_box


def _parse_comment_line(line):
    # Parses the comment line of xyz files to look for the simulation box size
    box = None
    line = line.split()
    if len(line) != 0:
        if len(line) == 3:
            if '#box:' in line[0]:
                line[0] = line[0].split("#box:")
                line[0] = line[0][1]
                box = line
            elif '#box' in line[0]:
                line[0] = line[0].split("#box")
                line[0] = line[0][1]
                box = line
            elif '#' in line[0]:
                line[0] = line[0].split("#")
                line[0] = line[0][1]
                box = line
            else:
                box = line
        elif len(line) == 4:
            if '#box:' == line[0]:
                box = line[1:]
            elif '#box' == line[0]:
                box = line[1:]
            elif "#" == line[0]:
                if 'box:' in line[1]:
                    line[1] = line[1].split('box:')
                    line[1] = line[1][1]
                    box = line[1:]
                elif 'box' in line[1]:
                    line[1] = line[1].split('box')
                    line[1] = line[1][1]
                    box = line[1:]
                else:
                    box = line[1:]
        elif len(line) == 5:
            box = line[2:]

    if box is not None:
        try:
            b = [float(b) for b in box]
            return b
        except ValueError:
            raise
    else:
        return None


def _check_box(file_box, arg_box):
    if file_box is None:
        if arg_box is None:
            raise ValueError("No box size found in comment string ",
                             " and no box size specified on cmd line.")
        else:
            box = arg_box
    else:
        if arg_box is not None:
            if not np.allclose(np.asarray(file_box),
                               np.asarray(arg_box)):
                fbox = file_box
                abox = arg_box
                raise ValueError("Specified cmd line box size "
                                 " does not match the one found in the "
                                 ".xyz file.\n"
                                 f"cmd:  {abox[0]} {abox[1]} {abox[2]}\n"
                                 f"file: {fbox[0]} {fbox[1]} {fbox[2]}\n")
            else:
                box = file_box
        else:
            box = file_box
    return box


def xyz_to_fort5(file_name, wrap, box, new_file_name='fort.5'):
    with open(file_name, 'r') as in_file, open(new_file_name, 'w') as out_file:
        line = in_file.readline()
        n_molecules = int(line.strip())
        line = in_file.readline()
        file_box = _parse_comment_line(line)
        box = _check_box(file_box, box)

        _write_box(out_file, box)
        _write_n_particles(out_file, n_molecules)

        for atom_ind in range(1, n_molecules+1):
            line = in_file.readline().split()
            label = line[0]
            pos = [float(l) for l in line[1:]]
            for i, x in enumerate(pos):
                pos[i] = _ensure_inside_box(x, box[i], wrap)
            x, y, z = pos
            _write_molecule(out_file, atom_ind, x, y, z, label=label)
    return new_file_name
