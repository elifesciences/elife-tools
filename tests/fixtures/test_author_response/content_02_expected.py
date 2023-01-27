from collections import OrderedDict

expected = OrderedDict(
    [
        ("id", "sa5"),
        ("doi", "10.7554/eLife.1234567890.4.sa5"),
        (
            "content",
            [
                OrderedDict(
                    [
                        ("type", "paragraph"),
                        (
                            "text",
                            "We thank the reviewers for the positive assessment of our work and their insightful remarks. Please find below a point-by-point response to each comment.",
                        ),
                    ]
                )
            ],
        ),
    ]
)
