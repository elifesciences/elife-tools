from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Welcome Bender'),
            ('index', u'Bender, Welcome')
            ])),
        ('affiliations', [
            OrderedDict([
                ('name', [u'Department of Biological Chemistry and Molecular Pharmacology', u'Harvard Medical School']),
                ('address', OrderedDict([
                    ('formatted', [u'Boston', u'United States']),
                    ('components', OrderedDict([
                        ('locality', [u'Boston']),
                        ('country', u'United States')
                        ]))
                    ]))
                ])
            ]),
        ('phoneNumbers', [u'+16174321906']),
        ('contribution', u'WB, Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting and revising the article'),
        ('competingInterests', u'The authors declare that no competing interests exist.')
    ])
]