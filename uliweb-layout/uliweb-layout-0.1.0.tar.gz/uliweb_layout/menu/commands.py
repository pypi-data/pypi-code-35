from optparse import make_option
from uliweb.core.commands import Command, get_input, get_answer

class MenuCommand(Command):
    name = 'menu'
    help = 'Display menu structure or menu html. If no menu_name, then display all menus.'
    args = '<menu_name>'
    option_list = (
        make_option('--html', dest='html', action='store_true', default=False,
            help='Output rendered html of menus.'),
        make_option('-t', '--type', dest='type', default='side',
            help='Menu type will be used. Current support "main" and "side".'),
    )

    def handle(self, options, global_options, *args):
        from . import print_menu, print_menu_html

        self.get_application(global_options)
        if not args:
            args = [None]
        for x in args:
            if options.html:
                print_menu_html(x, type=options.type)
            else:
                print_menu(x, title=True, verbose=global_options.verbose)