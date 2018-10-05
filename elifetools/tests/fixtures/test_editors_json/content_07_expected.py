from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Andy Collings'),
            ('index', u'Collings, Andy')
            ])),
        ('role', u'Senior and Reviewing Editor'),
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
        ]),
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Corinna Darian-Smith'),
            ('index', u'Darian-Smith, Corinna')
            ])),
        ('role', u'Reviewer'),
        ('affiliations', [
            OrderedDict([
                ('name', [u'Stanford University']),
                ('address', OrderedDict([
                    ('formatted', [u'United States']),
                    ('components', OrderedDict([
                        ('country', u'United States')
                        ]))
                    ]))
                ])
            ]),
        ]),
    ]
