#! /usr/bin/env python

descr = "Gathers unstructured News data into a SQLite3 db"

from distutils.core import setup

setup(
    name='GatherNews',
    version='0.2.2',
    maintainer='Tyler Brown',
    maintainer_email='tylers.pile@gmail.com',
    packages=['gathernews'],
    scripts=['examples/ex_gRSS.py'],
    url='http://pypi.python.org/pypi/GatherNews/',
    license='doc/LICENSE.txt',
    description= descr,
    long_description=open('README.md').read(),
    install_requires=[
        "feedparser",
        "requests",
    ],
)
