from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [
                        ("preferred", u"Melissa Harrison"),
                        ("index", u"Harrison, Melissa"),
                    ]
                ),
            ),
            ("role", u"Senior Editor"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"eLife"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [("country", u"United Kingdom")]
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
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Andy Collings"), ("index", u"Collings, Andy")]
                ),
            ),
            ("role", u"Reviewing Editor"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"eLife Sciences"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [("country", u"United Kingdom")]
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
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [
                        ("preferred", u"Corinna Darian-Smith"),
                        ("index", u"Darian-Smith, Corinna"),
                    ]
                ),
            ),
            ("role", u"Reviewer"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"Stanford University"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"United States"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [("country", u"United States")]
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
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Alison M. Smith"), ("index", u"Smith, Alison M.")]
                ),
            ),
            ("role", u"Reviewer"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"John Innes Centre"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [("country", u"United Kingdom")]
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
    ),
]
