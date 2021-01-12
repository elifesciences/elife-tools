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
                                        ("preferred", u"DM Cutler"),
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
                                        ("preferred", u"AS Deaton"),
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
                                        ("preferred", u"A Lleras-Muney"),
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
