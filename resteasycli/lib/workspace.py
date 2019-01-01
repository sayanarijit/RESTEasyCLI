import os
import json

from resteasycli.config import Config
from resteasycli.lib.site import Site
from resteasycli.lib.auth import Auth
from resteasycli.lib.headers import Headers
from resteasycli.lib.endpoint import Endpoint
from resteasycli.lib.abstract_reader import Reader
from resteasycli.lib.abstract_writer import Writer
from resteasycli.lib.abstract_finder import Finder
from resteasycli.lib.saved_request import SavedRequest
from resteasycli.exceptions import EntryNotFoundException


SITES_TEMPLATE_CONTENT = '''\
version: 0.1
sites:
  github_jobs:
    base_url: https://jobs.github.com
    endpoints:
      positions:
        route: positions.json
        timeout: 10
        methods:
          - GET

  testing:
    base_url: https://jsonplaceholder.typicode.com
    endpoints:
      todos:
        route: todos
      todo1:
        route: todos/1
'''

AUTH_TEMPLATE_CONTENT = '''\
version: 0.1
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
version: 0.1
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
version: 0.1
saved_requests:
  get_python_jobs:
    method: GET
    site: github_jobs
    endpoint: positions
    headers: demo_headers1
    kwargs:
      description: python
      full_time: 1

  remind_shopping:
    method: POST
    site: testing
    endpoint: todos
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
        self.reader.load_reader_by_extension(self.sites_file.extension)
        self.sites = self.reader.read(self.sites_file.path)['sites']

        if self.sites_file.extension != self.auth_file.extension:
            self.reader.load_reader_by_extension(self.auth_file.extension)
        self.auth = self.reader.read(self.auth_file.path)['auth']

        if self.auth_file.extension != self.headers_file.extension:
            self.reader.load_reader_by_extension(self.headers_file.extension)
        self.headers = self.reader.read(self.headers_file.path)['headers']

        if self.headers_file.extension != self.saved_requests_file.extension:
            self.reader.load_reader_by_extension(
                self.saved_requests_file.extension)
        self.saved_requests = self.reader.read(
            self.saved_requests_file.path)['saved_requests']

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
