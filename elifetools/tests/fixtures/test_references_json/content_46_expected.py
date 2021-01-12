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
                                        ("preferred", "DE Rumelhart"),
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
                                        ("preferred", "GE Hinton"),
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
                                        ("preferred", "RJ Williams"),
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
