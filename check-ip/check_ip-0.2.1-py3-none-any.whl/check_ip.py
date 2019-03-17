"""
check_ip.py
===========

Check your public IP address and update DNS records on Cloudflare.
"""

import sys

import requests
import yaml
from loguru import logger


# Endpoints
PUBLIC_IP_SERVICE = "https://api.ipify.org"
CLOUDFLARE_API = "https://api.cloudflare.com/client/v4"


def zone_url(zone_id):
    """Get the endpoint for a Cloudflare API request for a specific DNS zone.

    Args:
        zone_id (str): The zone ID.

    Returns:
        str: The Cloudflare API endpoint URL for this zone.
    """
    return f"{CLOUDFLARE_API}/zones/{zone_id}/dns_records/"


def record_url(zone_id, record_id):
    """Get the endpoint for a Cloudflare API request for a specific DNS record.

    Args:
        zone_id (str): The zone ID.
        record_id (str): The record ID.

    Returns:
        str: The Cloudflare API endpoint URL for this record.
    """
    return f"{CLOUDFLARE_API}/zones/{zone_id}/dns_records/{record_id}"


def main():
    """Main script."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "configfile",
        type=str,
        nargs="?",
        default="config.yaml",
        help="configuration file",
    )
    args = parser.parse_args()

    with open(args.configfile, "r") as f:
        config = yaml.safe_load(f)

    auth_header = {
        "X-Auth-Email": config["email"],
        "X-Auth-Key": config["api_key"],
        "Content-Type": "application/json",
    }
    zone_name = config["zone"]
    records = config["records"]

    # Get the current public IP
    response = requests.get(PUBLIC_IP_SERVICE)
    response.raise_for_status()
    public_ip = response.text

    # Get the zone ID from the zone name
    response = requests.get(f"{CLOUDFLARE_API}/zones", headers=auth_header)
    response.raise_for_status()
    zone_id = next(
        zone["id"] for zone in response.json()["result"] if zone["name"] == zone_name
    )

    for record in records:
        record_name = f"{record}.{zone_name}"

        # Get the record ID
        response = requests.get(zone_url(zone_id), headers=auth_header)
        response.raise_for_status()
        record_id = next(
            r["id"]
            for r in response.json()["result"]
            if r["type"] == "A" and r["name"] == record_name
        )

        # Get the current record value
        response = requests.get(record_url(zone_id, record_id), headers=auth_header)
        response.raise_for_status()
        record_ip = response.json()["result"]["content"]

        if record_ip == public_ip:
            logger.info("Public IP matches {} ({})", record_name, record_ip)
            sys.exit(0)

        # Update the record IP address if necessary
        logger.info(
            "Public IP ({}) does not match {} ({})", public_ip, record_name, record_ip
        )
        logger.info(f"Updating Cloudflare record for {record_name}")
        new_record = {"type": "A", "name": record_name, "content": public_ip}
        try:
            response = requests.put(
                record_url(zone_id, record_id), headers=auth_header, json=new_record
            )
            response.raise_for_status()
        except requests.HTTPError as err:
            logger.error(err)
            continue
        logger.info("DNS record updated: {} -> {}", record_ip, public_ip)


if __name__ == "__main__":
    main()
