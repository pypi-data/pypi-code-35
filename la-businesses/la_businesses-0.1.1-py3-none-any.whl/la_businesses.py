"""Save the latest database of businesses in Los Angeles as CSV and KML.

# Description
This script downloads and processes the listing of all active businesses 
currently registered with the City of Los Angeles Office of Finance. 
An 'active' business is defined as a registered business whose owner has not 
notified the Office of Finance of a cease of business operations. 
Update Interval: Monthly.

Data source: https://data.lacity.org/A-Prosperous-City/Listing-of-Active-Businesses/6rrh-rzua

This script fetches the data and saves it locally as a CSV file. It also selects
a subset of businesses with operation starting date within the last NDAYS days
(default 30) and saves this as a separate CSV file. Finally, it creates and 
saves a KML file from the subset, useful for importing into Google Maps or
similar software to visualize the distribution of recent businesses opened in
the Los Angeles area. 


# Installation
Install with pip. The package installs as a command-line script. 
```
pip install la-businesses
```

# Usage
Run from the command line (it installs as as script). All downloaded and 
generated files will be stored in a directory `files` inside the current 
working directory.
```
usage: la-businesses [-h] [-u] [-d NDAYS]

optional arguments:
  -h, --help              show this help message and exit
  -u, --update            update data (default: False)
  -d NDAYS, --days NDAYS  started since NDAYS days ago (default: 30)
```
  
# Known issues
## Locations with missing coordinates are omitted from KML file
The script relies on coordinate data already provided in the downloaded dataset. 
Some businesses contain addresses but no coordinates; in these cases, the 
business is ignored when creating the KML (but is included in any saved CSV 
file). Future implementations should include a function to look up location
coordinates from a given address (e.g., using the Open Street Maps API). 

## Locations with no DBA name simply show NaN in the KML file
The script could use better handling of business name / DBA combinations to 
omit NaN from KML when it does not have a business name. 

## No phone numbers
The data does not include any phone or email contact information; merging this
dataset with one that includes contact information would be more useful for 
market research. 

"""
# ----------------------------------------------------------------------------#
# LIBRARIES
# ----------------------------------------------------------------------------#
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
import logging
import datetime as dt
import pytz  # for timezone handling
import pandas as pd
import requests
import simplekml


# ----------------------------------------------------------------------------#
# CONSTANTS AND CONFIGURATION
# ----------------------------------------------------------------------------#
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

URL = "https://data.lacity.org/api/views/6rrh-rzua/rows.csv?accessType=DOWNLOAD"
COMPLETE_LIST = "all_businesses.csv"  # full database of businesses
RECENT_LIST = "recent_businesses.csv"  # subset of recent businesses
DEFAULT_NDAYS = 30  # select businesses opened since this many days ago
WRITE_CHUNK_SIZE = 1024  # bytes
OUTPUT_DIR = Path.cwd() / 'files'  # save all files here
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # make the dir if not exist


# ----------------------------------------------------------------------------#
# CORE FUNCTIONS
# ----------------------------------------------------------------------------#

def get_business_list():
    """Download latest businesses database."""
    response = requests.get(URL, stream=True)
    # Throw an error for bad status codes
    response.raise_for_status()
    with open(OUTPUT_DIR / COMPLETE_LIST, "wb") as handle:
        for block in response.iter_content(DEFAULT_NDAYS):
            handle.write(block)
    logging.info(f"Saved complete business list as {COMPLETE_LIST}.")
    return OUTPUT_DIR / COMPLETE_LIST


def load_business_list(file=None, update=False):
    """Load (optionally identified) database from file or download it first."""
    business_list_file = OUTPUT_DIR / COMPLETE_LIST
    if file:
        logging.info(f"Loading business list {file.name} ...")
        df = pd.read_csv(file)
        df["LOCATION START DATE"] = pd.to_datetime(df["LOCATION START DATE"])
        df["LOCATION END DATE"] = pd.to_datetime(df["LOCATION END DATE"])
        logging.debug("Converted dates")
        return df
    if update or not business_list_file.exists():
        logging.info("Downloading database of businesses ...")
        get_business_list()
    logging.info(
        f"Loading all businesses ...\n" \
        f"Using cached data from {last_mod(business_list_file)}. " \
        f"Use -u flag to update.")
    df = pd.read_csv(business_list_file)
    df["LOCATION START DATE"] = pd.to_datetime(df["LOCATION START DATE"])
    df["LOCATION END DATE"] = pd.to_datetime(df["LOCATION END DATE"])
    logging.debug("Converted dates")
    return df
    
    
def last_mod(file):
    """Returns a string of the last modified time of a Path() in local timezone"""
    fmt = "%d %b %Y at %I:%M %p %Z" # time format
    return pytz.utc.localize(dt.datetime.utcfromtimestamp(
        file.stat().st_mtime)).astimezone().strftime(fmt)

def select_recent(df, outfile=None, ndays=DEFAULT_NDAYS):
    logging.info(f"Selecting businesses starting {ndays} days ago or later ...")
    cutoff_date = dt.datetime.now() - dt.timedelta(days=ndays)
    df = df[df["LOCATION START DATE"] > cutoff_date]
    logging.debug(f"Selected recent since {cutoff_date.date()}: {len(df)} items")

    df = df.sort_values(by="LOCATION START DATE", ascending=False)
    logging.debug("Sorted by start date")

    output_filename = outfile or RECENT_LIST
    output_file = OUTPUT_DIR / output_filename
    df.to_csv(output_file, index=False)
    logging.info(f"Saved {len(df)} recent businesses to {output_file}.")

    return df


def df_to_kml(df, outfile=None):
    """Make a KML file from pd.DataFrame of addresses"""
    df = df.dropna(subset=["LOCATION"])
    df = df.reset_index(drop=True)
    logging.debug("Ignoring places with no lat-long")
    kml = simplekml.Kml()
    for id, row in df.iterrows():
        long, lat = eval(row["LOCATION"])
        kml.newpoint(
            name=str(row["BUSINESS NAME"]) + "\n" + str(row["DBA NAME"]),
            description=", ".join(
                [row["STREET ADDRESS"], row["CITY"], row["ZIP CODE"]]
            ),
            coords=[(lat, long)],
        )
    output_filename = outfile or "recent_businesses"
    output_file = OUTPUT_DIR / (output_filename + ".kml")
    kml.save(output_file)
    logging.debug("made points")
    logging.info("Created KML file " + str(output_file))


# ----------------------------------------------------------------------------#
# USER INTERFACE FUNCTIONS
# ----------------------------------------------------------------------------#
def get_parser():
    parser = ArgumentParser(
        description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-u", "--update", action="store_true", dest="update", help="update data"
    )
    parser.add_argument(
        "-d",
        "--days",
        action="store",
        dest="ndays",
        type=int,
        default=DEFAULT_NDAYS,
        help="started since NDAYS days ago",
    )
    return parser


def main():
    try:
        args = get_parser().parse_args()
        df = load_business_list(update=args.update)
        df = select_recent(df, ndays=args.ndays)
        df_to_kml(df)
    except KeyboardInterrupt:
        logging.error("!!! PROGRAM ABORTED WITH CTRL-C. !!!\n")


if __name__ == "__main__":
    main()
