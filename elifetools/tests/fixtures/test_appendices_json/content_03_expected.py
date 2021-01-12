from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"appendix-3"),
            ("title", u"Appendix 3"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                u"This is an example of an appendix with no sections.",
                            ),
                        ]
                    )
                ],
            ),
            ("doi", u"10.7554/eLife.00666.034"),
        ]
    )
]
