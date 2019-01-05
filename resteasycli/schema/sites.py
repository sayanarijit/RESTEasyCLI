from marshmallow import Schema, fields, validates, ValidationError

from resteasycli.config import Config
from resteasycli.schema.workspace import WorkspaceFileSchema
from resteasycli.schema.common import AbstractRequestPropertiesSchema, OrderedDictField


class AbstractSiteEndpointSchema(AbstractRequestPropertiesSchema):
    '''Schema common for both site and endpoint'''
    methods = fields.List(fields.Str())

    @validates('methods')
    def validate_methods(self, methods):
        invalid = set(methods) - set(Config.ALL_METHODS)
        if len(invalid) > 0:
            raise ValidationError(
                '{}: incorrect method(s). correct methods are: {}'.format(
                    ','.join(methods), ','.join(Config.ALL_METHODS)
                ))

    class Meta:
        ordered = True


class EndpointSchema(AbstractSiteEndpointSchema):
    '''Schema for a site's endpoint'''
    route = fields.Str(required=True)

    class Meta:
        ordered = True


class SiteSchema(AbstractSiteEndpointSchema):
    '''Schema for a saved request format'''
    base_url = fields.Url(required=True)
    endpoints = OrderedDictField(
        required=True,
        keys=fields.Str(),
        values=fields.Nested(EndpointSchema))
    
    @validates('endpoints')
    def validate_endpoints(self, endpoints):
        if len(endpoints) == 0:
            raise ValidationError('endpoints: endpoints can not be empty')

    class Meta:
        ordered = True


class SitesFileSchema(WorkspaceFileSchema):
    '''Schema for saved requests file format'''
    sites = OrderedDictField(
        required=True,
        keys=fields.Str(),
        values=fields.Nested(SiteSchema))

    class Meta:
        ordered = True
