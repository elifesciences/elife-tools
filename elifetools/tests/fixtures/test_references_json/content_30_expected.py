from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"journal"),
            ("id", u"bib6"),
            ("date", u"2015"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", u"J Berni"), ("index", u"Berni, J")]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            (
                "articleTitle",
                u"Genetic dissection of a regionally differentiated network for exploratory behavior in Drosophila larvae",
            ),
            ("journal", u"Current Biology"),
            ("volume", u"25"),
            (
                "pages",
                OrderedDict(
                    [
                        ("first", u"1319"),
                        ("last", u"1326"),
                        ("range", u"1319\u20131326"),
                    ]
                ),
            ),
            ("doi", u"10.1016/j.cub.2015.03.023"),
            ("pmid", 25959962),
        ]
    )
]
