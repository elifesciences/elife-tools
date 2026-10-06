from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", "Melissa Harrison"), ("index", "Harrison, Melissa")]
                ),
            ),
            ("role", "Senior Editor"),
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
                                        ("formatted", ["United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [("country", "United Kingdom")]
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
                    [("preferred", "Andy Collings"), ("index", "Collings, Andy")]
                ),
            ),
            ("role", "Reviewing Editor"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", ["eLife Sciences"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", ["United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [("country", "United Kingdom")]
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
                        ("preferred", "Simone de Beauvoir"),
                        ("index", "de Beauvoir, Simone"),
                    ]
                ),
            ),
            ("role", "Reviewer"),
        ]
    ),
]
