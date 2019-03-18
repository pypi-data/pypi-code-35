import logging

from .commons import BaseCommand
from ..functions import cerca_stringa_in_bacino


class CercaStringaInBacino(BaseCommand):
    """
    Cerca stringa in bacino
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--bacino', required=True)
        parser.add_argument('--stringa', required=True)
        parser.add_argument('--note', required=False)
        parser.add_argument('--id-licenza', required=False)
        parser.add_argument('--intervallo', type=int, default=5, required=False)

        return parser

    def do_take_action(self, parsed_args):
        return cerca_stringa_in_bacino(stringa=parsed_args.stringa,
                                       bacino=parsed_args.bacino,
                                       id_licenza=parsed_args.id_licenza,
                                       note=parsed_args.note,
                                       intervallo=parsed_args.intervallo)
