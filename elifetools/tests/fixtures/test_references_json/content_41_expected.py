from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"book"),
            ("id", u"bib10"),
            ("date", u"1998"),
            (
                "editors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"J Ekstrom"),
                                        ("index", u"Ekstrom, J"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"J. R Garrett"),
                                        ("index", u"Garrett, J. R"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"L. C Anderson"),
                                        ("index", u"Anderson, L. C"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "bookTitle",
                u"Glandular Mechanisms of Salivary Secretion (Frontiers of Oral Biology , Vol. 10)",
            ),
            (
                "publisher",
                OrderedDict(
                    [
                        ("name", [u"S Karger"]),
                        (
                            "address",
                            OrderedDict(
                                [
                                    ("formatted", [u"Basel"]),
                                    (
                                        "components",
                                        OrderedDict([("locality", [u"Basel"])]),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            ("edition", u"1st edn"),
            ("isbn", u"978-3805566308"),
        ]
    )
]
