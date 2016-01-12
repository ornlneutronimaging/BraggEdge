#!/usr/bin/env python

from setuptools import setup, find_packages

# define distribution
setup(
    name = "braggedge",
    version = "0.1",
    packages = find_packages("python", exclude=['tests', 'notebooks']),
    package_dir = {'': "python"},
    test_suite = 'tests',
    install_requires = [
        'numpy',
    ],
    dependency_links = [
    ],
    author = "iVenus team",
    description = "Bragg Edge work at the SNS",
    license = 'BSD',
    keywords = "neutron imaging",
    url = "https://github.com/ornlneutronimaging/BraggEdge",
    # download_url = '',
)

# End of file
