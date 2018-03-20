from collections import OrderedDict
expected = [
    OrderedDict([
        ('id', u'app1'),
        ('title', u'Appendix 1'),
        ('content', [
            OrderedDict([
                ('type', 'section'),
                ('id', u's25'),
                ('title', u'1 Definitions related to phyllotaxis'),
                ('content', [
                    OrderedDict([('type', 'paragraph'),
                        ('text', u'Phyllotactic patterns emerge ...')
                        ])
                    ])
                ]),
            OrderedDict([
                ('type', 'section'),
                ('id', u's26'),
                ('title', u'2 The classical model of phyllotaxis: a brief recap'),
                ('content', [
                    OrderedDict([
                        ('type', 'section'),
                        ('id', u's27'),
                        ('title', u'2.1 Model description'),
                        ('content', [
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', u'We implemented ...')
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ]),
    OrderedDict([
        ('id', u'app2'),
        ('title', u'Appendix 2'),
        ('content', [
            OrderedDict([
                ('type', 'section'),
                ('id', u's53'),
                ('title', u'Additional videos and initial conditions for all videos'),
                ('content', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'For all videos, ...')
                        ])
                    ])
                ])
            ])
        ])
    ]