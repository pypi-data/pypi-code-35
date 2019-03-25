import numpy as np
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

from pyplt.autoencoder import Autoencoder

mnist = input_data.read_data_sets("/MNIST_data/", one_hot=True)

# autoencoder = Autoencoder(input_size=18, code_size=4, encoder_topology=[14, 8], decoder_topology=[8, 14])

# MNIST example...

autoencoder = Autoencoder(input_size=784, code_size=196, encoder_topology=[392], decoder_topology=[392], epochs=50)

samples = mnist.train.images

# train encoder
autoencoder.train(samples)

# encode samples
encoded_samples = autoencoder.encode(samples)

# test the model
num_test_images = 10
results = autoencoder.predict(mnist.test.images[:num_test_images])

# do final clean up (close tf.Session)
autoencoder.clean_up()

# Comparing original images with reconstructions
f, a = plt.subplots(2, 10, figsize=(20, 4))
for i in range(num_test_images):
    a[0][i].imshow(np.reshape(mnist.test.images[i], (28, 28)))
    a[1][i].imshow(np.reshape(results[i], (28, 28)))

plt.show()
