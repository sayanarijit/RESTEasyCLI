import json
import unittest

from resteasycli.objects import workspace
from resteasycli.lib.workspace import WorkspaceTemplates
from resteasycli.lib.site import Site
from resteasycli.lib.auth import Auth
from resteasycli.lib.headers import Headers
from resteasycli.lib.saved_request import SavedRequest

workspace.init(force=True)
workspace.reload()

class WorkspaceTemplatesTest(unittest.TestCase):

    def test_initialize(self):
        WorkspaceTemplates.initialize(force=True)

        for t in WorkspaceTemplates.TEMPLATE.values():
            with open(t['filename']) as f:
                self.assertEqual(f.read(), t['content'])

class WorkspaceTest(unittest.TestCase):

    ws = workspace

    def test_list_sites(self):
        self.assertEqual(self.ws.list_sites(),
                {'github_jobs': 'https://jobs.github.com',
                 'testing': 'https://jsonplaceholder.typicode.com'})

    def test_list_endpoints(self):
        self.assertEqual(self.ws.list_endpoints(),
                {'github_jobs/positions': 'https://jobs.github.com/positions.json',
                 'testing/todos': 'https://jsonplaceholder.typicode.com/todos',
                 'testing/todo1': 'https://jsonplaceholder.typicode.com/todos/1'})

    def test_list_saved_requests(self):
        self.maxDiff = None
        self.assertEqual(self.ws.list_saved_requests(),
                {
                    'get_python_jobs': {
                        'method': 'GET',
                        'site_endpoint': 'github_jobs/positions',
                        'endpoint_url': 'https://jobs.github.com/positions.json',
                        'headers': 'demo_headers1',
                        'headers_values': {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'Custom-Header': 'demo1'
                        },
                        'headers_action': 'update',
                        'auth': None,
                        'kwargs': {'description': 'python', 'full_time': 1}
                    },
                    'remind_shopping': {
                        'method': 'POST',
                        'site_endpoint': 'testing/todos',
                        'endpoint_url': 'https://jsonplaceholder.typicode.com/todos',
                        'headers': None,
                        'headers_action': None,
                        'headers_values': {},
                        'auth': 'demo_basic_auth',
                        'kwargs': {'title': 'Go to shopping'}
                    }
                })

    def test_get_site(self):
        self.assertIsInstance(self.ws.get_site('testing'), Site)

    def test_get_auth(self):
        self.assertIsInstance(self.ws.get_auth('demo_basic_auth'), Auth)

    def test_get_headers(self):
        self.assertIsInstance(self.ws.get_headers('demo_headers1'), Headers)

    def test_get_saved_request(self):
        self.assertIsInstance(self.ws.get_saved_request(
            'remind_shopping'), SavedRequest)


if __name__ == "__main__":
    unittest.main()
