import logging
import unittest

from resteasycli.exceptions import FileExtensionNotSupportedException
from resteasycli.lib.abstract_reader import Reader, _read_json, _read_yaml

logger = logging.getLogger('test_logger')

class AbstractReaderTest(unittest.TestCase):

    def test_load_reader_by_extension(self):
        reader = Reader(logger=logger, extensions=['json', 'yml', 'yaml'])

        reader.load_reader_by_extension('json')
        self.assertEqual(reader.read, _read_json)

        reader.load_reader_by_extension('YAML')
        self.assertEqual(reader.read, _read_yaml)

        self.assertRaises(FileExtensionNotSupportedException, lambda: reader.load_reader_by_extension('txt'))


if __name__ == '__main__':
    unittest.main()
