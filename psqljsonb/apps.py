from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.utils.translation import ugettext_lazy as _

from .signals import register_default_json_handler


class PostgresConfig(AppConfig):
    name = 'psqljsonb'
    verbose_name = _('PostgreSQL jsonb extension')

    def ready(self):
        connection_created.connect(register_default_json_handler)
