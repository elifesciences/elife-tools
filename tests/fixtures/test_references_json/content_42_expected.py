from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"data"),
            ("id", u"bib105"),
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
                                    [
                                        ("preferred", u"Steinbaugh MJ"),
                                        ("index", u"Steinbaugh, MJ"),
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
                                        ("preferred", u"Dreyfuss JM"),
                                        ("index", u"Dreyfuss, JM"),
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
                                        ("preferred", u"Blackwell TK"),
                                        ("index", u"Blackwell, TK"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "title",
                u"RNA-seq analysis of germline stem cell removal and loss of SKN-1 in c. elegans",
            ),
            ("source", u"NCBI Gene Expression Omnibus"),
            ("dataId", u"GSE63075"),
            ("uri", u"http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63075"),
        ]
    )
]
