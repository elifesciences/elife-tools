from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", "appendix-1"),
            ("title", "Appendix 1"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                'For ..., <math id="inf1"><msub><mi>ϵ</mi><mi>i</mi></msub></math> and <math id="inf2"><msub><mi>ϵ</mi><mi>j</mi></msub></math>. That is, our goal is to compute:',
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "mathml"),
                            ("id", "equ1"),
                            (
                                "mathml",
                                '<math><mtable columnspacing="5pt" displaystyle="true"><mtr><mtd columnalign="right"><mrow><mi>I</mi><mo>\u2062</mo><mi>S</mi><mo>\u2062</mo><msub><mi>C</mi><mi>b</mi></msub></mrow></mtd><mtd columnalign="left"><mrow><mi/><mo>=</mo><mstyle displaystyle="false"><mfrac><msub><mi>a</mi><mi>B</mi></msub><mrow><msqrt><msub><mi>a</mi><mn>1</mn></msub></msqrt><mo>\u2062</mo><msqrt><msub><mi>a</mi><mn>2</mn></msub></msqrt></mrow></mfrac></mstyle></mrow></mtd></mtr></mtable></math>',
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )
]
