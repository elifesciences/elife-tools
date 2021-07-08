from collections import OrderedDict

expected = OrderedDict(
    [
        ("doi", u"10.7554/eLife.00070.001"),
        (
            "content",
            [
                OrderedDict([("type", "paragraph"), ("text", u"Paragraph 1")]),
                OrderedDict([("type", "paragraph"), ("text", u"Paragraph 2")]),
            ],
        ),
    ]
)
