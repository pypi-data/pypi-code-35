# -*- coding: utf-8 -*-
import datetime
import json
import pkg_resources
from pprint import pprint, pformat
import time
import shutil
import requests
import os

from pyriandx.log import log
from pyriandx.utilities import requests_retry_session


# ###HACK
# import random
# ###HACK


class client:

        def __init__(self, email, key, institution, baseURL="https://app.uat.pieriandx.com/cgw-api/v2.0.0"):
                self.baseURL=baseURL
                self.headers = {
                        'X-Auth-Email':email,
                        'X-Auth-Key':key,
                        'X-Auth-Institution':institution
                }
                #this is required to import static data from the module
                self.data_path = pkg_resources.resource_filename('pyriandx', 'json/') 
                

        def create_case(self,case_data_file):
                """Creates case with given case data file"""

                with open(case_data_file, 'r') as f:
                        request_data = json.load(f)

                # ###HACK
                # accession_number = random.randint(1,9999)
                # request_data["specimens"][0]["accessionNumber"] = accession_number
                # ###HACK

                log.debug("Creating case with data:")
                log.debug(request_data)
                response = self._post_api("/case",data=request_data).json()

                return response["id"]


        def create_sequencer_run(self,data):
                """Creates case with given accession number"""

                with open(self.data_path + 'create_sequencer_run.json', 'r') as f:
                        request_data = json.load(f)

                request_data["specimens"][0]["accessionNumber"] = data["accessionNumber"]
                log.debug("Creating sequencer run with data:")
                log.debug(pformat(request_data))
                response = self._post_api("/sequencerRun",data=request_data).json()
                return response["id"]



        def create_job(self,case_id, accession_number):
                """Creates job with given accession number - NOT CURRENTLY WORKING"""

                with open(self.data_path + 'create_job.json', 'r') as f:
                        request_data = json.load(f)

                request_data["input"][0]["accessionNumber"] = str(accession_number)
                log.debug("Creating job with case_id: " + str(case_id) + " accession_number: " + str(accession_number))
                endpoint = "/case/"+str(case_id)+"/informaticsJobs"
                self._post_api(endpoint,data=request_data)



        def create_job_vcf(self,case_id):
                """Creates job with given case id"""
                log.debug("Creating job for vcf with case_id: " + str(case_id))
                endpoint = "/case/"+str(case_id)+"/informaticsJobsVCF"
                self._post_api(endpoint)



        def get_job_status(self,case_id,job_index=None):
                """Gets the status of an informatics job. If job_index is not passed in, grab latest."""
                log.debug("Getting status of job with case id: " + str(case_id))
                case_info=self.get_case_info(case_id)
                if job_index is None:
                        job_index = len(case_info["informaticsJobs"]) - 1
                
                try:
                        status = case_info["informaticsJobs"][job_index]["status"]
                except KeyError:
                        status = "nojobavailable"
                log.debug("Got status " + status)
                return status



        def get_report(self,case_id,output_dir=None):
                """
                Downloads report to output_dir. 
                If report_index is None, downloads all reports. 
                If output_dir is None, downloads to working directory.
                """

                log.debug("Finding report IDs for case " + str(case_id))
                case_info = self.get_case_info(case_id)
                if 'reports' not in case_info:
                        log.info("No reports available for case " + str(case_id) + ". Try again later.")
                        return
                
                for r in case_info["reports"]:
                        report_id = r["id"]
                        local_filename = "case-" + str(case_id) + "_report-" + report_id + ".pdf.gz" #will probably want to change this
                        url = self.baseURL + "/case/"+str(case_id)+"/reports/"+report_id+"?format=pdf"

                        if output_dir is not None:
                                os.makedirs(output_dir,exist_ok=True)
                                local_filename = output_dir + "/" + local_filename

                        log.info("Found report with id " + report_id + ". Downloading as " + local_filename + " from " +url)
                        r = requests.get(url,stream=True, headers=self.headers)
                        if r.ok:
                                with open(local_filename, 'wb') as f:
                                        shutil.copyfileobj(r.raw, f)
                        else:
                                log.critical(f"Issue downloading file from {endpoint}. {r.status_code} ::: {r.text}")
                        


        def upload_file(self,filename, case_id):
                """Upload file to given accession number"""
                files = {'file': open(filename, 'rb')}
                endpoint = "/case/"+str(case_id)+"/caseFiles/"+filename
                log.debug("Upload file to endpoint: " + endpoint)
                self._post_api(endpoint,files=files)
        


        def get_case_info(self,case_id):
                """Get case info for given case ID"""
                return self._get_api("/case/"+str(case_id))



        def _get_api(self, endpoint): 
                """Internal function to create get requests to the API"""
                url = self.baseURL + endpoint
                log.debug("Sending request to {}".format(url))
                t0 = time.time()

                try: 
                        response = requests_retry_session(self.headers).get(url)
                except Exception as x:
                        log.critical('{} call failed after retry: {}'.format(endpoint, x))
                else:
                        if(response.status_code == 200):
                                log.debug('call to {} succeeded'.format(endpoint))
                                return json.loads(response.text)
                        else:
                                log.critical('call to {} failed. Error code was {}'.format(endpoint, response.status_code))
                                log.critical("server responded with " + response.text)
                                
                finally:
                        t1 = time.time()
                        log.debug("call took {} seconds".format(t1 - t0))



        def _post_api(self, endpoint, data=None, files=None): 
                """Internal function to create post requests to the API"""
                url = self.baseURL + endpoint
                log.debug("Sending request to {}".format(url))
                t0 = time.time()

                post_headers = self.headers.copy()

                if data is not None:        
                        post_headers['Content-Type'] = "application/json"
                        post_headers['Accept-Encoding'] = "*"


                # uncomment if youd like to inspect the json data we're sending
                # with open("request-debug.json", "w") as data_file:
                #         json.dump(data, data_file, indent=2)

                try: 
                        response = requests_retry_session(post_headers,retries=0).post(url, json=data, files=files)
                except Exception as x:
                        log.critical('{} call failed after retry: {}'.format(endpoint, x))
                else:
                        if(response.status_code == 200):
                                log.debug("call to " + endpoint + " succeeded")
                                log.debug("response was " + response.text)
                                return response
                        else:
                                log.critical('Call to {} failed. Error code was {}'.format(endpoint, response.status_code))
                                log.critical("server responded with " + response.text)
                                #what to return here?
                finally:
                        t1 = time.time()
                        log.debug("Call took {} seconds".format(t1 - t0))


