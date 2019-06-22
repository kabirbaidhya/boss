"""Packaging settings."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from boss import __version__

path = abspath(dirname(__file__))

with open(join(path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


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
    description='Yet another pythonic deployment tool built on top of fabric.',
    long_description_content_type='text/markdown',
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
    install_requires=[
        'fabric==1.14.0',
        'paramiko==2.4.2',
        'pyyaml>=4.2b1',
        'requests==2.20.0',
        'inquirer==2.2.0',
        'python-dotenv==0.6.5',
        'terminaltables==3.1.0',
        'click==6.7',
        'hvac==0.6.4',
        'cryptography==2.4.2'
    ],
    extras_require={
        'test': ['mock', 'coverage', 'pytest', 'pytest-cov', 'pylint', 'pytest-watch'],
    },
    entry_points={
        'console_scripts': [
            'boss=boss.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
    include_package_data=True
)
