from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', u'unknown'),
        ('id', u'bib1'),
        ('date', '2013'),
        ('authors', [
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', 'Ghanasyam Rallapalli'),
                    ('index', 'Rallapalli, Ghanasyam')
                    ]))
                ])
            ]),
        ('title', u'Fraxinus version1 data analysis'),
        ('details', u'URL: https://github.com/shyamrallapalli/fraxinus_version1_data_analysis'),
        ('uri', u'https://github.com/shyamrallapalli/fraxinus_version1_data_analysis')
        ]),
    OrderedDict([
        ('type', u'unknown'),
        ('id', u'bib2'),
        ('date', '2014'),
        ('authors', [
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', 'Steven Bazyl'),
                    ('index', 'Bazyl, Steven')
                    ]))
                ])
            ]),
        ('title', u'Google api ruby client samples'),
        ('details', u'URL: https://github.com/google/google-api-ruby-client-samples/tree/master/service_account'),
        ('uri', u'https://github.com/google/google-api-ruby-client-samples/tree/master/service_account')
        ])
    ]
