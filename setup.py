"""Install the disk-objectstore implementation."""
import os
import io

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

MODULENAME = 'disk_objectstore'
THE_LICENSE = 'The MIT license'

# Get the version number in a dirty way
FOLDER = os.path.split(os.path.abspath(__file__))[0]
FNAME = os.path.join(FOLDER, MODULENAME, '__init__.py')
with open(FNAME) as init:
    # Get lines that match, remove comment part
    # (assuming it's not in the string...)
    VERSIONLINES = [l.partition('#')[0] for l in init.readlines() if l.startswith('__version__')]
assert len(VERSIONLINES) == 1, 'Unable to detect the version lines'
VERSIONLINE = VERSIONLINES[0]
VERSION = VERSIONLINE.partition('=')[2].replace('"', '').replace("'", '').strip()

setup(
    name=MODULENAME,
    description='An implementation of an efficient object store writing directly into a disk folder',
    url='http://github.com/aiidateam/disk-objectstore',
    license=THE_LICENSE,
    author='Giovanni Pizzi',
    version=VERSION,
    install_requires=[
        'sqlalchemy',
    ],
    extras_require={
        'dev': [
            'click', 'coverage', 'memory-profiler', 'pre-commit', 'profilehooks', 'prospector', 'psutil', 'pylint',
            'pytest', 'pytest-cov', 'pytest-benchmark', 'pywin32; platform_system == "Windows"', 'yapf'
        ],
    },
    packages=find_packages(),
    # Needed to include some static files declared in MANIFEST.in
    include_package_data=True,
    keywords=[
        'object store',
        'repository',
        'file store',
    ],
    long_description=io.open(os.path.join(FOLDER, 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8', 'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X', 'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux', 'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
