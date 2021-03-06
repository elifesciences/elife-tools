from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "section"),
            ("id", u"s4"),
            ("title", u"Keep this section"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "section"),
                            ("id", u"s4-1-1"),
                            ("title", u"Keep this inner section"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [("type", "paragraph"), ("text", u"Content")]
                                    )
                                ],
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "section"),
                            ("id", u"s4-1-2"),
                            ("title", u"Keep this section too"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", u"More content"),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )
]
