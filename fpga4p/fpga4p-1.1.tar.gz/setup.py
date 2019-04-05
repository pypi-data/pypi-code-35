from setuptools import setup

setup(
    name="fpga4p",
    version='1.1',
    packages=['fpga4p',
              'fpga4p.classify',
              'fpga4p.train'],
    include_package_data=True,
    install_requires=[
        'Click',
        'singleton_decorator',
        'pyserial',
        'colorama',
        'pandas',
        'setuptools'],

    description='Python package / GNU Linux terminal utility for porting machine learning algorithms to FPGA.',
    long_description="""
    MANUAL:

    Training opportunities:

        1) Training tasks executes in parallel processes.

        2) Each training task generates: ".sv" file for FPGA, ".wd" file
         and ".tar" archive with model data for prospective
             classification task.


    Training specialities:

        1) "training_file.csv" must contain classes in the first column.

        2) "training_file.csv" must not contain a column head.

        3) The character - separator of "training_file.csv" must be ",".

        4) You can check available training algorithms with option "--info".


    Classification opportunities:

        1) Classification tasks might be executed parallel on several FPGAs.

        2) Several classification tasks, addressed to FPGA, execute consistently.

        3) Each classification task generates ".csv" file with predicted answers.


    Classification specialities:

        1) "classification_file.csv" must not contain a column head.

        2) The character - separator of "training_file.csv" must be ",".

        3) The "word_dict.wd" might match to firmware of FPGA.

        4) You can check available training algorithms and USB serial ports
            with option "--info".

    Examples:

         1) This example starts the training task:

            $ fpga4p --trn "training.csv,train_nbc"

        2) This example starts the classification task:

            $ fpga4p --cls "class.csv,classify_nbc,training.wd,/dev/ttyUSB0"

        3) This example prints available modules for training and
            classification, as well as available serial USB ports:


            $ fpga4p --info
    """,

    entry_points='''
        [console_scripts]
        fpga4p=fpga4p.start:entry_point
    ''',
    author='Dmitriy Mandjiev, Pavel Ivanov',
    author_email='fmnpro19@gmail.com',
    platform='GNU/LINUX'
)
