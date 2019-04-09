from pyquilted.quilted.detail_factory import DetailFactory
from pyquilted.quilted.detail import Objective
from pyquilted.quilted.heading_details import HeadingDetails


class HeadingDetailsBuilder:
    def __init__(self, odict):
        self.odict = odict
        self.heading_details = HeadingDetails(**odict)

    def deserialize(self):
        for key in self.odict.keys():
            detail = DetailFactory.create(key, self.odict)
            if detail:
                self._add_detail(detail)

        return self.heading_details

    def _add_detail(self, detail):
        if isinstance(detail, Objective):
            self.heading_details.set_objective(detail)
        else:
            self.heading_details.add_detail(detail)
