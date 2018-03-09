from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'section'),
        ('id', u's1'),
        ('title', u'Section title'),
        ('content', [
            OrderedDict([
                ('type', 'paragraph'),
                ('text', u'Content.')
                ]),
            OrderedDict([
                ('type', 'figure'),
                ('assets', [
                    OrderedDict([
                        ('type', 'image'),
                        ('doi', u'10.7554/eLife.00666.008'),
                        ('id', u'fig2'),
                        ('label', u'Figure 2'),
                        ('title', u'Figure title'),
                        ('caption', [
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', u'Figure caption')
                                ])
                            ]),
                        ('image', {'alt': '', 'uri': u'elife-00666-fig2-v1.tif'})
                        ]),
                    OrderedDict([
                        ('type', 'image'),
                        ('doi', u'10.7554/eLife.00666.009'),
                        ('id', u'fig2s1'),
                        ('label', u'Figure 2'),
                        ('title', u'Figure title'),
                        ('caption', [
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', u'Figure caption')
                                ])
                            ]),
                        ('image', {'alt': '', 'uri': u'elife-00666-fig2-figsupp1-v1.tif'})
                        ])
                    ])
                ]),
            OrderedDict([
                ('type', 'paragraph'),
                ('text', u'More content')
                ])
            ])
        ])
    ]
