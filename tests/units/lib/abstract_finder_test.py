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
        finder = Finder(logger=logger, search_paths=['.'], extensions=['yml'])
        if os.path.exists('sites.yml'):
            os.remove('sites.yml')

        self.assertRaises(FileNotFoundException, lambda: finder.find(names=['sites']))
        WorkspaceTemplates.initialize()
        
        found = finder.find(names=['sites'])
        
        self.assertEqual(found.name, 'sites')
        self.assertEqual(found.extension, 'yml')
        self.assertEqual(found.path, os.path.join('.', 'sites.yml'))

if __name__ == "__main__":
    unittest.main()
