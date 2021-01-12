from collections import OrderedDict

expected = [
    OrderedDict(
        [
            (
                "content",
                [
                    OrderedDict([("type", "paragraph"), ("text", u"This")]),
                    OrderedDict(
                        [
                            ("type", "mathml"),
                            ("id", u"equ2"),
                            ("label", u"(2)"),
                            ("mathml", "<math><mrow/></math>"),
                        ]
                    ),
                    OrderedDict([("type", "paragraph"), ("text", u"was also")]),
                    OrderedDict(
                        [
                            ("type", "figure"),
                            (
                                "assets",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "image"),
                                            ("doi", u"10.7554/eLife.01944.005"),
                                            ("id", u"fig3"),
                                            ("label", u"Figure 3"),
                                            ("title", u"Title"),
                                            (
                                                "caption",
                                                [
                                                    OrderedDict(
                                                        [
                                                            ("type", "paragraph"),
                                                            ("text", u"Caption"),
                                                        ]
                                                    )
                                                ],
                                            ),
                                            (
                                                "image",
                                                {
                                                    "alt": "",
                                                    "uri": u"elife-01944-fig3-v1.tif",
                                                },
                                            ),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                ],
            )
        ]
    )
]
