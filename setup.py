# -*- coding: utf-8 -*-
#!/usr/bin/python
""" This is the setup script for Pypelid which uses setuptools for automatic installation.

    Based on: 
    - https://packaging.python.org/en/latest/distributing.html
    - https://github.com/pypa/sampleproject.

    Some reasources about how to write one of these that may or may not add to one's understanding: 
    - http://pythonhosted.org/setuptools,
    - https://docs.python.org/2/distutils,
    - http://python-packaging.readthedocs.org,
    - https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts,
    - http://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use,
    - https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications

"""

# Always prefer setuptools over distutils
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
# To use a consistent encoding
from codecs import open
import os
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


os.system("git describe --always && echo version = \\\"`git describe --always`\\\" > datam/version.py")
from datam import version

setup(
    name = 'datam',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html    
    version = version.version,

    description = 'data manager',
    long_description = long_description,

    # The project's main homepage.
    url = 'https://gitlab.euclid-sgs.uk/bgranett/datacontrol',
    download_url = 'none',

    # Author details
    author = 'Ben Granett',
    author_email = 'ben.granett@brera.inaf.it',

    license = "GPL",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GPL License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='astronomy',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages = ['datam'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],


    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # Other possible resources about this rather complicated topic:
    # - https://pip.pypa.io/en/latest/user_guide/#requirements-files,
    # - https://pip.pypa.io/en/latest/reference/pip_install/#requirements-file-format,
    # - http://setuptools.readthedocs.io/en/latest/setuptools.html#id13,
    # - http://stackoverflow.com/questions/11032125/how-can-i-make-setuptools-install-a-package-from-another-source-thats-also-avai,
    install_requires = [
        'pyblake2',
         ],
    # Specify these in pip url syntax, prepend 'git+' if you want to do fancy things like .git@branch or .git@commit.
    dependency_links = [
        ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points = {
        'console_scripts': [
            'datam = datam.dm:main',
            ]
        },

    # Tests
    test_suite = 'nose.collector',
    tests_require = ['nose'],
)
