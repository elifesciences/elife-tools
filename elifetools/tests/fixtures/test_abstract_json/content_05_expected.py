# coding=utf-8
from collections import OrderedDict
expected = OrderedDict([
    ('content', [
        OrderedDict([
            ('type', 'section'),
            ('id', 'abs1'),
            ('title', 'Background:'),
            ('content', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', 'Background text.')
                ])
            ])
        ]),
        OrderedDict([
            ('type', 'section'),
            ('id', 'abs2'),
            ('title', 'Methods:'),
            ('content', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', 'Methods text.')
                ])
            ])
        ]),
        OrderedDict([
            ('type', 'section'),
            ('id', 'abs3'),
            ('title', 'Results:'),
            ('content', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', 'Results text.')
                ])
            ])
        ]),
        OrderedDict([
            ('type', 'section'),
            ('id', 'abs4'),
            ('title', 'Conclusions:'),
            ('content', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', 'Conclusions text.')
                ])
            ])
        ]),
        OrderedDict([
            ('type', 'section'),
            ('id', 'abs5'),
            ('title', 'Funding'),
            ('content', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', 'Funded by X, Y and Z.')
                ])
            ])
        ]),
        OrderedDict([
            ('type', 'section'),
            ('id', 'abs6'),
            ('title', 'Clinical trial number:'),
            ('content', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('id', 'CT1'),
                    ('text', (
                        '<a href="https://clinicaltrials.gov/show/NCT02968459">NCT02968459.</a>'))
                ])
            ])
        ])
    ])
])
