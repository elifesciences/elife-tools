from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("title", "Reviewer #1 (public review)"),
            ("id", "sa1"),
            ("doi", "10.7554/eLife.1234567890.4.sa1"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                "Reviewer #1: Each reviewer's report is included as a separate sub-article. This will usually mean three reviews, though more or fewer are permitted. Reviews may be published anonymously.",
                            ),
                        ]
                    )
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("title", "Reviewer #2 (public review)"),
            ("id", "sa2"),
            ("doi", "10.7554/eLife.1234567890.4.sa2"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                "Reviewer #2: Each reviewer's report is included as a separate sub-article. This will usually mean three reviews, though more or fewer are permitted. Reviews may be published anonymously.",
                            ),
                        ]
                    )
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("title", "Reviewer #3 (public review)"),
            ("id", "sa3"),
            ("doi", "10.7554/eLife.1234567890.4.sa3"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                "Reviewer #3: Each reviewer's report is included as a separate sub-article. This will usually mean three reviews, though more or fewer are permitted. Reviews may be published anonymously.",
                            ),
                        ]
                    )
                ],
            ),
        ]
    ),
]
