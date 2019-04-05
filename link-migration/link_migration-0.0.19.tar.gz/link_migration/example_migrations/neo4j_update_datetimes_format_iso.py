# -*- coding: utf-8 -*-
"""
    Neo4j Scan datetime fields

    Check datetime format, strictly parse each encountered format and update the field
    to the same explicit format.

"""

from datetime import datetime
from link_migration.framework.changelog import changelog

version = 5

date_fields = [
    'agreed_date',
    'approved_at',
    'assessor_attestation_date',
    'created_at',
    'date_incorporated',  # only a date, no time
    'last_login',
    'modified_at',
    'ordered_at',
    'owner_attestation_date',
    'released_at',
    # 'report_order:requested_completion_date',
    'requested_completion_date',
    'submitted_at',
    'subscribe_expire',
    'subscribe_start',
    'updated_at'
]


@changelog("/data_changelogs/neo4j_update_datetimes_format_iso.csv")
def up(self, output=None):
    """
    Iterate over all datetime fields:
        [
          'agreed_date', 'approved_at', 'created_at', 'date_incorporated', 'last_login', 'modified_at', 'ordered_at',
          'owner_attestation_date', 'submitted_at', 'subscribe_expire', 'subscribe_start', 'updated_at'
        ]

        "MATCH (n) WHERE EXISTS(n.{date_field}) RETURN n.{date_field}, n.id"

        Check against format '%Y-%m-%dT%H:%M:%S.%fZ' and if inconsistent, update Neo4J with '%Y-%m-%dT%H:%M:%S.%fZ'
    """

    with self.driver.session() as session:
        mismatch_count = 0
        match_count = 0

        for date_field in date_fields:
            payload = f'MATCH (n) WHERE EXISTS(n.{date_field}) RETURN n.{date_field}, n.id'

            response_data = self.driver.read(session, payload)

            for record in response_data:
                found_id = record['n.id']
                found_date = record[f'n.{date_field}']

                date = None

                known_formats = [
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                    '%Y-%m-%dT%H:%M:%SZ',
                    '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%dT%H:%M:%S.%f',
                    '%Y-%m-%dT%H:%M:%S.%f%z',
                    '%Y-%m-%dT%H:%M:%S%z',
                    '%Y-%m-%d %H:%M:%S%z',
                    '%Y-%m-%d %H:%M:%S.%f%z',
                    '%Y-%m-%d'
                ]

                for known_format in known_formats:
                    try:
                        if ":" == found_date[-3:-2]:
                            date = datetime.strptime(found_date[:-3] + found_date[-2:], known_format)
                        date = datetime.strptime(found_date, known_format)
                    except ValueError:
                        pass

                if not date:
                    print(f'{found_date} was unable to be parsed by the known formats: {known_formats}')
                    continue

                if date.strftime('%Y-%m-%dT%H:%M:%S.%fZ') != found_date:
                    payload = (
                        f'{{"statements" : [ {{"statement" : "MATCH (n {{id: "{found_id}""}}) SET n.{date_field}'
                        f' = "{date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}" RETURN n.{date_field}, n.id"}} ]}}'
                    )
                    mismatch_count += 1
                    output.record(found_id, date_field, found_date, date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
                else:
                    match_count += 1

        print("mismatched format count:" + f"{mismatch_count}".rjust(10))
        print("matched format count:" + f"{match_count}".rjust(13))


def down(self):
    """
        Get a count of the total nodes in the graph.

        MATCH ()-->() RETURN count(*)
    """
    payload = "{\"statements\" : [ {\"statement\" : \"MATCH ()-->() RETURN count(*)\"} ]}"

    response_data = self.config.post_neo(data=payload)

    # get count from neo
    total_nodes = response_data['results'][0]['data'][0]['row'][0]
    print("Total count queried from Neo: %s" % total_nodes)
