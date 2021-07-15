from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "journal"),
            ("id", "bib5"),
            ("date", "2012"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", "Baker JL"), ("index", "Baker, JL")]
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
                                    [("preferred", "Wei XF"), ("index", "Wei, XF")]
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
                                    [("preferred", "Ryou JW"), ("index", "Ryou, JW")]
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
                                        ("preferred", "Butson CR"),
                                        ("index", "Butson, CR"),
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
                                        ("preferred", "Schiff ND"),
                                        ("index", "Schiff, ND"),
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
                                        ("preferred", "Purpura KP"),
                                        ("index", "Purpura, KP"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "articleTitle",
                "Modulation of behavior and global brain oscillations with central thalamic deep brain stimulation in the non-human primate",
            ),
            ("journal", "Society for Neuroscience"),
            ("volume", "Abstract 597.14"),
        ]
    )
]
