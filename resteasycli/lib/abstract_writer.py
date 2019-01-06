import json
from codecs import open

from resteasycli.lib.utils import yaml, Dumper
from resteasycli.exceptions import FileExtensionNotSupportedException


def _write_json(data, filepath):
    '''Write json files'''
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def _write_yaml(data, filepath):
    '''Write yaml files'''
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, Dumper=Dumper)


class Writer(object):
    '''Interface for writing to all supported file formats'''

    def __init__(self, logger, extensions):
        self.logger = logger
        self.extensions = extensions

    def load_writer_by_extension(self, ext):
        '''Initialize write() interface based on file extension'''

        ext = ext.lower()

        if ext not in self.extensions:
            raise FileExtensionNotSupportedException(
                '{}: extension not supported. Supported extensions are: {}'.format(
                    ext, ', '.join(self.extensions)
                ))

        if ext == 'json':
            self.write = _write_json
        else:
            self.write = _write_yaml
