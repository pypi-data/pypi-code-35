from pyquilted.quilted.heading_complex import HeadingComplex
from pyquilted.quilted.heading_simple import HeadingSimple
from pyquilted.quilted.contacts_list import ContactsList
from pyquilted.quilted.style_options import StyleOptions


class Resume:
    """The quilted resume object

       This object contains a heading, contact list and all section
       list of a resume. The content sections are sorted in order they
       appear in the data.
    """
    def __init__(self, heading=None, contacts=None, sections=None, style=None):
        self.heading = heading
        self.contacts = contacts or []
        self.sections = sections or []
        self.style = style or vars(StyleOptions())

    def add_section(self, section):
        if type(section) is HeadingComplex:
            self.style['heading_complex'] = True
            self._set_heading(section.serialize())
        elif type(section) is HeadingSimple:
            self._set_heading(section.serialize())
        elif type(section) is ContactsList:
            self._set_contacts(section.serialize())
        else:
            self.sections.append(section.serialize())

    def _set_heading(self, heading):
        self.heading = heading

    def _set_contacts(self, contacts):
        self.contacts = contacts
