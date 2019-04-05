from cliff.command import Command
import cray.jobs as jobs
import logging
import tempfile

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
        desc = parsed_args.desc[0].replace(" ", "_")
        jobID = '{}:{}'.format(ticket, desc)
        self.log.debug('Ticket={} Desc={} JobID={}'.format(ticket, desc, jobID))

        if jobs.exists(jobID):
            raise Exception("Duplicate job: '{}'".format(jobID))

        with tempfile.TemporaryDirectory() as tempdir:
            jobs.build_job_archive(tempdir)
            jobs.submit_job_zip('{}/job.zip'.format(tempdir), jobID)

        self.log.info('Created job {}'.format(jobID))