from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "list"),
        ("prefix", "none"),
        (
            "items",
            [
                [OrderedDict([("type", "paragraph"), ("text", u"List paragraph one")])],
                [OrderedDict([("type", "paragraph"), ("text", u"List paragraph two")])],
            ],
        ),
    ]
)
