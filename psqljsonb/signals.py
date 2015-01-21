import json
import psycopg2

from django.core.serializers.json import DjangoJSONEncoder
from psycopg2.extras import Json


class JSONAdapter(Json):
    """Custom adapter uses Django's encoder for dates"""

    def dumps(self, obj):
        return json.dumps(obj, cls=DjangoJSONEncoder)


def register_default_json_handler(connection, **kwargs):
    if connection.vendor != 'postgresql':
        return

    psycopg2.extensions.register_adapter(dict, JSONAdapter)
    psycopg2.extensions.register_adapter(list, JSONAdapter)
    psycopg2.extensions.register_adapter(bool, JSONAdapter)

