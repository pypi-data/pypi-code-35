import json
from abc import ABC, abstractmethod

from cliff.command import Command


class BaseCommand(ABC, Command):
    @abstractmethod
    def do_take_action(self, parsed_args):
        pass

    def take_action(self, parsed_args):
        _json = self.do_take_action(parsed_args=parsed_args)
        _str = '{}\n'.format(json.dumps(obj=_json, ensure_ascii=False,
                                        indent=4))
        self.app.stdout.write(_str)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument('--debug', required=False)
        parser.add_argument('--request-timeout', required=False, type=int)
        parser.add_argument('--pescatore-base-url', required=False)
        parser.add_argument('--pescatore-cli-jwt-header', required=False)
        parser.add_argument('--pescatore-cli-jwt', required=False)
        parser.add_argument('--pescatore-cli-api-key-header', required=False)
        parser.add_argument('--pescatore-cli-api-key', required=False)

        return parser
