from marshmallow import fields

from resteasycli.schema.workspace import WorkspaceFileSchema
from resteasycli.schema.common import AbstractRequestPropertiesSchema


class SavedRequestSchema(AbstractRequestPropertiesSchema):
    '''Schema for a saved request format'''
    method = fields.Str(required=True)
    site = fields.Str(required=True)
    endpoint = fields.Str(required=True)
    kwargs = fields.Dict()


class SavedRequestsFileSchema(WorkspaceFileSchema):
    '''Schema for saved requests file format'''
    saved_requests = fields.Dict(
        required=True,
        keys=fields.Str(),
        values=fields.Nested(SavedRequestSchema))
