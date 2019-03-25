import numpy as np
import matplotlib.pyplot as plt

from pyplt.autoencoder import Autoencoder
from pyplt.experiment import Experiment

# autoencoder = Autoencoder(input_size=18, code_size=4, encoder_topology=[14, 8], decoder_topology=[8, 14])

# MNIST example...

autoencoder = Autoencoder(input_size=3, code_size=1, encoder_topology=[2], decoder_topology=[2], epochs=10)

exp = Experiment()
exp.load_single_data("..\\sample data sets\\single_synth.csv", has_ids=True, has_fnames=True)
samples = exp.get_data().iloc[:, 1:-1].values  # exclude ID column and ratings column
print("Original samples: ")
print(samples)

# train encoder
autoencoder.train(samples)

# encode samples
encoded_samples = autoencoder.encode(samples)

# test the model
results = autoencoder.predict(samples)

# do final clean up (close tf.Session)
autoencoder.clean_up()

# Comparing original images with reconstructions
print("Results: ")
print(results)
