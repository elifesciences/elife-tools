from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'conference-proceeding'),
        ('id', u'bib35'),
        ('date', u'1971'),
        ('authors', [
            OrderedDict([
                ('type', 'group'),
                ('name', u'World Health Organization')
                ])
            ]),
        ('conference', {
            'name': ['WHO Expert Committee on Malaria']
            }),
        ('articleTitle', 'WHO Expert Committee on Malaria [meeting held in Geneva from 19 to 30 October 1970]: fifteenth report'),
        ('publisher', OrderedDict([
            ('name', ['World Health Organization']),
            ('address', OrderedDict([
                ('formatted', ['Geneva']),
                ('components', OrderedDict([
                    ('locality', ['Geneva'])
                    ])),
                ])),
            ])),
        ])
    ]
