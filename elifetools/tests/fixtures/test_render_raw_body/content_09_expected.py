from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "box"),
            ("id", u"B1"),
            (
                "content",
                [
                    OrderedDict(
                        [("type", "paragraph"), ("text", u"Boxed text with no title")]
                    )
                ],
            ),
        ]
    )
]
