from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"journal"),
            ("id", u"bib32"),
            ("date", u"2012"),
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
                                        ("preferred", u"Kyoung M"),
                                        ("index", u"Kyoung, M"),
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
                                    [("preferred", u"Zhang Y"), ("index", u"Zhang, Y")]
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
                                    [("preferred", u"Diao J"), ("index", u"Diao, J")]
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
                                    [("preferred", u"Chu S"), ("index", u"Chu, S")]
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
                                        ("preferred", u"Brunger AT"),
                                        ("index", u"Brunger, AT"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "articleTitle",
                u"Studying calcium triggered vesicle fusion in a single vesicle content/lipid mixing system",
            ),
            ("journal", u"Nature Protocols"),
            ("volume", u"7"),
            ("pages", "In press"),
            ("uri", u"http://dx.doi.org/10.1038/nprot.2012.134"),
        ]
    )
]
