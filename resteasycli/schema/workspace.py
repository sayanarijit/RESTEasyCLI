from marshmallow import Schema, fields, ValidationError, validates


class WorkspaceFileSchema(Schema):
    version = fields.Str(required=True)

    @validates('version')
    def validate_version(self, version):
        checks = [
                lambda v: v.startswith('v'),
                lambda v: len(v.split('.')) == 2,
                lambda v: all(map(lambda x: x.isdigit(),
                    v.replace('v', '', 1).split('.')))
        ]
        if not all(map(lambda check: check(version), checks)):
            raise ValidationError(
                '{}: incorrect format. correct format is: "v(digit).(digit)"'.format(version))
