#!/usr/bin/env python3
from setuptools import setup
import sys


def readme():
    with open("README.rst", "r") as f:
        return f.read()


setup(
    name="agenda",
    version="0.1",
    description="Programmable agenda application.",
    long_description=readme(),
    author="kspi",
    author_email="kspi@github.com",
    url="https://github.com/kspi/agenda",
    license="LGPLv2.1 or later",
    packages=['agenda'],
    scripts=["bin/agenda"],

    install_requires=[
        "icalendar",
        "pyephem",
        "pyxdg",
        "parsedatetime",
    ],
)
