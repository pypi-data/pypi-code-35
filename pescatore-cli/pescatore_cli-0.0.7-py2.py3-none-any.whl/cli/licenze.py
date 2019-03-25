from .commons import BaseCommand
from ..api import licenze as licenze_api


class List(BaseCommand):
    """
    List Licenze
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--page', required=False)
        parser.add_argument('--ipp', required=False)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        return licenze_api.list(
            page=parsed_args.page,
            items_per_page=parsed_args.ipp,
            consumer_id=parsed_args.consumer_id)


class Create(BaseCommand):
    """
    Create Licenza
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--bacino', required=True)
        parser.add_argument('--consumer-key', required=False)
        parser.add_argument('--consumer-secret', required=False)
        parser.add_argument('--access-token', required=False)
        parser.add_argument('--access-token-secret', required=False)
        parser.add_argument('--url', required=False)
        parser.add_argument('--limite', required=False)
        parser.add_argument('--active', required=False, default=True)
        parser.add_argument('--is-public', required=False, default=False)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj = vars(parsed_args)
        consumer_id = obj.pop('consumer_id', None)

        obj = dict([(k, v) for k, v in obj.items() if v is not None])

        return licenze_api.create(obj, consumer_id=consumer_id)


class Read(BaseCommand):
    """
    Get Licenza
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return licenze_api.read(obj_id=obj_id,
                                consumer_id=parsed_args.consumer_id)


class Delete(BaseCommand):
    """
    Delete Licenza
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--id', required=True)
        parser.add_argument('--consumer-id', required=False)

        return parser

    def do_take_action(self, parsed_args):
        obj_id = parsed_args.id

        return licenze_api.delete(obj_id=obj_id,
                                  consumer_id=parsed_args.consumer_id)
