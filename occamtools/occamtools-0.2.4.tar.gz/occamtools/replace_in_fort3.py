import os
from copy import deepcopy
import numpy as np


class _Properties:
    ATOM_TYPE = 0
    BOND_TYPE = 1
    BOND_ANGLE = 2
    TORSION = 3
    NON_BONDED = 4
    SCF = 5
    COMPRESSIBILITY = 6
    CHI = 7

    @staticmethod
    def _type_from_index(index):
        for v in _Properties.__dict__:
            if not v.startswith('__'):
                if _Properties.__dict__[v] == index:
                    return v
        raise IndexError(f'Property index {index} not valid. Expected:\n'
                         '0 <= index <= 7')


class Fort3Replacement:
    def __init__(self, property=None, replace=None, new=None, content=None):
        self._content = content

        if property is not None:
            self._parse_property_name(property)
        else:
            self.property = property

        if isinstance(replace, bool) and isinstance(new, bool):
            if replace is new:
                raise ValueError('Replace and new cannot both be ' + str(new))
            else:
                self._new = new
                self._replace = replace
        elif isinstance(replace, bool) or isinstance(new, bool):
            if isinstance(replace, bool):
                self._replace = replace
                self._new = not replace
            else:
                self._new = new
                self._replace = not new
        elif (new is None) and (replace is None):
            self._new = new
            self._replace = replace
        else:
            raise TypeError('Expected None or bool for new and replace, not '
                            + str(type(new)) + ' and ' + str(type(replace)))

    @property
    def new(self):
        return self._new

    @new.setter
    def new(self, new):
        if not isinstance(new, bool):
            raise TypeError('Expected bool for new, got ' + str(type(new)))
        self._new = new
        self._replace = not new

    @property
    def replace(self):
        return self._replace

    @replace.setter
    def replace(self, replace):
        if not isinstance(replace, bool):
            raise TypeError('Expected bool for replace, got '
                            + str(type(replace)))
        self._replace = replace
        self._new = not replace

    def _parse_property_name(self, prop):
        p = prop.lower()
        if 'atom' in p:
            self.property = _Properties.ATOM_TYPE
        elif 'bond' in p and 'type' in p:
            self.property = _Properties.BOND_TYPE
        elif 'angle' in p:
            self.property = _Properties.BOND_ANGLE
        elif 'torsion' in p:
            self.property = _Properties.TORSION
        elif 'non' in p and 'bond' in p:
            self.property = _Properties.NON_BONDED
        elif 'scf' in p or 'hpf' in p:
            self.property = _Properties.SCF
        elif 'comp' in p or 'kappa' in p:
            self.property = _Properties.COMPRESSIBILITY
        elif 'chi' in p:
            self.property = _Properties.CHI
        else:
            error_string = ('Property string ' + str(property) + ' was not'
                            ' recognized')
            raise ValueError(error_string)

    def __repr__(self):
        prop_type = _Properties._type_from_index(self.property)
        return (f'Fort3Replacement(property={prop_type}, '
                f'replace={self._replace}, new={self._new}, '
                f'content={self._content})')


def _count_property_instances(*args):
    counts = {key: 0 for key in range(5)}
    for p in args:
        if (p.new is True) and (p.property <= 4):
            counts[p.property] += 1
    return counts


def _is_int(s):
    try:
        s = float(s)
        if s.is_integer():
            return True
        else:
            return False
    except ValueError:
        return False


def _count_existing_instances(fort_file):
    keys = ['atom types', 'bond types', 'bond angles', 'torsions', 'non-bond']
    counts = {key: 0 for key in range(5)}
    with open(fort_file, 'r') as in_file:
        for line in in_file:
            sline = line.split()
            if len(sline) > 1:
                if _is_int(sline[0]):
                    for i, key in enumerate(keys):
                        if key in line:
                            counts[i] = int(sline[0])
                            break
    return counts


