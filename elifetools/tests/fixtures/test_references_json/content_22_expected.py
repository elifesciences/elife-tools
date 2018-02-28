from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', u'book'),
        ('id', u'bib101'),
        ('date', u'1988'),
        ('authors', [
            OrderedDict([
                ('type', 'person'),
                ('name', OrderedDict([
                    ('preferred', u'WB Wood'),
                    ('index', u'Wood, WB')
                    ]))
                ]),
            OrderedDict([
                ('type', 'group'),
                ('name', u'The Community of <i>C. elegans</i> Researchers')
                ])
            ]),
        ('bookTitle', u'The nematode Caenorhabditis elegans'),
        ('publisher', OrderedDict([
            ('name', [u'Cold Spring Harbor Laboratory Press']),
            ('address', OrderedDict([
                ('formatted', [u'Cold Spring Harbor, New York']),
                ('components', OrderedDict([
                    ('locality', [u'Cold Spring Harbor, New York'])
                    ]))
                ]))
            ]))
        ])
    ]
