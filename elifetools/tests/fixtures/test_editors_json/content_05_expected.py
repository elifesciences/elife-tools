from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Melissa Harrison'),
            ('index', u'Harrison, Melissa')
            ])),
        ('role', u'Senior Editor'),
        ('affiliations', [
            OrderedDict([
                ('name', [u'eLife']),
                ('address', OrderedDict([
                    ('formatted', [u'United Kingdom']),
                    ('components', OrderedDict([
                        ('country', u'United Kingdom')
                        ]))
                    ]))
                ])
            ]),
        ]),
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Andrew Collings'),
            ('index', u'Collings, Andrew')
            ])),
        ('role', u'Reviewing Editor'),
        ('affiliations', [
            OrderedDict([
                ('name', [u'eLife Sciences']),
                ('address', OrderedDict([
                    ('formatted', [u'United Kingdom']),
                    ('components', OrderedDict([
                        ('country', u'United Kingdom')
                        ]))
                    ]))
                ])
            ]),
        ])
    ]
