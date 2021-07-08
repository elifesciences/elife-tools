from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", u"clinical-trial"),
        (
            "authors",
            [
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
                )
            ],
        ),
        ("authorsEtAl", True),
        ("authorsType", "sponsors"),
    ]
)
