from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'section'),
        ('id', u's1'),
        ('content', [
            OrderedDict([
                ('type', 'paragraph'),
                ('text', u'Paragraph 1')
                ]),
            OrderedDict([
                ('type', 'section'),
                ('id', u's2'),
                ('title', u'How failure promotes translation'),
                ('content', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'Paragraph 2')
                        ])
                    ])
                ])
            ]),
        ('title', 'Main text')
        ])
    ]
