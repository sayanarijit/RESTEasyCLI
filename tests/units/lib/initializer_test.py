import unittest

from resteasycli.config import Config
from resteasycli.lib.initializer import initialize, SITES_TEMPLATE_CONTENT


class InitializerTest(unittest.TestCase):
    
    def test_initialize(self):
        initialize(force=True)
        with open(Config.SITE_TEMPLATE_FILENAME) as f:
            self.assertEqual(f.read(), SITES_TEMPLATE_CONTENT)


if __name__ == "__main__":
    unittest.main()