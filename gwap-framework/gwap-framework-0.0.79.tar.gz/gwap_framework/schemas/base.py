from schematics import Model


class BaseSchema(Model):

    def __hash__(self):
        return hash(tuple(self))
