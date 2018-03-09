from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', u'journal'),
        ('id', u'bib42'),
        ('date', '2016'),
        ('authors', [
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', u'H Ellegren'),
                    ('index', u'Ellegren, H')
                    ]))
                ]),
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', u'N Galtier'),
                    ('index', u'Galtier, N')
                    ]))
                ])
            ]),
        ('articleTitle', u'Self fertilization and population variability in the higher plants (vol 91, pg 41, 1957)'),
        ('journal', u'Nature Reviews Genetics'),
        ('volume', u'17'),
        ('pages', OrderedDict([
            ('first', u'422'),
            ('last', u'433'),
            ('range', u'422\u2013433')
            ])),
        ('doi', u'10.1038/nrg.2016.58')
        ])
    ]