def _parse_fort_3_file(fort_file):
    atom_name = {}
    atoms = []
    bonds = []
    angles = []
    torsions = []
    non_bonds = []

    with open(fort_file, 'r') as in_file:
        for _ in range(4):
            line = in_file.readline()
        while '*****' not in line:  # atom types
            index, name, mass, charge = line.split()
            index, mass, charge = int(index), float(mass), float(charge)
            atom_name[index] = name
            atoms.append(Fort3Replacement(property='atom', new=True,
                                          content=[name, mass, charge]))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # bond types
            index_1, index_2, sigma, eps = line.split()
            index_1, index_2 = int(index_1), int(index_2)
            sigma, eps = float(sigma), float(eps)
            content = [atom_name[index_1], atom_name[index_2], sigma, eps]
            bonds.append(Fort3Replacement(property='bond type', new=True,
                                          content=content))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # bond angles
            ind1, ind2, ind3, theta, eps = line.split()
            ind1, ind2, ind3 = (int(i) for i in (ind1, ind2, ind3))
            theta, eps = float(theta), float(eps)
            content = [atom_name[ind1], atom_name[ind2], atom_name[ind3],
                       theta, eps]
            angles.append(Fort3Replacement(property='bond angle', new=True,
                                           content=content))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # torsions
            ind1, ind2, ind3, ind4, phi, eps = line.split()
            ind1, ind2, ind3, ind4 = (int(i) for i in (ind1, ind2, ind3, ind4))
            phi, eps = float(phi), float(eps)
            content = [atom_name[ind1], atom_name[ind2], atom_name[ind3],
                       atom_name[ind4], phi, eps]
            torsions.append(Fort3Replacement(property='bond angle', new=True,
                                             content=content))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # non-bonded interactions
            index_1, index_2, sigma, eps = line.split()
            index_1, index_2 = int(index_1), int(index_2)
            sigma, eps = float(sigma), float(eps)
            content = [atom_name[index_1], atom_name[index_2], sigma, eps]
            non_bonds.append(Fort3Replacement(property='non bonded', new=True,
                                              content=content))
            line = in_file.readline()

        for _ in range(2):
            line = in_file.readline()
        scf = [int(i) for i in line.split()]
        for _ in range(2):
            line = in_file.readline()
        kappa = float(line)
        line = in_file.readline()
        chi = np.empty(shape=(len(atom_name), len(atom_name)))
        for i in range(chi.shape[1]):
            sline = in_file.readline().split()
            chi[i, :] = np.asarray([float(s) for s in sline])

        return (atom_name, atoms, bonds, angles, torsions, non_bonds, scf,
                kappa, chi)


def _sort_new_replace_args_atom(atom_names_, atoms_, *args):
    atom_names = deepcopy(atom_names_)
    atoms = deepcopy(atoms_)
    for arg in args:
        if arg.property == _Properties.ATOM_TYPE:
            if len(arg._content) != 3:
                error_str = (f'Invalid content for replacement object '
                             f'{repr(arg)}, the content kwarg must have length'
                             f'3, not {len(arg._content)}')
                raise ValueError()
            name = arg._content[0]
            found = False
            index = None
            for i, atom in enumerate(atoms):
                if name == atom._content[0]:
                    found = True
                    index = i
                    break
            if found and (arg.replace is True):
                atoms[index] = arg
            elif found and (arg.new is True):
                error_str = (f'Cannot add atom type {repr(arg)}, a type of '
                             f'this name already exists')
                raise ValueError(error_str)
            elif (not found) and (arg.new is True):
                atoms.append(arg)
                atom_names[max(atom_names)+1] = arg._content[0]
            elif (not found) and (arg.replace is True):
                error_str = (f'No existing atom with name {name} was '
                             f'found to replace with {repr(args)}')
                raise ValueError(error_str)
    return atom_names, atoms


def _sort_new_replace_args_bonds(atom_names_, bonds_, *args, non_bond=False):
    atom_names = deepcopy(atom_names_)
    bonds = deepcopy(bonds_)
    check_prop = _Properties.NON_BONDED if non_bond else _Properties.BOND_TYPE
    for arg in args:
        if arg.property == check_prop:
            if len(arg._content) != 4:
                error_str = (f'Invalid content for replacement object '
                             f'{repr(arg)}, the content kwarg must have length'
                             f'4, not {len(arg._content)}')
                raise ValueError()
            name_1, name_2 = arg._content[:2]
            if name_1 not in atom_names.values():
                error_str = (f'Cannot establish bond type {repr(arg)}, '
                             f'between atoms {name_1} and {name_2}. {name_1} '
                             f'not found in atom dict: {atom_names}.')
                raise ValueError(error_str)
            elif name_2 not in atom_names.values():
                error_str = (f'Cannot establish bond type {repr(arg)}, '
                             f'between atoms {name_1} and {name_2}. {name_2} '
                             f'not found in atom dict: {atom_names}.')
                raise ValueError(error_str)

            found = False
            index = None
            for i, bond in enumerate(bonds):
                n1, n2 = bond._content[:2]
                if (((name_1 == n1) and (name_2 == n2)) or
                        ((name_1 == n2) and (name_2 == n1))):
                    found = True
                    index = i
                    break
            if found and (arg.replace is True):
                bonds[index] = arg
            elif found and (arg.new is True):
                error_str = (f'Cannot add bond type {repr(arg)}, a bond '
                             f' between {name_1} and {name_2} already exists')
                raise ValueError(error_str)
            elif (not found) and (arg.new is True):
                bonds.append(arg)
            elif (not found) and (arg.replace is True):
                error_str = (f'No existing bond between {name_1} and {name_2} '
                             f'was found to replace with {repr(arg)}')
                raise ValueError(error_str)
    return bonds


