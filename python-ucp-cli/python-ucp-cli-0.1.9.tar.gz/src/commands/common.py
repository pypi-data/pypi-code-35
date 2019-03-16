import click

class State(object):

    def __init__(self):
        self.verbosity = 0
        self.debug = False
        self.insecure_tls = False

pass_state = click.make_pass_decorator(State, ensure=True)

def verbosity_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.verbosity = value
        return value
    return click.option('-v', '--verbose', count=True,
                        expose_value=False,
                        help='Enable verbosity.',
                        callback=callback)(f)

def debug_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.debug = value
        return value
    return click.option('--debug/--no-debug',
                        expose_value=False,
                        help='Enables or disables debug mode.',
                        callback=callback)(f)

def insecure_tls_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.insecure_tls = value
        return value
    return click.option('--insecure-tls', count=True,
                        expose_value=False,
                        help='Enable insecure tls.',
                        callback=callback)(f)

def common_options(f):
    f = verbosity_option(f)
    f = debug_option(f)
    f = insecure_tls_option(f)
    return f
