import os
import yaml
import logging
import unittest

from resteasycli.lib.endpoint import Endpoint
from resteasycli.lib.site import Site
from resteasycli.lib.abstract_reader import Reader
from resteasycli.lib.abstract_finder import Finder
from resteasycli.exceptions import MethodNotAllowedException


pwd = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('test_logger')

finder = Finder(logger=logger)
finder.SEARCH_PATHS.append(pwd)
found = finder.find(names=['sites'])
reader = Reader(logger=logger)
reader.load_reader_by_extension(found.extension)
data = reader.read(found.path)

site = Site(data['sites']['github_jobs'])

class EndpointTest(unittest.TestCase):
    ep = site.get_endpoint(data['sites']['github_jobs']['endpoints']['positions'])
    ep.api.debug = True
    ep.api.timeout = 10

    def test_get(self):
        info = self.ep.do('GET', kwargs={'description': 'python', 'full_time': 1})
        self.assertEqual(info['endpoint'], 'https://jobs.github.com/positions.json')
        self.assertEqual(info['kwargs'], {'description': 'python', 'full_time': 1})
        self.assertEqual(info['method'], 'GET')
        self.assertEqual(info['timeout'], 10)

        self.assertRaises(MethodNotAllowedException, lambda: self.ep.do('POST', kwargs={}))


if __name__ == '__main__':
    unittest.main()
