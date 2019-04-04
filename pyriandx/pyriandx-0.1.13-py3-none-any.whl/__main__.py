import sys
import os
import json
from pprint import pprint, pformat
import time

import pyriandx.cli as cli
from pyriandx.client import client as _client
from pyriandx.log import *

spin = ['\\', '|', '/', '-']


def main(args=sys.argv[1:]):

    args = cli.parse_args(args)

    if args['--verbose'] == True:
        coloredlogs.install(level='DEBUG')
        os.environ["DEBUG_HTTP"] = "true"

    log.debug("Received arguments:\n" + str(args))

    input_file    = args['<json-file>']
    target_vcf    = args['<target-vcf>']
    output_dir    = args['--output-dir']
    username      = args['--username']
    password      = args['--password']
    institution   = args['--institution']

    client = _client(
    email=username,
    key=password,
    institution=institution
    )

    log.info("Creating case with input file: " + input_file)    
    case_id = client.create_case(input_file)
    log.info("Successfully created case with ID: " + str(case_id))

    log.info(f"Uploading target vcf {target_vcf}...")
    client.upload_file(target_vcf, case_id)

    log.info("Creating processing job...")
    client.create_job_vcf(case_id)

    sys.stdout.write("Waiting for job to transition to 'running' (API BUG)...   ") #logging doesn't allow surpression of newline
    status=client.get_job_status(case_id)
    while status != "running":
        log.debug(f"Status is: {status}")
        for _ in range(15): #Check API every 30 seconds
            for c in spin:
                sys.stdout.write("\b%s" % c)
                sys.stdout.flush()
                time.sleep(.5)
        status=client.get_job_status(case_id)

    # #TODO: what are the other statuses?
    sys.stdout.write("\nJob is running, waiting for it to 'complete'...   ")
    status=client.get_job_status(case_id)
    while status != "complete":
        log.debug(f"Status is: {status}")
        for _ in range(15): #Check API every 30 seconds
            for c in spin:
                sys.stdout.write("\b%s" % c)
                sys.stdout.flush()
                time.sleep(.5)
        status=client.get_job_status(case_id)

    sys.stdout.write('\n')
    print("Downloading report...")
    client.get_report(case_id, "output")

    log.info("Done.")




if __name__ == '__main__':
    assert sys.version_info >= (3, 6), "This tool requires python3.6"
    try:
        main()
    except KeyboardInterrupt:
        pass
    