# coding=utf-8
from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Geraldine Seydoux'),
            ('index', u'Seydoux, Geraldine')
            ])
         ),
        ('orcid', u'0000-0001-8257-0493'),
        ('affiliations', [
            OrderedDict([
                ('name', [u'Department of Molecular Biology and Genetics',
                          u'Howard Hughes Medical Institute, Johns Hopkins University School of Medicine']
                 ),
                ('address', OrderedDict([
                    ('formatted', [u'Baltimore', u'United States']),
                    ('components', OrderedDict([
                        ('locality', [u'Baltimore']),
                        ('country', u'United States')
                        ]))
                    ]))
                ])
            ]),
        ('emailAddresses', [u'gseydoux@jhmi.edu']),
        ('competingInterests', u'The authors declare that no competing interests exist.')
        ])
    ]