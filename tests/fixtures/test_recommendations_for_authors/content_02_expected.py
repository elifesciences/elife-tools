from collections import OrderedDict

expected = OrderedDict(
    [
        ("title", "Recommendations for authors"),
        ("id", "sa4"),
        ("doi", "10.7554/eLife.1234567890.4.sa4"),
        (
            "content",
            [
                OrderedDict(
                    [
                        ("type", "paragraph"),
                        (
                            "text",
                            "Recommendations for edits to the initial preprint, based on the reviewers' comments.",
                        ),
                    ]
                )
            ],
        ),
    ]
)
