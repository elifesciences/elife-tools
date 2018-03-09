from collections import OrderedDict
expected = [
    OrderedDict([
        ('content', [
            OrderedDict([
                ('type', 'section'),
                ('id', u's2-1-1-1'),
                ('title', u'Article types (XML only, not display) (level 4 heading)'),
                ('content', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'This is an example of a list where the prefix character is a uppercase roman numeral. This is a controlled list from the JATS DTD')
                        ]),
                    OrderedDict([
                        ('type', 'list'),
                        ('prefix', u'roman-upper'),
                        ('items', [
                            [
                                OrderedDict([
                                    ('type', 'list'),
                                    ('prefix', u'roman-lower'),
                                    ('items', [
                                        [
                                            OrderedDict([
                                                ('type', 'paragraph'),
                                                ('text', '<i>P. falciparum</i>')
                                                ])
                                            ]
                                        ])
                                    ]),
                                OrderedDict([
                                    ('type', 'paragraph'),
                                    ('text', u'Genus: Leishmania. There are 3 subgenus of Leishmania:')
                                    ])
                                ],
                            [
                                OrderedDict([
                                    ('type', 'list'),
                                    ('prefix', u'roman-lower'),
                                    ('items', [
                                        [
                                            OrderedDict([
                                                ('type', 'paragraph'),
                                                ('text', u'Leishmania')
                                                ])
                                            ],
                                        [
                                            OrderedDict([
                                                ('type', 'paragraph'),
                                                ('text', u'Sauroleishmania')
                                                ])
                                            ],
                                        [
                                            OrderedDict([
                                                ('type', 'paragraph'),
                                                ('text', u'Viannia')
                                                ])
                                            ],
                                        [
                                            OrderedDict([
                                                ('type', 'paragraph'),
                                                ('text', u'Within Viannia subgenus, there are 11 species:')
                                                ]),
                                            OrderedDict([
                                                ('type', 'list'),
                                                ('prefix', u'bullet'),
                                                ('items', [
                                                    [
                                                        OrderedDict([
                                                            ('type', 'paragraph'),
                                                            ('text', '<i>L. braziliensis</i>')
                                                            ])
                                                        ]
                                                    ])
                                                ])
                                            ]
                                        ])
                                    ])
                                ]
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ]
