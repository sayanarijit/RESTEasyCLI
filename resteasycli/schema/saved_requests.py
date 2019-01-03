from marshmallow import Schema, fields, ValidationError, validates

from resteasycli.schema.workspace import WorkspaceFileSchema


class SavedRequestSchema(Schema):
    '''Schema for a saved request format'''
    method = fields.Str(required=True)
    site = fields.Str(required=True)
    endpoint = fields.Str(required=True)
    headers = fields.Str()
    auth = fields.Str()
    kwargs = fields.Dict(keys=fields.Str())


class SavedRequestsFileSchema(WorkspaceFileSchema):
    '''Schema for saved requests file format'''
    saved_requests = fields.Dict(
        keys=fields.Str,
        values=fields.Nested(SavedRequestSchema),
        required=True)
