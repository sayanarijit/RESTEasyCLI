from marshmallow import fields, Schema, ValidationError, post_load

from resteasycli.schema.workspace import WorkspaceFileSchema


class BasicAuthSchema(Schema):
    '''Schema for basic auth'''
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class TokenAuthSchema(Schema):
    '''Schema for token auth'''
    header = fields.Str(required=True)
    value = fields.Str(required=True)

class AuthSchema(Schema):
    '''Schema for a saved request format'''
    type = fields.Str(required=True)
    credentials = fields.Dict(required=True, keys=fields.Str())

    @post_load(pass_original=True)
    def validate_credentials(self, data, _):
        '''Validate credentials using approtriate schema'''
        if data['type'] == 'basic':
            data['credentials'] = BasicAuthSchema().load(data['credentials'])
        elif data['type'] == 'token':
            data['credentials'] = TokenAuthSchema().load(data['credentials'])
        else:
            raise ValidationError('{}: invalid authentication type'.format(data['type']))
        return data

class AuthFileSchema(WorkspaceFileSchema):
    '''Schema for auth file format'''
    auth = fields.Dict(
        required=True,
        keys=fields.Str(),
        values=fields.Nested(AuthSchema))
