import unittest
from marshmallow import ValidationError

from resteasycli.schema.saved_requests import SavedRequestSchema, SavedRequestsFileSchema


valid_file_datas = [{'version': 'v1.0', 'saved_requests': {}}]
invalid_file_datas = [
    {'version': 'v1.0', 'saved_requests': []},
    {'version': 'v1.0', 'saved_requests': 'abc'},
    {'version': 'v1.0', 'saved_requests': 123},
    {'version': 'v1.0', 'saved_requests': None},
    {'version': 'v1.0'}
]

valid_datas = [
    {
        'method': 'GET',
        'site': 'github_jobs',
        'endpoint': 'positions',
    },
    {
        'method': 'GET',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'verify': False,
    },
    {
        'method': 'GET',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'headers': 'demo_headers1',
        'auth': 'demo_token_auth',
        'verify': 'tests/units/schema/fake_certfile',
        'kwargs': {'description': 'python', 'full_time': 1}
    },
    {
        'method': 'POST',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'kwargs': {}
    }
]

invalid_datas = [
    None,
    'abc',
    [valid_datas[0]],
    {'site': 'github_jobs', 'endpoint': 'positions'},
    {'method': 'POST', 'site': 'github_jobs'},
    {'method': 'POST', 'endpoint': 'positions'},
    {
        'method': 'GET',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'kwargs': []
    },
    {
        'method': 'POST',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'kwargs': None
    },
    {
        'method': 'GET',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'headers': {'abc': 'xyz'}
    },
    {
        'method': 'GET',
        'site': 'github_jobs',
        'endpoint': 'positions',
        'auth': {'abc': 'xyz'}
    }
]


class SavedRequestsFileSchemaTest(unittest.TestCase):

    schema = SavedRequestsFileSchema()

    def test_validation(self):
        for x in valid_file_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_file_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))

class SavedRequestSchemaTest(unittest.TestCase):
    
    schema = SavedRequestSchema()

    def test_validation(self):
        for x in valid_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))


if __name__ == "__main__":
    unittest.main()
