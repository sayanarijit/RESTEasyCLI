import os
import unittest

from resteasycli.config.template import ConfigTemplate


class ConfigTemplatesTest(unittest.TestCase):

    def test_initialize(self):
        self.maxDiff = None

        if os.path.exists('recli.cfg'):
            os.remove('recli.cfg')
            
        ConfigTemplate.initialize(force=True)

        self.assertTrue(os.path.isfile('recli.cfg'))


if __name__ == "__main__":
    unittest.main()
