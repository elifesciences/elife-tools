from collections import OrderedDict

expected = [
    OrderedDict(
        [
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "section"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "box"),
                                            (
                                                "title",
                                                u"Strange content for test coverage",
                                            ),
                                            (
                                                "content",
                                                [
                                                    OrderedDict(
                                                        [
                                                            ("type", "figure"),
                                                            (
                                                                "assets",
                                                                [
                                                                    OrderedDict(
                                                                        [
                                                                            (
                                                                                "type",
                                                                                "table",
                                                                            ),
                                                                            (
                                                                                "label",
                                                                                u"A label",
                                                                            ),
                                                                            (
                                                                                "tables",
                                                                                [],
                                                                            ),
                                                                        ]
                                                                    )
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    OrderedDict([("type", "image")]),
                                                    OrderedDict(
                                                        [
                                                            ("type", "image"),
                                                            (
                                                                "doi",
                                                                u"10.7554/eLife.00666.024",
                                                            ),
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
                ],
            )
        ]
    )
]
