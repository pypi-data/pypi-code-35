from setuptools import setup

setup(
    name='text_classifikation',
    version='0.1',
    packages=['text_classifikation', 'text_classifikation.features',
              'text_classifikation.classifiers',
              'text_classifikation.classifiers.sgd',
              'text_classifikation.classifiers.svm',
              'text_classifikation.classifiers.tree',
              'text_classifikation.classifiers.naive',
              'text_classifikation.classifiers.ridge',
              'text_classifikation.classifiers.forest',
              'text_classifikation.classifiers.logreg',
              'text_classifikation.classifiers.adaboost',
              'text_classifikation.classifiers.gradboost',
              'text_classifikation.classifiers.perceptron',
              'text_classifikation.classifiers.passive_agressive'],
    url='https://github.com/JarbasAl/text_classifikation',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='utils to find best text classifier for your data'
)
