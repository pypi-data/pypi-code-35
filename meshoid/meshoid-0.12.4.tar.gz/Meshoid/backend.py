from numba import jit, vectorize, float32, float64, cfunc, njit
import numpy as np
from scipy.special import comb

@jit(fastmath=True)
def d2matrix(dx):
    N, Nngb, dim = dx.shape
    N_derivs = 2*dim + comb(dim, 2, exact=True)
    A = np.empty((N, Nngb, N_derivs), dtype=np.float64)    
    for k in range(N):
        for i in range(Nngb):
            for j in range(N_derivs):
                if j < dim:
                    A[k,i,j] = dx[k,i,j] 
                elif j < 2*dim:
                    A[k,i,j] = dx[k,i,j-dim] * dx[k,i,j-dim] / 2
                else:
                    A[k,i,j] = dx[k,i,(j+1)%dim] * dx[k,i,(j+2)%dim]  # this does the cross-terms, e.g. xy, xz, yz
    return A

@jit
def HsmlIter(neighbor_dists,  dim=3, error_norm=1e-6):
    if dim==3:
        norm = 32./3
    elif dim==2:
        norm = 40./7
    else:
        norm = 8./3
    N, des_ngb = neighbor_dists.shape
    hsml = np.zeros(N)
    n_ngb = 0.0
    bound_coeff = (1./(1-(2*norm)**(-1./3)))
    for i in range(N):
        upper = neighbor_dists[i,des_ngb-1] * bound_coeff
        lower = neighbor_dists[i,1]
        error = 1e100
        count = 0
        while error > error_norm:
            h = (upper + lower)/2
            n_ngb=0.0
            dngb=0.0
            q = 0.0
            for j in range(des_ngb):
                q = neighbor_dists[i, j]/h
                if q <= 0.5:
                    n_ngb += (1 - 6*q**2 + 6*q**3)
                elif q <= 1.0:
                    n_ngb += 2*(1-q)**3
            n_ngb *= norm
            if n_ngb > des_ngb:
                upper = h
            else:
                lower = h
            error = np.fabs(n_ngb-des_ngb)
        hsml[i] = h
    return hsml

@vectorize([float32(float32), float64(float64)])
def Kernel(q):
    if q <= 0.5:
        return 1 - 6*q**2 + 6*q**3
    elif q <= 1.0:
        return 2 * (1-q)**3
    else: return 0.0
    
@jit
def DF(f, ngb):
    if len(f.shape) > 1:
        df = np.empty((ngb.shape[0],ngb.shape[1], f.shape[1]))
    else:
        df = np.empty(ngb.shape)
    for i in range(ngb.shape[0]):
        for j in range(ngb.shape[1]):
            df[i,j] = f[ngb[i,j]] - f[i]
    return df
    
@jit
def PeriodicizeDX(dx, boxsize):
    for i in range(dx.size):
        if np.abs(dx[i]) > boxsize/2:
            dx[i] = -np.sign(dx[i])*(boxsize - np.abs(dx[i]))

@jit
def invngb(ngb):
    result = np.empty_like(ngb)
    for i in range(len(ngb)):
        ngbi = ngb[i]
        for j in range(ngb.shape[1]):
            for k in range(ngb.shape[1]):
                if ngb[ngbi[j],k]==i:
                    result[i,j]=k
                    break
                if k==ngb.shape[1]-1: result[i,j]=-1
    return result


@jit
def NearestNeighbors1D(x, des_ngb):
    N = len(x)
    neighbor_dists = np.empty((N,des_ngb))
    neighbors = np.empty((N,des_ngb),dtype=np.int64)
    for i in range(N):
        x0 = x[i]
        left = 0
#        if i == N-1:
#            right = 0
#        else:
#            right = 1
        right = 1
        total_ngb = 0
        while total_ngb < des_ngb:
            lpos = i - left
            rpos = i + right
            if lpos < 0:
                dl = 1e100
            else:
                dl = np.fabs(x0 - x[lpos])
            if rpos > N-1:
                dr = 1e100
            else:
                dr = np.fabs(x0 - x[rpos])

            if dl < dr:
                neighbors[i,total_ngb] = lpos
                neighbor_dists[i, total_ngb] = dl
                left += 1
            else:
                neighbors[i,total_ngb] = rpos
                neighbor_dists[i, total_ngb] = dr
                right += 1
            total_ngb += 1
    return neighbor_dists, neighbors

@jit
def invsort(index):
    out = np.empty_like(index)
    for i in range(len(index)):
        out[index[i]] = i

