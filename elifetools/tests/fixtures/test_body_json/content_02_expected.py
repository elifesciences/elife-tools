from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "section"),
            ("id", u"s1"),
            (
                "content",
                [
                    OrderedDict([("type", "paragraph"), ("text", u"Paragraph")]),
                    OrderedDict(
                        [
                            ("type", "box"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", "<b>Boxed text</b>"),
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
