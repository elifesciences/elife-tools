from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "report"),
            ("id", "bib37"),
            ("date", "1985"),
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
                                        ("preferred", "Rumelhart DE"),
                                        ("index", "Rumelhart, DE"),
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
                                        ("preferred", "Hinton GE"),
                                        ("index", "Hinton, GE"),
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
                                        ("preferred", "Williams RJ"),
                                        ("index", "Williams, RJ"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            ("title", "Learning Internal Representations by Error Propagation"),
            ("source", "Learning Internal Representations by Error Propagation"),
            (
                "publisher",
                OrderedDict(
                    [
                        (
                            "name",
                            [
                                "California Univ San Diego La Jolla Inst for Cognitive Science"
                            ],
                        )
                    ]
                ),
            ),
            ("doi", "10.21236/ADA164453"),
            ("uri", "https://doi.org/10.21236/ADA164453"),
        ]
    )
]
