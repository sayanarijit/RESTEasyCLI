import unittest

from common import workspace


class HeadersTest(unittest.TestCase):

    headers1 = workspace.get_headers('demo_headers1')
    headers2 = workspace.get_headers('demo_headers2')

    def test_apply1(self):
        self.maxDiff = None
        def session(): return None
        session.headers = {'key': 'val'}
        self.headers1.apply(session)

        self.assertEqual(
            session.headers,
            {
                'key': 'val',
                'Custom-Header': 'demo1',
            },
        )

    def test_apply2(self):

        self.maxDiff = None
        def session(): return None
        session.headers = {'key': 'val'}

        self.headers2.apply(session)
        self.assertEqual(
            session.headers,
            {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Custom-Header': 'demo2',
            },
        )


if __name__ == '__main__':
    unittest.main()
