class Auth(object):
    '''Authentication for your session'''

    def __init__(self, auth_id, workspace):
        self.auth_id = auth_id
        data = workspace.auth[auth_id]
        self.type = data['type']
        self.credentials = data['credentials']

    def apply(self, session):
        '''Perform action on the session'''
        if self.type == 'basic':
            session.auth = (
                self.credentials['username'], self.credentials['password'])
        elif self.type == 'token':
            session.headers.update(self.credentials)
