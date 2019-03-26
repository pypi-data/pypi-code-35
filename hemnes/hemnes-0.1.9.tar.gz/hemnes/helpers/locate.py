"""Helper functions for locating elements of interest on beautifulsoup of ikea's webpages

Attributes:
  __COLORS (set[str]): set of colors to search for on product pages

Todo:
  * get all colors of a product

"""

__author__ = 'sayeef moyen'

# import
from bs4 import BeautifulSoup as bs

# file attributes
__COLORS = {
    'white',
    'aluminum',
    'nickel',
    'turquoise',
    'brass',
    'mustard',
    'silver',
    'golden',
    'bronze',
    'platinum',
    'iron',
    'black',
    'beige',
    'tan',
    'eggshell',
    'egg',
    'granite',
    'pink',
    'rose',
    'gold',
    'copper',
    'amber',
    'indigo',
    'lavender',
    'onyx',
    'steel',
    'cream',
    'vanilla',
    'ivory',
    'coffee',
    'gray',
    'grey',
    'blue',
    'cyan',
    'teal',
    'navy',
    'green',
    'chartreuse',
    'perrywinkle',
    'red',
    'scarlet',
    'purple',
    'magenta',
    'yellow',
    'orange',
    'violet',
    'indigo'
}

def get_product_page_product_colors(product_overview):
    """Returns the colors of a product given it's over

    Args:
        product_overview (bs4.Tag): soup of the product overview

    Returns:
        list[str]: product color(s)
    """
    short_descr = product_overview.find('span', id='type')
    if short_descr is None or short_descr.string is None: return None
    return [color for color in short_descr.string.strip().replace(',', '').replace('/', '').replace('\\', '').replace('-', '').split() if color in __COLORS]

def get_product_page_product_images(product_container):
    """Returns a list of img urls for a product given it's container

    Args:
        product_container (bs4.Tag): soup of the product container

    Returns:
        list[str]: product img urls
    """
    # Container is mispelled on purpose
    img_container = product_container.find('div', id='mainImgConatiner')
    if img_container is None: return None

    images = []
    # ikea unpredictably leaves out the thumb container for products with a single image, so we check both if the thumbs are missing
    thumb_container = img_container.find('div', id='moreImgThumbContainer')
    if thumb_container is not None:
        thumbs = thumb_container.find_all('div', class_='imageThumb')
        for thumb in thumbs:
            url_extension = thumb.find('img')['src']
            # get rid of this *(SDF*SDFSDFSDLF
            # only want jpgs
            if url_extension.split('.')[-1].lower() == 'jpg':
                images.append('https://www.ikea.com%s' % (url_extension))
    # try the main product image
    else:
        main_img = img_container.find('img', id='productImg')
        if main_img is not None:
            url_extension = main_img['src']
            # only want jpgs
            if url_extension.split('.')[-1].lower == 'jpg':
                images.append('https://www.ikea.com%s' % (url_extension))

    return images if len(images) > 0 else None

def get_product_page_product_name(product_overview):
    """Returns the name of the product given it's overview

    Args:
        product_overview (bs4.Tag): soup of the product overview

    Returns:
        str: product name
    """
    name_tag = product_overview.find('span', id='name')
    if name_tag is None: return None
    return name_tag.string.strip()

def get_product_page_product_price(product_overview):
    """Returns the price of the product given it's overview

    Args:
        product_overview (bs4.Tag): soup of the product overview

    Returns:
        float: product price
    """
    price_tag = product_overview.find('span', id='price1')
    if price_tag is None: return None
    return float(price_tag.string.strip().split()[0].strip().replace('$', '').replace(',', ''))

def get_product_page_product_rating(product_container):
    """Returns the product rating given it's container

    Args:
        product_container (bs4.Tag): soup of the product container

    Returns:
        float: product rating
    """
    rating_container = product_container.find('div', id='ratingStarsReview')
    if rating_container is None: return None
    rating_wrapper = rating_container.find('a', class_='ratingsCount')
    if rating_wrapper is None: return None
    try:
        rating = float(rating_wrapper.string.strip())
        return rating
    except:
        return 0.0

def get_search_results_hit_count(search_results):
    """Returns total number of results given a page of search results

    Args:
        search_results (bs4.Tag): soup of a page of search results

    Returns:
        int: number of results
    """
    products_container = locate_search_results_products_container(search_results)
    if products_container is None: return 0
    result_summary = products_container.find('h2', id='resultSummary')
    if result_summary is None or result_summary.string is None: return 0
    return int(result_summary.string.strip().split()[0])

def get_search_results_product_description(product_overview):
    """Returns the product's short description given it's overview tag

    Args:
        product_overview (bs4.Tag): soup of the product's overview

    Returns:
        str: short product description
    """
    return product_overview.string.strip()

def get_search_results_product_link(product_overview):
    """Returns the url to the product's page given it's overview tag

    Args:
        product_overview (bs4.Tag): soup of the product's overview

    Returns:
        str: url to the product
    """
    return product_overview['href'].strip()

def locate_product_page_product_container(product_page):
    """Returns the product container given soup of a product's page

    Args:
        product_page (bs4.BeautifulSoup): soup of the product's page
   
    Returns:
        bs4.Tag: soup of the product container
    """
    return product_page.find('div', class_='rightContent')

def locate_product_page_product_overview(product_container):
    """Returns the product overview given the product container

    Args:
        product_container (bs4.Tag): soup of the product container

    Returns:
        bs4.Tag: soup of the product overview
    """
    return product_container.find('div', id='productInfoWrapper2')

def locate_search_results_product_overview(product_container):
    """Returns tag containing link and description given a product's container tag
    
    Args:
        product_container (bs4.Tag): soup of the product's container
    
    Returns:
        bs4.Tag: tag containing link and short description
    """
    return product_container.find('a', class_='short-desc')

def locate_search_results_products(products_container):
    """Returns all of the products on a given page of search results

    Args:
        products_container (bs4.Tag): soup of the products container for a page of search results

    Returns:
        list[bs4.Tag]: list of individual product tags
    """
    return [product.find('div', class_='unbxd-result-item-wrapper') for product in products_container.find_all('div', class_='pseudo-wrapper-2')]

def locate_search_results_products_container(search_results):
    """Returns products container for a page of search results

    Args:
        search_results (bs4.BeautifulSoup): soup of page of search results

    Returns:
        bs4.Tag: soup of the products container
    """
    return search_results.find('div', class_='unbxd-results-meta')
