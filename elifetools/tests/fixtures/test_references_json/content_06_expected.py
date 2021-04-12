from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"journal"),
            ("id", u"bib12"),
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
                                        ("preferred", u"Culumber ZW"),
                                        ("index", u"Culumber, ZW"),
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
                                        ("preferred", u"Ochoa OM"),
                                        ("index", u"Ochoa, OM"),
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
                                        ("preferred", u"Rosenthal GG"),
                                        ("index", u"Rosenthal, GG"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "articleTitle",
                u"Assortative mating and the maintenance of population structure in a natural hybrid zone",
            ),
            ("journal", u"American Naturalist"),
            ("pages", "In press"),
        ]
    )
]
