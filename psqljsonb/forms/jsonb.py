import json

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


__all__ = ['JSONBField']


class JSONBField(forms.CharField):
    """A field for JSONB data."""
    widget = forms.Textarea
    default_error_messages = {
        'invalid_json': _('Could not load JSON data.'),
    }

    def prepare_value(self, value):
        """4-space indentation for the admin interface"""
        return json.dumps(value, indent=4)

    def to_python(self, value):
        """Invalid input gets invalidated and stringified"""
        if value is None:
            return None
        try:
            # if it passes validation here, it passes for postgres
            json.loads(value)
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid_json'],
                code='invalid_json',
            )

        return value
