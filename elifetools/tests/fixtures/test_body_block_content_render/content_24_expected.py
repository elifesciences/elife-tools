from collections import OrderedDict
expected = [
    OrderedDict([
        ('content', [
            OrderedDict([
                ('type', 'table'),
                ('doi', u'10.7554/eLife.22264.016'),
                ('id', u'tbl1'),
                ('caption', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'Table caption. A second sentence.')
                        ])
                    ]),
                ('tables', [
                    '<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'
                    ])
                ])
            ])
        ])
    ]
