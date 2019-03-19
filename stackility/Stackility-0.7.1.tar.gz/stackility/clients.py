import boto3
import logging


def init_boto3_clients(services, profile, region, role):
    """
    Get boto3 clients for all the requested services.

    Args:
        services - list of services for which we want clients
        profile - CLI profile to use
        region - where do you want the clients

    Returns:
        Good or Bad; True or False
    """
    try:
        clients = {}
        session = None
        if profile and region:
            session = boto3.session.Session(profile_name=profile, region_name=region)
        elif profile:
            session = boto3.session.Session(profile_name=profile)
        elif region:
            session = boto3.session.Session(region_name=region)
        else:
            session = boto3.session.Session()

        for svc in services:
            clients[svc] = session.client(svc)

        return clients
    except Exception as wtf:
        logging.error(wtf, exc_info=True)
        return None
