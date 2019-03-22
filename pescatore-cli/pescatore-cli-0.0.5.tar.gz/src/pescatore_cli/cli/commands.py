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
        parser.add_argument('--stringa', required=False)
        parser.add_argument('--note', required=False)
        parser.add_argument('--id-licenza', required=False)
        parser.add_argument('--id-esca', required=False)
        parser.add_argument('--id-consumer', required=False)
        parser.add_argument('--intervallo', type=int, default=5, required=False)

        return parser

    def do_take_action(self, parsed_args):
        if parsed_args.stringa is None and parsed_args.id_esca is None:
            raise RuntimeError('Either --stringa or --id-esca must be specified')

        return cerca_stringa_in_bacino(stringa=parsed_args.stringa,
                                       bacino=parsed_args.bacino,
                                       id_licenza=parsed_args.id_licenza,
                                       id_esca=parsed_args.id_esca,
                                       id_consumer=parsed_args.id_consumer,
                                       note=parsed_args.note,
                                       intervallo=parsed_args.intervallo)
