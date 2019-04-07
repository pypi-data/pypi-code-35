#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function,
                            unicode_literals)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--eps", help="genereate .eps file",action="store_true")
args = parser.parse_args()

if args.eps:
  import matplotlib
  matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import ellc

# AI Phe - approximately
phase = np.linspace(-0.3,0.8,num=5001)
t_zero = 0.0
period = 24.6
sbratio = 0.5
r_1 = 0.03760
r_2 = 0.06125
incl = 88.36
a = 47.9
q = 1.042
f_c = -0.15065
f_s =  0.40555

t = phase*period

ld_1 = 'power-2'
ldc_1 = [0.60, 0.52]
ld_2 = 'power-2'
ldc_2 = [0.66, 0.63]

lc = ellc.lc(t,t_zero=t_zero, period=period, a=a, q=q,verbose=4,
    ld_1=ld_1,ldc_1=ldc_1,ld_2=ld_2,ldc_2=ldc_2,f_c=f_c, f_s=f_s,
    radius_1=r_1, radius_2=r_2,incl=incl,sbratio=sbratio)

lc_0 = ellc.lc(t,t_zero=t_zero, period=period, a=0, q=q,
    ld_1=ld_1,ldc_1=ldc_1,ld_2=ld_2,ldc_2=ldc_2,f_c=f_c, f_s=f_s,
    radius_1=r_1, radius_2=r_2,incl=incl,sbratio=sbratio)

fontsize=9
fig=plt.figure(1,figsize=(8,4))
fig=plt.figure(1)
plt.subplot(211)
plt.xlim([-0.25,0.75])
plt.ylim([0.4,1.1])
plt.plot(phase,lc,color='darkblue')
plt.xlabel("Time [d]",fontsize=fontsize)
plt.ylabel("Flux",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)

plt.subplot(223)
plt.xlim([-0.03,0.03])
plt.plot(phase,1e6*(lc-lc_0),color='darkblue')
plt.xlabel("Time [d]",fontsize=fontsize)
plt.ylabel(r"Flux$_{\rm LTTE}$ -Flux$_{\rm no LTTE}$ [ppm]",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)

plt.subplot(224)
plt.xlim([0.42,0.485])
plt.plot(phase,1e6*(lc-lc_0),color='darkblue')
plt.xlabel("Time [d]",fontsize=fontsize)
plt.tick_params(axis='both', labelsize=fontsize)

plt.tight_layout()
if args.eps:
  fig.savefig("ltte.eps")
else:
  plt.show()

