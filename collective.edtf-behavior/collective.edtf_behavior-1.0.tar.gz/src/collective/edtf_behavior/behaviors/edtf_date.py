# -*- coding: utf-8 -*-

from collective.edtf_behavior import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider

import edtf


class IEDTFDateMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IEDTFDate(model.Schema):
    """
    """

    edtf_date = schema.TextLine(
        title=_(u'Date'),
        description=_(
            u'Enter a date or date interval in <a target="_blank" href="http://www.loc.gov/standards/datetime/edtf.html">EDTF</a> format. Examples: "1860-03-31", "1860-03~," or "1860-03-31/1860-04-15"',  # NOQA E501
        ),
        required=False,
    )


@implementer(IEDTFDate)
@adapter(IEDTFDateMarker)
class EDTFDate(object):
    def __init__(self, context):
        self.context = context

    @property
    def edtf_date(self):
        if hasattr(self.context, 'edtf_date'):  # NOQA: P002
            return self.context.edtf_date
        return None

    @edtf_date.setter
    def edtf_date(self, value):
        edtf_date = value
        self.context.edtf_date = edtf_date

    @property
    def date_earliest(self):
        if not self.context.edtf_date:
            return
        edtf_obj = edtf.parse_edtf(self.context.edtf_date)
        if not edtf_obj:
            return
        return edtf.struct_time_to_date(edtf_obj.lower_fuzzy())

    @property
    def date_latest(self):
        if not self.context.edtf_date:
            return
        edtf_obj = edtf.parse_edtf(self.context.edtf_date)
        if not edtf_obj:
            return
        return edtf.struct_time_to_date(edtf_obj.upper_fuzzy())

    @property
    def date_sort_ascending(self):
        if not self.context.edtf_date:
            return
        edtf_obj = edtf.parse_edtf(self.context.edtf_date)
        if not edtf_obj:
            return
        return edtf.struct_time_to_date(edtf_obj.lower_strict())

    @property
    def date_sort_descending(self):
        if not self.context.edtf_date:
            return
        edtf_obj = edtf.parse_edtf(self.context.edtf_date)
        if not edtf_obj:
            return
        return edtf.struct_time_to_date(edtf_obj.upper_strict())
