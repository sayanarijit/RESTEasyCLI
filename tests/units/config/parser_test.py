import os
import unittest

from resteasycli.config.parser import Parser
from resteasycli.config.template import ConfigTemplate


ConfigTemplate.initialize(force=True)

class ConfigParserTest(unittest.TestCase):

    parser = Parser()

    def test_parse(self):
        parsed = self.parser.parse(search_paths=['.'])
        self.assertEqual(parsed, {})


if __name__ == "__main__":
    unittest.main()
