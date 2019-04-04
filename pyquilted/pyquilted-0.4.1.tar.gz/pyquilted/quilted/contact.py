"""This module contains all classes referring to the contact
   objects at the at the bottom of a quilted resume.
"""


class EmailContact:
    """The email part in the contact list"""
    def __init__(self, email, icons=None):
        self.label = 'email'
        self.value = email  # need to validate
        self.icons = icons or ['fa-envelope']
        self.link = 'mailto:' + email


class PhoneContact:
    """The phone part in the contact list"""
    def __init__(self, phone, icons=None):
        self.label = 'phone'
        self.value = phone  # need to validate
        self.icons = icons or ['fa-phone']
        self.link = 'tel:+1' + self.to_digits()

    def to_digits(self):
        return ''.join(i for i in self.value if i.isdigit())


class SocialContact:
    """The social part in the contact list"""
    def __init__(self, handle=None, sites=None, link=None, **kwargs):
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
        self.link = link

    def _iconify(self, sites):
        """appends fa- to list of sites to create the font awesome
           icon string
        """
        return list(map(lambda i: 'fa-' + i, sites))
