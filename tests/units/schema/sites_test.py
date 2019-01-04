import unittest

from resteasycli.schema.sites import SiteSchema, SitesFileSchema
from marshmallow import ValidationError

valid_file_datas = [{'version': 'v1.0', 'sites': {}}]
invalid_file_datas = [
    {'version': 'v1.0', 'sites': []},
    {'version': 'v1.0', 'sites': 'abc'},
    {'version': 'v1.0', 'sites': 123},
    {'version': 'v1.0', 'sites': None},
    {'version': 'v1.0'}
]

valid_datas = [
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}},
        'headers': 'demo_headers1',
        'auth': 'demo_token_auth',
        'timeout': 10,
        'verify': 'tests/units/schema/fake_certfile',
        'methods': ['GET', 'POST']
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {
            'p': {
                'route': 'positions.json',
                'headers': 'demo_headers1',
                'auth': 'demo_token_auth',
                'timeout': 10,
                'verify': False,
                'methods': ['GET', 'POST']
            }
        },
        'headers': 'demo_headers1',
        'auth': 'demo_token_auth',
        'timeout': 10,
        'verify': 'tests/units/schema/fake_certfile',
        'methods': ['GET', 'POST']
    }
]

invalid_datas = [
    None,
    'abc',
    [valid_datas[0]],
    {
        'endpoints': {'p': {'route': 'positions.json'}}
    },
    {
        'base_url': 'https://jobs.github.com'
    },
    {
        'base_url': None,
        'endpoints': {'p': {'route': 'positions.json'}}
    },
    {
        'base_url': 'jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': None
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': None}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {}}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': [{'route': 'positions.json'}]}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}},
        'methods': {}
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}},
        'methods': ['SOME_WEIRD_METHOD']
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}},
        'verify': True
    },
    {
        'base_url': 'https://jobs.github.com',
        'endpoints': {'p': {'route': 'positions.json'}},
        'verify': '/some/invalid/path'
    }
]


class SitesFileSchemaTest(unittest.TestCase):

    schema = SitesFileSchema()

    def test_validation(self):
        for x in valid_file_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_file_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))


class SiteSchemaTest(unittest.TestCase):
    
    schema = SiteSchema()

    def test_validation(self):
        for x in valid_datas:
            self.assertIsInstance(self.schema.load(x), dict)
        for x in invalid_datas:
            self.assertRaises(ValidationError, lambda: self.schema.load(x))


if __name__ == "__main__":
    unittest.main()
