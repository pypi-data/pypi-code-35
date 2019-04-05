#MESHOID: MESHless Operations including Integrals and Derivatives
# "It's not a mesh; it's a meshoid!" - Alfred H. Einstimes

import numpy as np
from scipy.spatial import cKDTree
from scipy.linalg import inv
from scipy.special import comb
from numba import jit, vectorize, float32, float64, njit, guvectorize
from .backend import *
import h5py

class Meshoid(object):
    def __init__(self, pos, m=None, hsml=None, des_ngb=None, boxsize=None, verbose=False, particle_mask=None, n_jobs=1):
        """
        Arguments:
        x -- shape (N,3) array of particle positions

        Keyword arguments:
        m -- shape (N,) array of particle masses - defaults to 1    
        h -- shape (N,) array of particle kernel lengths
        des_ngb -- integer number of nearest neighbors (defaults to 4/20/32 for 1D/2D/3D)
        boxsize -- size of box if periodic boundary conditions
        verbose -- bool whether to print everything the code is doing to stdout
        particle_mask -- array-like of indices of the particles you want to compute things for (defaults to all)
        n_jobs -- number of logical cores available (default 1)
        """
    
        self.tree=None
        if len(pos.shape)==1:
            pos = pos[:,None]

        self.verbose = verbose
        self.N, self.dim = pos.shape
        if particle_mask is None:
            self.particle_mask = np.arange(self.N)
        else:
            self.particle_mask = particle_mask
        self.Nmask = len(self.particle_mask)
        
        if des_ngb==None:
            des_ngb = {1: 4, 2: 20, 3:32}[self.dim]
                
        self.des_ngb = des_ngb
        self.n_jobs = n_jobs    

        self.volnorm = {1: 2.0, 2: np.pi, 3: 4*np.pi/3}[self.dim]
        self.boxsize = boxsize
        self.pos = pos
        
        if self.boxsize is None:
            self.center = np.average(self.pos, axis=0)
            self.L = 2*np.percentile(np.sum((self.pos-self.center)**2,axis=1),90)**0.5
        else:
            self.center = np.ones(3) * self.boxsize / 2
            self.L = self.boxsize
            
        if m is None:
            m = np.repeat(1.,self.N)
        self.m = m[self.particle_mask]

        self.ngb = None
        self.hsml = hsml
        self.weights = None
        self.dweights = None
        self.d2weights = None
        self.sliceweights = None
        self.slicegrid = None

        if self.hsml is None:
