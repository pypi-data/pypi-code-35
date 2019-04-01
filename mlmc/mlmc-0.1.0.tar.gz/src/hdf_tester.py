import h5py


# file_path = "/home/martin/Documents/01_MLMC_data/exp_0.3_1/mlmc_5.hdf"
# file_path = "/home/martin/Documents/MLMC/test/_test_tmp/mlmc_5.hdf5"
#
# hdf_file = h5py.File(file_path, 'r')
#
# #print(hdf_file['Levels/0/collected_ids'])
# #print(hdf_file['ints'])
#
# for attr_name, attr_value in hdf_file.attrs.items():
#     print("attr name ", attr_name)
#     print("attr value ", attr_value)
import numpy as np
import json

with open('/home/martin/Documents/profiler.json', "r") as f:
    prof_content = json.load(f)

print("prof content ", prof_content)
print("prof_content['children'][0] ", prof_content['children'][0])

for name, value in prof_content['children'][0].items():
    print("name ", name)
    print("value ", value)
print(prof_content['children'][0]['cumul-time-sum'])


exit()

f = h5py.File("swmr.hdf5", 'r+', libver='latest')
arr = np.array([1, 2, 3, 4])
dset = f.create_dataset("data", chunks=(2,), maxshape=(None,), data=arr)
f.swmr_mode = True
# Now it is safe for the reader to open the swmr.h5 file
for i in range(5):
    new_shape = ((i+1) * len(arr), )
    dset.resize(new_shape)
    dset[i*len(arr):] = arr
    dset.flush()

f = h5py.File("swmr.hdf5", 'r', libver='latest', swmr=True)
dset = f["data"]
while True:
    dset.id.refresh()
    shape = dset.shape
    print(shape)
    break

f = h5py.File("swmr.hdf5", 'r', libver='latest', swmr=True)

f_append = h5py.File("swmr.hdf5", 'a', libver='latest')


f.close()

    # Notify the r
# file_name = "test"
# file_reader = h5py.File(file_name, 'r')
# print(file_reader.attrs)
#
# file_reader.close()
#
#
# file_writer = h5py.File(file_name, 'w')
#
# dset = file_writer.create_dataset("first", (100,))
# print("dset name ", dset.name)
#
# file_writer.close()
#
# file_writer = h5py.File(file_name, 'w')
# file_writer.create_dataset("second", (100,))
# file_writer.close()

#print("hdf file attributes ", hdf_file.attrs.items())