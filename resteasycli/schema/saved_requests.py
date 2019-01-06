from marshmallow import fields, validates, ValidationError, ValidationError

from resteasycli.schema.workspace import WorkspaceFileSchema
from resteasycli.schema.common import AnyField, AbstractRequestPropertiesSchema, OrderedDictField


class SavedRequestSchema(AbstractRequestPropertiesSchema):
    '''Schema for a saved request format'''
    method = fields.Str(required=True)
    site = fields.Str(required=True)
    endpoint = fields.Str(required=True)
    kwargs = fields.Dict()
    slug = AnyField()

    @validates('slug')
    def validate_slug(self, slug):
        '''Validates slug field'''
        if isinstance(slug, int) or isinstance(slug, str):
            return
        raise ValidationError('{}: Not a valid string or integer'.format(slug))

    class Meta:
        ordered = True


class SavedRequestsFileSchema(WorkspaceFileSchema):
    '''Schema for saved requests file format'''
    saved_requests = OrderedDictField(
        required=True,
        keys=fields.Str(),
        values=fields.Nested(SavedRequestSchema))

    class Meta:
        ordered = True
