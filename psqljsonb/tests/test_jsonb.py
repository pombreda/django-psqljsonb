from django.utils.translation import ugettext_lazy as _
from django.core import exceptions
from django.test import TestCase
from . import models


class JSONBTestCase(TestCase):
    def setUp(self):
        models.Item.objects.create(name='Primus', data={'main': 'Main 1'})
        models.Item.objects.create(name='Secundus', data={'main': 'Main 2'})
        models.Item.objects.create(name='Tertius', data={'main': 'Main 2',
                                                    'additional_data': {
                                                        'boolean': False,
                                                        'first_appearance': 'book',
                                                    }
                                                })  # NOQA
        models.Item.objects.create(name='Quartus', data={'main': 'Main 3',
                                                    'additional_data': {
                                                        'boolean': True,
                                                        'first_appearance': 'book',
                                                    }
                                                })  # NOQA
        models.Item.objects.create(name='Quintus', data={'main': 'Main 3',
                                                    'additional_data': {
                                                        'boolean': False,
                                                        'first_appearance': 'movie',
                                                    }
                                                })  # NOQA
        models.Item.objects.create(name='Sextus', data={'main': 'Main 4',
                                                    "list": [5, 10, 15],
                                                    "additional_data": {
                                                        "boolean": False,
                                                        "string": "text",
                                                     }
                                                })  # NOQA

        models.Item.objects.create(name='Break', data='null')

    ### Test queries

    def testMain2Count(self):
        self.assertEquals(models.Item.objects.filter(data__json__main='Main 2').count(), 2)

    def testRabid(self):
        item_qs = models.Item.objects.filter(data__json__additional_data__boolean=True)
        self.assertEquals(len(item_qs), 1)
        self.assertEquals(item_qs[0].name, 'Quartus')

    def testWeirdo(self):
        item_qs = models.Item.objects.filter(data__json__list__2=15)
        self.assertEquals(len(item_qs), 1)
        self.assertEquals(item_qs[0].name, 'Sextus')

    def testTextString(self):
        item_qs = models.Item.objects.filter(data__json__additional_data__string='text')
        self.assertEquals(len(item_qs), 1)

    def testHasKey(self):
        item_qs = models.Item.objects.filter(data__json__has_key='additional_data')
        self.assertEquals(item_qs.count(), 4)

    def testContains1(self):
        item_qs = models.Item.objects.filter(data__json__contains={'additional_data': {
                                                                        'boolean': False,
                                                                        'first_appearance': 'movie'
                                                                    }
                                                                })  # NOQA
        self.assertEquals(item_qs.count(), 1)
        self.assertEquals(item_qs[0].name, 'Quintus')

    def testContains2(self):
        item_qs = models.Item.objects.filter(data__json__additional_data__contains={'boolean': False,
                                                                'first_appearance': 'movie'
                                                                })  # NOQA
        self.assertEquals(item_qs.count(), 1)
        self.assertEquals(item_qs[0].name, 'Quintus')

    def testContains3(self):
        item_qs = models.Item.objects.filter(data__json__list__contains=[5, 10, 15])
        self.assertEquals(item_qs.count(), 1)
        self.assertEquals(item_qs[0].name, 'Sextus')

    ### Test updates

    def testJsonBool(self):
        item = models.Item.objects.get(name='Primus')

        item.data = False
        item.save()

        item = models.Item.objects.get(name='Primus')
        self.assertFalse(item.data)

    def testJsonArray(self):
        item = models.Item.objects.get(name='Primus')

        item.data = [1, 2, 3, 5, 8, 13]
        item.save()

        item = models.Item.objects.get(name='Primus')
        self.assertEquals(item.data, [1, 2, 3, 5, 8, 13])

    def testJsonObject(self):
        item = models.Item.objects.get(name='Primus')

        item.data = {}
        item.save()

        item = models.Item.objects.get(name='Primus')
        self.assertEquals(item.data, {})

    ### Test for failure

    def testUnserializableUpdate(self):
        item = models.Item.objects.get(name='Break')

        # Function cannot be serialized into json
        item.data = lambda x: x.upper()

        try:
            item.full_clean()
            raise AssertionError(_('Invalid data should have failed'))
        except exceptions.ValidationError:
            pass

    def testIntObjectKey(self):
        item = models.Item.objects.get(name='Break')

        item.data = {
            1: 'foo',
        }

        try:
            item.full_clean()
            raise AssertionError(_('Invalid data should have failed'))
        except exceptions.ValidationError:
            pass

    def testIntishObjectKey(self):
        item = models.Item.objects.get(name='Break')

        item.data = {
            '1': 'foo',
        }

        try:
            item.full_clean()
            raise AssertionError(_('Invalid data should have failed'))
        except exceptions.ValidationError:
            pass

    def testJsonObjectKey1(self):
        item = models.Item.objects.get(name='Break')

        item.data = {
            'json': [1],
        }

        try:
            item.full_clean()
            raise AssertionError(_('Invalid data should have failed'))
        except exceptions.ValidationError:
            pass

    def testJsonObjectKey2(self):
        item = models.Item.objects.get(name='Break')

        item.data = {
            'additional_data': {
                'json': [1],
            }
        }

        try:
            item.full_clean()
            raise AssertionError(_('Invalid data should have failed'))
        except exceptions.ValidationError:
            pass

