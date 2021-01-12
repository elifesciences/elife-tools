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
                                [("preferred", "Person One"), ("index", "One, Person")]
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
