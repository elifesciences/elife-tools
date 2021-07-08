from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "figure"),
        (
            "assets",
            [
                OrderedDict(
                    [
                        ("type", "table"),
                        ("id", u"keyresource"),
                        ("label", u"This is a label"),
                        (
                            "tables",
                            [
                                u"<table><thead><tr><th/><th>pY</th><th>Experiment</th><th>Concentration (\u03bcM)</th></tr></thead><tbody><tr><td>IGF1R-fl + IGF1</td><td>+</td><td><i>K</i><sub><i>m</i></sub> ATP</td><td>500, 400, 300, 250, 125, 62.5, 31.3, 15.6, 7.8</td></tr></tbody></table>"
                            ],
                        ),
                        (
                            "footnotes",
                            [
                                OrderedDict(
                                    [
                                        (
                                            "text",
                                            [
                                                OrderedDict(
                                                    [
                                                        ("type", "paragraph"),
                                                        (
                                                            "text",
                                                            u"This is an unmarked footnote for an anchored/inline table",
                                                        ),
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                )
                            ],
                        ),
                    ]
                )
            ],
        ),
    ]
)
