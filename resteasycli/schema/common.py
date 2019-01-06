import os
import collections
from marshmallow.compat import iteritems
from marshmallow import Schema, fields, ValidationError, validates


class OrderedDictField(fields.Dict):
    '''An workaround for fields.Dict(ordered=True)'''
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if not self.value_container and not self.key_container:
            return value
        if not isinstance(value, collections.Mapping):
            self.fail('invalid')

        if self.key_container is None:
            keys = {k: k for k in value.keys()}
        else:
            keys = {
                k: self.key_container._serialize(k, None, None, **kwargs)
                for k in value.keys()
            }

        if self.value_container is None:
            result = collections.OrderedDict([(keys[k], v)
                                  for k, v in iteritems(value) if k in keys])
        else:
            result = collections.OrderedDict([
                (keys[k], self.value_container._serialize(v, None, None, **kwargs))
                for k, v in iteritems(value)
            ])

        return result

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, collections.Mapping):
            self.fail('invalid')
        if not self.value_container and not self.key_container:
            return value

        errors = collections.defaultdict(dict)

        if self.key_container is None:
            keys = {k: k for k in value.keys()}
        else:
            keys = {}
            for key in value.keys():
                try:
                    keys[key] = self.key_container.deserialize(key)
                except ValidationError as error:
                    errors[key]['key'] = error.messages

        if self.value_container is None:
            result = collections.OrderedDict([(keys[k], v) for k, v in iteritems(value) if k in keys])
        else:
            result = collections.OrderedDict()
            for key, val in iteritems(value):
                try:
                    deser_val = self.value_container.deserialize(val)
                except ValidationError as error:
                    errors[key]['value'] = error.messages
                    if error.valid_data is not None and key in keys:
                        result[keys[key]] = error.valid_data
                else:
                    if key in keys:
                        result[keys[key]] = deser_val

        if errors:
            raise ValidationError(errors, valid_data=result)

        return result

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
