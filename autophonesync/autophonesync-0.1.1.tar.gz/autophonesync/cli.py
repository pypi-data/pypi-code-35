import click
import configparser
import subprocess
import shutil
import sys
import re
from pathlib import Path
from .adb import AdbWrapper


class App:
    adb = None
    config = None

    def __init__(self):
        self.adb = AdbWrapper()

        self.config = configparser.ConfigParser(
            strict=True,
            interpolation=None,
        )
        cp = self._config_path()
        if cp.exists():
            self.config.read(cp)

    @staticmethod
    def _config_path():
        return Path.home() / '.config' / 'phonesync'

    def save_config(self):
        with open(self._config_path(), 'wt') as cf:
            self.config.write(cf)

    def device(self, serialnumber):
        return (
            self.adb.device(serialnumber),
            self.config.setdefault(serialnumber, {}),
        )


@click.group()
@click.pass_context
def phonesync(ctx):
    ctx.obj = App()


def _serials(app):
    for line in app.adb['devices'](no_empty=True):
        if '\t' not in line:
            continue
        serial, _ = line.split('\t', 1)
        yield serial


@phonesync.command()
@click.option('--configured/--no-configured', default=False, help='Include configured devices')
@click.option('--unconfigured/--no-unconfigured', default=True, help='Include unconfigured devices')
@click.pass_obj
def devices(app, configured, unconfigured):
    """
    List serial numbers of connected devices
    """
    for serial in _serials(app):
        if serial in app.config:
            if configured:
                click.echo(serial)
        else:
            if unconfigured:
                click.echo(serial)


def validate_serial_plugged_in(ctx, param, value):
    app = ctx.obj

    try:
        for _ in app.adb.device(value)['shell']('true'):
            pass
    except Exception:
        raise click.BadParameter("Phone {} not plugged in".format(value), param=param)
    else:
        return value


@phonesync.command()
@click.option('--serial', help="Phone's serial number", prompt=True, callback=validate_serial_plugged_in)
@click.option(
    '--path', type=click.Path(exists=True, file_okay=False, writable=True),
    help='Path to back up to', prompt=True
)
@click.pass_context
def add(ctx, serial, path):
    """
    Add a device to your configuration
    """
    app = ctx.obj
    if serial in app.config:
        ctx.fail("Phone {} already configured".format(serial))

    app.config[serial] = {
        'destination': path,
        'prescript': '',
        'postscript': '',
    }

    app.save_config()


@phonesync.command()
@click.argument('serial')  # Don't validate plugged in; we'll see soon enough
@click.pass_context
def run(ctx, serial):
    """
    Run a backup
    """
    app = ctx.obj

    adb, config = app.device(serial)

    if not config:
        ctx.fail("Device {} not configured".format(serial))

    if 'prescript' in config:
        subprocess.run(config['prescript'], shell=True, check=True)
    _iter_pull(adb['pull']('/sdcard', config['destination']))
    if 'postscript' in config:
        subprocess.run(config['postscript'], shell=True, check=True)


def _changed(gen):
    gen = iter(gen)
    prev = next(gen)
    yield prev
    for item in gen:
        if item != prev:
            yield item
        prev = item


def _iter_pull(output):
    lpat = re.compile(r"\[\s*(\d+)%] (.+): (\d+)%")
    with click.progressbar(
        map(lpat.match, output),
        label='Backing up',
        item_show_func=lambda m: m.group(2) if m is not None else '',
    ) as bar:
        for fname in _changed(m.group(2) for m in bar if m is not None):
            if bar.is_hidden:
                click.echo(fname)


@phonesync.command()
@click.pass_context
def install(ctx):
    """
    Install the udev rule for autophonesync
    """
    rulefile = Path("/etc/udev/rules.d/99-autophonesync.rules")
    cmd = shutil.which("autophonesync-udev-handler")
    if cmd is None:
        curfile = Path(sys.argv[0]).resolve()
        maybe = curfile.parent / "autophonesync-udev-handler"
        if maybe.exists():
            cmd = str(maybe)
    if cmd is None:
        ctx.fail("Cannot find autophonesync-udev-handler on your PATH")
    # FIXME: This rule might only be for debians?
    rules = 'ACTION=="bind", ENV{adb_user}=="yes", ENV{ID_SERIAL_SHORT}=="*?", RUN+="' + cmd + '"\n'

    if rulefile.exists():
        ctx.fail("Rules file already exists")

    rulefile.write_text(rules)


@phonesync.command()
@click.argument('serial')
@click.pass_context
def edit_pre(ctx, serial):
    """
    Edit the prescript of a phone
    """
    app = ctx.obj

    _, config = app.device(serial)

    if not config:
        ctx.fail("Device {} not configured".format(serial))

    newscript = click.edit(
        text=config.get('prescript', ''),
        extension='.sh',  # TODO: Detect non-bourne shells and pick an appropriate extension
    )

    if newscript is not None:
        config['prescript'] = newscript
        app.save_config()


@phonesync.command()
@click.argument('serial')
@click.pass_context
def edit_post(ctx, serial):
    """
    Edit the postscript of a phone
    """
    app = ctx.obj

    _, config = app.device(serial)

    if not config:
        ctx.fail("Device {} not configured".format(serial))

    newscript = click.edit(
        text=config.get('postscript', ''),
        extension='.sh',  # TODO: Detect non-bourne shells and pick an appropriate extension
    )

    if newscript is not None:
        config['postscript'] = newscript
        app.save_config()


if __name__ == '__main__':
    phonesync()
