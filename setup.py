import os
import io

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

modulename = 'disk_objectstore'
the_license = "The MIT license"

# Get the version number in a dirty way
folder = os.path.split(os.path.abspath(__file__))[0]
fname = os.path.join(folder, modulename, '__init__.py')
with open(fname) as init:
    ns = {}
    # Get lines that match, remove comment part
    # (assuming it's not in the string...)
    versionlines = [
        l.partition('#')[0]
        for l in init.readlines()
        if l.startswith('__version__')
    ]
if len(versionlines) != 1:
    raise ValueError("Unable to detect the version lines")
versionline = versionlines[0]
version = versionline.partition('=')[2].replace('"', '').strip()

setup(
    name=modulename,
    description=
    "An implementation of an efficient object store writing directly into a disk folder",
    url='http://github.com/giovannipizzi/disk-objectstore',
    license=the_license,
    author='Giovanni Pizzi',
    version=version,
    install_requires=[
        'sqlalchemy',
    ],
    extras_require={
        "testing": [
            'profilehooks',
            'psutil',
            'click',
            'numpy',
        ],
    },
    packages=find_packages(),
    # Needed to include some static files declared in MANIFEST.in
    include_package_data=True,
    keywords=[
        'object store', 'repository', 'file store',
    ],
    long_description=io.open(os.path.join(folder, 'README.md'), encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
