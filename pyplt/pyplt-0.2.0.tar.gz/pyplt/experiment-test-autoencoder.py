from pyplt.experiment import Experiment
from pyplt.plalgorithms.ranksvm import RankSVM
from pyplt.util.enums import KernelType
from pyplt.evaluation.cross_validation import KFoldCrossValidation
from pyplt.autoencoder import Autoencoder
import time

exp = Experiment()

# load ratings data
# exp.load_single_data("..\\sample data sets\\single_synth.csv", has_ids=True, has_fnames=True)

# dir_path = "C:\\Users\\Elizabeth Camilleri\\Documents\\PLT Project\\mario believability dataset\\"
# exp.load_object_data(dir_path + "objects.csv", has_ids=True, has_fnames=True)
# exp.load_rank_data(dir_path + "rankings_good_mario.csv", has_ids=False, has_fnames=False)

dir_path = "C:\\Users\\Elizabeth Camilleri\\Documents\\PLT Project\\sonanciadataset_modified\\"
exp.load_object_data(dir_path + "OpenSMILE Low-Level Descriptors\\General_AllFeatures_DataSet(Unpruned).csv",
                     has_ids=True, has_fnames=True)
exp.load_rank_data(dir_path + "Preference_Annotations\\Arousal_General_Preferences.csv",
                   has_ids=False, has_fnames=False)

# set up autoencoder
# ae = Autoencoder(input_size=18, code_size=4, encoder_topology=[8], decoder_topology=[8], epochs=100)
ae = Autoencoder(input_size=387, code_size=48, encoder_topology=[194, 97], decoder_topology=[97, 194], epochs=1000, learn_rate=0.05)
exp.set_autoencoder(ae)

# set up RankSVM algorithm
pl_algorithm = RankSVM(kernel=KernelType.RBF, gamma=1)
exp.set_pl_algorithm(pl_algorithm)

# set up K-Fold Cross Validation
pl_evaluator = KFoldCrossValidation(k=3)
exp.set_pl_evaluator(pl_evaluator)

# run the experiment
exp.run()

# save the results
t = time.time()
exp.save_exp_log(t, path="my_results.csv")
