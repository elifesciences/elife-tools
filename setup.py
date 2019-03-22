from setuptools import setup

import elifetools

with open('README.rst') as fp:
    README = fp.read()

setup(
    name='elifetools',
    version=elifetools.__version__,
    description='Tools for using article data in Python.',
    long_description=README,
    packages=['elifetools'],
    license='MIT',
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "python-slugify",
        "six"
    ],
    url='https://github.com/elifesciences/elife-tools',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='py@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ])
