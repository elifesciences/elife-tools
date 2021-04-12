from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"appendix-1"),
            ("title", u"Appendix 1"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "section"),
                            ("id", u"s8"),
                            ("title", u"Preparation"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", u"Paragraph content."),
                                        ]
                                    )
                                ],
                            ),
                            ("doi", u"10.7554/eLife.00666.023"),
                        ]
                    )
                ],
            ),
        ]
    )
]
