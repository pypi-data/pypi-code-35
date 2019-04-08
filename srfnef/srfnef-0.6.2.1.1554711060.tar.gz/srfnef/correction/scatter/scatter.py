from .listmode2sinogram import lm2sino,sino2lm,get_all_lors_id
from .scatter_fraction import get_scatter_fraction
import srfnef as nef
import numpy as np
import time
import sys
from srfnef.typing import funcclass
np.seterr(divide='ignore', invalid='ignore')


@funcclass
class ScatterCorrector:
    low_energy: float
    high_energy: float
    resolution: float
    scatter_fraction: float

    def __call__(self,emission_image,u_map,scanner,listmode):
        lors = get_all_lors_id(scanner.nb_rings*scanner.nb_detectors_per_ring)
        sinogram = lm2sino(listmode,scanner)
        index = np.where(sinogram>0)[0].astype(np.int32)
        fraction,scale,atten = get_scatter_fraction(emission_image,u_map,index,lors,scanner,self.low_energy,self.high_energy,self.resolution)
        corrected_sinogram = np.zeros_like(sinogram)
        corrected_sinogram[index] = (sinogram[index]-fraction/np.sum(fraction)*np.sum(sinogram[index])*self.scatter_fraction)*scale/(atten+sys.float_info.min)
        corrected_data = sino2lm(scanner,corrected_sinogram,lors)
        return nef.Listmode(corrected_data[:,6],nef.Lors.from_fst_snd(corrected_data[:,0:3],corrected_data[:,3:6]))

    