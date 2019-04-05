from click.parser import OptionParser
from click.core import Option
import shlex


class InputOptionParser(OptionParser):
    def add_option(self, dest, action=None, nargs=1, const=None, obj=None):
        """added support for +- flags"""
        if dest.startswith('+-') or dest.startswith('-+'):
            dest = '+' + dest.strip('+-')
            super().add_option([dest], dest, action, nargs, const, obj)
            dest = '-' + dest.strip('+-')
            super().add_option([dest], dest, action, nargs, const, obj)
        else:
            super().add_option([dest], dest, action, nargs, const, obj)


if __name__ == '__main__':
    o = InputOptionParser()
    o.add_option('-fetch', nargs=1, )

    o.add_option('-test', action='store_const',
                 const=True, )
    o.add_option('-default', nargs=-1, action='store')
    o.add_option('-fetch', nargs=1)
    o.add_option('+-strip', nargs=0)
    # o.add_option('-strip')
    # o.add_option(['-update'], 'update', 'store_const', const=True, nargs=0)
    o.add_option('-update', nargs=0)
    text = '-fetch foo bar qux -test -default 1 -test'
    print(o.parse_args(shlex.split(text)))
