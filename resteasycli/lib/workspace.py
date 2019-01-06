import os
import logging
from collections import OrderedDict
from marshmallow.exceptions import ValidationError

from resteasycli.config import Config
from resteasycli.lib.site import Site
from resteasycli.lib.auth import Auth
from resteasycli.lib.headers import Headers
from resteasycli.lib.endpoint import Endpoint
from resteasycli.lib.abstract_reader import Reader
from resteasycli.lib.abstract_writer import Writer
from resteasycli.lib.abstract_finder import Finder
from resteasycli.lib.saved_request import SavedRequest
from resteasycli.lib.utils import yaml, Dumper
from resteasycli.schema.auth import AuthFileSchema
from resteasycli.schema.sites import SitesFileSchema
from resteasycli.schema.headers import HeadersFileSchema
from resteasycli.schema.saved_requests import SavedRequestsFileSchema
from resteasycli.exceptions import EntryNotFoundException, InvalidFormatException, CorruptFileException


SITES_TEMPLATE_CONTENT = OrderedDict([
    ('version', Config.DEFAULT_FILE_FORMAT),
    ('sites', OrderedDict([
        ('ghjobs', OrderedDict([
            ('base_url', 'https://jobs.github.com'),
            ('endpoints', OrderedDict([
                ('p', OrderedDict([
                    ('route', 'positions.json'),
                    ('timeout', 10),
                    ('methods', ['GET'])
                ]))
            ]))
        ])),
        ('testing', OrderedDict([
            ('base_url', 'https://jsonplaceholder.typicode.com'),
            ('endpoints', OrderedDict([
                ('t', OrderedDict([
                    ('route', 'todos')
                ])),
                ('t1', OrderedDict([
                    ('route', 'todos/1')
                ]))
            ]))
        ]))
    ]))
])

AUTH_TEMPLATE_CONTENT = OrderedDict([
    ('version', Config.DEFAULT_FILE_FORMAT),
    ('auth', OrderedDict([
        ('demo_basic_auth', OrderedDict([
            ('type', 'basic'),
            ('credentials', OrderedDict([
                ('username', 'user1'),
                ('password', 'password1')
            ]))
        ])),
        ('demo_token_auth', OrderedDict([
            ('type', 'token'),
            ('credentials', OrderedDict([
                ('header', 'Authorization'),
                ('value', 'Bearer uu6OgZqaChWj8vlTSiSBTirjeGpQqa83MycWiWHdPL2ppcrKTpDgrlegT87dhkhr')
            ]))
        ]))
    ]))
])

HEADERS_TEMPLATE_CONTENT = OrderedDict([
    ('version', Config.DEFAULT_FILE_FORMAT),
    ('headers', OrderedDict([
        ('demo_headers1', OrderedDict([
            ('action', 'update'),
            ('values', OrderedDict([
                ('Custom-Header', 'demo1')
            ]))
        ])),
        ('demo_headers2', OrderedDict([
            ('action', 'only'),
            ('values', OrderedDict([
                ('Content-Type', 'application/json'),
                ('Accept', 'application/json'),
                ('Custom-Header', 'demo2')
            ]))
        ]))
    ]))
])

SAVED_REQUESTS_TEMPLATE_CONTENT = OrderedDict([
    ('version', Config.DEFAULT_FILE_FORMAT),
    ('saved_requests', OrderedDict([
        ('get_python_jobs', OrderedDict([
            ('method', 'GET'),
            ('site', 'ghjobs'),
            ('endpoint', 'p'),
            ('headers', 'demo_headers1'),
            ('kwargs', OrderedDict([
                ('description', 'python'),
                ('full_time', 1)
            ]))
        ])),
        ('remind_shopping', OrderedDict([
            ('method', 'POST'),
            ('site', 'testing'),
            ('endpoint', 't'),
            ('auth', 'demo_basic_auth'),
            ('kwargs', OrderedDict([
                ('title', 'Go to shopping')
            ]))
        ]))
    ]))
])

class WorkspaceTemplates(object):
    '''Default templates and initializer for workspace'''

    TEMPLATE = {
      'sites': {'filename': Config.SITES_TEMPLATE_FILENAME,
                'content': SITES_TEMPLATE_CONTENT},
      'auth': {'filename': Config.AUTH_TEMPLATE_FILENAME,
               'content': AUTH_TEMPLATE_CONTENT},
      'headers': {'filename': Config.HEADERS_TEMPLATE_FILENAME,
                  'content': HEADERS_TEMPLATE_CONTENT},
      'saved_requests': {'filename': Config.SAVED_REQUESTS_TEMPLATE_FILENAME,
                         'content': SAVED_REQUESTS_TEMPLATE_CONTENT}
    }

    @staticmethod
    def initialize(force=False, writer=None, extension=Config.DEFAULT_FILE_EXTENSION):
        if Config.DEFAULT_FILE_FORMAT not in ['v0.1', 'v1.0']:
            raise InvalidFormatException(
                '{}: file format not supported'.format(Config.DEFAULT_FILE_FORMAT))
        if writer is None:
            writer = Writer(
                logger=logging.getLogger('resteasycli'),
                extensions=[extension])
        writer.load_writer_by_extension(extension)
        for t in WorkspaceTemplates.TEMPLATE.values():
            filepath = '{}.{}'.format(t['filename'], extension)
            if os.path.exists(filepath) and not force:
                continue
            writer.write(data=t['content'], filepath=filepath)

