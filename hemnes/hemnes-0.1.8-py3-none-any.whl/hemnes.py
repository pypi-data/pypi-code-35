"""Main script for hemnes - ikea scraping"""

__author__ = 'sayeef moyen'

# import
import hemnes.helpers.scrape as scrape
import json

def get_products(query, data_path = None, keywords = None, tag = None):
    """Returns a list of Product objects for the given query

    Common use cases:
        get_products("coffee table", "coffeetable.json")
        get_products("armchair", "armchair.json", keywords=["comfortable", "large"])
        get_products("bed", "bed.json", tag="bed general")

    The Product objects contain the following data:
        name (str)
        price (float)
        rank (int): numbered result from ikea's search
        rating (float): average user rating
        url (str): product url
        color (list[str]): list of colors as strings of the product
        images (list[str]): list of full urls to product images

    If data_path is provided, Hemnes will save the Products to a .json file at the
    specified path

    If keywords is provided, Hemnes will look through the product description provided on 
    each product's page for ALL of the given keywords, and will only return data for 
    that product if it contains all of the given keywords.

    Tag is a meta parameter intended for flexible use to group product results by the
    specific instance in which they were scraped. Another such use could be to provide
    a specific term to a number of queried products for use in a database (e.g. Uploading
    resulting .json data to AWS dynamodb, using tag as a key
    
    Args:
        query (str): space separated query terms
        data_path (str): path to output json file
        keywords (list[str]): list of required keywords for returned products
        tag (str): meta arg for labelling scraping results
    """
    required_words = None if keywords is None else [keyword.lower() for keyword in keywords.strip().split()]
    results = scrape.get_products_for_query(query, tag, required_words)
    if data_path is not None:
        json.dump([result.to_dict() for result in results], open(data_path, 'w+'), sort_keys=True, indent=4)
    return results
