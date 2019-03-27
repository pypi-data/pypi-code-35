import inspect
import os

from openlego.api import AbstractDiscipline
from ssbjkadmos.tools import ssbj_scalers, ssbj_nonscalers, scale_values
from ssbjkadmos.utils.general import get_dict_name


class SsbjDiscipline(AbstractDiscipline):

    @property
    def name(self):
        # type: () -> str
        """:obj:`str`: Name of this discipline."""
        return self.__class__.__name__

    @property
    def creator(self):
        return u'S. Dubreuil and R. Lafage'

    @property
    def owner(self):
        return u'J. Sobieszczanski-Sobieski'

    @property
    def operator(self):
        return u'I. van Gent'

    @property
    def description(self):
        return u'Discipline of the SSBJ test case.'

    @property
    def version(self):
        return u'1.0'

    @property
    def path(self):
        # type: () -> str
        """:obj:`str`: Path at which this discipline resides."""
        return os.path.dirname(inspect.getfile(self.__class__))

    @property
    def scale_values(self):
        return scale_values

    @property
    def scalers(self):
        if self.scale_values:
            return ssbj_scalers
        else:
            return ssbj_nonscalers

    def generate_input_xml(self):
        raise NotImplementedError

    def generate_output_xml(self):
        raise NotImplementedError

    def get_scaler(self, xpath):
        return self.scalers[get_dict_name(xpath)]

    def scale_value(self, val, xpath):
        return val/self.scalers[get_dict_name(xpath)]

    def unscale_float_value(self, xpath, doc):
        return float(doc.xpath(xpath)[0].text) * self.scalers[get_dict_name(xpath)]
