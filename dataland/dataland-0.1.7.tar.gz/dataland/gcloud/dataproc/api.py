import time
from typing import Callable, Dict, Iterable, List

from box import Box
from googleapiclient import discovery


class _Api:
    def __init__(self, project_id: str, region: str):

        self.project_id = project_id
        self.region = region


class _Jobs(_Api):
    @property
    def clusters(self) -> "_Clusters":
        return self._api_root.clusters

    def __init__(self, api_root, **kwargs):
        super().__init__(**kwargs)
        self._jobs = api_root._dataproc.projects().regions().jobs()
        self._api_root = api_root

    def lz_submit(self, body: Dict, callbacks: Iterable[Callable] = None):
        def _submit():
            results = []
            submitted = self.submit(body).execute()

            results.append(submitted)

            if callbacks:
                if isinstance(callbacks, Callable):
                    results.append(callbacks(submitted))
                elif isinstance(callbacks, Iterable):
                    for cb in callbacks:
                        results.append(cb(submitted))

                else:
                    raise ValueError(
                        f"`callbacks` should be Iterable[Callable], got: {callbacks}"
                    )

            return results

        self._api_root._requests.append(_submit)

        return self

    def lz_wait(
        self,
        job_id: str,
        target_state: str,
        interval: int = 60,
        timeout: int = 36000,
        verbose: bool = True,
        error_states: List[str] = ["ERROR", "CANCELLED"],
    ):
        def _wait():
            return self.wait(
                job_id,
                target_state,
                interval=interval,
                timeout=timeout,
                verbose=verbose,
                error_states=error_states,
            )

        self._api_root._requests.append(_wait)

        return self

    def cancel(self):
        # TODO
        pass

    def delete(self):
        pass

    def get(self, job_id: str):
        return self._jobs.get(
            projectId=self.project_id, region=self.region, jobId=job_id
        )

    def list(self):
        # TODO
        pass

    def submit(self, body: Dict):

        return self._jobs.submit(
            projectId=self.project_id, region=self.region, body=body
        )

    def update(self):
        # TODO
        pass

    def wait(
        self,
        job_id: str,
        target_state: str,
        interval: int = 60,
        timeout: int = 36000,
        verbose: bool = True,
        error_states: List[str] = ["ERROR", "CANCELLED"],
    ):
        """Wait for job to reach some status states.

        Params:
            `job_id`: specify the target job to be monitored
            `target_state`: state string returned by `jobs.get` api,
                            wait util the target cluster reaches to this state,
                            ex: we expect it will eventally reach "DONE" state
                            while submitting a new job.
            `timeout`: interrupt waiting and raise `TimeoutError` after elapsed time exceeds this threshold, default: 36000 (10hr)
            `interval`: waiting interval between consecutive api requests, in seconds
            `error_states`: interrupt waiting and raise `RuntimeError` while job's status reaches these states
        """
        tic = time.time()

        # TODO: set maximum timeout
        while True:
            try:
                request = self.get(job_id)
                status = Box(request.execute()["status"])

                toc = time.time()
                if verbose:
                    print(
                        (
                            f'[JOB] "{status.state}" >> "{target_state}",'
                            f" {toc - tic:.3f} seconds elapsed"
                        ),
                        flush=True,
                    )

                if status.state == target_state:
                    break
                elif status.state in error_states:
                    raise RuntimeError(
                        f'Unexpected "{status.state}" state, Please check the log of the job on Dataproc browser for details, job_id: "{job_id}"'
                    )

                if (toc - tic) > timeout:
                    raise TimeoutError(
                        f"Job execution reaches time out: {timeout} seconds"
                    )

                time.sleep(interval)

            except Exception as err:
                raise err

    def execute(self) -> List:
        """Execute requests sequentially in pipeline"""

        return self._api_root.execute()


