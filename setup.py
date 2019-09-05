import setuptools
import sys

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

# We raise an error if trying to install with python2
if sys.version[0] == '2':
    print("Error: This package must be installed with python3")
    sys.exit(1)

setuptools.setup(
    name="mape_maker_pkg",
    version="2.0.0",
    author="Guillaume_Goujard",
    author_email="guillaume.goujard@polytechnique.edu",
    description="A small package to simulate timeseries according to a training dataset and a target error",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/GuillaumeGoujard/mape_maker_up_to_date",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # install_requires=install_requires,
    include_package_data=True,
)