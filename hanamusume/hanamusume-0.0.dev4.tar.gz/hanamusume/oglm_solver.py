import sys, os
import math
from hanamusume.utils import check_read
        
class OGLMSolver(object):
    def __init__(self, pred=None, bias=True, dim=2**20, alpha=0.1, beta=0.001, l1=0.00001, l2=0.000001):
        self.__name__ = 'OGLMSolver'
        self._dim = dim
        self._w = {}
        self._n = {}
        self._z = {}
        self._a = alpha
        self._b = beta
        self._l1 = l1
        self._l2 = l2
        self._bias = bias
        if pred is None:
            raise AttributeError('OGLMSolver requires a prediction function')
        else:
            self._pred = pred
        
    def predict(self, x):
        dec = 0
        if self._bias:
            x[-1] = 1.
        for i in x:
            if i in self._w:
                dec += self._w[i]*x[i]
        return self._pred(dec)
    
    def update(self, x,p,y):
        if self._bias:
            x[-1] = 1.
        g = (p - y)
        if g == 0:
            return
        for i in x:
            gi = g * x[i]
            self._z[i] = self._z.get(i,0.) + gi
            if i in self._w:
                if i in self._n:
                    ni = self._n[i]
                    self._z[i] -= (1/self._a)*((ni + gi**2)**0.5 - ni**0.5)*self._w[i]
                else:
                    self._z[i] -= gi * self._w[i]
            self._n[i] = self._n.get(i,0.) + gi**2
        for i in x:
            zi = self._z[i]
            ni = self._n[i]
            if abs(zi) > self._l1:
                if zi > 0:
                    self._w[i] = -1/((self._b+ni**0.5)/self._a + self._l2)*(zi-self._l1)
                else:
                    self._w[i] = -1/((self._b+ni**0.5)/self._a + self._l2)*(zi+self._l1)
                    
    def predict_update(self, x,y):
        p = self.predict(x)
        self.update(x, p, y)

    def train_batch(self, data_X, data_y, epoch=20):
        for _ in range(epoch):
           for yy, xx in zip(data_y, data_X):
               self.predict_update(xx,yy)

    def save_model(self, filename, override=False):
        if not override and os.path.exists(filename):
            raise IOError('{} exists'.format(filename))
        i_w = set(self._w.keys())
        i_z = set(self._z.keys())
        i_n = set(self._n.keys())
        assert i_w == i_z
        assert i_w == i_n
        with open(filename,'w') as f:
            f.write('self.__name__:{}\n'.format(self.__name__))
            f.write('self._dim:{}\n'.format(self._dim))
            f.write('self._a:{}\n'.format(self._a))
            f.write('self._b:{}\n'.format(self._b))
            f.write('self._l1:{}\n'.format(self._l1))
            f.write('self._l2:{}\n'.format(self._l2))
            f.write('self._bias:{}\n'.format(self._bias))
            f.write('ind w,z,n:\n')
            for index in sorted(i_w):
                f.write('{} {},{},{}'.format(index, self._w[index], self._z[index], self._n[index]))
                f.write('\n')

    def load_model(self, filename):
        with open(filename) as f:
            check_read(f.readline(),'self.__name__', self.__name__)
            self._dim = int(check_read(f.readline(),'self._dim'))
            self._a = float(check_read(f.readline(),'self._a'))
            self._b = float(check_read(f.readline(),'self._b'))
            self._l1 = float(check_read(f.readline(),'self._l1'))
            self._l2 = float(check_read(f.readline(),'self._l2'))
            self._bias = (check_read(f.readline(),'self._bias') == 'True')
            assert f.readline().strip() == 'ind w,z,n:'
            for line in f.readlines():
                index ,wzn = line.split()
                w,z,n = wzn.split(',')
                index = int(index)
                self._w[index] = float(w)
                self._z[index] = float(z)
                self._n[index] = float(n)