@njit(fastmath=True)
def GridSurfaceDensity(f, x, h, bounds, res=100):
    if len(bounds) > 2: bounds = bounds[:2]
    Lx = bounds[0,1] - bounds[0,0]
    Ly = bounds[1,1] - bounds[1,0]
    nx, ny = res, int(res*Ly/Lx + 0.5)
    dx = Lx/(nx-1)
    dy = Ly/(ny-1)

    x2d = x[:,:2] - bounds[:,0]
    
    grid = np.zeros((nx,ny))
    
    N = len(x)
    for i in range(N):
        xs = x2d[i]
        hs = h[i]
        hinv = 1/hs
        mh2 = f[i]*hinv*hinv
        
        gxmin = max(int((xs[0] - hs)/dx+1),0)
        gxmax = min(int((xs[0] + hs)/dx),nx-1)
        gymin = max(int((xs[1] - hs)/dy+1), 0)
        gymax = min(int((xs[1] + hs)/dy),ny-1)
        
        for gx in range(gxmin, gxmax+1):
            delta_x_Sqr = xs[0] - dx
            delta_x_Sqr *= delta_x_Sqr
            for gy in range(gymin,gymax+1):
                delta_y_Sqr = xs[1] - gy*dy
                delta_y_Sqr *= delta_y_Sqr
                q = np.sqrt(delta_x_Sqr + delta_y_Sqr) * hinv
                #if q <= 0.5:
                #    kernel = 1 - 6*q*q + 6*q*q*q
                #elif q <= 1.0:
                #    kernel = 2 * (1-q)*(1-q)*(1-q)
                #else:
                #    continue
                kernel = q
                #kernel = 1.8189136353359467 * Kernel2.ctypes(((xs[0] - gx*dx)**2 + (xs[1] - gy*dx)**2)**0.5 / hs)
#                kernel = 1.
                grid[gx,gy] += 1.8189136353359467 * kernel * mh2
#                count += 1
    return grid

@jit
def GridAverage(f, x, h, gridres, L):
#    count = 0
    grid1 = np.zeros((gridres,gridres))
    grid2 = np.zeros((gridres,gridres))
    dx = L/(gridres-1)
    N = len(x)
    for i in range(N):
        xs = x[i] + L/2
        hs = h[i]
        hinv = 1/hs
        mh2 = hinv * hinv
        fi = f[i]

        gxmin = max(int((xs[0] - hs)/dx+1),0)
        gxmax = min(int((xs[0] + hs)/dx),gridres-1)
        gymin = max(int((xs[1] - hs)/dx+1), 0)
        gymax = min(int((xs[1] + hs)/dx), gridres-1)
        
        for gx in range(gxmin, gxmax+1):
            for gy in range(gymin,gymax+1):
                q = np.sqrt((xs[0] - gx*dx)*(xs[0] - gx*dx) + (xs[1] - gy*dx)*(xs[1] - gy*dx)) * hinv
                if q <= 0.5:
                    kernel = 1 - 6*q**2 + 6*q**3
                elif q <= 1.0:
                    kernel = 2 * (1-q)**3
                kernel *= 1.8189136353359467
                grid1[gx,gy] +=  kernel * mh2
                grid2[gx,gy] +=  fi * kernel * mh2
#                count += 1

    return grid2/grid1
   
   
@jit
def GridSurfaceDensityPeriodic(mass, x, h, gridres, L, boxsize): # need to fix this
    x = (x+L/2)%boxsize
    grid = np.zeros((gridres,gridres))
    dx = L/(gridres-1)
    N = len(x)

    b2 = boxsize/2
    for i in range(N):
        xs = x[i]
        hs = h[i]
        mh2 = mass[i]/hs**2

        gxmin = int((xs[0] - hs)/dx + 1)
        gxmax = int((xs[0] + hs)/dx)
        gymin = int((xs[1] - hs)/dx + 1)
        gymax = int((xs[1] + hs)/dx)
        
        for gx in range(gxmin, gxmax+1):
            ix = gx%gridres
            for gy in range(gymin,gymax+1):
                iy = gy%gridres
                delta_x = np.abs(xs[0] - ix*dx)
                if b2 < delta_x: delta_x -= boxsize
                delta_y = np.abs(xs[1] - iy*dx)
                if b2 < delta_y: delta_y -= boxsize
                kernel = 1.8189136353359467 * Kernel((delta_x**2 + delta_y**2)**0.5 / hs)
                grid[ix,iy] +=  kernel * mh2
                 
    return grid

@jit
def ComputeFaces(ngb, ingb, vol, dweights):
    N, Nngb, dim = dweights.shape
    result = np.zeros_like(dweights)
    for i in range(N):
        for j in range(Nngb):
            result[i,j] += vol[i] * dweights[i,j]
            if ingb[i,j] > -1: result[ngb[i,j],ingb[i,j]] -= vol[i] * dweights[i,j]
    return result
