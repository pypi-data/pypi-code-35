from .commons import BaseCommand
from ..api import esche as esche_api


class List(BaseCommand):
    """
    List Esche
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--page', required=False)
        parser.add_argument('--ipp', required=False)

        return parser

    def do_take_action(self, parsed_args):
        return esche_api.list(
            page=parsed_args.page,
            items_per_page=parsed_args.ipp)


class Create(BaseCommand):
    """
    Create Esca
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--hashtag', required=False)
        parser.add_argument('--lingua', required=False)
        parser.add_argument('--posizione', required=False)
        parser.add_argument('--regexp', required=False)
        parser.add_argument('--stringa', required=False)
        parser.add_argument('--url', required=False)
        parser.add_argument('--user-email', required=False)
        parser.add_argument('--user-id', required=False)
        parser.add_argument('--user-name', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj = vars(parsed_args)
        obj = dict([(k, v) for k, v in obj.items() if v is not None])

        return esche_api.create(obj)

class Read(BaseCommand):
    """
    Get Esca
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return esche_api.read(obj_id=obj_id)


class Delete(BaseCommand):
    """
    Delete Esca
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return esche_api.delete(obj_id=obj_id)
