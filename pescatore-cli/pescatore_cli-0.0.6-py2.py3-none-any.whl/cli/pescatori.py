from .commons import BaseCommand
from ..api import pescatori as pescatori_api


class List(BaseCommand):
    """
    List Pescatori
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--page', required=False)
        parser.add_argument('--ipp', required=False)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        return pescatori_api.list(
            page=parsed_args.page,
            items_per_page=parsed_args.ipp,
            consumer_id=parsed_args.consumer_id)

class Read(BaseCommand):
    """
    Get Pescatore
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return pescatori_api.read(obj_id=obj_id,
                               consumer_id=parsed_args.consumer_id)
