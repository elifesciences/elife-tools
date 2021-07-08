from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "unknown"),
            ("id", u"bib11"),
            ("date", u"2006"),
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
                                        ("preferred", u"Cutler DM"),
                                        ("index", u"Cutler, DM"),
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
                                        ("preferred", u"Deaton AS"),
                                        ("index", u"Deaton, AS"),
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
                                        ("preferred", u"Lleras-Muney A"),
                                        ("index", u"Lleras-Muney, A"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            ("title", u"The determinants of mortality (No. w11963)"),
            ("details", u"Cambridge, National Bureau of Economic Research"),
        ]
    )
]
