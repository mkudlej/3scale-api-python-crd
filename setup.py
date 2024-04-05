import re
import sys

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "devel"
if sys.argv[1] == "--release-version":
    sys.argv.pop(1)
    VERSION = sys.argv.pop(1)
    assert re.match(r"[0-9]+\.[0-9]+\.[0-9]+", VERSION), "Version definition required as first arg"

requirements = ['3scale-api', 'openshift-client']

extra_requirements = {
    'dev': [
        'flake8',
        'mypy',
        'pylint',
        'pytest',
        'python-dotenv',
        'backoff'
    ],
    'docs': ['sphinx']
}

setup(name='3scale-api-crd',
      version=VERSION,
      description='3scale CRD Python Client',
      author='Martin Kudlej',
      author_email='kudlej.martin@gmail.com',
      maintainer='Martin Kudlej',
      url='https://github.com/3scale-qe/3scale-api-python-crd',
      packages=find_packages(exclude=("tests",)),
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extra_requirements,
      entry_points={},
      classifiers=[
          "Programming Language :: Python :: 3",
          'Programming Language :: Python :: 3.11',
          "Operating System :: OS Independent",
          "License :: OSI Approved :: Apache Software License",
          'Intended Audience :: Developers',
          'Topic :: Utilities',
      ],
      )
