import unittest

from common import workspace
from resteasycli.lib.endpoint import Endpoint


class SiteTest(unittest.TestCase):

    site = workspace.get_site('testing')

    def test_get_endpoint(self):
        self.assertIsInstance(self.site.get_endpoint('t'), Endpoint)


if __name__ == "__main__":
    unittest.main()
