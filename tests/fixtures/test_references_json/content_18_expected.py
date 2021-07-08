from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "unknown"),
            ("id", u"bib24"),
            ("date", u"1992"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", u"Laue TM"), ("index", u"Laue, TM")]
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
                                    [("preferred", u"Shah BD"), ("index", u"Shah, BD")]
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
                                        ("preferred", u"Ridgeway RM"),
                                        ("index", u"Ridgeway, RM"),
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
                                        ("preferred", u"Pelletier SL"),
                                        ("index", u"Pelletier, SL"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            ("title", u"90\u2013125, Cambridge, The Royal Society of Chemistry"),
            ("details", u"90\u2013125, Cambridge, The Royal Society of Chemistry"),
        ]
    )
]
