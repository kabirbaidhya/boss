''' Tests for our main boss CLI module. '''

import envoy
from unittest import TestCase

from boss import __version__ as VERSION


class TestVersion(TestCase):

    def test_version_option_returns_package_version(self):
        output = envoy.run('boss --version').std_out
        self.assertEqual(output.strip(), VERSION)
