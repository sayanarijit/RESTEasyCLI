from marshmallow import Schema, fields, ValidationError, validates

from resteasycli.config import Config


class WorkspaceFileSchema(Schema):
    version = fields.Str(required=True)

    @validates('version')
    def validate_version(self, version):
        if version not in Config.SUPPORTED_FILE_FORMATS:
            raise ValidationError('{}: supported versions for file format are: {}'.format(
                version, ','.join(Config.SUPPORTED_FILE_FORMATS)
            ))

    class Meta:
        ordered = True
