from setuptools import setup

import elifetools

with open('README.rst') as fp:
    readme = fp.read()

with open('LICENSE') as fp:
    license = fp.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='elifetools',
      version=elifetools.__version__,
      description='Tools for using article data in Python.',
      long_description=readme,
      packages=['elifetools'],
      license = license,
      install_requires=install_requires
      )
