import unittest

from common import workspace


class AuthTest(unittest.TestCase):

    basic_auth = workspace.get_auth('demo_basic_auth')
    token_auth = workspace.get_auth('demo_token_auth')

    def test_apply1(self):
        self.maxDiff = None

        def session(): return None
        session.auth = None
        self.basic_auth.apply(session)

        self.assertEqual(session.auth,
                (self.basic_auth.credentials['username'],
                 self.basic_auth.credentials['password']))

    def test_apply2(self):

        self.maxDiff = None

        def session(): return None
        session.headers = {'key': 'val'}

        self.token_auth.apply(session)

        result = {self.token_auth.credentials['header']: self.token_auth.credentials['value']}
        result.update({'key': 'val'})
        self.assertEqual(session.headers, result)


if __name__ == "__main__":
    unittest.main()
