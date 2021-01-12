from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Achim Kramer"), ("index", u"Kramer, Achim")]
                ),
            ),
            ("role", u"Reviewing editor"),
        ]
    )
]
