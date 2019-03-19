from distutils.core import setup

setup(
    name='democlassi',
    version='0.1.0',
    author='A. Alka M. Salissou',
    author_email='alkasalissou@hotmail.com',
    packages=['vision_utils', 'emotion_detection', 'multitask_rag'],
    url='https://github.com/AlkaSaliss/DEmoClassi',
    license='LICENSE',
    description='Collection of my python functions for training pytorch models to classify emotion, age, race, gender',
    long_description=open('README.md').read(),
    install_requires=[
        "torch",
        "torchvision",
        "pytorch-ignite",
        "imutils",
        "dlib",
        "kaggle",
        "tensorboardX",
    ],
)
