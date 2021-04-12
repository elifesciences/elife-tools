from collections import OrderedDict

expected = [
    OrderedDict(
        [
            (
                "content",
                [
                    OrderedDict([("type", "paragraph"), ("text", "content")]),
                    OrderedDict(
                        [
                            ("type", "table"),
                            (
                                "tables",
                                [
                                    "<table><thead><tr><th/></tr></thead><tbody><tr><td/></tr></tbody></table>"
                                ],
                            ),
                        ]
                    ),
                ],
            )
        ]
    )
]
