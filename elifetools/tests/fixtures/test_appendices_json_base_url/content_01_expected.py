from collections import OrderedDict
expected = [
    OrderedDict([
        ('title', u'Appendix 5'),
        ('content', [
            OrderedDict([
                ('type', 'section'),
                ('id', u's61'),
                ('title', u'E. Volatiles'),
                ('content', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'Paragraph content.')
                        ]),
                    OrderedDict([
                        ('type', 'figure'),
                        ('assets', [
                            OrderedDict([
                                ('type', 'table'),
                                ('doi', u'10.7554/eLife.17092.035'),
                                ('id', u'A5-tbl2'),
                                ('label', u'Appendix 5\u2014table 2'),
                                ('caption', [
                                    OrderedDict([
                                        ('type', 'paragraph'),
                                        ('text', u'Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901). NA = no structural isomer can be determined.')
                                        ])
                                    ]),
                                ('tables', ['<table><tbody><tr><td valign="top"><img src="elife-17092-inf1-v1.jpg"/><br/><img src="elife-17092-inf2-v1.jpg"/></td></tr></tbody></table>'])
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ]
