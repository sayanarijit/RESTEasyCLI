import os
from collections import OrderedDict
from marshmallow import Schema, fields, ValidationError, validates


class OrderedDictField(fields.Mapping):
    '''Custom ordered dict field'''

    mapping_type = OrderedDict


class AnyField(fields.Field):
    '''Custom field to accept any value'''

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value


class AbstractRequestPropertiesSchema(Schema):
    '''Abstract schema for sites, endpoints, and requests'''
    headers = fields.Str()
    auth = fields.Str()
    verify = AnyField()
    timeout = fields.Float()

    @validates('verify')
    def validate_verify(self, verify):
        '''Validates verify field'''
        if verify is False or verify is None:
            return
        if isinstance(verify, str) and os.path.exists(verify):
            return
        raise ValidationError(
            '{}: accepted value is False of a valid file path'.format(verify))
    
    @validates('timeout')
    def validate_timeout(self, timeout):
        '''Validates timeout field'''
        if timeout < 0:
            raise ValidationError('timeout cannot be negative')
    
    class Meta:
        ordered = True
