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
                        ("doi", u"10.7554/eLife.00013.011"),
                        ("id", u"tbl2"),
                        ("label", u"Table 2"),
                        (
                            "caption",
                            [
                                OrderedDict(
                                    [
                                        ("type", "paragraph"),
                                        (
                                            "text",
                                            u'Caption <a href="#tblfn2">*</a>content',
                                        ),
                                    ]
                                )
                            ],
                        ),
                        (
                            "tables",
                            [
                                '<table><thead><tr><th>Species</th><th>Reference<a href="#tblfn3">*</a></th></tr></thead><tbody><tr><td><i>Algoriphagus machipongonensis</i> PR1</td><td><a href="#bib3">Alegado et al. (2012)</a></td></tr></tbody></table>'
                            ],
                        ),
                        (
                            "footnotes",
                            [
                                OrderedDict(
                                    [
                                        ("id", u"tblfn1"),
                                        ("label", u"*"),
                                        (
                                            "text",
                                            [
                                                OrderedDict(
                                                    [
                                                        ("type", "paragraph"),
                                                        ("text", u"Footnote 1"),
                                                    ]
                                                )
                                            ],
                                        ),
                                    ]
                                ),
                                OrderedDict(
                                    [
                                        ("id", u"tblfn3"),
                                        ("label", u"\xa7"),
                                        (
                                            "text",
                                            [
                                                OrderedDict(
                                                    [
                                                        ("type", "paragraph"),
                                                        (
                                                            "text",
                                                            u"CM = conditioned medium;",
                                                        ),
                                                    ]
                                                )
                                            ],
                                        ),
                                    ]
                                ),
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
                                                            u"MP, Middle Pleistocene.",
                                                        ),
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
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
                                                            u"Footnote parsed with no id",
                                                        ),
                                                    ]
                                                )
                                            ],
                                        )
                                    ]
                                ),
                            ],
                        ),
                    ]
                )
            ],
        ),
    ]
)
