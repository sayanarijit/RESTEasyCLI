class SiteEndpoint(object):
    '''Combination of site ID and endpoint ID and an optional slug'''

    def __init__(self, txt):
        if len(txt.split('/')) == 2:
            self.site_id, self.endpoint_id = txt.split('/')
            self.slug = None
        elif len(txt.split('/')) > 2:
            self.site_id, self.endpoint_id, self.slug = txt.split('/', 2)
        else:
            raise InvalidCommandException(
                ('{}: correct format is: $site_id/$endpoint_id'
                    ' or $site_id/$endpoint_id/$slug').format(txt))

    def __repr__(self):
        '''Overriding object representation'''
        if self.slug is None:
            return '{}/{}'.format(self.site_id, self.endpoint_id)
        return '{}/{}/{}'.format(self.site_id, self.endpoint_id, self.slug)

    def __str__(self):
        '''Overriding string representation'''
        return str(self.__repr__())

    def __eq__(self, obj):
        '''Overriding "==" operator'''
        return obj.site_id == self.site_id and obj.endpoint_id == self.endpoint_id

    def __ne__(self, obj):
        '''Overriding "!=" operator'''
        return not self.__eq__(obj)