class Workspace(object):
    '''Workspace manager'''
    def __init__(self, logger):
        self.logger = logger
        self.finder = Finder(
                logger=logger,
                extensions=Config.SUPPORTED_FILE_EXTENSIONS,
                search_paths=Config.SEARCH_PATHS)
        self.reader = Reader(
                logger=logger,
                extensions=Config.SUPPORTED_FILE_EXTENSIONS)
        self.writer = Writer(
                logger=logger,
                extensions=Config.SUPPORTED_FILE_EXTENSIONS)
        self.file_schemas = {
            'saved_requests': SavedRequestsFileSchema(),
            'sites': SitesFileSchema(),
            'auth': AuthFileSchema(),
            'headers': HeadersFileSchema()
        }
        self.load_files()

    def init(self, force=False):
        WorkspaceTemplates.initialize(
            writer=self.writer, force=force, extension=Config.DEFAULT_FILE_EXTENSION)

    def reload(self):
        '''Reload workspace changes'''
        self.load_files()

    def load_files(self):
        '''Load files from current workspace'''
        self.logger.debug('finding available files in workplace')
        self.sites_file = self.finder.find(names=[Config.SITES_TEMPLATE_FILENAME])
        self.auth_file = self.finder.find(names=[Config.AUTH_TEMPLATE_FILENAME])
        self.headers_file = self.finder.find(names=[Config.HEADERS_TEMPLATE_FILENAME])
        self.saved_requests_file = self.finder.find(names=[Config.SAVED_REQUESTS_TEMPLATE_FILENAME])

        self.logger.debug('reading found files')
        self.load_auth()
        self.load_headers()
        self.load_sites()
        self.load_saved_requests()

    def load_using_schema(self, schema, fileinfo):
        '''Helps loading validated data from file'''
        self.reader.load_reader_by_extension(fileinfo.extension)
        try:
            raw_data = self.reader.read(fileinfo.path)
        except Exception as e:
            raise CorruptFileException('{}: {}'.format(fileinfo.path, e))

        try:
            data = schema.load(raw_data)
        except ValidationError as e:
            raise InvalidFormatException(
                '{}: while reading this file below errors were found:\n{}'.format(
                    fileinfo.path, yaml.dump(e.messages, default_flow_style=False, Dumper=Dumper)))
        return data

    def load_auth(self):
        '''Loads authentication methods from files'''
        data = self.load_using_schema(fileinfo=self.auth_file,
                                      schema=self.file_schemas['auth'])
        self.auth = data['auth']

    def load_headers(self):
        '''Loads headers from files'''
        data = self.load_using_schema(fileinfo=self.headers_file,
                                      schema=self.file_schemas['headers'])
        self.headers = data['headers']

    def load_sites(self):
        '''Loads sites with endpoints from files'''
        data = self.load_using_schema(fileinfo=self.sites_file,
                                      schema=self.file_schemas['sites'])
        self.sites = data['sites']

    def load_saved_requests(self):
        '''Loads saved requests from files'''
        data = self.load_using_schema(fileinfo=self.saved_requests_file,
                schema=self.file_schemas['saved_requests'])
        self.saved_requests = data['saved_requests']

    def get_site(self, site_id):
        '''Returns initialized site obect'''
        if site_id not in self.sites:
            raise EntryNotFoundException('{}: site not found'.format(site_id))
        return Site(site_id=site_id, workspace=self)

    def get_auth(self, auth_id):
        '''Returns initialized auth obect'''
        if auth_id not in self.auth:
            raise EntryNotFoundException('{}: auth not found'.format(auth_id))
        return Auth(auth_id=auth_id, workspace=self)

    def get_headers(self, headers_id):
        '''Returns initialized headers obect'''
        if headers_id not in self.headers:
            raise EntryNotFoundException(
                '{}: headers not found'.format(headers_id))
        return Headers(headers_id=headers_id, workspace=self)

    def get_saved_request(self, request_id):
        '''Returns initialized request obect'''
        if request_id not in self.saved_requests:
            raise EntryNotFoundException(
                '{}: request not found'.format(request_id))
        return SavedRequest(request_id=request_id, workspace=self)
