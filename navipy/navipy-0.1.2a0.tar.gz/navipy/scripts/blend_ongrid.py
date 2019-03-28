"""

"""
import sys
import os
import inspect
import pkg_resources
import tempfile
from navipy.scripts import parser_logger, args_to_logparam
# Following need to be imported in blender as well
import yaml
import numpy as np
from navipy.sensors.renderer import BlenderRender
from navipy.maths import constants as mconst
from navipy import logger


importwithinblender = [
    'import yaml',
    'import numpy as np',
    'from navipy.sensors.renderer import BlenderRender',
    'from navipy.maths import constants as mconst',
    'from navipy import logger']


def parser_blend_ongrid():
    # Create command line options
    parser = parser_logger()
    arghelp = 'Path to the environment (.blend) in which your agent lives'
    defaultworld = pkg_resources.resource_filename(
        'navipy', 'resources/twocylinders_world.blend')
    defaultconfig = pkg_resources.resource_filename(
        'navipy', 'resources/configs/BlenderOnGridRender.yaml')
    defaultoutput = tempfile.NamedTemporaryFile().name + '.db'
    parser.add_argument('--blender-world',
                        type=str,
                        default=defaultworld,
                        help=arghelp)
    arghelp = 'Outputfile to store the rendered database'
    parser.add_argument('--output-file',
                        type=str,
                        default=defaultoutput,
                        help=arghelp)
    arghelp = 'Configuration file'
    parser.add_argument('--config-file',
                        type=str,
                        default=defaultconfig,
                        help=arghelp)
    arghelp = 'Command to run blender\n'
    arghelp += 'If not provided, the script will try to find the command'
    arghelp += " by using: shutil.which('blender')"
    parser.add_argument('--blender-command',
                        type=str,
                        default=None,
                        help=arghelp)

    return parser


def run(config_file, outputfile, level, logfile):
    logger(level, logfile)
    renderer = BlenderRender()
    renderer.config_file = config_file
    try:
        with open(config_file, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    except IOError:
        print("The file could not be read")
    if 'OnGrid' not in config.keys():
        raise KeyError(
            'OnGrid should be a section in the yaml config file')
    ongrid_config = config['OnGrid']
    grid_param = dict()
    for val in ['x', 'y', 'z']:
        if val in ongrid_config.keys():
            xs = ongrid_config[val]
            if len(xs) != 3:
                raise ValueError(
                    '{} should have 3 values (min, max, nsample)'.format(val))
            grid_param[val] = np.linspace(xs[0], xs[1], xs[2])
        else:
            raise KeyError('Yaml config file should contain {}'.format(val))
    if 'rotconv' in ongrid_config.keys():
        rotconv = ongrid_config['rotconv']
        if (rotconv in mconst._AXES2TUPLE) or (rotconv == 'quaternion'):
            for ii in range(3):
                val_a = 'alpha_{}'.format(ii)
                val_q = 'q_{}'.format(ii)
                if val_a in ongrid_config.keys():
                    xs = ongrid_config[val_a]
                    if len(xs) != 3:
                        msg = '{} should have 3 values (min, max, nsample)'
                        msg = msg.format(val_a)
                        raise ValueError(msg)
                    grid_param[val_a] = np.linspace(xs[0], xs[1], xs[2])
                elif val_q in ongrid_config.keys():
                    xs = ongrid_config[val_q]
                    if len(xs) != 3:
                        msg = '{} should have 3 values (min, max, nsample)'
                        msg = msg.format(val_q)
                        raise ValueError(msg)
                    grid_param[val_q] = np.linspace(xs[0], xs[1], xs[2])
                else:
                    msg = 'Yaml config file should contain {} or {}'
                    msg = msg.format(val_a, val_q)
                    raise KeyError(msg)
            if rotconv == 'quaternion':
                val_q = 'q_{}'.format(3)
                if val_q in ongrid_config.keys():
                    xs = ongrid_config[val_q]
                    if len(xs) != 3:
                        msg = '{} should have 3 values (min, max, nsample)'
                        msg = msg.format(val_q)
                        raise ValueError(msg)
                    grid_param[val_q] = np.linspace(xs[0], xs[1], xs[2])
                else:
                    msg = 'Yaml config file should contain {}'
                    msg = msg.format(val_q)
                    raise KeyError(msg)
    else:
        raise KeyError('Yaml config file should contain {}'.format(rotconv))
    renderer.render_ongrid(outputfile, rotconv=rotconv, **grid_param)


def main():
    # encoding for temporary file
    encoding = 'utf-8'

    # Fetch arguments
    args = parser_blend_ongrid().parse_args()
    loglevel, logfile = args_to_logparam(args)
    # Some output
    print('-----')
    print('Config file:\n{}'.format(args.config_file))
    print('Blender file:\n{}'.format(args.blender_world))
    print('Output file:\n{}'.format(args.output_file))
    print('-----')
    # Create tempfile with testing code and then call blendnavipy
    header = '# Generated by {}\n'.format(sys.argv[0])
    with tempfile.NamedTemporaryFile() as tfile:
        # Start of file
        tfile.write(header.encode(encoding))
        for line in importwithinblender:
            tfile.write(line.encode(encoding))
            tfile.write('\n'.encode(encoding))
        for line in inspect.getsourcelines(run)[0]:
            tfile.write(line.encode(encoding))
        tfile.write('\n\n'.encode(encoding))
        tfile.write('try:\n'.encode(encoding))
        tfile.write('     run("{}","{}",{},"{}")\n'.format(
            args.config_file, args.output_file, loglevel,
            logfile).encode(encoding))
        tfile.write('     sys.exit(0)\n'.encode(encoding))
        tfile.write('except Exception:\n'.encode(encoding))
        tfile.write('     sys.exit(1)\n'.encode(encoding))
        tfile.seek(0)

        command = 'blendnavipy --background '
        command += '--blender-world {} --python-script {}'
        command = command.format(args.blender_world, tfile.name)
        if args.blender_command is not None:
            command += ' --blender-command {}'.format(args.blender_command)
        for _ in range(args.verbose):
            command += ' -v'
        os.system(command)


if __name__ == "__main__":
    # execute only if run as a script
    main()
