import pygsti
from pygsti.construction import std1Q_XYI as std

from mpi4py import MPI
comm = MPI.COMM_WORLD

target_model = std.target_model().copy()
target_model.set_all_parameterizations("CPTP")
target_model.set_simtype('matrix') # the default for 1Q, so we could remove this line


maxLengths = [1,2,4,8,16] #,32,64,128,256]
mdl_datagen = std.target_model().depolarize(op_noise=0.1, spam_noise=0.001)
listOfExperiments = pygsti.construction.make_lsgst_experiment_list(
    std.target_model(), std.prepStrs, std.effectStrs, std.germs, maxLengths)
ds = pygsti.construction.generate_fake_data(mdl_datagen, listOfExperiments,
                                            nSamples=1000, sampleError="multinomial", seed=1234)

results = pygsti.do_long_sequence_gst(ds, target_model, std.prepStrs, std.effectStrs,
                                      std.germs, maxLengths, verbosity=4, comm=comm)
