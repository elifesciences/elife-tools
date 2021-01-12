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
                                        ("preferred", u"ZW Culumber"),
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
                                        ("preferred", u"OM Ochoa"),
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
                                        ("preferred", u"GG Rosenthal"),
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
