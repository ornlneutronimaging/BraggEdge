
#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = "neutronbraggedge",
    version = "0.2",
    packages = find_packages("python", exclude=['tests', 'notebooks']),
    package_dir = {'': "python"},
    package_data = { 'python.neutronbraggedge' : ['material_list.dat']},
    include_package_data = True,
    test_suite = 'tests',
    install_requires = [
        'numpy',
        'configparser',
        'pandas',
        'lxml',
        'html5lib',
        'beautifulsoup4',
    ],
    dependency_links = [
    ],
    author = "iVenus team",
    author_email = "bilheuxjm@ornl.gov",
    description = "Bragg Edge work at the SNS",
    license = 'BSD',
    keywords = "neutron imaging bragg edge",
    url = "https://github.com/ornlneutronimaging/BraggEdge",
    classifiers = ['Development Status :: 3 - Alpha',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research'
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'],
    # download_url = '',
)


# End of file