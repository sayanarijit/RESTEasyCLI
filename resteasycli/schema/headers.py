from marshmallow import fields, Schema, validates, ValidationError

from resteasycli.schema.common import OrderedDictField
from resteasycli.schema.workspace import WorkspaceFileSchema


class HeadersSchema(Schema):
    '''Schema for a set of headers'''
    action = fields.Str(required=True)
    values = OrderedDictField(
        required=True,
        keys=fields.Str(),
        values=fields.Str())

    @validates('action')
    def validate_action(self, action):
        '''Validate action'''
        if action in ['only', 'update']:
            return
        raise ValidationError(
            '{}: invalid action. use one of: only,update'.format(action))

    class Meta:
        ordered = True


class HeadersFileSchema(WorkspaceFileSchema):
    '''Schema for headers file format'''
    headers = fields.Dict(
        required=True,
        keys=fields.Str(),
        values=fields.Nested(HeadersSchema))

    class Meta:
        ordered = True
