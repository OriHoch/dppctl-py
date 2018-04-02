from setuptools import setup, find_packages
import os, time


if os.path.exists("VERSION.txt"):
    # this file can be written by CI tools (e.g. Travis)
    with open("VERSION.txt") as version_file:
        version = version_file.read().strip().strip("v")
else:
    version = str(time.time())


setup(
    name="dppctl",
    version=version,
    packages=find_packages(exclude=["tests", "test.*"]),
    install_requires=[],
    url='https://github.com/OriHoch/dppctl-py',
    license='MIT',
    entry_points={
      'console_scripts': [
        'dppctl = dppctl.cli:cli',
      ]
    },
)
