import setuptools

setuptools.setup(name='RLDQN',
      version='0.0.5',
      description='Asynchronous DQN',
      long_description=open('README.rst').read(),
      url='https://github.com/screenwidth/GameAI/tree/master/RLDQN',
      author='maigua',
      author_email='396032050@qq.com',
      license='MIT',
      install_requires=[
        'numpy==1.12','tensorflow==1.1.0','scipy==0.19.0','Keras==2.0.4','six==1.10.0',
            'gym==0.9.1'
        ],
      packages=setuptools.find_packages())
