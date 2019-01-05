from collections import OrderedDict

class Headers(object):
    '''Headers for your session'''

    def __init__(self, headers_id, workspace):
        self.headers_id = headers_id
        data = workspace.headers[headers_id]
        self.action = data['action']
        self.values = dict(data['values'])

    def apply(self, session):
        '''Perform action on the session'''
        if self.action == 'only':
            session.headers = self.values
        elif self.action == 'update':
            session.headers.update(self.values)

    def dict(self):
        return OrderedDict([
            ('action', self.action),
            ('values', self.values)
        ])
