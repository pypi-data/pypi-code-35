"""
**A hexagonal lattice of cylinders with disorder**

We observe the suppression of higher order peaks with increasing disorder (Debye-Waller like factor)
"""

import jscatter as js

q = js.loglist(0.001, 5, 1000)
unitcelllength = 50
N = 5
rms = 1
domainsize = unitcelllength * N
hexgrid = js.sf.hex2DLattice(unitcelllength, N)
p = js.grace()
p.multi(2, 1)
cyl = js.formel.pDA(js.ff.cylinder, sig=0.01, parname='radius', q=q, L=50, radius=15, SLD=1e-4)
cyl.Y = js.formel.smooth(cyl, 20)
for i, rms in enumerate([1, 3, 10, 30], 2):
    hex = js.sf.latticeStructureFactor(q, lattice=hexgrid, rmsd=rms, domainsize=domainsize)
    p[1].plot(hex, li=[1, 2, i], sy=0)
    p[0].plot(hex.X, hex.Y * cyl.Y, li=[1, 3, i], sy=0, le='hex cylinders rms= ' + str(rms))
p[0].plot(cyl, li=[3, 2, 1], sy=0, le='cylinder formfactor')
# pretty up
p[1].yaxis(scale='n', label='I(Q)', max=10, min=0)
p[0].yaxis(scale='l', label='I(Q)')  # ,max=10000,min=0.01)
p[0].xaxis(scale='n', label='', min=0)
p[1].xaxis(scale='n', label='Q / A\S-1', min=0)
p[0].legend(x=0.6, y=60, charsize=0.8)
p[0].title('hex lattice of cylinders')
p[0].subtitle('increasing disorder rmsd')

"""
**A hexagonal lattice of cylinders with disorder and diffusive scattering**

This model is for SBA-15 a silica with hexagonal pores.
Material defects in the matrix lead to diffusive scattering. 
The power law (Shin :math:`q^-4` ) is not included but the low Q behaviour 
described by Förster for mesoscopic materials with a  :math:`q^-1`

References 
Shin et al Progr Colloid Polym Sci (2006) 133: 116–122 DOI 10.1007/2882_069
Förster et al J. Phys. Chem. B 2005, 109, 1347-1360, DOI 10.1021/jp0467494 CCC:


"""

import jscatter as js


def hexcylinders(q, rms, domainsize, L, radius, unitcelllength, Adiff=1, sdiff=2, bgr=0.01, Ahex=1):
    # a hexagonal grid
    hexgrid = js.sf.hex2DLattice(unitcelllength, 5)
    # cylinder form factor
    cyl = js.formel.pDA(js.ff.cylinder, sig=0.01, parname='radius', q=q, L=L, radius=radius, SLD=1e-4)
    # calc the structure factor
    hex = js.sf.latticeStructureFactor(q, lattice=hexgrid, rmsd=rms, domainsize=domainsize)
    # combine with background and diffusive scattering
    hex.Y = Ahex * hex.Y * cyl.Y + Adiff / (1 + sdiff ** 2 * q ** 2) ** 2 + bgr
    # copy attributes
    hex.setattr(cyl)
    return hex


p = js.grace()
q = js.loglist(0.002, 3, 1000)
hex = hexcylinders(q, rms=1, unitcelllength=50, domainsize=200, L=0, radius=6, Adiff=0.0003, sdiff=4, bgr=0.001)
p[0].plot(hex, li=[1, 3, i], sy=0, le='hex cylinders rms= ' + str(rms))
# pretty up
p[0].yaxis(scale='l', label='I(Q)')  # ,max=10000,min=0.01)
p[0].xaxis(scale='l', label='', min=0)
p[0].legend(x=0.6, y=60, charsize=0.8)
p[0].title('hex lattice of cylinders')
p[0].subtitle('increasing disorder rmsd')

"""
**A membrane stack **

"""
import jscatter as js
import numpy as np

q = np.r_[0.1:7:500j]
unitcelllength = 60
N = 15
rms = 1
domainsize = unitcelllength * N
# define grid (size is not used)
lamgrid = js.sf.lamLattice(unitcelllength, 1)
p = js.grace()
p.multi(2, 1)
# single layer membrane
membrane = js.ff.multilayer(q, 6, 1)
for i, rms in enumerate([1, 2, 4, 6], 2):
    sf = js.sf.latticeStructureFactor(q, lattice=lamgrid, rmsd=rms, domainsize=domainsize)
    p[1].plot(sf, li=[1, 2, i], sy=0)
    p[0].plot(sf.X, sf.Y * membrane.Y + 0.008, li=[1, 3, i], sy=0, le='stacked membrane rms= ' + str(rms))
p[0].plot(membrane.X, membrane.Y + 0.008, li=[3, 2, 1], sy=0, le='membrane formfactor')
p[1].yaxis(scale='n', label='I(Q)', max=10, min=0)
p[0].yaxis(scale='l', label='I(Q)')  # ,max=10000,min=0.01)
p[0].xaxis(scale='l', label='', min=0)
p[1].xaxis(scale='l', label='Q / A\S-1', min=0)
p[0].legend(x=2, y=1, charsize=0.8)
p[0].title('lamellar layers with some background')
