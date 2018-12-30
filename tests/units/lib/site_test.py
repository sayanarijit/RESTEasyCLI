import json
import unittest

from resteasycli.objects import workspace
from resteasycli.lib.endpoint import Endpoint


class SiteTest(unittest.TestCase):

    site = workspace.get_site('testing')

    def test_get_endpoint(self):
        self.assertIsInstance(self.site.get_endpoint('todos'), Endpoint)


if __name__ == "__main__":
    unittest.main()