from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'group'),
        ('name', u'ICGC Breast Cancer Group'),
        ('affiliations', [
            OrderedDict([
                ('name', [u'Cancer Genome Project', u'Wellcome Trust Sanger Institute']),
                ('address', OrderedDict([
                    ('formatted', [u'Hinxton', u'United Kingdom']),
                    ('components', OrderedDict([
                        ('locality', [u'Hinxton']),
                        ('country', u'United Kingdom')
                        ]))
                    ]))
                ])
            ]),
        ('people', [
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', u'Elena Provenzano'),
                    ('index', u'Provenzano, Elena')
                    ])
                 ),
                ('affiliations', [
                    OrderedDict([
                        ('name', [u'Cambridge Breast Unit',
                                  u'Addenbrooke\u2019s Hospital, Cambridge University Hospital NHS Foundation Trust and NIHR Cambridge Biomedical Research Centre']),
                        ('address', OrderedDict([
                            ('formatted', [u'Cambridge CB2 2QQ', u'UK']),
                            ('components', OrderedDict([
                                ('locality', [u'Cambridge CB2 2QQ']),
                                ('country', u'UK')
                                ]))
                            ]))
                        ])
                    ])
                ])
            ])
        ])
    ]
