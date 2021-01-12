from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "section"),
            ("id", u"s2-6-4"),
            ("title", u"Inline graphics"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                'Here is an example of pulling in an inline graphic <img src="elife-00666-inf001.jpeg"/>.',
                            ),
                        ]
                    )
                ],
            ),
        ]
    )
]
