#! /usr/bin/env python

descr = 'Structures and stores News data'

from distutils.core import setup

setup(
    name='GatherNews',
    version='0.1.0',
    maintainer='Tyler Brown',
    maintainer_email='tylers.pile@gmail.com',
    packages=['gathernews', 'gathernews.tests'],
    scripts=['examples/capture_example.py'],
    url='http://pypi.python.org/pypi/GatherNews/',
    license='doc/LICENSE.txt',
    description= descr,
    long_description=open('README.rst').read(),
    install_requires=[
        "argparse==1.2.1",
        "feedparser==5.1.3",
        "nose==1.3.0",
        "simpleflake==0.1.5",
        "wsgiref==0.1.2",
    ],
)
