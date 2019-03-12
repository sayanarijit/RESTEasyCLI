import os
import logging
import unittest

from resteasycli.lib.abstract_finder import Finder
from resteasycli.lib.workspace import WorkspaceTemplates
from resteasycli.exceptions import FileNotFoundException

pwd = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('test_logger')


class FinderTest(unittest.TestCase):
    def test_find_file(self):
        finder = Finder(logger=logger, search_paths=['.'], extensions=['yaml'])
        if os.path.exists('sites.yaml'):
            os.remove('sites.yaml')

        self.assertRaises(
            FileNotFoundException,
            lambda: finder.find(names=['sites']),
        )
        WorkspaceTemplates.initialize()

        found = finder.find(names=['sites'])

        self.assertEqual(found.name, 'sites')
        self.assertEqual(found.extension, 'yaml')
        self.assertEqual(found.path, os.path.join('.', 'sites.yaml'))


if __name__ == '__main__':
    unittest.main()
