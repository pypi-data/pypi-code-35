import logging

from cliff.command import Command


class Submit(Command):
    "Submits the current working directory to the batch processing system"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Submit, self).get_parser(prog_name)
        parser.add_argument('-t', '--ticket', nargs=1, required=True, help="Jira ticket identifier", type=str, dest='ticket')
        parser.add_argument('-d', '--description', nargs=1, required=True, help="A description of the job", type=str, dest='desc')
        return parser

    def take_action(self, parsed_args):
        ticket = parsed_args.ticket[0]
        desc = parsed_args.desc[0]
        self.log.debug('Ticket={} Desc={}'.format(ticket, desc))
        self.app.stdout.write('hi!\n')