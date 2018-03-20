from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', u'journal'),
        ('id', u'bib96'),
        ('date', u'2010'),
        ('authors', [
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', u'DR Zerbino'),
                    ('index', u'Zerbino, DR')
                    ]))
                ])
            ]),
        ('articleTitle', u'Using the Velvet de novo assembler for short-read sequencing technologies'),
        ('journal', u'Curr Protoc Bioinformatics'),
        ('volume', u'11'),
        ('pages', OrderedDict([
            ('first', u'11.5.1'),
            ('last', u'11.5.12'),
            ('range', u'11.5.1\u201311.5.12')])),
        ('doi', u'10.1002/0471250953.bi1105s31')
        ])
    ]
