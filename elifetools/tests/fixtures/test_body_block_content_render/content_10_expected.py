from collections import OrderedDict
expected = [
    OrderedDict([
        ('content', [
            OrderedDict([
                ('type', 'paragraph'),
                ('text', 'This <a href="#fig3">Figure 3A</a> test')
                ]),
            OrderedDict([
                ('type', 'mathml'),
                ('id', 'equ2'),
                ('label', '(2)'),
                ('mathml', '<math><mrow/></math>')
                ]),
            OrderedDict([
                ('type', 'paragraph'),
                ('text', 'was also')
                ]),
            OrderedDict([
                ('type', 'figure'),
                ('assets', [
                    OrderedDict([
                        ('type', 'image'),
                        ('doi', '10.7554/eLife.01944.005'),
                        ('id', 'fig3'),
                        ('label', 'Figure 3'),
                        ('title', 'Title'),
                        ('caption', [
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', 'Caption <b>b</b>')
                                ]),
                            OrderedDict([
                                ('type', 'mathml'),
                                ('id', 'equ3'),
                                ('label', '(3)'),
                                ('mathml', '<math><mrow/></math>')
                                ]),
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', 'where m<sub>i</sub> given by:')
                                ]),
                            OrderedDict([
                                ('type', 'mathml'),
                                ('id', 'equ4'),
                                ('label', '(4)'),
                                ('mathml', '<math><mrow/></math>')
                                ]),
                            OrderedDict([
                                ('type', 'paragraph'),
                                ('text', 'More caption')
                                ])
                            ]),
                        ('image', {'alt': '', 'uri': 'elife-01944-fig3-v1.tif'})
                        ])
                    ])
                ])
            ])
        ])
    ]
