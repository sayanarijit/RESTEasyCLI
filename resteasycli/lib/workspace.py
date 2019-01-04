import os
import yaml
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
from resteasycli.schema.auth import AuthFileSchema
from resteasycli.schema.sites import SitesFileSchema
from resteasycli.schema.headers import HeadersFileSchema
from resteasycli.schema.saved_requests import SavedRequestsFileSchema
from resteasycli.exceptions import EntryNotFoundException, InvalidFormatException, CorruptFileException


SITES_TEMPLATE_CONTENT = '''\
version: v0.1
sites:
  ghjobs:
    base_url: https://jobs.github.com
    endpoints:
      p:
        route: positions.json
        timeout: 10
        methods: [ GET ]

  testing:
    base_url: https://jsonplaceholder.typicode.com
    endpoints:
      t:
        route: todos
      t1:
        route: todos/1
'''

AUTH_TEMPLATE_CONTENT = '''\
version: v0.1
auth:
  demo_basic_auth:
    type: basic
    credentials:
      username: user1
      password: password1

  demo_token_auth:
    type: token
    credentials:
      header: Authorization
      value: Bearer uu6OgZqaChWj8vlTSiSBTirjeGpQqa83MycWiWHdPL2ppcrKTpDgrlegT87dhkhr
'''

HEADERS_TEMPLATE_CONTENT = '''\
version: v0.1
headers:
  demo_headers1:
    action: update
    values:
      Content-Type: application/json
      Accept: application/json
      Custom-Header: demo1

  demo_headers2:
    action: only
    values:
      Content-Type: application/json
      Accept: application/json
      Custom-Header: demo2
'''

SAVED_REQUESTS_TEMPLATE_CONTENT = '''\
version: v0.1
saved_requests:
  get_python_jobs:
    method: GET
    site: ghjobs
    endpoint: p
    headers: demo_headers1
    kwargs:
      description: python
      full_time: 1

  remind_shopping:
    method: POST
    site: testing
    endpoint: t
    auth: demo_basic_auth
    kwargs:
      title: Go to shopping
'''

class WorkspaceTemplates(object):
    '''Default templates and initializer for workspace'''

    TEMPLATE = {
      'sites': {'filename': '{}.{}'.format(Config.SITES_TEMPLATE_FILENAME, Config.DEFAULT_FILE_EXTENSION),
                'content': SITES_TEMPLATE_CONTENT},
      'auth': {'filename': '{}.{}'.format(Config.AUTH_TEMPLATE_FILENAME, Config.DEFAULT_FILE_EXTENSION),
               'content': AUTH_TEMPLATE_CONTENT},
      'headers': {'filename': '{}.{}'.format(Config.HEADERS_TEMPLATE_FILENAME, Config.DEFAULT_FILE_EXTENSION),
                  'content': HEADERS_TEMPLATE_CONTENT},
      'saved_requests': {'filename': '{}.{}'.format(Config.SAVED_REQUESTS_TEMPLATE_FILENAME, Config.DEFAULT_FILE_EXTENSION),
                         'content': SAVED_REQUESTS_TEMPLATE_CONTENT}
    }

    @staticmethod
    def initialize(force=False):
        for t in WorkspaceTemplates.TEMPLATE.values():
            if os.path.exists(t['filename']) and not force:
                continue
            with open(t['filename'], 'w') as f:
                f.write(t['content'])

class Workspace(object):
    '''Workspace manager'''
    def __init__(self, logger):
        self.finder = Finder(logger=logger)
        self.reader = Reader(logger=logger)
        self.writer = Writer(logger=logger)
        self.logger = logger
        self.file_schemas = {
            'saved_requests': SavedRequestsFileSchema(),
            'sites': SitesFileSchema(),
            'auth': AuthFileSchema(),
            'headers': HeadersFileSchema()
        }
        self.load_files()

    @staticmethod
    def init(force=False):
        WorkspaceTemplates.initialize(force=force)

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
            raise InvalidFormatException('{}: {}'.format(fileinfo.path,
                yaml.dump(e.messages, default_flow_style=False)))
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
