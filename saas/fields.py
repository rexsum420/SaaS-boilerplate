from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class SSNField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 11
        kwargs['validators'] = [
            RegexValidator(
                regex=r'^\d{3}-\d{2}-\d{4}$',
                message='SSN must be in the format XXX-XX-XXXX',
                code='invalid_ssn'
            )
        ]
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        value = super().clean(value, model_instance)
        if value:
            parts = value.split('-')
            if parts[0] == '000' or parts[1] == '00' or parts[2] == '0000':
                raise ValidationError('SSN contains invalid segments.')
        return value

    def from_db_value(self, value, expression, connection):
        if value and len(value) == 9:
            return f"{value[:3]}-{value[3:5]}-{value[5:]}"
        return value

    def to_python(self, value):
        if isinstance(value, str) and len(value) == 9:
            return f"{value[:3]}-{value[3:5]}-{value[5:]}"
        return value

    def get_prep_value(self, value):
        if value:
            return value.replace('-', '')
        return value

    def masked_value(self, value):
        if value and len(value) == 11:
            return f"XXX-XX-{value[-4:]}"
        return value