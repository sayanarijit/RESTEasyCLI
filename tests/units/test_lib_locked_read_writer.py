import logging
import unittest

from resteasycli.lib.locked_read_writer import LockedReadWriter, locked


logger = logging.getLogger('test_logger')
lrw = LockedReadWriter(logger=logger)


class LockedReadWriterTest(unittest.TestCase):

    filepath = 'sites.yml'

    def test_open(self):
        locked_file = lrw.open(self.filepath)
        self.assertTrue(locked(self.filepath))
        locked_file.close()

    def test_close(self):
        locked_file = lrw.open(self.filepath)
        locked_file.close()
        self.assertTrue(not locked(self.filepath))
        self.assertRaises(IOError, lambda: locked_file.read())
        self.assertRaises(IOError, lambda: locked_file.write('abc'))


if __name__ == '__main__':
    unittest.main()
