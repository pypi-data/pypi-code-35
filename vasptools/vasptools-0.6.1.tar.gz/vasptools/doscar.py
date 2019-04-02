"""
vasptools doscar module
"""



import os
from . import vasprun
# from .ext_types import ExtDict
from . import atom_selector

MOD_NAME = DOSCAR_STRING = 'doscar'
DOSCAR_SECTION_STRING = '['+DOSCAR_STRING+']'
SUPPORTED_ANGULAR_MOMENTUM = ['s', 'px', 'py', 'pz',\
    'dxy', 'dxz', 'dyz', 'dz2', 'x2-y2']



def parse_doscar(doscar=None, force_basic_parser=False):
    """
    parse doscar file to a dict using configparser
    """
    doscar = doscar or DOSCAR_STRING
    assert isinstance(doscar, str) and os.path.exists(doscar),\
        'DOSCAR file should be given'
    if not force_basic_parser and vasprun.find_vasprun(doscar):
        return vasprun.connection_with_other_file(doscar)
    raise NotImplementedError("Parse DOSCAR directly not support!")


def preview_parse_doscar(doscar=None):
    """
    preview the dict parsed
    """
    print(parse_doscar(doscar))

def generate_picture(args):
    import matplotlib.pyplot as plt
    sdict = parse_doscar(args.filename, args.basic_parser)
    symbols = sdict['symbols']
    positions = sdict['positions']
    if args.angular_momentum:
        dos_type = 'partial'
        label_fmt = '{2}{3} {0} {1}'
        if not isinstance(args.angular_momentum, (list, tuple)):
            args.angular_momentum = [args.angular_momentum]
        assert all([am in SUPPORTED_ANGULAR_MOMENTUM \
            for am in args.angular_momentum]), \
            'only {0} are supported'.format(SUPPORTED_ANGULAR_MOMENTUM)
        select_atoms = atom_selector.select_atoms(symbols, \
                            positions, args.atoms,\
                            (args.xregion, args.yregion, args.zregion))
    else:
        dos_type = 'total'
        label_fmt = '{0} {1}'
        select_atoms = [0]
        args.angular_momentum = ['total']
    args.spin_type = args.spin_type or ['spin1']
    basepath = '/calc_arrays/dos/{0}'.format(dos_type)
    for angular in args.angular_momentum:
        if args.figsize:
            plt.figure(figsize=args.figsize)
        else:
            plt.figure()
        title = args.title or 'DOS: {0} of {1}'.format(angular, 'system')
        for atomi in select_atoms:
            for spin_type in args.spin_type:
                direction = 1
                if spin_type == 'spin2' and 'spin1' in args.spin_type:
                    direction = -1
                label = label_fmt.format(dos_type, spin_type, atomi%len(symbols), symbols[atomi])
                x = sdict['{0}/{1}/energy'.format(basepath, spin_type)]
                if x.ndim > 1:
                    x = x[atomi]
                if spin_type in ['spin1', 'spin2']:
                    y = sdict['{0}/{1}/{2}'.format(basepath, spin_type, angular)]
                else:
                    y = sdict['{0}/{1}/{2}'.format(basepath, 'spin1', angular)] -\
                        sdict['{0}/{1}/{2}'.format(basepath, 'spin2', angular)]
                if y.ndim > 1:
                    y = y[atomi]
                plt.plot(x, direction * y, label=label)
        if args.xlim:
            plt.xlim(args.xlim)
        if args.ylim:
            plt.ylim(args.ylim)
        plt.title(title)
        plt.legend()
        if not args.preview:
            plt.savefig('{0}/{1}.png'.format(args.outputdir, title))






def test(test_dir=None):
    """
    Test doscar
    """
    class Args(object):
        def __init__(self, **kwargs):
            for key, val in kwargs.items():
                setattr(self, key, val)
        def __getattr__(self, name):
            if not name in self.__dict__:
                return None
            return super(Args, self).__getattribute__(name)

    test_dir = test_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    assert isinstance(test_dir, str) and os.path.isdir(test_dir), \
        'test_dir: {0}\nYou need to git clone the repo and run the test'.format(test_dir)
    doscar = os.path.join(test_dir, 'DOSCAR')
    doscar_dict = parse_doscar(doscar)
    preview_parse_doscar(doscar)
    print(doscar_dict)
    test_cases = [
        {
            'filename': doscar,
            'xlim' : (-5, 1),
            'atoms' : [-1],
            'angular_momentum' : 'dz2',
        },
        {
            'filename': doscar,
            'xlim' : (-5, 1),
            'ylim' : (0, 10),
            'title' : '2',
            'atoms' : None,
        },
        {
            'filename': doscar,
            'title' : '3',
            'atoms' : [-1],
            'spin_type' : ['spin2'],
        },
        {
            'filename': doscar,
            'atoms' : ['O'],
            'title' : '4',
            'yregion' : (5, float('inf')),
        },
        ]
    for case in test_cases:
        case['outputdir'] = '/tmp'
        args = Args(**case)
        generate_picture(args)




def cli_add_parser(subparsers):
    """
    potcar add_parser
    """
    subp = subparsers.add_parser(MOD_NAME, help='DOSCAR')
    subp.add_argument('filename', metavar='PATH', help='DOSCAR filename')
    subp.add_argument('--outputdir', nargs=1, metavar='PATH', default='.', help='output directory')
    subp.add_argument('--title', metavar='string', help='title of picture')
    subp.add_argument('--atoms', nargs='*', help='generate picture')
    subp.add_argument('--xlim', nargs=2, metavar='float', help='xlimit of picture')
    subp.add_argument('--ylim', nargs=2, metavar='float', help='ylimit of picture')
    subp.add_argument('-a', '--angular_momentum', nargs='*', 
                      help='selected angular momentum, supports:{0}'.format(SUPPORTED_ANGULAR_MOMENTUM ))
    subp.add_argument('--spin_type', nargs='*', metavar='float', help='ylimit of picture')
    subp.add_argument('--xregion', nargs=2, metavar='float', help='x region of system')
    subp.add_argument('--yregion', nargs=2, metavar='float', help='y region of system')
    subp.add_argument('--zregion', nargs=2, metavar='float', help='z region of system')


def cli_args_exec(args):
    """
    potcar args_exec
    """
    if args.DEBUG:
        print(__file__)
    if args.test:
        test(args.test_dir)
    else:
        generate_picture(args)
