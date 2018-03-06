from collections import OrderedDict
expected = [
    OrderedDict([
        ('content', [
            OrderedDict([
                ('type', 'list'),
                ('prefix', 'number'),
                ('items', [
                    [
                        OrderedDict([
                            ('type', 'paragraph'),
                            ('text', u'At least 4 unique reads supporting variants and all variant reads at least 20 phred scale sequencing quality score (Q 20 = 1% sequencing error rate) and at least 3% variant allele fractions (VAFs).')
                            ]),
                        OrderedDict([
                            ('type', 'list'),
                            ('prefix', 'none'),
                            ('items', [
                                [
                                    OrderedDict([
                                        ('type', 'paragraph'),
                                        ('text', u'A. Regardless of in WGS and in WES, the \u22654 mismatches and the \u22653% VAF criteria must be satisfied simultaneously.')
                                        ])
                                    ],
                                [
                                    OrderedDict([
                                        ('type', 'paragraph'),
                                        ('text', u'B. However, in WGS, the minimum number of reads (n = 4) criterion is not essential, because the \u22653% VAF criterion is much more stringent (3% VAF request at least 240 mismatches (&gt;&gt;4) given mtDNA coverage is \u223c8000 for WGS).')
                                        ])
                                    ],
                                [
                                    OrderedDict([
                                        ('type', 'paragraph'),
                                        ('text', u'C. In WES, the \u22653% VAF criterion is relatively less important than in WGS, because the \u22654 mismatches criterion is more stringent. For example, 4 mismatches in 90x (WXS average) coverage region (VAF = 4.4%) automatically fulfill the \u22653% VAF criterion. For less covered regions (i.e. &lt;40x coverage; n = 285 out of total 1907 substitutions), the VAF criterion becomes less important, because 4 mismatches would generate \u226510% VAF, much higher than the minimum threshold (i.e. 3%). As results, we are missing lower heteroplasmic variants (i.e. variants with 3\u201310% heteroplasmic levels) from low coverage samples (mostly by WXS). The lower sensitivity of WXS is also confirmed in our validation study (see \u201cValidation of somatic variants\u201d below).')
                                        ])
                                    ]
                                ])
                            ])
                        ]
                    ])
                ])
            ])
        ])
    ]