class _Clusters(_Api):
    @property
    def jobs(self) -> _Jobs:
        return self._api_root.jobs

    def __init__(self, api_root, **kwargs):
        super().__init__(**kwargs)
        self._clusters = api_root._dataproc.projects().regions().clusters()
        self._api_root = api_root

    def reset_requests(self):

        self._api_root.reset_requests()

        return self

    def lz_create(self, body: Dict, callbacks: Iterable[Callable] = None):

        self._api_root._requests.append(self.create(body, callbacks).execute)

        return self

    def lz_wait(
        self,
        cluster_name: str,
        target_state: str,
        interval: int = 5,
        fail_ok: bool = False,
        verbose: bool = True,
    ):
        def _wait():
            return self.wait(
                cluster_name,
                target_state,
                interval=interval,
                fail_ok=fail_ok,
                verbose=verbose,
            )

        self._api_root._requests.append(_wait)

        return self

    def lz_get(self, cluster_name: str):

        self._api_root._requests.append(self.get(cluster_name).execute)

        return self

    def lz_delete(self, cluster_name: str, callbacks: Iterable[Callable] = None):

        self._api_root._requests.append(self.delete(cluster_name, callbacks).execute)

        return self

    def execute(self) -> List:
        """Execute requests sequentially in pipeline"""

        return self._api_root.execute()

    def create(self, body: Dict, callbacks: Iterable[Callable] = None):
        request = self._clusters.create(
            projectId=self.project_id, region=self.region, body=body
        )

        if callbacks:
            if isinstance(callbacks, Callable):
                request.add_response_callback(callbacks)
            elif isinstance(callbacks, Iterable):
                for cb in callbacks:
                    request.add_response_callback(cb)

            else:
                raise ValueError(
                    f"`callbacks` should be Iterable[Callable], got: {callbacks}"
                )

        return request

    def delete(self, cluster_name: str, callbacks: Iterable[Callable] = None):

        request = self._clusters.delete(
            projectId=self.project_id, region=self.region, clusterName=cluster_name
        )

        if callbacks:
            if isinstance(callbacks, Callable):
                request.add_response_callback(callbacks)
            elif isinstance(callbacks, Iterable):
                for cb in callbacks:
                    request.add_response_callback(cb)
            else:
                raise ValueError(
                    f"`callbacks` should be Iterable[Callable], got: {callbacks}"
                )
        return request

    def diagnose(self):
        # TODO
        pass

    def get(self, cluster_name: str):

        return self._clusters.get(
            projectId=self.project_id, region=self.region, clusterName=cluster_name
        )

    def list(self):
        # TODO
        pass

    def patch(self):
        # TODO
        pass

    def wait(
        self,
        cluster_name: str,
        target_state: str,
        interval: int = 10,
        timeout: int = 300,
        fail_ok: bool = False,
        verbose: bool = True,
    ) -> None:
        """Wait for dataproc cluster to reach target status

        Params:
            `cluster_name`: get the target cluster to be monitored
            `target_state`: state string return by `clusters.get` api,
                            wait util the target cluster reaches to this state,
                            ex: we expect it will eventally reach "RUNNING" state
                            while creating a new cluster.
            `interval`: waiting interval between consecutive api requests, in seconds.
            `timeout`: interrupt waiting and raise `TimeoutError` after elapsed time exceeds this threshold, default: 300 (5min)
            `fail_ok`: ignore the request exception,
                       set to `True` when we expect cluster is about to die.
        """
        tic = time.time()

        # TODO: set maximum timeout
        while True:
            try:
                request = self.get(cluster_name)
                status = Box(request.execute()["status"])

                toc = time.time()
                if verbose:
                    print(
                        (
                            f'[CLUSTER] "{status.state}" >> "{target_state}",'
                            f" {toc - tic:.3f} seconds elapsed"
                        ),
                        flush=True,
                    )

                if status.state == target_state:
                    break

                if status.state == "ERROR":
                    raise RuntimeError(
                        f'Unexpected "{status.state}" state.'
                        f" Please check the log of the cluster on Dataproc browser for details,"
                        f' cluster_name: "{cluster_name}"'
                    )

                if (toc - tic) > timeout:
                    raise TimeoutError(
                        f"Cluster execution reaches time out: {timeout} seconds"
                    )

                time.sleep(interval)

            except Exception as err:
                if fail_ok:
                    break
                else:
                    raise err


class DataprocApi(_Api):
    _apis = {}

    def __init__(
        self, project_id: str, region: str, api_version: str = "v1", credentials=None
    ):
        """Dataproc api wraper.

        Params:
            `project_id`: mapping to `projectId` parameter in dataproc api
            `region`: mapping to `region` parameter in dataproc api
        """

        super().__init__(project_id, region)

        creds = credentials or self._default_credentials

        dataproc = discovery.build("dataproc", api_version, credentials=creds)

        self._credentials = creds
        self._dataproc = dataproc
        self._version = api_version
        self._namespace = (self._version, self._credentials)

        if self._namespace not in DataprocApi._apis:
            DataprocApi._apis[self._namespace] = {}

        self._requests = []
        self._responses = {}

    def reset_requests(self):

        self._requests = []

    def get_response(self):
        pass

    @property
    def _default_credentials(self):
        from google.auth import _default

        return _default.default()[0]

    @property
    def clusters(self) -> _Clusters:

        if "_clusters" not in DataprocApi._apis[self._namespace]:

            DataprocApi._apis[self._namespace]["_clusters"] = _Clusters(
                self, project_id=self.project_id, region=self.region
            )

        return DataprocApi._apis[self._namespace]["_clusters"]

    @property
    def jobs(self):

        if "_jobs" not in DataprocApi._apis[self._namespace]:

            DataprocApi._apis[self._namespace]["_jobs"] = _Jobs(
                self, project_id=self.project_id, region=self.region
            )

        return DataprocApi._apis[self._namespace]["_jobs"]

    def execute(self) -> List:
        """Execute requests sequentially in pipeline"""

        results = []
        if isinstance(self._requests, Iterable):

            for ex in self._requests:
                if not isinstance(ex, Callable):
                    raise TypeError(
                        f"All `executable` objects in request-pipeline should be callable, got: {ex}"
                    )

            while len(self._requests) > 0:
                execute = self._requests.pop(0)

                results.append(execute())

        return results

    def create(self, body: Dict, callbacks: Iterable[Callable] = None):
        request = self._clusters.create(
            projectId=self.project_id, region=self.region, body=body
        )

        if callbacks:
            if isinstance(callbacks, Callable):
                request.add_response_callback(callbacks)
            elif isinstance(callbacks, Iterable):
                for cb in callbacks:
                    request.add_response_callback(cb)

            else:
                raise ValueError(
                    f"`callbacks` should be Iterable[Callable], got: {callbacks}"
                )
