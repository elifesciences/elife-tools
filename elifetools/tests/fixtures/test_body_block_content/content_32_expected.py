from collections import OrderedDict
expected = OrderedDict([
    ('type', 'figure'),
    ('assets', [
        OrderedDict([
            ('type', 'table'),
            ('doi', u'10.7554/eLife.07141.007'),
            ('id', u'tbl3'),
            ('label', u'Table 3'),
            ('caption', [
                OrderedDict([
                    ('type', 'paragraph'),
                    ('text', u'Residues modeled for each chain of \u03b1 (1\u2013761) and \u03b2 (1\u2013375) in all four \u03b1<sub>4</sub>\u03b2<sub>4</sub> structures. In all four structures, the following regions are disordered and cannot be seen in the experimental electron density: the last ~24 C-terminal residues of \u03b1 that contain redox active cysteines Cys754 and Cys759 and the ~20 residues of \u03b2 that connect residue 330 to the ~15 C-terminal residues (360\u2013375) that bind to the \u03b1 subunit.')
                    ])
                ]),
            ('tables', [
                u'<table><thead><tr><th/><th colspan="8">Chain</th></tr></thead><tbody><tr><td>Structure</td><td>A (\u03b1)</td><td>B (\u03b1)</td><td>C (\u03b1)</td><td>D (\u03b1)</td><td>E (\u03b2)</td><td>F (\u03b2)</td><td>G (\u03b2)</td><td>H (\u03b2)</td></tr><tr><td>CDP/dATP</td><td>5-736</td><td>4-737</td><td>5-736</td><td>4-737</td><td>1-339, 363-375</td><td>1-341, 360-375</td><td>1-341, 360-375</td><td>1-340,<br/>361-375</td></tr><tr><td>UDP/dATP</td><td>4-737</td><td>4-737</td><td>4-737</td><td>4-736</td><td>1-339,<br/>363-373</td><td>1-341,<br/>360-375</td><td>1-341,<br/>360-375</td><td>1-340,<br/>361-375</td></tr><tr><td>ADP/dGTP</td><td>5-736</td><td>4-736</td><td>4-736</td><td>4-736</td><td>1-339,<br/>363-375</td><td>1-341,<br/>360-375</td><td>1-341,<br/>360-375</td><td>1-340,<br/>361-375</td></tr><tr><td>GDP/TTP</td><td>1-736</td><td>5-736</td><td>4-737</td><td>4-737</td><td>1-339,<br/>363-375</td><td>1-341,<br/>360-375</td><td>1-341,<br/>360-375</td><td>1-344,<br/>361-375</td></tr></tbody></table>'
                ])
            ])
        ])
    ])
