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
                            ("doi", u"10.7554/eLife.05519.003"),
                            ("label", u"Box 1"),
                            ("title", u"Example: Elastomer pump study"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", "<b>Boxed text</b>"),
                                        ]
                                    ),
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", u"Paragraph 2"),
                                        ]
                                    ),
                                ],
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )
]
