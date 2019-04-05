import boto3
from cliff.command import Command
import cray.config as config
import cray.s3 as cs3
import logging

def is_job_cancelled(jobID):
    return cs3.file_exists(config.bucket(), cs3.job_file_prefix(jobID, 'job_cancelled.zip'))

def is_job_active(jobID):
    return cs3.file_exists(config.bucket(), cs3.job_file_prefix(jobID, 'job.zip'))

def cancel_job(jobID):
    s3 = boto3.resource('s3')
    jobZip = cs3.job_file_prefix(jobID, 'job.zip')
    cancelledZip = cs3.job_file_prefix(jobID, 'job_cancelled.zip')
    s3.Object(config.bucket(), cancelledZip).copy_from(CopySource='{}/{}'.format(config.bucket(), jobZip))
    s3.Object(config.bucket(), jobZip).delete()

class Cancel(Command):
    "Cancels a job"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Cancel, self).get_parser(prog_name)
        parser.add_argument('-j', '--job', nargs=1, required=True, help="Job ID", type=str, dest='job')
        return parser

    def take_action(self, parsed_args):
        jobID = parsed_args.job[0]
        self.log.debug('JobID={}'.format(jobID))

        if is_job_cancelled(jobID):
            raise Exception("Already cancelled: '{}'".format(jobID))

        if not is_job_active(jobID):
            raise Exception("Unknown job: '{}'".format(jobID))

        cancel_job(jobID)

        self.log.info('Job {} cancelled'.format(jobID))

