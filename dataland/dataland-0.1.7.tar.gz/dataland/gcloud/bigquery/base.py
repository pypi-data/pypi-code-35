import time
from typing import Any, List, Union

from google.cloud import bigquery

from ...base import DataNode


class BqDataNode(DataNode):
    def load(self):
        raise NotImplementedError()

    def dump(
        self,
        uris: Union[str, List[str]],
        schema: Any = None,
        destination: Any = None,
        create_disposition: str = "CREATE_IF_NEEDED",
        write_disposition: str = "WRITE_TRUNCATE",
    ) -> bigquery.LoadJob:

        client = bigquery.Client()

        dataset_ref = client.dataset(self.data.source.dataset)
        table_ref = dataset_ref.table(self.data.source.tablename)

        job_config = bigquery.LoadJobConfig()

        job_config.source_format = self.data.format
        job_config.schema = schema or self.data.schema
        job_config.create_disposition = create_disposition
        job_config.write_disposition = write_disposition

        is_valid_urls = isinstance(uris, str) or (
            isinstance(uris, List) and all(isinstance(uri, str) for uri in uris)
        )
        if not is_valid_urls:
            raise ValueError("`uris` contains invalid values")

        load_job = client.load_table_from_uri(
            uris, destination=destination or table_ref, job_config=job_config
        )  # API request

        # elif isinstance(pdf, pd.DataFrame):
        #     load_job = client.load_table_from_dataframe(
        #         pdf, destination=destination or table_ref, job_config=job_config
        #     )  # API request

        return load_job

    def copy_to(
        self,
        dest_node: "BqDataNode",
        create_disposition: str = "CREATE_IF_NEEDED",
        write_disposition: str = "WRITE_TRUNCATE",
    ) -> bigquery.CopyJob:

        client = bigquery.Client()

        src_ref = client.dataset(self.data.source.dataset).table(
            self.data.source.tablename
        )  # yapf: disable
        dest_ref = client.dataset(dest_node.data.source.dataset).table(
            dest_node.data.source.tablename
        )  # yapf: disable

        job_config = bigquery.CopyJobConfig()

        job_config.create_disposition = create_disposition
        job_config.write_disposition = write_disposition

        copy_job = client.copy_table(src_ref, dest_ref, job_config=job_config)

        return copy_job

    @classmethod
    def wait(
        cls,
        job_id: str,
        target_state: str = "DONE",
        interval: int = 10,
        timeout: int = 600,
        verbose: bool = True,
    ) -> bigquery.job._AsyncJob:

        tic = time.time()
        client = bigquery.Client()

        while True:
            try:
                job: bigquery.job._AsyncJob = client.get_job(job_id)
                toc = time.time()
                if verbose:
                    print(
                        (
                            f'[BQ-JOB] "{job.state}" >> "{target_state}",'
                            f" {toc - tic:.3f} seconds elapsed"
                        ),
                        flush=True,
                    )

                if job.state == target_state:
                    break

                if (toc - tic) > timeout:
                    raise TimeoutError(
                        f"bigquery operation reaches time out: {timeout} seconds"
                    )

                time.sleep(interval)

            except Exception as err:
                raise err

        return job
