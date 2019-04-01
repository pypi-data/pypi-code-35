"""This module contains all classes referring to the contact
   objects at the at the bottom of a quilted resume.
"""


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


class EmailContact:
    """The email part in the contact list"""
    def __init__(self, email, icons=None):
        self.label = 'email'
        self.value = email  # need to validate
        self.icons = icons or ['fa-envelope']


class PhoneContact:
    """The phone part in the contact list"""
    def __init__(self, phone, icons=None):
        self.label = 'phone'
        self.value = phone  # need to validate
        self.icons = icons or ['fa-phone']


class SocialContact:
    """The social part in the contact list"""
    def __init__(self, handle=None, sites=None, **kwargs):
        """A social contact whose sites will be iconified and grouped

        Args:
            handle: handle or username for sites like twitter,
                    facebook, linkedin, github...etc as str
            sites: a list of strings for social sites that will be
                   converted into icons and links
            kwargs: extra arguments that were passed by deserialization

        Returns:
            A social contact object
        """
        self.label = 'social'
        self.value = handle
        self.icons = self._iconify(sites)

    def _iconify(self, sites):
        """appends fa- to list of sites to create the font awesome
           icon string
        """
        return list(map(lambda i: 'fa-' + i, sites))
