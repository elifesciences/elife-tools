from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "mathml"),
        ("id", u"equ7"),
        ("label", u"(3)"),
        (
            "mathml",
            u"<math><mrow><msub><mi>P</mi><mrow><mi>k</mi><mo>,</mo><mi>j</mi></mrow></msub><mrow><mo>(</mo><mi>I</mi><mi>O</mi><mo>)</mo></mrow><mo>=</mo><mn>0.1</mn><mo>+</mo><mfrac><mrow><mn>0.5</mn></mrow><mrow><mo>(</mo><mn>1</mn><mo>+</mo><msup><mi>e</mi><mrow><mo>-</mo><mn>0.3</mn><mrow><mo>(</mo><mi>I</mi><msub><mi>N</mi><mrow><mi>k</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>-</mo><mn>100</mn><mo>)</mo></mrow></mrow></msup><mo>)</mo></mrow></mfrac></mrow></math>",
        ),
    ]
)
