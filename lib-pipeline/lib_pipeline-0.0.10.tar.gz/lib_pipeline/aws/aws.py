from lib_pipeline.helpers import execute
import json


class AWS:
    def run(self, resource, command, cwd=None):
        return execute(f"aws {resource} {command}", cwd)


class S3(AWS):
    def __init__(self):
        self.resource = "s3"

    def copy(self, bucket_path, files, *args, cwd=None):
        options = " ".join(args)
        return self.run(
            self.resource, f"cp {files} s3://{bucket_path} {options}", cwd=cwd
        )

    def empty(self, bucket_path, *args):
        options = " ".join(args)
        return self.run(self.resource, f"rm s3://{bucket_path} {options}")


class Route53(AWS):
    def __init__(self):
        self.resource = "route53"

    def list_resource_record_sets(self, hosted_zone_id, *args):
        options = " ".join(args)
        return self.run(
            self.resource,
            f"list-resource-record-sets --hosted-zone-id {hosted_zone_id} {options}",
        )

    def get_active_region(self, hosted_zone_id, domain, dns_prefix, *args):
        result = self.list_resource_record_sets(
            hosted_zone_id,
            f"--query 'ResourceRecordSet[?starts_with(Name,`{dns_prefix}`)]'",
            *args,
        )
        for i in json.loads(result.stdout)["ResourceRecordSets"]:
            if i["Name"] == domain and i["Failover"] == "PRIMARY":
                return i["SetIdentifier"].split(f"{dns_prefix}-")[1]
        return None
