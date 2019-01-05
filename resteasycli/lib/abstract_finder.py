import os
from resteasycli.config import Config
from resteasycli.exceptions import FileNotFoundException

class FileInfo(object):
    '''Keeps information about a file'''
    def __init__(self, name, extension, path):
        self.name = name
        self.extension = extension
        self.path = path

    def __repr__(self):
        return 'FileInfo({})'.format(self.path)

class Finder(object):
    '''Interface for finding files'''

    SEARCH_PATHS = Config.SEARCH_PATHS
    DEFAULT_FILE_EXTENSION = Config.DEFAULT_FILE_EXTENSION
    SUPPORTED_FILE_EXTENSIONS = Config.SUPPORTED_FILE_EXTENSIONS

    def __init__(self, logger):
        self.logger = logger

    def find(self, names):
        '''Find and return file info'''
        for sp in self.SEARCH_PATHS:
            for fn in names:
                for fe in [self.DEFAULT_FILE_EXTENSION] + self.SUPPORTED_FILE_EXTENSIONS:
                    fullpath = os.path.expanduser(os.path.join(sp, fn)+'.'+fe)
                    self.logger.debug('Searching for file: ' + fullpath)
                    if not os.path.exists(fullpath):
                        continue
                    self.logger.debug('found file: ' + fullpath)
                    return FileInfo(name=fn, extension=fe, path=fullpath)
        raise FileNotFoundException(
            '{}: file not found in any of: {}. Note: supported file extensions are: {}'.format(
                '|'.join(names), ', '.join(self.SEARCH_PATHS), ', '.join(self.SUPPORTED_FILE_EXTENSIONS)))
