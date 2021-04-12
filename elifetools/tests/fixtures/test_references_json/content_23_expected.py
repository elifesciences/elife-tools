from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"journal"),
            ("id", u"bib13"),
            ("date", "1996"),
            ("discriminator", "a"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"Castro-Alamancos MA"),
                                        ("index", u"Castro-Alamancos, MA"),
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
                                        ("preferred", u"Connors BW"),
                                        ("index", u"Connors, BW"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "articleTitle",
                u"Cellular mechanisms of the augmenting response: short-term plasticity in a thalamocortical pathway",
            ),
            ("journal", u"Journal of Neuroscience"),
            ("volume", u"16"),
            (
                "pages",
                OrderedDict(
                    [
                        ("first", u"7742"),
                        ("last", u"7756"),
                        ("range", u"7742\u20137756"),
                    ]
                ),
            ),
        ]
    )
]
