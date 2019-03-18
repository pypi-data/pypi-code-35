import h5py, numpy
import pygrisb


class gsolver_h5:
    '''base class to solver Gutzwiller embedding Hamiltonian.
    '''
    def __init__(self, imp=1):
        # impurity index
        self.imp = imp
        self.emol = 0.

    def driver(self):
        self.set_parameters()
        self.evaluate()
        self.save_results()

    def evaluate(self)  :
        pass

    @property
    def dm(self):
        return self._dm

    def set_parameters(self):
        with h5py.File(f'EMBED_HAMIL_{self.imp}.h5', 'r') as f:
            self.d = f['/D'][()].T
            self.h1e = f['/H1E'][()].T
            self.lam = f['/LAMBDA'][()].T

    def save_results(self):
        with h5py.File(f'EMBED_HAMIL_RES_{self.imp}.h5', 'w') as f:
            f['/DM'] = self._dm.T
            f['/emol'] = self.emol


class gsolver_h5ml(gsolver_h5):
    '''machine learning eigen solver class.
    '''
    def driver(self):
        self.set_parameters()
        self.sanity_check()
        self.reduce_parameters()
        self.evaluate()
        self.save_results()

    def sanity_check(self):
        pass

    def set_ref_data_path(self):
        self.ref_path = pygrisb.__path__[0]+"/ref_data/"


class gsolver_h5ml_fsoc(gsolver_h5ml):
    '''machine learning eigen solver class for f-eletron system gutzwiller
    embedding hamiltonian with spin-orbit interactin only.
    '''
    def __init__(self, nval, imp=1):
        self.nval = nval
        self.l = 3
        super().__init__(imp)

    def reduce_parameters(self):
        # unique parameters for h_embed with spin-orbit interaction only.
        self.e1 = self.h1e[0,0].real
        self.e2 = self.h1e[6,6].real
        self.l1 = self.lam[0,0].real
        self.l2 = self.lam[6,6].real
        # convert d to negative real convention.
        d1 = self.d[0,0]
        self.d1_phase = -d1/numpy.abs(d1)
        self.d1 = (d1*numpy.conj(self.d1_phase)).real
        d2 = self.d[6,6]
        self.d2_phase = -d2/numpy.abs(d2)
        self.d2 = (d2*numpy.conj(self.d2_phase)).real
        # Reparameterize
        delta = (self.e1+self.e2+self.l1+self.l2)/4.0
        delta1 = (self.e1-self.e2)/2.0
        delta2 = (self.l1-self.l2)/2.0
        # Build vector representing point to predict
        self.v = numpy.array([self.d1,self.d2,delta,delta1,delta2])

    def get_density_matrix(self):
        na2 = (2*self.l+1)*2
        na4 = na2*2
        dm = numpy.zeros([na4, na4], dtype=numpy.complex)
        # j = 5/2 block
        idx = numpy.arange(2*self.l)
        dm[idx, idx] = self.res[0]
        dm[idx+na2, idx+na2] = self.res[2]
        dm[idx, idx+na2] = self.res[4]*numpy.conj(self.d1_phase)
        dm[idx+na2, idx] = self.res[4]*self.d1_phase
        # j = 7/2 block
        idx = numpy.arange(2*self.l, na2)
        dm[idx, idx] = self.res[1]
        dm[idx+na2, idx+na2] = self.res[3]
        dm[idx, idx+na2] = self.res[5]*numpy.conj(self.d2_phase)
        dm[idx+na2, idx] = self.res[5]*self.d2_phase
        # normalize dm to half-filling case.
        dm += (na2-dm.trace())/na4*numpy.eye(na4)
        self._dm = dm

    def check_unique_elements(self):
        print(self._dm[[0,6,14,20,0,6], [0,6,14,20,14,20]])

