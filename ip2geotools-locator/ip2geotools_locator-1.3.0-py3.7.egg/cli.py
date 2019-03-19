# -*- coding: utf-8 -*-

"""Console script for ip2geotools_locator."""
import click
import logging

from ip2geotools_locator import Locator
from ip2geotools_locator.utils import LOGGER as logger

LOCATOR = Locator()

@click.command()
@click.argument('ip_address', type=click.STRING)

@click.option('-g', '--generate-map', 'gen_map', is_flag=True)

@click.option('-a', '--average', 'average', is_flag=True)
@click.option('-c', '--clustering', 'clustering', is_flag=True)
@click.option('-m', '--median', 'median', is_flag=True)

@click.option('--commercial', 'commercial', is_flag=True)
@click.option('--noncommercial', 'noncommercial', is_flag=True)
@click.option('-d', '--database', 'database', type=click.STRING, multiple=True)
@click.option('--logs/--no-logs', default=False)
@click.option('-v', '--verbose', count=True)
# pylint: disable=too-many-arguments
def cmd(logs, verbose, ip_address, gen_map, average, clustering, median, commercial, noncommercial, 
        database):
    """Calculate estimate of geographical location for IP address"""
    databases = []

    if ip_address == "setup":
        setup()

    match = ip_address.split(".")
    # pylint: disable=too-many-boolean-expressions, literal-comparison
    if (len(match) is not 4 or int(match[0]) < 0 or int(match[0]) > 255 or int(match[1]) < 0 or
            int(match[1]) > 255 or int(match[2]) < 0 or int(match[2]) > 255 or int(match[3]) < 0 or
            int(match[3]) > 255):
        click.echo("IP address is not valid!")
        exit(1)

    stream_handler = logging.StreamHandler()
    
    if logs is False:
        logger.disabled = True

    if verbose != 0:
        log_level = logging.WARNING
    
        if verbose == 1:
             log_level = logging.INFO
        elif verbose == 3:
             log_level = logging.DEBUG

        logger.disabled = False
        logger.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s %(stack_info)s'))
        stream_handler.setLevel(log_level)
        logger.addHandler(stream_handler)

    if commercial is True:
        databases.append("commercial")

    elif noncommercial is True:
        databases.append("noncommercial")

    else:
        databases = list(database)
    LOCATOR.generate_map = gen_map
    LOCATOR.get_locations(ip_address, databases)

    if (average is False and clustering is False and median is False):
        for location in LOCATOR.locations:
            click.echo("Location retrieved from %s database is: %f N, %f E" 
                        %(location, LOCATOR.locations[location].latitude,
                        LOCATOR.locations[location].longitude))
    else:
        calculated_locations = LOCATOR.calculate(average=average, clustering=clustering,
                                                 median=median)

        for calc_loc in calculated_locations:
            click.echo("\nLocation estimated by %s is: %f N, %f E" %
                       (calc_loc, calculated_locations[calc_loc].latitude,
                        calculated_locations[calc_loc].longitude))

def setup():
    print("setup")
    exit(0)


#TODO -no location processing from databases
#TODO -výchozí databáze, add region