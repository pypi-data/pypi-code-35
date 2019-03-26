#import
from decimal import Decimal

class Product:
    """Semantic class for storing products as they are scraped before writing to json"""
    
    def __init__(self, tag, name, rank, rating, price, color, imgs, link):
        self.tag = tag
        self.name = name
        self.rank = rank
        self.rating = rating
        self.price = price
        self.color = color
        self.imgs = imgs
        self.link = link

    def to_dict(self):
        return {
            'tag': self.tag,
            'name': self.name,
            'rank': self.rank,
            'rating': self.rating,
            'price': self.price,
            'color': self.color,
            'images': self.imgs,
            'url': self.link
        }
