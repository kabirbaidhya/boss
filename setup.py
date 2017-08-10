"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from boss import __version__


try:
    this_dir = abspath(dirname(__file__))
    with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
        long_description = file.read()
except IOError:
    # Handle file not found Exception.
    long_description = 'boss-cli - Yet another pythonic deployment tool built on top of fabric.'


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=boss', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='boss-cli',
    version=__version__,
    description='A lightweight deployment tool based upon fabric',
    long_description=long_description,
    url='https://github.com/kabirbaidhya/boss-cli',
    author='Kabir Baidhya',
    author_email='kabirbaidhya@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['fabric', 'pyyaml', 'requests'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'boss=boss.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
