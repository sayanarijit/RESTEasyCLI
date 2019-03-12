import logging
import unittest

from resteasycli.exceptions import FileExtensionNotSupportedException
from resteasycli.lib.abstract_writer import Writer, _write_json, _write_yaml

logger = logging.getLogger('test_logger')


class AbstractWriterTest(unittest.TestCase):

    def test_load_writer_by_extension(self):
        writer = Writer(logger=logger, extensions=['json', 'yml', 'yaml'])

        writer.load_writer_by_extension('json')
        self.assertEqual(writer.write, _write_json)

        writer.load_writer_by_extension('YAML')
        self.assertEqual(writer.write, _write_yaml)

        self.assertRaises(
            FileExtensionNotSupportedException,
            lambda: writer.load_writer_by_extension('txt'),
        )


if __name__ == '__main__':
    unittest.main()
