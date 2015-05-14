from setuptools import setup

import elifetools

with open('README.rst') as fp:
    readme = fp.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='elifetools',
    version=elifetools.__version__,
    description='Tools for using article data in Python.',
    long_description=readme,
    packages=['elifetools'],
    license = 'MIT',
    install_requires=install_requires,
    url='https://github.com/elifesciences/elife-tools',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='py@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        ]
    )
