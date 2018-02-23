# coding=utf-8
from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Jane Alfred'),
            ('index', u'Alfred, Jane')
            ])
         ),
        ('orcid', u'0000-0001-6798-0064'),
        ('role', u'Consultant Editor'),
        ('affiliations', [
            OrderedDict([
                ('address', OrderedDict([
                    ('formatted', [u'Cambridge', u'United Kingdom']),
                    ('components', OrderedDict([
                        ('locality', [u'Cambridge']),
                        ('country', u'United Kingdom')
                        ]))
                    ])
                 ),
                ('name', ['Cambridge'])
                ])
            ])
        ])
    ]
