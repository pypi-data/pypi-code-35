"""
Entry point for shelli cli
"""

import sys
from shelli import conf, target, cli_parser, execute

def main():
    """Does the things"""

    args = cli_parser.get()

    # Loads yml configuration. Without path argument, defaults to ~/.commander.yml
    yaml = conf.YAMLoader(path=args.config)
    targets = target.create_targets_from_yaml(yaml)

    target_found = False

    for targ in targets.values():
        if targ.name == args.target:
            target_found = True
            runner = execute.Executor(targ)
            runner.execute()

    if not target_found:
        sys.stderr.write("Target {target} not found!\n".format(target=args.target))
        exit(1)

if __file__ == '__main__':
    main()
