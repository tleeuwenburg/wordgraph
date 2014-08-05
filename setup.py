import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="wordgraph",
    version="0.0.1",
    author="Tennessee Leeuwenburg",
    author_email="tleeuwenburg@gmail.com",
    description=("Produce a lexical description of graphs"),
    license = "Apache2",
    keywords = "python3",
    package_data={
        'wordgraph': [
            'realiser/templates/en/long/*.txt',
        ]
    },
    packages=['wordgraph', 'wordgraph.realiser', 'tests'],
    install_requires=[
        'setuptools',
    ],
    url="https://github.com/tleeuwenburg/wordgraph/blob/master/README.md",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License",
    ],
)
