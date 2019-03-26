"""
GoodWan client library: classes
"""


class Basic:
    """ Basic class """

    def __repr__(self):
        """ Representation """
        return "<{}.{} {}>".format(
            self.__module__,
            self.__class__.__name__,
            ", ".join(
                "{}={}".format(k, v) for k, v in self.__dict__.items()
                if not k.startswith("__")
            )
        )
