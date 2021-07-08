from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", u"thesis"),
        (
            "author",
            OrderedDict(
                [
                    ("type", "person"),
                    (
                        "name",
                        OrderedDict(
                            [("preferred", "One Person"), ("index", "One, Person")]
                        ),
                    ),
                ]
            ),
        ),
    ]
)
