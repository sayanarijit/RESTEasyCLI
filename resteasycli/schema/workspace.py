from marshmallow import Schema, fields, ValidationError, validates


class WorkspaceFileSchema(Schema):
    version = fields.Str(required=True,
                         error_messages={'validate': 'correct format is "v.(int).(int)"'})

    @validates('version')
    def validate_version(self, version):
        valid = [
            version.startswith('v'),
            len(version.split('.')) == 2,
            all(map(lambda x: x.isdigit(),
                    version.replace('v', '', 1).split('.')))
        ]
        if not all(valid):
            raise ValidationError('correct format for version field is: "v(digit).(digit)"')
