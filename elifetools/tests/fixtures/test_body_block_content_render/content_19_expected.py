from collections import OrderedDict
expected = [
    OrderedDict([
        ('content', [
            OrderedDict([
                ('type', 'figure'),
                ('assets', [
                    OrderedDict([
                        ('type', 'table'),
                        ('doi', u'10.7554/eLife.22264.016'),
                        ('id', u'tbl1'),
                        ('label', u'Table 1'),
                        ('caption', [
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', u'Progeny of <i>Fn1<sup>syn/+</sup>;Itgb3<sup>+/-</sup></i> x <i>Fn1<sup>syn/+</sup>;Itgb3<sup>+/-</sup></i> intercrosses.')
                                ])
                            ]),
                        ('tables', [
                            '<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'
                            ]),
                        ('sourceData', [
                            OrderedDict([
                                ('doi', u'10.7554/eLife.22264.017'),
                                ('id', u'SD1-data'),
                                ('label', u'Table 1\u2014source data 1'),
                                ('title', u'Progeny of <i>Fn1<sup>syn/syn</sup>;Itgb3<sup>+/-</sup></i> x <i>Fn1<sup>syn/syn</sup>;Itgb3<sup>+/-</sup></i> crosses'),
                                ('mediaType', u'application/docx')
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ]
