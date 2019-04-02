from uliweb.core.commands import Command, get_input, get_answer

class MenuCommand(Command):
    name = 'menu'
    help = 'Display menu structure. If no menu_name, then display all menus.'
    args = '<menu_name>'

    def handle(self, options, global_options, *args):
        from . import print_menu

        self.get_application(global_options)
        if not args:
            args = [None]
        for x in args:
            print_menu(x, title=True, verbose=global_options.verbose)