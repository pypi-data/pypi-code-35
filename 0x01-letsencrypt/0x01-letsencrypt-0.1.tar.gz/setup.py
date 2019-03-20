from setuptools import setup

setup(
    name='0x01-letsencrypt',
    version='0.1',
    description="Let's Encrypt library for human beings",
    url='https://github.com/Smart-Hypercube/autocert',
    author='Hypercube',
    author_email='hypercube@0x01.me',
    license='MIT',
    py_modules=['letsencrypt'],
    python_requires='>=3.6',
    install_requires=['acme>=0.32'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
    ],
)