def _sort_new_replace_args_angles(atom_names_, angles_, *args):
    atom_names = deepcopy(atom_names_)
    angles = deepcopy(angles_)
    for arg in args:
        if arg.property == _Properties.BOND_ANGLE:
            if len(arg._content) != 5:
                error_str = (f'Invalid content for replacement object '
                             f'{repr(arg)}, the content kwarg must have length'
                             f' 5, not {len(arg._content)}')
                raise ValueError()
            name_1, name_2, name_3 = arg._content[:3]
            if name_1 not in atom_names.values():
                error_str = (f'Cannot establish bond angle {repr(arg)}, '
                             f'between atoms {name_1}, {name_2}, and {name_3}.'
                             f' {name_1} not found in atom dict: {atom_names}')
                raise ValueError(error_str)
            elif name_2 not in atom_names.values():
                error_str = (f'Cannot establish bond angle {repr(arg)}, '
                             f'between atoms {name_1}, {name_2}, and {name_3}.'
                             f' {name_2} not found in atom dict: {atom_names}')
                raise ValueError(error_str)
            elif name_3 not in atom_names.values():
                error_str = (f'Cannot establish bond angle {repr(arg)}, '
                             f'between atoms {name_1}, {name_2}, and {name_3}.'
                             f' {name_3} not found in atom dict: {atom_names}')
                raise ValueError(error_str)
            found = False
            index = None
            for i, angle in enumerate(angles):
                n1, n2, n3 = angle._content[:3]
                if n2 == name_2:
                    if (name_1 == n1) and (name_3 == n3):
                        found = True
                        index = i
                        break
                    elif (name_1 == n3) and (name_3 == n1):
                        found = True
                        index = i
                        break
            if found and (arg.replace is True):
                angles[index] = arg
            elif found and (arg.new is True):
                error_str = (f'Cannot add angle type {repr(arg)}, an angle '
                             f' between {name_1}, {name_2}, and {name_3} '
                             f'already exists')
                raise ValueError(error_str)
            elif (not found) and (arg.new is True):
                angles.append(arg)
            elif (not found) and (arg.replace is True):
                error_str = (f'No existing angle between {name_1}, {name_2}, '
                             f'and {name_3} was found to replace with '
                             f'{repr(arg)}')
                raise ValueError(error_str)
    return angles


def _check_new_kappa(kappa_, *args):
    kappa = deepcopy(kappa_)
    for arg in args:
        if arg.property == _Properties.COMPRESSIBILITY:
            content = arg._content
            if (isinstance(content, list) or isinstance(content, tuple)
                    or hasattr(content, 'shape')):
                content = content[0]
            kappa = content
            break
    return kappa


