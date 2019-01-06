import os
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

    def __init__(self, logger, search_paths, extensions):
        self.logger = logger
        self.search_paths = search_paths
        self.extensions = extensions

    def find(self, names):
        '''Find and return file info'''
        for sp in self.search_paths:
            for fn in names:
                for fe in self.extensions:
                    fullpath = os.path.expanduser(os.path.join(sp, fn)+'.'+fe)
                    self.logger.debug('Searching for file: ' + fullpath)
                    if not os.path.exists(fullpath):
                        continue
                    self.logger.debug('found file: ' + fullpath)
                    return FileInfo(name=fn, extension=fe, path=fullpath)
        raise FileNotFoundException(
            '{}: file not found in any of: {}. Note: supported file extensions are: {}'.format(
                '|'.join(names), ', '.join(self.search_paths), ', '.join(self.extensions)))
