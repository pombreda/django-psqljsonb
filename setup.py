#!/usr/bin/env python
# vim: fileencoding=utf-8

from distutils.core import setup

setup(
    name='psqljsonb',
    version='0.0.1',
    description='Django jsonb field for PostgreSQL',
    url='https://github.com/codento/django-psqljsonb/',
    author=u'Markus Törnqvist',
    author_email='markus.tornqvist@codento.com',
    packages=['psqljsonb', 'psqljsonb/fields', 'psqljsonb/forms', 'psqljsonb/tests'],
    data_files=[
        ('share/django-psqljsonb/', ['requirements.txt', 'LICENSE', 'README.md']),
    ],
)