def _write_fort3_from_replace_objects(atom_names, atoms, bonds, angles,
                                      torsions, non_bonds, scf, kappa, chi,
                                      old_atom_names, file_path):
    atom_indices = {val: key for key, val in atom_names.items()}
    with open(file_path, 'w') as out_file:
        out_file.write('******************* model file *******************\n')
        out_file.write(f'{len(atom_names)} different atom types\n')
        out_file.write('*label   name      mass   charge\n')
        for index in atom_names:
            out_file.write(f'{index:>5} {atom_names[index]:>7} ')
            for atom in atoms:
                if atom._content[0] == atom_names[index]:
                    mass = atom._content[1]
                    charge = atom._content[2]
                    out_file.write(f'{mass:>9.3f} {charge:>8.3f}\n')
        out_file.write('**************************************************\n')
        out_file.write(f'{len(bonds)} different bond types\n')
        out_file.write('*atom1   atom2   bond_length   force_constant\n')
        for bond in bonds:
            name_1, name_2 = bond._content[:2]
            i, j = atom_indices[name_1], atom_indices[name_2]
            sigma, eps = bond._content[2:]
            out_file.write(f'{i:>6} {j:>7} {sigma:>13.5f} {eps:>16.5f}\n')
        out_file.write('**************************************************\n')
        out_file.write(f'{len(angles)} different bond angles\n')
        out_file.write('*atom1   atom2   atom3   theta0(deg)   force_constant\n')  # noqa: E501
        for angle in angles:
            name_1, name_2, name_3 = angle._content[:3]
            i, j, k = (atom_indices[name_1], atom_indices[name_2],
                       atom_indices[name_3])
            theta, eps = angle._content[3:]
            out_file.write(f'{i:>6} {j:>7} {k:>7} {theta:>13.5f} {eps:>16.5f}\n')  # noqa: E501
        out_file.write('**************************************************\n')
        out_file.write(f'{len(torsions)} different torsions\n')
        out_file.write('*atom1   atom2    atom3   atom4         phi0   force_constant\n')  # noqa: E501
        for torsion in torsions:
            name_1, name_2, name_3, name_4 = torsion._content[:4]
            a, b, c, d = (atom_indices[name_1], atom_indices[name_2],
                          atom_indices[name_3], atom_indices[name_4])
            phi, eps = torsion._content[4:]
            out_file.write(f'{a:>6} {b:>7} {c:>7} {d:>7} {phi:>13.5f} {eps:>16.5f}\n')  # noqa: E501
        out_file.write('**************************************************\n')
        out_file.write(f'{len(non_bonds)} different non-bonded interactions\n')
        out_file.write('*atom1   atom2   sigma   epsilon\n')
        for nb in non_bonds:
            name_1, name_2 = nb._content[:2]
            i, j = atom_indices[name_1], atom_indices[name_2]
            sigma, eps = nb._content[2:]
            out_file.write(f'{i:>6} {j:>7} {sigma:>13.5f} {eps:>16.5f}\n')
        out_file.write('****************** SCF settings ******************\n')
        out_file.write('*   mx      my      mz  cells in  X Y Z directions\n')
        out_file.write(f'{scf[0]:>6} {scf[1]:>7} {scf[2]:>7}\n')
        out_file.write(f'* compressibility\n{kappa:>7.5f}\n')
        out_file.write(f'*chi (Z={chi.shape[0]})\n')
        for row in chi:
            for n in row:
                out_file.write(f'{n:>10.3f}')
            out_file.write('\n')


def _construct_new_chi(atom_names_, old_atom_names_, chi):
    if atom_names_ == old_atom_names_:
        return chi

    min_key = min(atom_names_.keys())
    if min_key > 0:
        atom_names = {key-min_key: val for key, val in atom_names_.items()}
    else:
        atom_names = deepcopy(atom_names_)

    min_key = min(old_atom_names_.keys())
    if min_key > 0:
        old_atom_names = {key-min_key: val for key, val in
                          old_atom_names_.items()}
    else:
        old_atom_names = deepcopy(old_atom_names_)

    old_to_new = {}
    key_list, val_list = list(atom_names.keys()), list(atom_names.values())
    for key, val in old_atom_names.items():
        old_to_new[key] = key_list[val_list.index(val)]

    n = len(atom_names)
    new_chi = np.ones(shape=(n, n)) * (-1)
    for (i, j), element in np.ndenumerate(chi):
        new_i, new_j = old_to_new[i], old_to_new[j]
        new_chi[new_i, new_j] = element

    return new_chi


def replace_in_fort3(input_file, output_path, *args):
    """Replace or add to an existing fort.3 file

    The output file is named <input_file_name>_new by default, if no other
    output name is supplied.

    The replacement specification is done using Fort3Replacement instances,
    any number of which may be given as positional arguments
    """
    if (output_path is None) or (output_path == ''):
        output_path = os.path.join(os.path.dirname(input_file),
                                   input_file + '_new')
    for arg in args:
        if (not arg.new) and (not arg.replace):
            error_str = (f'Property {repr(arg)} has neither the new or the'
                         ' replace flag set')
            raise ValueError(error_str)

    atom_names, atoms, bonds, angles, torsions, non_bonds, scf, kappa, chi = (
        _parse_fort_3_file(input_file)
    )
    old_atom_names = deepcopy(atom_names)
    atom_names, atoms = _sort_new_replace_args_atom(atom_names, atoms, *args)
    bonds = _sort_new_replace_args_bonds(atom_names, bonds, *args)
    angles = _sort_new_replace_args_angles(atom_names, angles, *args)
    non_bonds = _sort_new_replace_args_bonds(atom_names, non_bonds, *args,
                                             non_bond=True)
    kappa = _check_new_kappa(kappa, *args)
    chi = _construct_new_chi(atom_names, old_atom_names, chi)
    _write_fort3_from_replace_objects(atom_names, atoms, bonds, angles,
                                      torsions, non_bonds, scf, kappa, chi,
                                      old_atom_names, output_path)
    return output_path
