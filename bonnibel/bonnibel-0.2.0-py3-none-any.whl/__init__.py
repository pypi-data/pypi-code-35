
def die(message):
    import sys
    print("Error: " + message, file=sys.stderr)
    sys.exit(1)


def get_template(env, typename, name):
    from jinja2.exceptions import TemplateNotFound
    try:
        return env.get_template("{}.{}.j2".format(typename, name))
    except TemplateNotFound:
        return env.get_template("{}.default.j2".format(typename))


def get_var_from_string(var):
    if not '=' in var:
        die("Missing var value {}".format(var))

    return var.split('=', 1)


def get_git_version():
    from subprocess import run
    cp = run(['git', 'describe', '--dirty'],
            check=True, capture_output=True)
    full_version = cp.stdout.decode('utf-8').strip()

    cp = run(['git', 'rev-parse', 'HEAD'],
            check=True, capture_output=True)
    full_sha = cp.stdout.decode('utf-8').strip()

    dirty = False
    parts1 = full_version.split('-')
    if parts1[-1] == "dirty":
        dirty = True
        parts1 = parts1[:-1]

    parts2 = parts1[0].split('.')

    from collections import namedtuple
    version = namedtuple('version',
        ['major', 'minor', 'patch', 'sha', 'dirty'])

    return version(
        parts2[0],
        parts2[1],
        parts2[2],
        full_sha[:7],
        dirty)


def generate(generator, buildroot, modulefile, args):
    import os
    from os.path import abspath, dirname, join
    from os.path import isabs, isdir, isfile, islink

    exeroot = dirname(__file__)

    srcroot = os.getcwd()
    if isfile(modulefile):
        modulefile = abspath(modulefile)
        srcroot = dirname(modulefile)
    else:
        die("Could not find module file.")

    if not isabs(buildroot):
        buildroot = join(srcroot, buildroot)

    if not isdir(buildroot):
        os.mkdir(buildroot)

    from .config import Config
    config = Config(modulefile)

    git_version = get_git_version()
    print("Generating build files for {} {}.{}.{}-{}...".format(
        config.name,
        git_version.major,
        git_version.minor,
        git_version.patch,
        git_version.sha))

    from jinja2 import Environment, FileSystemLoader
    template_path = [
        join(srcroot, config.templates),
        join(exeroot, "templates"),
    ]
    loader = FileSystemLoader(template_path)
    env = Environment(loader=loader)

    tvars = {}
    for var in args:
        tvars.update([get_var_from_string(var)])

    for var, value in config.vars.items():
        if var in tvars: continue
        tvars[var] = value

    buildfiles = []
    templates = set()

    for mod in config.modules.values():
        buildfile = join(buildroot, mod.name + ".ninja")
        buildfiles.append(buildfile)
        with open(buildfile, 'w') as out:
            template = get_template(env, mod.kind, mod.name)
            templates.add(template.filename)
            out.write(template.render(
                module=mod,
                buildfile=buildfile,
                vars=tvars,
                version=git_version))

    for target, mods in config.targets.items():
        root = join(buildroot, target)
        if not isdir(root):
            os.mkdir(root)

        buildfile = join(root, "target.ninja")
        buildfiles.append(buildfile)
        with open(buildfile, 'w') as out:
            template = get_template(env, "target", target)
            templates.add(template.filename)
            out.write(template.render(
                target=target,
                modules=mods,
                buildfile=buildfile,
                vars=tvars,
                version=git_version))

    # Top level buildfile cannot use an absolute path or ninja won't
    # reload itself properly on changes.
    # See: https://github.com/ninja-build/ninja/issues/1240
    buildfile = "build.ninja"
    buildfiles.append(buildfile)

    with open(join(buildroot, buildfile), 'w') as out:
        template = env.get_template("build.ninja.j2")
        templates.add(template.filename)

        out.write(template.render(
            targets=config.targets,
            buildroot=buildroot,
            srcroot=srcroot,
            buildfile=buildfile,
            buildfiles=buildfiles,
            templates=[abspath(f) for f in templates],
            generator=generator,
            modulefile=modulefile,
            vars=tvars,
            version=git_version))
