from collections import OrderedDict
expected = OrderedDict([
    ('type', 'figure'),
    ('assets', [
        OrderedDict([
            ('type', 'image'),
            ('doi', u'10.7554/eLife.00666.024'),
            ('id', u'fig1'),
            ('label', u'Figure 1'),
            ('title', u'Figure title'), 
            ('caption', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', u'Figure caption')
                    ])
                ]),
            ('image', OrderedDict([
                ('uri', u'elife-00666-fig1-v1.tif'),
                ('alt', u''),
                ('attribution', [
                   u'\u00a9 1991, Publisher 1, All Rights Reserved. The in situ image in panel 3 is reprinted with permission from Figure 2D, <a href="#bib72">Small et al. (1991)</a>, <i>Test &amp; Automated</i>.', 
                   u'\u00a9 1991, Publisher 2, All Rights Reserved. In situ images in panels 4 and 5 are reprinted with permission from Figure 3A and 3C, <a href="#bib74">Stanojevic et al. (1991)</a>, <i>Journal</i>.'
                   ])
                ])),
            ])
        ])
    ])
