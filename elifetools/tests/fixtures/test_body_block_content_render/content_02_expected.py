from collections import OrderedDict

expected = [
    OrderedDict(
        [
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "box"),
                            ("doi", u"10.7554/eLife.00013.009"),
                            ("id", u"box1"),
                            ("label", u"Box 1"),
                            ("title", u"Box title"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [("type", "paragraph"), ("text", u"content 1")]
                                    ),
                                    OrderedDict(
                                        [("type", "paragraph"), ("text", u"content 2")]
                                    ),
                                ],
                            ),
                        ]
                    )
                ],
            )
        ]
    )
]