#            self.hsml = -np.ones(self.N)
            self.TreeUpdate()
        else:
            self.vol = self.volnorm * self.hsml**self.dim / self.des_ngb
            self.density = self.m / self.vol


    def ComputeDWeights(self, order=1, weighted=True):
        if self.weights is None: self.TreeUpdate()
        
        dx = self.pos[self.ngb] - self.pos[self.particle_mask][:,None,:]
        self.dx = dx

        if order == 1:
            dx_matrix = np.einsum('ij,ijk,ijl->ikl', self.weights, dx, dx, optimize='greedy') # matrix for least-squares fit to a linear function
        
            dx_matrix = np.linalg.inv(dx_matrix) # invert the matrices 
            self.dweights = np.einsum('ikl,ijl,ij->ijk',dx_matrix, dx, self.weights, optimize='greedy') # gradient estimator is sum over j of dweight_ij (f_j - f_i)
        elif order == 2:
            if weighted: w = self.weights
            else: w = np.ones_like(self.weights)
            Nngb = self.des_ngb
            N_derivs = 2*self.dim + comb(self.dim, 2, exact=True)            
            dx_matrix = d2matrix(dx)
            dx_matrix2 = np.einsum('ij,ijk,ijl->ikl', w, dx_matrix, dx_matrix, optimize='optimal')
            dx_matrix2 = np.linalg.inv(dx_matrix2)
            self.d2weights = np.einsum('ikl,ijl,ij->ijk', dx_matrix2, dx_matrix, w, optimize='optimal')

            self.d2weights, self.dweights_3rdorder = self.d2weights[:,:,self.dim:], self.d2weights[:,:,:self.dim]
            # gradient estimator is sum over j of dweight_ij (f_j - f_i)

    def TreeUpdate(self):
        if self.verbose: print("Finding nearest neighbours...")
                
        self.tree = cKDTree(self.pos, boxsize=self.boxsize)
        self.ngbdist, self.ngb = self.tree.query(self.pos[self.particle_mask], self.des_ngb, n_jobs=self.n_jobs)
                
        if self.verbose: print("Neighbours found!")

        if self.verbose: print("Iterating for smoothing lengths...")

        self.hsml = HsmlIter(self.ngbdist, error_norm=1e-13,dim=self.dim)
        if self.verbose: print("Smoothing lengths found!")

        q = self.ngbdist / self.hsml[:,None]
        K = Kernel(q)
        self.weights = K / np.sum(K, axis=1)[:,None]
        self.density = self.des_ngb * self.m / (self.volnorm * self.hsml**self.dim)
        self.vol = self.m / self.density

    def Volume(self):
        return self.vol

    def NearestNeighbors(self):
        if self.ngb is None: self.TreeUpdate()
        return self.ngb

    def NeighborDistance(self):
        if self.ngbdist is None: self.TreeUpdate()
        return self.ngbdist

    def SmoothingLength(self):
        return self.hsml

    def Density(self):
        return self.density

    def D(self, f):
        """
        Computes the kernel-weighted least-squares gradient estimator of the function f.

        Arguments:
        f -- shape (N,...) array of (possibly vector- or tensor-valued) function values (N is the total number of particles)

        Returns:
        gradf - (Nmask, ..., dim) array of partial derivatives, evaluated at the positions of the particles in the particle mask
        """
        #if len(f) == self.N:
        #    f = f[self.particle_mask]
            
        if self.ngb is None: self.TreeUpdate()
            
        df = f[self.ngb] - f[self.particle_mask,None] #DF(f, self.ngb)
        
        if self.dweights is None:
            self.ComputeDWeights()
        return np.einsum('ijk,ij...->i...k',self.dweights,df, optimize='greedy')

    def D2(self, f, weighted=True):
        """
        Computes the kernel-weighted least-squares Jacobian estimator of the function f.

        Arguments:
        f -- shape (N,...) array of (possibly vector- or tensor-valued) function values (N is the total number of particles)

        Returns:
        jacf - (Nmask, ..., dim,dim) array of partial derivatives, evaluated at the positions of the particles in the particle mask
        """
        if self.ngb is None: self.TreeUpdate()
            
        df = f[self.ngb] - f[self.particle_mask,None]

        if self.d2weights is None:
            self.ComputeDWeights(2, weighted=weighted)
        return np.einsum('ijk,ij...->i...k',self.d2weights,df, optimize='greedy')
        

    def Curl(self, v):
        dv = self.D(v)
        return np.c_[dv[:,1,2]-dv[:,2,1], dv[:,0,2]-dv[:,2,0], dv[:,0,1] - dv[:,1,0]]
        
    def Div(self, v):
        dv = self.D(v)
        return dv[:,0,0]+dv[:,1,1] + dv[:,2,2]
    
    def Integrate(self, f):
        if self.hsml is None: self.TreeUpdate()
        elif self.vol is None: self.vol = self.volnorm * self.hsml**self.dim
        return np.einsum('i,i...->...', self.vol,f)

    def KernelVariance(self, f):
        if self.ngb is None: self.TreeUpdate()
