from Orange.preprocess.discretize import Discretization, Discretizer


class IntervalDiscretizer(Discretization):
    """Discretizes the data with the given cut-off points.

    .. attribute:: points
       
       Dictionary of the following format:
       
       {
          'table1': {
              'att1': [p11, p12, ...],
              'att2': [p21, p22, ...],
              ...
          },
          ...
       }
    """
    def __init__(self, points):
        self.points = points

    def __call__(self, data, attribute):
        att_points = self.points[data.name][attribute.name]
        return Discretizer.create_discretized_var(data.domain[attribute], att_points)
