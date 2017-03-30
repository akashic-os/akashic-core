import os
from setuptools import setup

from os import listdir
from os.path import isfile, join

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

scripts = ['akashic/bin/'+f for f in listdir('akashic/bin') if isfile(join('akashic/bin', f))]
print(scripts)

setup(
    name = "akashic",
    version = "0.0.1",
    author = "traverseda (Alex Davies)",
    author_email = "traverseda@gmail.com",
    description = ("Unix Style tools for dealing with json stored in rethinkdb"),
    license = "lgpl",
    keywords = "rethinkdb oject store",
    url = "https://github.com/traverseda/akashic",
    install_requires=[
        "rethinkdb",
        "arrow",
        "deepdiff",
        "marshmallow",
    ],
    packages=['akashic'],
    long_description=read('README.md'),
    scripts= scripts,
#    classifiers=[
#        "Topic :: Utilities",
#    ],
)
