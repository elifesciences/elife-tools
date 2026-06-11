from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [
                        ("preferred", "Frederick Peter Atherden III"),
                        ("index", "Atherden, Frederick Peter, III"),
                    ]
                ),
            ),
            ("orcid", "0000-0002-6048-1470"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", ["The department of production, eLife Sciences"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", ["Cambridge", "United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", ["Cambridge"]),
                                                    ("country", "United Kingdom"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("emailAddresses", ["f.atherden@elifesciences.org"]),
            (
                "contribution",
                "Conceptualization, Data curation, Formal analysis, Validation, Investigation, Visualization, Methodology, Writing - original draft",
            ),
            (
                "competingInterests",
                "is a member of some group, and has shares in some company. No other competing interests to declare",
            ),
            ("equalContributionGroups", [1]),
        ]
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", "Melissa Harrison"), ("index", "Harrison, Melissa")]
                ),
            ),
            ("orcid", "0000-0002-4932-938X"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", ["The department of production, eLife Sciences"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", ["Cambridge", "United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", ["Cambridge"]),
                                                    ("country", "United Kingdom"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("emailAddresses", ["...@elifesciences.org"]),
            (
                "contribution",
                "Conceptualization, Resources, Supervision, Funding acquisition, Validation, Writing – review and editing",
            ),
            ("competingInterests", "No competing interests declared"),
            ("equalContributionGroups", [1]),
        ]
    ),
    OrderedDict(
        [
            ("type", "group"),
            ("name", "Example Group author"),
            ("emailAddresses", ["...@elifesciences.org"]),
            (
                "contribution",
                "Resources, Methodology, Group atuhor contributions may break-down contribution per author in some cases",
            ),
            ("competingInterests", "No competing interests declared"),
            (
                "people",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", "James Gilbert"),
                                        ("index", "Gilbert, James"),
                                    ]
                                ),
                            ),
                            ("orcid", "0000-1002-4932-938X"),
                            (
                                "affiliations",
                                [
                                    OrderedDict(
                                        [
                                            ("name", ["eLife"]),
                                            (
                                                "address",
                                                OrderedDict(
                                                    [
                                                        (
                                                            "formatted",
                                                            [
                                                                "Cambridge",
                                                                "United Kingdom",
                                                            ],
                                                        ),
                                                        (
                                                            "components",
                                                            OrderedDict(
                                                                [
                                                                    (
                                                                        "locality",
                                                                        ["Cambridge"],
                                                                    ),
                                                                    (
                                                                        "country",
                                                                        "United Kingdom",
                                                                    ),
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    )
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict([("preferred", "Santa Claus"), ("index", "Claus, Santa")]),
            ),
            ("deceased", True),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", ["The department of production, eLife Sciences"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", ["Cambridge", "United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", ["Cambridge"]),
                                                    ("country", "United Kingdom"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            (
                "contribution",
                "Resources, Supervision, Writing – review and editing, Free text contribution",
            ),
            ("competingInterests", "No competing interests declared"),
            ("equalContributionGroups", [2]),
        ]
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", "Cornel West Jnr"), ("index", "West, Cornel, Jnr")]
                ),
            ),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", ["JATS4R"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", ["Bethesda", "United States"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", ["Bethesda"]),
                                                    ("country", "United States"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            (
                "contribution",
                "Resources, Supervision, Writing – review and editing, Free text contribution",
            ),
            ("competingInterests", "No competing interests declared"),
            ("equalContributionGroups", [2]),
        ]
    ),
    OrderedDict(
        [
            ("type", "on-behalf-of"),
            ("onBehalfOf", "on behalf of whoever finds this interesting"),
        ]
    ),
]
