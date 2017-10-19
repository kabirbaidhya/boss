"""Tests for our main boss CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from boss import NAME, __version__ as VERSION


class TestVersion(TestCase):

    def test_returns_version_information(self):
        output = popen(['boss', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), '{} {}'.format(NAME, VERSION))
