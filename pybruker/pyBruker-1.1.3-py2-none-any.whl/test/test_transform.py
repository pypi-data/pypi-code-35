import pybruker as brk
from pprint import pprint
filepath = '/Users/shlee419/Projects/dataset/RawData/20180904_150338_20180904_PDL_RobinsonTHS_1_1'
epi_num = 5

raw = brk.BrukerRaw(filepath)

dic_reco = raw.get_dic_reco(raw.scans, epi_num, 1)
dic_method = raw.get_dic_method(raw.scans, epi_num)

print(raw.subject_entry)
print(raw.subject_position)
import numpy as np
core_extent = dic_reco['core_extent']
shape = dic_reco['shape']
dist = dic_reco['dist']
core_extent.append(shape[2] * dist)
print(core_extent)

resol = np.asarray(map(float, core_extent)) / np.asarray(shape[:3])
temp_resol = raw.get_temp_resol(dic_method)
orient = dic_reco['method_slice_orient']

for i in [resol, temp_resol, orient, dic_reco['tf']]:
    pprint(i)

#%%
import pybruker as brk
from pprint import pprint
filepath = '/Users/shlee419/Projects/dataset/RawData/20180905_140013_20180905_NDP_Robinson_1_1'
epi_num = 11

raw = brk.BrukerRaw(filepath)
# pprint(raw.print_summary(True))

dic_reco = raw.get_dic_reco(raw.scans, epi_num, 1)
dic_method = raw.get_dic_method(raw.scans, epi_num)

#
print(raw.subject_entry)
print(raw.subject_position)
import numpy as np
core_extent = dic_reco['core_extent']
shape = dic_reco['shape']
dist = dic_reco['dist']
core_extent.append(shape[2] * dist)
print(core_extent)

resol = np.asarray(map(float, core_extent)) / np.asarray(shape[:3])
temp_resol = raw.get_temp_resol(dic_method)
orient = dic_reco['method_slice_orient']

for i in [resol, temp_resol, orient, dic_reco['tf']]:
    pprint(i)


#%%


#%%

#%%
raw.get_code(dic_reco)
#%%
raw.get_resol(dic_reco)