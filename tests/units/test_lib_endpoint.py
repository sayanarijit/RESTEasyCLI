import unittest

from .common import workspace
from resteasycli.exceptions import MethodNotAllowedException


class EndpointTest(unittest.TestCase):
    ep = workspace.get_site('ghjobs').get_endpoint('p')
    ep.api.debug = True
    ep.api.timeout = 10

    def test_get(self):
        info = self.ep.do(
            'GET', kwargs={'description': 'python', 'full_time': 1},
        )
        self.assertEqual(
            info['endpoint'],
            'https://jobs.github.com/positions.json',
        )
        self.assertEqual(
            info['kwargs'], {
                'description': 'python', 'full_time': 1,
            },
        )
        self.assertEqual(info['method'], 'GET')
        self.assertEqual(info['timeout'], 10)

        self.ep.api.debug = False
        self.assertRaises(
            MethodNotAllowedException,
            lambda: self.ep.do('POST', kwargs={}),
        )


if __name__ == '__main__':
    unittest.main()
