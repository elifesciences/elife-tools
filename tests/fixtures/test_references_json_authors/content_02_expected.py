from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", u"patent"),
        (
            "inventors",
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
        ("inventorsEtAl", True),
    ]
)
