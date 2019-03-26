"""Core functionality for scraping data from ikea 

Attributes:
  __BS_HTML_PARSER (str): html parser to use for beautifulsoup
  __PRODUCTS_PER_PAGE (int): products per page of search results

Exceptions:

Todo:

"""

__author__ = 'sayeef moyen'

# import
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from . import locate as ikea
from . import product
import math
import time

# file attributes
__BS_HTML_PARSER = 'html.parser'
__PRODUCTS_PER_PAGE = 40

def fetch_angular_page(url, sleep_time = 4):
    """Returns soup of an angular-generated webpage

    Args:
        url (str): url to page of an angular app
        sleep_time (int): time to wait for page to load

    Returns:
        bs4.BeautifulSoup: soup of the generated webpage
    """
    # headless chrome doesn't load angular for some reason
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    # an adequate sleep time is crucial to retrieving the proper html
    time.sleep(4)
    soup = bs(driver.page_source, __BS_HTML_PARSER)
    driver.close()
    driver.quit()
    return soup

def fetch_non_angular_page(url):
    """Returns soup of a non-angular generated webpage

    Args:
        url (str): url to webpage

    Returns:
        bs4.BeautifulSoup: soup of the webpage
    """
    chrome_options = Options()
#    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = bs(driver.page_source, __BS_HTML_PARSER)
    driver.close()
    driver.quit()
    return soup

def get_num_of_pages(num_of_results, products_per_page = __PRODUCTS_PER_PAGE):
    """Returns the number of pages of search results, given hits

    Args:
        num_of_results (int): number of product hits for some query

    Returns:
        int: number of pages of search results
    """
    return int(math.ceil(num_of_results/products_per_page))

def get_url_for_query(query, page_num, products_per_page = __PRODUCTS_PER_PAGE):
    """Returns the url to ikea's search for given query term(s) and page number

    Args:
        query (str): query term(s)/product keyword(s)
        page_num (int): desired page number, indexed from 0

    Returns:
        str: url to ikea's search for the query
    """
    url_friendly_query = query.replace(' ', '+')
    return 'https://www.ikea.com/ms/en_US/usearch/?query=%s&rows=%d&view=grid&start=%d' % (url_friendly_query, products_per_page, page_num * products_per_page)

def get_product_from_product_page(prod_page_soup, tag, rank, url):
    """Returns a Product object representation of a given product page with given meta parameters

    Args:
        prod_page_soup (bs4.BeautfulSoup): soup of a product page
        tag (str): product tag (for data storage purposes, typically = query)
        rank (int): product relevance rank (order given by ikea's search)
        url (str): product url (for use in creating the Product object)

    Returns:
        product.Product: Product object
    """
    product_container = ikea.locate_product_page_product_container(prod_page_soup)
    if product_container is None: return None
    product_overview = ikea.locate_product_page_product_overview(product_container)
    if product_overview is None: return None

    name = ikea.get_product_page_product_name(product_overview)
    price = ikea.get_product_page_product_price(product_overview)
    images = ikea.get_product_page_product_images(product_container)
    # consider name, price, and images as necessary components for a Product, return None if not available
    if name is None or price is None or images is None: return None
    rating = ikea.get_product_page_product_rating(product_container)
    colors = ikea.get_product_page_product_colors(product_container)
    print('stored product %s: %s' % (name, url))
    return product.Product(tag, name, rank, rating, price, colors, images, url)

def get_products_from_page_of_search_results(results_soup, prod_tag, page_num, required = None, products_per_page = __PRODUCTS_PER_PAGE):
    """Returns a list of Product containing the products on the given page of results

    Args:
        results_soup (bs4.BeautifulSoup): soup of a page of search results
        prod_tag (str): tag for new products (for data storage, typically = query)
        page_num (int): current page number, for determining product rank
        required (list[str]): required words in product description (for stricter searching)
        products_per_page (int): number of products shown per page, can be altered in get_url_query, used for determining product ranks
    
    Returns:
        list[product.Product]: products found on the page
    """
    products_container = ikea.locate_search_results_products_container(results_soup)
    if products_container is None: return []
    products_on_page = ikea.locate_search_results_products(products_container)
    
    products = []
    relative_rank = 1
    for product in products_on_page:
        product_overview = ikea.locate_search_results_product_overview(product)
        if product_overview is not None:
            product_url = product_overview['href'].strip()
            # for strict searches
            strict = True
            if required is not None:
                # remove any separators and replace with spaces to get all of the keywords in the description
                product_keywords = [word.lower() for word in ikea.get_search_results_product_description(product_overview).replace('-', ' ').replace('.', ' ').replace(',', ' ').replace('\\', ' ').replace('/', ' ').replace('+', ' ').split()]
                strict = product_has_keywords(required, product_keywords)
            if strict:
                product_page = fetch_non_angular_page(product_url)
                next_product = get_product_from_product_page(product_page, prod_tag, relative_rank+(page_num*products_per_page), product_url)
                if next_product is not None: products.append(next_product)
                relative_rank += 1
    return products

def get_products_for_query(query, prod_tag, required = None, products_per_page = __PRODUCTS_PER_PAGE):
    """Returns a list of Product found for the given query

    Args:
        query (str): query term(s)/product keyword(s)
        prod_tag (str): meta parameter for tagging the product for data storage purposes 
        required (list[str]): required keywords in product descriptions (lowercase)
        products_per_page (int): number of products to display per page of results
    
    Returns:
        list[product.Product]: products found for the query
    """
    # page numbers are indexed in the usual way
    search_results_url = get_url_for_query(query, 0)
    # the search results pages seem to be angular-generated while individual product pages are not
    search_results = fetch_angular_page(search_results_url)
    
    num_of_results = ikea.get_search_results_hit_count(search_results)
    num_of_pages = get_num_of_pages(num_of_results)
    products = []
    for page_num in range(num_of_pages):
        print('processing page #%d' % (page_num+1))
        # avoid reloading the first page - already done above
        if page_num != 0:
            search_results_url = get_url_for_query(query, page_num)
            search_results = fetch_angular_page(search_results_url)
        next_products = get_products_from_page_of_search_results(search_results, prod_tag, page_num, required, products_per_page)
        products.extend(next_products)
    return products

def product_has_keywords(required_keywords, product_keywords):
    """Returns True if a product with the given keywords has all of the given required keywords

    Args:
        required_keywords (list[str]): required keywords
        product_keywords (list[str]): keywords found for product
    
    Returns:
        bool: True if product has all required keywords, false otherwise
    """
    for required_keyword in required_keywords:
        if required_keyword not in product_keywords:
            return False
    return True
