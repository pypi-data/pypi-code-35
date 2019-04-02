"""
format_string contain vasp-out
"""
from collections import OrderedDict
from .format_parser import datablock_to_numpy, xml_parameters
from .ext_types import ExtList, ExtDict


FORMAT_STRING = {
    'vasp-out': {
        'prefered' : 'vasp-xml',
        'file_format' : 'plain_text',
        'calculator' : 'VASP',
        'primitive_data': {
            r'free  energy   TOTEN\s*=\s*(.*?)\s+eV\s*\n' : {
                'important' : True,
                'selection' : -1,
                'type' : float,
                'key' : 'calc_arrays/freeE',
                },
            r'energy  without entropy=\s*(.*?)\s+' : {
                'important' : True,
                'selection' : -1,
                'type' : float,
                'key' : 'calc_arrays/E_without_S',
                },
            r'energy\(sigma->0\)\s*=\s*(.*)' : {
                'important' : True,
                'selection' : -1,
                'type' : float,
                'key' : 'calc_arrays/potential_energy',
                },
            r'ions per type\s*=\s*(.*)\n' : {
                'important' : True,
                'selection' : -1,
                'type' : list,
                'process' : lambda data, arrays: datablock_to_numpy(data).astype(int).flatten(),
                'key' : 'ions_per_type',
                },
            r'VRHFIN\s*=\s*(.*?):' : {
                'important' : True,
                'selection' : 'all',
                'type' : ExtList,
                'key' : 'elements_per_type',
                },
            r'POSITION\s*TOTAL-FORCE[\s\S]*?-{2,}\n([\s\S]*?)\n\s+-{2,}' : {
                'important' : True,
                'selection' : -1,
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'key' : [
                    {
                        'key' : 'positions',
                        'type': float,
                        'index': ':,:3'
                    },
                    {
                        'key' : 'calc_arrays/forces',
                        'type': float,
                        'index': ':,3:6'
                    },
                    ],
                },
            r'FORCES acting on ions[\s\S]*?-{2,}\n([\s\S]*?)\s+-{2,}': {
                'important' : True,
                'selection' : -1,
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'key': [
                    {
                        'key' : 'calc_arrays/forces_e_ion',
                        'type': float,
                        'index' : ':,0:3'
                    },
                    {
                        'key' : 'calc_arrays/forces_ewald',
                        'type': float,
                        'index' : ':,3:6'
                    },
                    {
                        'key' : 'calc_arrays/forces_nonlocal',
                        'type': float,
                        'index' : ':,6:9'
                    },
                    {
                        'key' : 'calc_arrays/forces_convergence_correction',
                        'type': float,
                        'index' : ':,9:12'
                    },
                    ],
                },
            },
        'synthesized_data' : {
            'symbols' : {
                'equation' : lambda arrays: arrays['elements_per_type'] * arrays['ions_per_type'],
                },
        },
    },
    'DOSCAR' : {
        'prefered' : 'vasp-xml',
        'file_format' : 'plain_text',
        'primitive_data' : {
            r'.*\n.*\n.*\n.*\n.*\n.*\n([\s\S]*)' : {
                'important' : True,
                'selection' : -1,
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'key' : 'calc_arrays/doscar',
            },
        },
        'synthesized_data' : {},
    },
    'vasp-xml' : {
        'file_format' : 'lxml',
        'primitive_data' : {
            '(//varray[@name="basis"])[last()]//v//text()' : {
                'important' : True,
                'join' : '\n',
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'key' : 'cell',
                },
            '(//varray[@name="positions"])[last()]//v//text()' : {
                'important' : True,
                'join' : '\n',
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'key' : 'cell_scaled_positions',
                'type' : float,
                },
            '//atominfo/array[@name="atoms"]/set/rc/c[1]/text()' : {
                'important' : True,
                'selection' : 'all',
                'key' : 'symbols',
                },
            '//atominfo/array[@name="atomtypes"]/set/rc/c[5]/text()' : {
                'important' : True,
                'selection' : 'all',
                'process' : lambda data, arrays: data.strip(),
                'type' : ExtList,
                'key' : 'vasp_pot',
                },
            '//dos/total/array/field/text()' : {
                'important' : False,
                'selection' : 'all',
                'process' : lambda data, arrays: data.strip(),
                'key' : 'dos_total_header',
                },
            '//dos/total/array/set/set[@comment="spin 1"]/r/text()' : {
                'important' : False,
                'join' : '\n',
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'type' : float,
                'key' : 'dos_total_spin1',
            },
            '//dos/total/array/set/set[@comment="spin 2"]/r/text()' : {
                'important' : False,
                'join' : '\n',
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'type' : float,
                'key' : 'dos_total_spin2',
            },
            '//dos/partial/array/field/text()' : {
                'important' : False,
                'selection' : 'all',
                'process' : lambda data, arrays: data.strip(),
                'key' : 'dos_partial_header',
                },
            '//dos/partial/array/set/set/set[@comment="spin 1"]/r/text()' : {
                'important' : False,
                'join' : '\n',
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'type' : float,
                'key' : 'dos_partial_spin1',
            },
            '//dos/partial/array/set/set/set[@comment="spin 2"]/r/text()' : {
                'important' : False,
                'join' : '\n',
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'type' : float,
                'key' : 'dos_partial_spin2',
            },
            '//parameters' : {
                'important' : True,
                'process' : lambda data, arrays: xml_parameters(data),
                'key' : 'calc_arrays/parameters',
            },
            '//generator' : {
                'important' : True,
                'process' : lambda data, arrays: xml_parameters(data),
                'key' : 'calc_arrays/calc_properties',
            },
            '//kpoints/varray[@name="kpointlist"]/v/text()' : {
                'important' : True,
                'process' : lambda data, arrays: datablock_to_numpy(data),
                'type' : float,
                'key' : 'calc_arrays/kpoints/kpointlist',
            },
            '//kpoints/varray[@name="weights"]/v/text()' : {
                'important' : True,
                'process' : lambda data, arrays: datablock_to_numpy(''.join(data)),
                'type' : float,
                'key' : 'calc_arrays/kpoints/weights',
            },
        },
        'synthesized_data' : OrderedDict({
            'calc_arrays/dos/partial/spin1' : {
                'prerequisite' : ['dos_partial_header', 'dos_partial_spin1'],
                'equation' : lambda arrays: dict(zip(arrays['dos_partial_header'], \
                    [arrays['dos_partial_spin1'][:,i].reshape((-1, len(arrays['dos_total_spin1']))) \
                        for i in range(len(arrays['dos_partial_header']))])),
                'delete' : ['dos_partial_spin1'],
            },
            'calc_arrays/dos/partial/spin2' : {
                'prerequisite' : ['dos_partial_header', 'dos_partial_spin2'],
                'equation' : lambda arrays: dict(zip(arrays['dos_partial_header'], \
                    [arrays['dos_partial_spin2'][:,i].reshape((-1, len(arrays['dos_total_spin1']))) \
                        for i in range(len(arrays['dos_partial_header']))])),
                'delete' : ['dos_partial_spin2'],
            },
            'calc_arrays/dos/total/spin1' : {
                'prerequisite' : ['dos_total_header', 'dos_total_spin1'],
                'equation' : lambda arrays: dict(zip(arrays['dos_total_header'], \
                    [arrays['dos_total_spin1'][:,i] for i in range(len(arrays['dos_total_header']))])),
                'delete' : ['dos_total_spin1'],
            },
            'calc_arrays/dos/total/spin2' : {
                'prerequisite' : ['dos_total_header', 'dos_total_spin2'],
                'equation' : lambda arrays: dict(zip(arrays['dos_total_header'], \
                    [arrays['dos_total_spin2'][:,i] for i in range(len(arrays['dos_total_header']))])),
                'delete' : ['dos_total_spin2'],
            },
            'positions' : {
                'prerequisite' : ['cell', 'cell_scaled_positions'],
                'equation' : lambda arrays: arrays['cell_scaled_positions'].dot(arrays['cell']),
                'delete' : ['cell_scaled_positions'],
                },
        }),
    }
}
