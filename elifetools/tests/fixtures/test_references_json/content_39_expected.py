from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"periodical"),
            ("id", u"bib40"),
            ("date", u"1993-09-09"),
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
                                        ("preferred", u"Schwartz J"),
                                        ("index", u"Schwartz, J"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("articleTitle", u"Obesity affects economic, social status"),
            ("periodical", u"The Washington Post"),
            (
                "pages",
                OrderedDict(
                    [("first", u"A1"), ("last", u"A4"), ("range", u"A1\u2013A4")]
                ),
            ),
        ]
    )
]
