# coding=utf-8
from collections import OrderedDict

expected = OrderedDict(
    [
        ("doi", u"10.7554/eLife.00001.001"),
        (
            "content",
            [
                OrderedDict(
                    [
                        ("type", "paragraph"),
                        (
                            "text",
                            u'Example <sub>in</sub> <i>cis</i> <span class="small-caps">or</span> <i>trans</i> <span class="underline">and</span> <i>Gfrα2</i> <math id="inf1"><mstyle displaystyle="true" scriptlevel="0"><mrow><munder><mo/><mi>m</mi></munder><mrow><msub><mover accent="true"><mi>p</mi><mo/></mover><mi>m</mi></msub><mo>=</mo><mn>0</mn></mrow></mrow></mstyle></math> <sup>by</sup> <b>its</b> co-receptors as *p&lt;0.05 &gt;0.25% <a href="#bib25">Schneider et al., 2006</a> and ligands.',
                        ),
                    ]
                )
            ],
        ),
    ]
)
