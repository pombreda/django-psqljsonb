from django.db.models import Lookup

import json


class JSONBLookup(Lookup):
    LOOKUPS = {
        'exact': {
            'operator': '=',
            # This breaks with {"1": "one"} style data
            'lookup_func': lambda val: val if val.isdigit() else "'%s'" % val,
            'prep_func': lambda val: json.dumps(val),
            'path_elem': '->',
        },
        'has_key': {
            'operator': '?',
            'lookup_func': lambda val: '',
            'prep_func': lambda val: val,
            'path_elem': '',
        },
        'contains': {
            'operator': '@>',
            'lookup_func': lambda val: '',
            'prep_func': lambda val: val,
            'path_elem': '',
        },
    }

    def __init__(self, lookup_name):
        self.lookup_name = lookup_name

    def __call__(self, lhs, rhs):
        """FIXME: duplicated __init__ code
        """

        self.lhs, self.rhs = lhs, rhs
        self.rhs = self.get_prep_lookup()

        if hasattr(self.lhs, 'get_bilateral_transforms'):
            bilateral_transforms = self.lhs.get_bilateral_transforms()
        else:
            bilateral_transforms = []
        if bilateral_transforms:
            # We should warn the user as soon as possible if he is trying to apply
            # a bilateral transformation on a nested QuerySet: that won't work.
            # We need to import QuerySet here so as to avoid circular
            from django.db.models.query import QuerySet
            if isinstance(rhs, QuerySet):
                raise NotImplementedError("Bilateral transformations on nested querysets are not supported.")
        self.bilateral_transforms = bilateral_transforms

        return self

    def get_lookup_data(self):
        """Helper for doing queries"""

        # Look at our known lookups
        if self.lookup_name not in self.LOOKUPS:
            lookup_data = self.LOOKUPS['exact']
        else:
            lookup_data = self.LOOKUPS[self.lookup_name]

        return lookup_data

    def get_prep_lookup(self):
        """Prepare lookup value; defaults to json.dumps()"""

        super_lookup = super(JSONBLookup, self).get_prep_lookup()
        lookup_data = self.get_lookup_data()

        return lookup_data['prep_func'](super_lookup)

    def as_sql(self, qn, connection):
        """Looks up the json path as string"""

        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params

        lookup_data = self.get_lookup_data()

        operator = lookup_data['operator']
        lookup = lookup_data['lookup_func'](self.lookup_name)
        path_elem = lookup_data['path_elem']

        return "%s %s %s %s %s" % (lhs, path_elem, lookup, operator, rhs), params


