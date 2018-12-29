import os
import logging
import unittest

from resteasycli.exceptions import FileNotFoundException
from resteasycli.lib.abstract_finder import Finder

pwd = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('test_logger')

class FinderTest(unittest.TestCase):
    def test_find_file(self):
        finder = Finder(logger=logger)
        finder.SEARCH_PATHS .append(pwd)
        found = finder.find(names=['sites'])
        self.assertEqual(found.name, 'sites')
        self.assertEqual(found.extension, 'yml')
        self.assertEqual(found.path, os.path.join('.', 'sites.yml'))

if __name__ == "__main__":
    unittest.main()