import boto3
from cliff.command import Command
import cray.config as config
import cray.s3 as cs3
import logging
import os
import subprocess
import tempfile

def is_duplicate_job(jobID):
    return cs3.file_exists(config.bucket(), '{}/{}/job.zip'.format(config.job_prefix(), jobID))

def build_job_archive(tempdir):
    cmd = 'docker run -v ${{PWD}}:/build -v ${{HOME}}/.ssh:/root/.ssh:ro -v {}:/output senseyeio/cray-builder:latest'.format(tempdir)
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code is not 0:
        raise Exception("'{}' exited with code '{}'".format(cmd, exit_code))

class Submit(Command):
    "Submits the current working directory to the batch processing system"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Submit, self).get_parser(prog_name)
        parser.add_argument('-t', '--ticket', nargs=1, required=True, help="Jira ticket identifier", type=str, dest='ticket')
        parser.add_argument('-d', '--description', nargs=1, required=True, help="A description of the job", type=str, dest='desc')
        return parser

    def submit_job_zip(self, zip_path, jobID):
        bucket = config.bucket()
        prefix = '{}/{}.zip'.format(config.submit_prefix(), jobID)
        self.log.info('Uploading to {}:/{}'.format(bucket, prefix))
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(zip_path, bucket, prefix)

    def take_action(self, parsed_args):
        ticket = parsed_args.ticket[0]
        desc = parsed_args.desc[0].replace(" ", "_")
        jobID = '{}:{}'.format(ticket, desc)
        self.log.debug('Ticket={} Desc={} JobID={}'.format(ticket, desc, jobID))

        if is_duplicate_job(jobID):
            raise Exception("Duplicate job: '{}'".format(jobID))

        with tempfile.TemporaryDirectory() as tempdir:
            build_job_archive(tempdir)
            self.submit_job_zip('{}/job.zip'.format(tempdir), jobID)

        self.log.info('Created job {}'.format(jobID))