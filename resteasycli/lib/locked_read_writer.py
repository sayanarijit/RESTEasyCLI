import os
import time

from resteasycli.lib.abstract_reader import Reader
from resteasycli.lib.abstract_writer import Writer


def l(filepath):
    '''Return lock filepath'''
    return '{}.lock'.format(filepath)

def lock(filepath):
    '''Lock the file'''
    with open(l(filepath), 'w') as f:
        f.write('')

def release(filepath):
    '''Release the file'''
    os.remove(l(filepath))

def locked(filepath):
    '''Check if file is locked'''
    return os.path.exists(l(filepath))


class LockedFile(object):
    '''A locked file object for safe reading and writing with suppport for file extensions'''

    def __init__(self, filepath, reader, writer):
        lock(filepath)
        self.filepath = filepath
        self._closed = False
        self._reader = reader
        self._writer = writer

    def read(self):
        '''Read from locked file'''
        if self._closed:
            self._throw_io_error()
        return self._reader.read(self.filepath)

    def write(self, data):
        '''Write info locked file'''
        if self._closed:
            self._throw_io_error()
        return self._writer.write(data=data, filepath=self.filepath)

    def close(self):
        '''Release lock and close file'''
        release(self.filepath)
        self._closed = True

    def _throw_io_error(self):
        raise IOError('{}: file is closed for any operation'.format(self.filepath))


class LockedReadWriter(object):
    '''Helper class for concurrent reading and writing with support for file extensions'''

    def __init__(self, logger):
        self.logger = logger

    def open(self, filepath):
        '''Lock file and return open file object for concurrent read/write'''

        extension = filepath.split('.')[-1]
        reader = Reader(logger=self.logger, extensions=[extension])
        writer = Writer(logger=self.logger, extensions=[extension])
        reader.load_reader_by_extension(extension)
        writer.load_writer_by_extension(extension)

        is_locked = locked(filepath)
        while is_locked:
            self.logger.debug('{}: file locked. waiting...'.format(filepath))
            time.sleep(.5)
            is_locked = locked(filepath)
        return LockedFile(filepath=filepath, reader=reader, writer=writer)

