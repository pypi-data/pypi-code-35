from pynosql.base.base_model import BaseModel
from pynosql.common.model_helper import ModelHelper


class Model(BaseModel):
    """ Model """

    BASE = {}

    def __init__(self, base_model=BASE):
        self.mh = ModelHelper(base_model)

    @property
    def model(self):
        """ Return Model

        :return: obj model
        """
        return self.mh.model

    def reset(self):
        """ Reset Model

        :return: None
        """
        self.mh.reset()

    def load(self, values, is_list=False):
        """ Load Model Values

        :param values: obj values
        :param is_list: bool if list expected
        :return: obj model
        """
        return self.mh.load(values, is_list)
