from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"book"),
            ("id", u"bib18"),
            ("date", u"2013"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", u"Fung YC"), ("index", u"Fung, YC")]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("bookTitle", u"Biomechanics: Mechanical Properties of Living Tissues"),
            (
                "publisher",
                OrderedDict(
                    [
                        ("name", [u"Springer Science & Business Media"]),
                        (
                            "address",
                            OrderedDict(
                                [
                                    ("formatted", [u"New York"]),
                                    (
                                        "components",
                                        OrderedDict([("locality", [u"New York"])]),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            ("isbn", u"978-1-4757-2257-4"),
        ]
    )
]
