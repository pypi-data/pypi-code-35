

def _convert_file_name(in_file_name):
    if '.' in in_file_name:
        splitStr = in_file_name.split('.')
        no_extension = '.'.join(splitStr[:-1])
        new_file_name = no_extension + '.xyz'
    else:
        new_file_name = in_file_name + '.xyz'
    return new_file_name


def _ensure_inside_box(x, box, wrap):
    if wrap:
        while x > box:
            x -= box
        while x < 0.0:
            x += box
    return x


def fort5_to_xyz(file_name, wrap=True):
    xyz_file_name = _convert_file_name(file_name)

    with open(file_name, 'r') as in_file, open(xyz_file_name, 'w') as out_file:
        for _ in range(2):
            line = in_file.readline().split()
        box = [float(line[i]) for i in range(3)]

        for _ in range(2):
            line = in_file.readline().strip()
        n_particles = int(line)

        out_file.write(f'{n_particles}\n')
        out_file.write(f'# box: {box[0]:.15f} {box[1]:.15f} {box[2]:.15f}\n')

        for i in range(n_particles):
            for _ in range(3):
                line = in_file.readline()
            line = line.split()
            label = line[1]
            out_file.write(f'{label} ')
            for i, p in enumerate(line[4:7]):
                # Fortran scientific float output gives 1.2345D+02, convert to
                # 1.2345E+02 to allow python to parse it as a float.
                p = float(p.replace('D', 'E'))
                out_file.write('{pos:.15f} '.format(
                    pos=_ensure_inside_box(p, box[i], wrap))
                )
            out_file.write('\n')
    return xyz_file_name
