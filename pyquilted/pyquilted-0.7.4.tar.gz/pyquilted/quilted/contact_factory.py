from pyquilted.quilted.contact import *


class ContactFactory:
    """A factory class that returns contact objects"""
    @staticmethod
    def create(key, val):
        contact = None
        if key in 'email':
            contact = EmailContact(val)
        elif key in 'phone':
            contact = PhoneContact(val)
        elif key in 'social':
            contact = SocialContact(**val)
        return contact