#        return np.einsum('ij,ij->i', (f[self.ngb] - self.KernelAverage(f)[:,np.newaxis])**2, self.weights)
        return np.std(f[self.ngb], axis=1)
    
    def KernelAverage(self, f):
        if self.weights is None: self.TreeUpdate()        
        return np.einsum('ij,ij->i',self.weights, f[self.ngb])

    def Slice(self, f, size=None, plane='z', center=None, res=100, gridngb=32):
        
        if center is None: center = self.center
        if size is None: size = self.L
        if self.tree is None: self.TreeUpdate()
        
        x, y = np.linspace(-size/2,size/2,res), np.linspace(-size/2, size/2,res)
        x, y = np.meshgrid(x, y)

        self.slicegrid = np.c_[x.flatten(), y.flatten(), np.zeros(res*res)] + center
        if plane=='x':
            self.slicegrid = np.c_[np.zeros(res*res), x.flatten(), y.flatten()] + center
        elif plane=='y':
            self.slicegrid = np.c_[x.flatten(), np.zeros(res*res), y.flatten()] + center
        
        ngbdist, ngb = self.tree.query(self.slicegrid,gridngb)

        if gridngb > 1:
            hgrid = HsmlIter(ngbdist,dim=3,error_norm=1e-3, particle_mask=self.particle_mask)
            self.sliceweights = Kernel(np.einsum('ij,i->ij',ngbdist, hgrid**-1))
            self.sliceweights = np.einsum('ij,i->ij', self.sliceweights, 1/np.sum(self.sliceweights,axis=1))
        else:
            self.sliceweights = np.ones(ngbdist.shape)

        if len(f.shape)>1:
            return np.einsum('ij,ij...->i...', self.sliceweights, f[ngb]).reshape((res,res,f.shape[-1]))
        else:
            return np.einsum('ij,ij...->i...', self.sliceweights, f[ngb]).reshape((res,res))

    def SurfaceDensity(self, f=None, size=None, plane='z', center=None, res=128, smooth_fac=1.):
        if f is None: f = self.m
        if center is None: center = self.center
        if size is None: size = self.L
#        if self.boxsize is None:
        return GridSurfaceDensity(f, self.pos, np.clip(smooth_fac*self.hsml, 2*size/res,1e100), np.c_[self.center - size/2,self.center + size/2], res)
        #else:
#            return GridSurfaceDensityPeriodic(f, (self.pos-center) % self.boxsize, np.clip(self.h, size/res,1e100), res, size, self.boxsize)

    def ProjectedAverage(self, f, size=None, plane='z', center=None, res=128):
        if size is None: size = self.L
        if center is None: center = self.center
        return GridAverage(f, self.pos-center, np.clip(self.hsml, size/res,1e100), res, size)

    def Projection(self, f, size=None, plane='z', center=None, res=128, smooth_fac=1.):
        if size is None: size = self.L
        if center is None: center = self.center
        return GridSurfaceDensity(f * self.vol, self.pos-center, np.clip(smooth_fac*self.hsml, 2*size/res,1e100), res, size) #GridSurfaceDensity(f * self.vol, size, plane=plane, center=center,res=res)

    def KDE(self, grid, bandwidth=None):
        if bandwidth is None:
            bandwidth = self.SmoothingLength()

        f = np.zeros_like(grid)
        gtree = cKDTree(np.c_[grid,])
        for d, bw in zip(self.pos, bandwidth):
            ngb = gtree.query_ball_point(d, bw)
            ngbdist = np.abs(grid[ngb] - d)
            f[ngb] += Kernel(ngbdist/bw) / bw * 4./3
            
        return f

def FromSnapshot(filename, ptype=None):
    F = h5py.File(filename)
    meshoids = {}
    if ptype is None: types = list(F.keys())[1:]
    else: types = ["PartType%d"%ptype,]
    for k in types:
        x = np.array(F[k]["Coordinates"])
        m = np.array(F[k]["Masses"])
        if "SmoothingLength" in list(F[k].keys()):
            h = np.array(F[k]["SmoothingLength"])
        elif "AGS-Softening" in list(F[k].keys()):
            h = np.array(F[k]["AGS-Softening"])
        else:
            h = None
        boxsize = F["Header"].attrs["BoxSize"]
        if np.any(x<0): boxsize=None    
        if ptype is None:
            meshoids[k] = meshoid(x, m, h,boxsize=boxsize)
        else: return meshoid(x,m,h,boxsize=boxsize)
    F.close()
    return meshoids

