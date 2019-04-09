#	Copyright (C) 2019, Mentice AB
#	See accompanying LICENSE file

import os
import shlex

import click
import jsonmerge

import jobber as dj

@click.group(invoke_without_command = True)
@click.pass_context
@click.option('--version', is_flag=True, default=False, help='Print version and exit')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Print extra information during execution')
@click.option('--host', '-H', default='', help='Host URL')
@click.option('--reg', '-r', default='', help='Default registry to use')
@click.option('configs', '--config', '-c', multiple=True, help='Configuration names')
def cli(ctx, version, verbose, host, reg, configs):
	"""Machine learning with Docker"""
	global jobber

	if ctx.invoked_subcommand is None:
		if version:
			print('Docker-Jobber version {version}'.format(version = dj.__version__))
		else:
			print(cli.get_help(ctx))
			exit()
	if len(configs) > 0:
		config = dj.get_config(configs)
	else:
		config = dj.get_config()
	if verbose:
		config = jsonmerge.merge(config, {'verbose' : True})
	if host:
		config = jsonmerge.merge(config, {'host' : host})
	if reg:
		config = jsonmerge.merge(config, {'registry' : reg})
	jobber = dj.Jobber(config)

@cli.command()
@click.option('tags', '--tag', '-t', multiple=True)
@click.option('--file', '-f', help='Name of the Dockerfile (default: "Dockerfile")')
def build(tags, file):
	"""Build an experiment as a docker image
	"""
	exit(jobber.build_image(".", tags=tags, dockerfile=file))

@cli.command()
@click.argument('cmd', nargs=-1)
@click.option('--runtime', type=click.Choice(['runc', 'nvidia']), help='Docker runtime (default nvidia)')   # Passed as a string
@click.option('inputs', '--in', '-i', multiple=True, help='Input images(s)')
@click.option('--out', '-o', default='', help='Output image')
@click.option('result_image', '--result-image', '-ri', type=click.Choice(['none', 'success', 'always']), help='Create a result image on exit')
@click.option('--Xdocker', '-Xd', multiple=True, help='Pass options to docker command')
def run(cmd, runtime, inputs, out, result_image, xdocker):
	"""Run a Docker image; snapshot the file system at exit as a new image
	"""
	cmd = [s for item in cmd for s in shlex.split(item)]
	if len(cmd) == 0:
		image_name = os.path.basename(os.getcwd())    # Default name is directory name
	elif len(cmd) == 1:
		image_name = cmd[0]
	elif len(cmd) > 1:	# Override CMD
		image_name = cmd[0]
		jobber.config['cmd'] = cmd[1:]

	if runtime:
		jobber.config['runtime'] = runtime
	if len(inputs) > 0:
		jobber.config['inputs'] = inputs
	if out:
		jobber.config['out'] = out
	if result_image:
		jobber.config['result-image'] = result_image
	if len(xdocker) > 0:
		jobber.config['Xdocker'] = xdocker
	exit(jobber.run_image(image_name))
