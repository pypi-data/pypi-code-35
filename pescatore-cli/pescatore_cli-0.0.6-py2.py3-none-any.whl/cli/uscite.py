from .commons import BaseCommand
from ..api import uscite as uscite_api


class List(BaseCommand):
    """
    List Uscite
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--page', required=False)
        parser.add_argument('--ipp', required=False)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        return uscite_api.list(
            page=parsed_args.page,
            items_per_page=parsed_args.ipp,
            consumer_id=parsed_args.consumer_id)

class Create(BaseCommand):
    """
    Create Uscita
    """

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--licenza', required=True)
        parser.add_argument('--esca', required=True)
        parser.add_argument('--intervallo', type=int, required=False, default=5)
        parser.add_argument('--note', required=False)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj = vars(parsed_args)
        consumer_id = obj.pop('consumer_id', None)

        obj = dict([(k, v) for k, v in obj.items() if v is not None])

        return uscite_api.create(obj, consumer_id=consumer_id)

class Read(BaseCommand):
    """
    Get Uscita
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return uscite_api.read(obj_id=obj_id,
                               consumer_id=parsed_args.consumer_id)

class Delete(BaseCommand):
    """
    Delete Uscita
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return uscite_api.delete(obj_id=obj_id,
                                 consumer_id=parsed_args.consumer_id)

class ListPesci(BaseCommand):
    """
    List Pesci Uscita
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)
        parser.add_argument('--page', required=False)
        parser.add_argument('--ipp', required=False)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return uscite_api.list_pesci(obj_id=obj_id,
                                     page=parsed_args.page,
                                     items_per_page=parsed_args.ipp,
                                     consumer_id=parsed_args.consumer_id)
