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
        WorkspaceTemplates.initialize(force=True, extension='yml')

        for t in WorkspaceTemplates.TEMPLATE.values():
            self.assertEqual(workspace.reader.read('{}.yml'.format(t['filename'])), t['content'])

class WorkspaceTest(unittest.TestCase):

    ws = workspace

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
