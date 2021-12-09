#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-experiments',
    version='0.1.0',
    author='Matt Battifarano',
    author_email='matthew.battifarano@gmail.com',
    maintainer='Matt Battifarano',
    maintainer_email='matthew.battifarano@gmail.com',
    license='MIT',
    url='https://github.com/mbattifarano/pytest-experiments',
    description='A pytest plugin for numerical experiments.',
    long_description=read('README.rst'),
    packages=find_packages(where='src', exclude=['test']),
    package_dir={"": "src"},
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'experiments = pytest_experiments.fixtures',
        ],
    },
)
