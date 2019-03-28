# -----------------
# SMNet Blob
# Written by smarsu
# -----------------

import numpy as np
from .net import sm


class Blob(object):
    _name_id = 0

    def __init__(self, data=None, dtype=np.float32, name='blob'):
        self._data = None
        self._grad = 0

        self._dtype = dtype

        if data is not None:
            self.init_feed(data)

        self._name = self._get_name(name)


    def _get_name(self, name):
        Blob._name_id += 1
        return '_'.join([name, str(Blob._name_id)])

    
    def init_feed(self, v):
        v = np.array(v, dtype=self._dtype)
        # If the data is a scalar, then its shape needs to be set to [1].
        if not v.shape:
            v = np.reshape(v, [-1])
        self.feed(v)

    
    def feed(self, v):
        # We will not set shape here.
        self._data = v


    def add_grad(self, grad):
        if grad is 0:
            return self._grad

        if self._grad is 0:
            self._grad = grad  # Here may cause bug.
        else:
            self._grad += grad
        return self._grad


    def clear_grad(self):
        self._grad = 0
    

    # ----------------------------------------------------------------------
    # Attributes
    #

    @property
    def shape(self):
        return self._data.shape

    
    @property
    def data(self):
        return self._data

    
    @property
    def grad(self):
        return self._grad


    @property
    def dtype(self):
        return self._dtype

    
    @property
    def name(self):
        return self._name

    
    def __str__(self):
        return self._name

    
    def __repr__(self):
        return self.__str__()

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # Overloaded operator
    #
    # TODO(smarsu): Fix the problem of `cross import`.
    #

    # Arithmetic operation

    def __add__(self, v):
        from .layer import add
        return add(self, v)

    
    def __sub__(self, v):
        from .layer import subtract
        return subtract(self, v)

    
    def __mul__(self, v):
        from .layer import multiply
        return multiply(self, v)

    
    def __truediv__(self, v):
        from .layer import divide
        return divide(self, v)

    # InvArithmetic operation

    def __radd__(self, v):
        from .layer import add
        return add(v, self)
    

    def __rsub__(self, v):
        from .layer import subtract
        return subtract(v, self)

    
    def __rmul__(self, v):
        from .layer import multiply
        return multiply(v, self)

    
    def __rtruediv__(self, v):
        from .layer import divide
        return divide(v, self)

    # Unary operator

    def __pos__(self):
        return self
    

    def __neg__(self):
        from .layer import subtract
        return subtract(Tensor(0), self)

    # ----------------------------------------------------------------------


class Variable(Blob):
    def __init__(self, data=None, name='Variable', dtype=np.float32):
        """
        Attention: In theory, our Variable must have initialized values, 
                    we will not provide initialization at the network level.
        """
        assert data is not None, 'Variable: data can not be None'
        super(Variable, self).__init__(data, dtype=dtype, name=name)
        sm.add_variable(self)


    def update(self):
        if self._grad is not 0:
            self._data -= self._grad


class Tensor(Blob):
    def __init__(self, data=None, name='Tensor',  dtype=np.float32):
        super(Tensor, self).__init__(data, dtype=dtype, name=name)
        sm.add_tensor(self)


    def set_grad(self, grad):
        self._grad = grad
