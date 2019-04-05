"""
Functions to preproces images from the web or a local machine
"""

import cv2
import numpy as np
import urllib, requests
from io import BytesIO
from PIL import Image

def img_read_url(url, h = 256, w = 256, to_grey = False, timeout = 2):
    """
    Returns an image via an url
    
    Parameters
    ----------
    url : string 
        url (in a string format)
    h: int 
        Desired height of the returned image (px)
    w: int 
        Desired width of the returned image (px)   
    to_grey: bool
        should the image be returned in greyscale? 
    timeout: int
        maximum wait time before dropping the request
    
    Returns
    -------
    numpy.ndarray
        a numpy array width dimensions (h, w, 3) or (h, w, 1) if to_grey=True
    """        
        
    resp = urllib.request.urlopen(url, timeout = timeout)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)[...,::-1]
    image = cv2.resize(image, (h, w))
    if(to_grey):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image   

def img_read_url_PIL(url, h = 256, w = 256, timeout = 2):
    """
    Returns an image via an url (using PIL framework)
    
    Parameters
    ----------
    url : string 
        url (in a string format)
    h: int 
        Desired height of the returned image (px)
    w: int 
        Desired width of the returned image (px)   
    timeout: int
        maximum wait time before dropping the request
    
    Returns
    -------
    PIL.Image.Image
        a PIL image
    """
    
    response = requests.get(url)    
    image = Image.open(BytesIO(response.content))
    image = image.resize((h, w), Image.ANTIALIAS)
        
    return image   

def img_read(path, h = 256, w = 256, to_grey = False):
    """
    Reads an image from the local machine
    
    Parameters
    ----------
    path : string 
        path to image on a local machine
    h: int 
        Desired height of the returned image (px)
    w: int 
        Desired width of the returned image (px)   
    to_grey: bool
        Should the image be returned in greyscale? 
    
    Returns
    -------
    numpy.ndarray
        a numpy array width dimensions (h, w, 3) or (h, w, 1) if to_grey=True
    """
    image = cv2.imread(path)[...,::-1]
    image = cv2.resize(image, (h, w))
    if(to_grey):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image 

def return_image_hist(image, no_bins_per_channel=10, normalize=False):
    """ 
    Function to get the histogram of the colours in a photo
    
    Parameters
    ----------
    image : numpy ndarray 
        A numpy array with the shape (x, y, 3)
    no_bins_per_channel: int 
        How many bins should a histgoram have for each channel of colors
    normalize : bool 
        Should the coordinates add up to 1?

    Returns
    -------
    A list of size 3 * no_bins_per_channel representing the distribution
    of colors in the image
    
    """
    hist_container = []
    for channel in range(3):
        hist = cv2.calcHist([image], [channel], None, [no_bins_per_channel], [0, 256])    
        hist = [x[0] for x in hist.tolist()]
        hist_container += hist
    
    if normalize:
        hist_container = [x/np.sum(hist_container) for x in hist_container]
    
    return hist_container    
