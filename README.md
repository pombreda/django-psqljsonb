django-psqljsonb
================

JSONBField for Django 1.8 and PostgreSQL 9.4

Ever wanted to use PostgreSQL's ``jsonb`` data type for actual ORM lookups but couldn't? Now you can!

Slightly tested with Python 3.4 as well as 2.7. Please report bugs if you find them!

Installation
------------

Simply add the app to your settings

    INSTALLED_APPS = (
        ...
        'psqljsonb'
        ...
    )

Usage
-----

Add the field to your model

    from psqljsonb.fields import JSONBField
    from django.db import models

    class Item(models.Model):
        name = models.CharField(max_length=32)
        data = JSONBField()

Creating JSON data is straight-forward:

    models.Item.objects.create(name='Foo', data={'name': 'Foo',
                                                "list": [5, 10, 15],
                                                "additional_data": {
                                                    "boolean": False,
                                                    "string": "text",
                                                 }
                                            })

The extra query component ``json`` must be used in the query keyword for
``psqljsonb`` to query within the json structure.

    item_qs = models.Item.objects.filter(data__json__additional_data__boolean=True)

``django-psqljsonb`` also supports the ``has_key`` and ``contains`` operators:


    item_qs = models.Item.objects.filter(data__json__has_key='additional_data')


``contains`` works on every nesting level in the jsonb data:

    item_qs = models.Item.objects.filter(data__json__additional_data__contains={
                                            'boolean': False,
                                            'string': 'text'
                                        })

Also lookups by array index work:

    item_qs = models.Item.objects.filter(data__json__list__2=15)

Limitations
-----------

All digits in the query keyword are cast as integers. This is ok for most common
cases, but does not work if you store an object with a key "2" or other digit.
This is as defined in [RFC 7159](https://tools.ietf.org/html/rfc7159#page-6)

Because ``json`` has a special meaning, you can't use it as a key in your jsonb
data.

Some array operations are currently not supported. The way escaping works and
because Python lists are json (not Postgres) arrays, implementing
``has_keys`` is not currently possible.

