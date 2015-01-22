import json
import six

from .. import forms, lookups
from django.core import exceptions
from django.db.models import Field, SubfieldBase, Transform
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.db.backends.postgresql_psycopg2.version import get_version


__all__ = ['JSONBField']


class JSONBField(six.with_metaclass(SubfieldBase, Field)):
    empty_strings_allowed = False
    description = _('Map of strings to strings')
    default_error_messages = {
        'unserializable_object': _('Could not serialize field to JSON.'),
        'invalid_key': _('Cannot create key named "%(key)s"'),
    }

    def db_type(self, connection):
        if connection.vendor != 'postgresql':
            raise RuntimeError('JSONBField works only with PostgreSQL')

        if get_version(connection) < 90400:
            raise RuntimeError('JSONBField works only with PostgreSQL >= 9.4')

        return 'jsonb'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return json.dumps(value)

    def validate(self, value, model_instance):
        super(JSONBField, self).validate(value, model_instance)

        try:
            value = json.loads(value)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages['unserializable_object'],
            )

        # Due to internal constraints, 'json' is not a valid key
        if isinstance(value, dict):
            if 'json' in value:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_key'],
                    params={'key': 'json'},
                )
            for k in value:
                if isinstance(k, six.string_types) and k.isdigit():
                    raise exceptions.ValidationError(
                        self.error_messages['invalid_key'],
                        params={'key': k},
                    )

    def get_transform(self, name):
        transform = super(JSONBField, self).get_transform(name)

        if transform:
            return transform
        return KeyTransformFactory(name)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.JSONBField,
        }
        defaults.update(kwargs)
        return super(JSONBField, self).formfield(**defaults)


class EnterJSONBTransform(Transform):
    """A dummy-ish Transform. After this, everything is handled
    as json. It exists because otherwise the Django query compiler
    will insert a literal "exact" into the query, breaking it.
    """

    def get_lookup(self, lookup_name):
        return lookups.JSONBLookup(lookup_name)

    def as_sql(self, compiler, connection):
        """Pass the query through"""

        lhs, params = compiler.compile(self.lhs)
        return lhs, params


class JSONBKeyTransform(EnterJSONBTransform):
    output_field = JSONBField()

    def __init__(self, key_name, *args, **kwargs):
        super(JSONBKeyTransform, self).__init__(*args, **kwargs)
        self.key_name = key_name

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)

        # This -> is used for path elements
        return "%s -> '%s'" % (lhs, self.key_name), params


class KeyTransformFactory(object):
    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, *args, **kwargs):
        if self.key_name == 'json':
            return EnterJSONBTransform(*args, **kwargs)

        return JSONBKeyTransform(self.key_name, *args, **kwargs)

