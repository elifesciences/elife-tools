from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "journal"),
            ("id", "bib17"),
            ("date", "2012"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", "Gall A"), ("index", "Gall, A")]
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
                                        ("preferred", "Treuting P"),
                                        ("index", "Treuting, P"),
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
                                    [("preferred", "Elkon KB"), ("index", "Elkon, KB")]
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
                                    [("preferred", "Loo YM"), ("index", "Loo, YM")]
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
                                        ("preferred", "Gale M Jnr"),
                                        ("index", "Gale, M, Jnr"),
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
                                        ("preferred", "Barber GN"),
                                        ("index", "Barber, GN"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "articleTitle",
                "Autoimmunity initiates in nonhematopoietic cells and progresses via lymphocytes in an interferon-dependent autoimmune disease",
            ),
            ("journal", "Immunity"),
            ("volume", "36"),
            (
                "pages",
                OrderedDict([("first", "120"), ("last", "131"), ("range", "120–131")]),
            ),
            ("doi", "10.1016/j.immuni.2011.11.018"),
            ("pmid", 22284419),
        ]
    )
]
