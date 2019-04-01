"""
Data module

Data structure is stored inside ```GHData``` or ```TSData``` objects.

- ```GHData``` contains data that is described using g<sub>nm</sub> and h<sub>nm</sub> spherical harmonics coefficients.
- ```TSData``` contains data that is described using poloidal/toroidal decomposition (Tc<sub>nm</sub>, Ts<sub>nm</sub>, Sc<sub>nm</sub>, Ss<sub>nm</sub> coefficients).

```MeasureData``` is the parent class containing common behavior for ```GHData``` or ```TSData```


Create a new measure by instancing ```GHData``` or ```TSData```

```python
from webgeodyn.data import GHData, TSData
from webgeodyn.data.normPnm import semiNormalisedSchmidt

PnmNorm=semiNormalisedSchmidt
myData = GHData(data,lmax,units,measureType,PnmNorm,gridth=tharray,gridph=pharray):
# data :
#   2D array [time,harmonics coef]
#   or 3D array [time,harmonics coef, realisations]
# lmax : int
# units : string
# measureType : "MF", "SV" or "U"
# PnmNorm : normalisation function
# gridth (optimal) : array containing list of theta points
# gridph (optimal) : array containing list of phi points
```

```normPnm``` contains normalisation functions for Legendre functions :
- ```semiNormalisedSchmidt``` returns Schmidt semi-normalised coefficients (default).
- ```noNorm``` should be used instead when no normalisation is desired.

#### Operation on data

 - ###### Setting data

 To set a new data array for ```GHData``` or ```TSData```, use the setData function (do not overwrite data array manually, this may cause errors when computing data)

 ```python
 myData.setData(newdata)
 # newdata :
 #   2D array [time,harmonics coef]
 #   or 3D array [time,harmonics coef, realisations]
 ```

 - ###### Computing values into real space

To compute value on the globe (r, theta, phi) use computeRThetaPhiData function

 ```python
 globeData = myData.computeRThetaPhiData(r,thlist,phlist,components=["th","ph","norm"],usegridPnm=False,computeallrealisation=False,irealisation=-1)

 # Returns a dictonary containing for each component, a 3D array [time, theta, phi]
 # (if computeallrealisation=True, the return array is 4D [time, theta, phi, realisation])
 #
 # r : (float) radius
 # thlist : (array or list) list of theta points to be calculated
 # phlist : (array or list) list of phi points to be calculated
 #    phlist or thetalist can contain unique values [theta] or [phi]
 # components : list of components to be calculated. Can contain "r", "th", "ph", "norm" for GHData and "th", "ph", "norm", "divh" for TSData.
 # usegridPnm : Whether to use precalculated Pnm for listed th and ph values (warning, use only if thlist and phlist are equals to myData.th and myData.ph)
 # computeallrealisation: (boolean)
 #    if True, returns a 4D array [time, theta, phi, realisation]
 #    if False, returns a 3D array [time, theta, phi]
 # irealisation: (int)
 #    if irealisation<0, returns a 3D array [time, theta, phi] corresponding to the mean of realisations
 #    if irealisation>0, returns a 3D array [time, theta, phi] corresponding to the ith realisation

 ```

 - ###### k indice <-> l,m,coef

 To convert **g<sub>nm</sub>** (or g<sub>lm</sub>) to/from **k** indice in the data array use:

```python
k = myData.lm2k(l,m,coef)
# l (equivalent to n in other notations) : integer
# m : integer
# coef :
#    "g" or "h" for GHData
#    "tc", "ts", "sc", or "ss" for TSData
#
# returns :
# k : integer indice

```
```python
l,m,coef = myData.k2lm(k)
# k : integer indice
#
# returns :
# l (equivalent to n in other notations) : integer
# m : integer
# coef :
#    "g" or "h" for GHData
#    "tc", "ts", "sc", or "ss" for TSData

```
"""

from .TSData import TSData
from .GHData import GHData
