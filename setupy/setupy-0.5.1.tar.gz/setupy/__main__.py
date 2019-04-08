import argparse

from setupy.setupy import setupy

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--features', dest='features', nargs='*')
parser.add_argument('-s', '--setting', dest='settings', nargs='*')
parser.add_argument('--include-setting', dest='literal_settings', nargs='*')
parser.add_argument('--include-help', action='store_true', default=False)
parser.add_argument('--server', action='store_true', default=False)

args = parser.parse_args()

if (args.server):
    from setupy.server import app
    app.run()
else:
    # Depending on how the arguments are passed, there may
    # be one or more blank settings in this list of literal
    # settings.  Strip those out.
    literal_settings = filter(lambda x: x.strip() != "", args.literal_settings)

    print(setupy(
        settings=args.settings,
        features=args.features,
        literal_settings=literal_settings,
        include_help=args.include_help
    ))
