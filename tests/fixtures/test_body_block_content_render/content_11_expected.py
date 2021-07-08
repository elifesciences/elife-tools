from collections import OrderedDict

expected = [
    OrderedDict(
        [
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                '<b>This</b> is <a href="#fig3">Figure 3A</a> test',
                            ),
                        ]
                    ),
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
                                                            (
                                                                "text",
                                                                "Caption <b>b</b>",
                                                            ),
                                                        ]
                                                    ),
                                                    OrderedDict(
                                                        [
                                                            ("type", "mathml"),
                                                            ("id", u"equ3"),
                                                            ("label", u"(3)"),
                                                            (
                                                                "mathml",
                                                                "<math><mrow/></math>",
                                                            ),
                                                        ]
                                                    ),
                                                    OrderedDict(
                                                        [
                                                            ("type", "paragraph"),
                                                            (
                                                                "text",
                                                                "where m<sub>i</sub> given by:",
                                                            ),
                                                        ]
                                                    ),
                                                    OrderedDict(
                                                        [
                                                            ("type", "mathml"),
                                                            ("id", u"equ4"),
                                                            ("label", u"(4)"),
                                                            (
                                                                "mathml",
                                                                "<math><mrow/></math>",
                                                            ),
                                                        ]
                                                    ),
                                                    OrderedDict(
                                                        [
                                                            ("type", "paragraph"),
                                                            ("text", u"More caption"),
                                                        ]
                                                    ),
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
