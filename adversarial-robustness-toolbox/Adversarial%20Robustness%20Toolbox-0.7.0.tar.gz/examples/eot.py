"""
This is an example of how to compute expectation over transformations during an evasion attack in ART
"""
import keras
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential

from art.attacks import FastGradientMethod, ExpectationOverTransformations
from art.classifiers import KerasClassifier
from art.utils import load_mnist, random_targets


# Example MNIST classifier architecture with Keras & ART
def cnn_mnist_k(input_shape):
    # Create simple CNN
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    return model

# Load data and normalize
(x_train, y_train), (x_test, y_test), min_, max_ = load_mnist()

# Create a toy Keras CNN architecture & wrap it under ART interface
classifier = KerasClassifier((0, 1), cnn_mnist_k((28, 28, 1)), use_logits=False)
classifier.fit(x_train, y_train, nb_epochs=5, batch_size=128)


# Define transformation
def t(x):
    return x


def transformation():
    while True:
        yield t
eot = ExpectationOverTransformations(sample_size=1, transformation=transformation)
fgsm = FastGradientMethod(classifier=classifier, expectation=eot, targeted=True)
fgsm.generate(x_test, **{'y': random_targets(y_test, classifier.nb_classes)})
