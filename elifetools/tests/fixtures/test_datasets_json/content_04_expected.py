from collections import OrderedDict
expected = OrderedDict([
    ('availability', [
        OrderedDict([
            ('type', 'paragraph'),
            ('text', 'This is the text entered for the data availability text entry box.')
            ])
        ]),
    ('generated', [
        OrderedDict([
            ('id', u'dataset1'),
            ('date', u'2016'),
            ('authors', [
                OrderedDict([
                    ('type', 'person'),
                    ('name', OrderedDict([
                        ('preferred', u'M Harrison'),
                        ('index', u'Harrison, M')
                        ]))
                    ]),
                OrderedDict([
                    ('type', 'group'),
                    ('name', u'York University')
                    ])
                ]),
            ('title', u'xml-mapping'),
            ('details', u'Publicly available on GitHub'),
            ('uri', u'https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml')
            ])
        ]),
    ('used', [
        OrderedDict([
            ('id', u'dataset2'),
            ('date', u'2012'),
            ('authors', [
                OrderedDict([
                    ('type', 'group'),
                    ('name', u'M Harrison')
                    ])
                ]),
            ('title', u'elife-vendor-workflow-config'),
            ('details', u'Publicly available on GitHub.'),
            ('uri', u'https://github.com/elifesciences/elife-vendor-workflow-config')
            ]),
        OrderedDict([
            ('id', u'dataset3'),
            ('date', u'2015'),
            ('authors', [
                OrderedDict([
                    ('type', 'group'),
                    ('name', u'Kok K')
                    ]),
                OrderedDict([
                    ('type', 'group'),
                    ('name', u'Ay A')
                    ]),
                OrderedDict([
                    ('type', 'group'),
                    ('name', u'Li L')
                    ]),
                OrderedDict([
                    ('type', 'group'),
                    ('name', u'Arnosti DN')
                    ])
                ]),
            ('title', u'Dryad Digital Repository'),
            ('doi', u'10.5061/dryad.cv323')
            ])
        ])
    ])