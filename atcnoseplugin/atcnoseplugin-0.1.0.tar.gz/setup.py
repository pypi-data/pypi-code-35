try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name='atcnoseplugin',
    version="0.1.0",
    description = 'test plugins for exec related plan based on nosetests',
    author = 'thomas.ning',
    author_email = 'ningruhu@163.com',
    license = 'MIT',
    long_description = """\

Extra plugins for the nose testing framework to atc exec \n

usage:\n
>>> nosetests --with-plan-loader --plan-file <test_plan_file> --loop <loop_num> --verbose \n

start from command-line:
    nosetests --with-plan-loader --plan-file plan1 --loop 100 --verbose

""",
    packages = ['atcnoseplugin'],
    entry_points = {
        'nose.plugins': [
            'file-output = atcnoseplugin.fileoutput:FileOutputPlugin',
            'plan-loader = atcnoseplugin.planloader:PlanLoaderPlugin',
            ],
         },
)
