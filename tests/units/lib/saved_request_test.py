import os
import yaml
import logging
import unittest

from resteasycli.objects import workspace


class SavedRequestTest(unittest.TestCase):
    get_python_jobs = workspace.get_saved_request('get_python_jobs')
    get_python_jobs.endpoint.api.debug = True
    get_python_jobs.endpoint.api.timeout = 10

    def test_get(self):
        info = self.get_python_jobs.do()
        self.assertEqual(info['endpoint'],
                         'https://jobs.github.com/positions.json')
        self.assertEqual(info['kwargs'], {
                         'description': 'python', 'full_time': 1})
        self.assertEqual(info['method'], 'GET')
        self.assertEqual(info['timeout'], 10)


if __name__ == '__main__':
    unittest.main()
