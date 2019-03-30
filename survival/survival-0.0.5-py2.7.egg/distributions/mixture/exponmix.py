import numpy as np

class ExpMix():
    def __init__(self, x):
        if x is not None:
            self.x=x

    @staticmethod
    def loglik_(x, mu, lmb, u):
        return np.log(u*mu*np.exp(-mu*x)+(1-u)*lmb*np.exp(-lmb*x))

    def loglik(self, x):
        return ExpMix.loglik_(self.x, self.mu, self.lmb, self.u)

