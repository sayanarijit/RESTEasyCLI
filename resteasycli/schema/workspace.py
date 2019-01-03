from marshmallow import Schema, fields, ValidationError, validates


class WorkspaceFileSchema(Schema):
    version = fields.Str(required=True,
                         error_messages={'validate': 'correct format is "v.(int).(int)"'})

    @validates('version')
    def validate_version(self, version):
        checks = [
                lambda v: v.startswith('v'),
                lambda v: len(v.split('.')) == 2,
                lambda v: all(map(lambda x: x.isdigit(),
                    v.replace('v', '', 1).split('.')))
        ]
        if not all(map(lambda check: check(version), checks)):
            raise ValidationError('correct format for version field is: "v(digit).(digit)"')
