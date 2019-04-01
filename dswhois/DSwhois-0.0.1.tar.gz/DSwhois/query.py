from .whois import query
import csv
import datetime
import json


class DomainInfo(object):

    """Docstring for Whois. """

    def __init__(self):
        """TODO: to be defined1. """
        pass

    def query(self, domain):
        """
        :domain: string | domain name | eg: google.com
        :returns: dict

        """
        domain_info = dict()
        domain = query(domain)
        if domain:
            domain_info['domain_name'] = domain.name
            if domain.registrar:
                domain_info['registrar'] = domain.registrar
            else:
                domain_info['registrar'] = None
            if domain.expiration_date:
                domain_info['expires'] = domain.expiration_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                domain_info['expires'] = None

            if domain.creation_date:
                domain_info['created'] = domain.creation_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                domain_info['created'] = None
            if domain.last_updated:
                domain_info['modified'] = domain.last_updated.strftime("%Y-%m-%d %H:%M:%S")
            else:
                domain_info['modified'] = None
            domain_info['date_checked'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return domain_info
