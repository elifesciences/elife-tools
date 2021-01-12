# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [
                        ("preferred", u"Rafael Edgardo Carazo Salas"),
                        ("index", u"Carazo Salas, Rafael Edgardo"),
                    ]
                ),
            ),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"the Gurdon Institute and the Genetics Department",
                                    u"University of Cambridge",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        (
                                            "formatted",
                                            [u"Cambridge", u"United Kingdom"],
                                        ),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Cambridge"]),
                                                    ("country", u"United Kingdom"),
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
            ("emailAddresses", [u"cre20@cam.ac.uk"]),
            ("equalContributionGroups", [1]),
        ]
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [
                        ("preferred", u"Attila Csik\xe1sz-Nagy"),
                        ("index", u"Csik\xe1sz-Nagy, Attila"),
                    ]
                ),
            ),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"Department of Computational Biology",
                                    u"Fondazione Edmund Mach",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        (
                                            "formatted",
                                            [u"San Michele all\u2019Adige", u"Italy"],
                                        ),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    (
                                                        "locality",
                                                        [u"San Michele all\u2019Adige"],
                                                    ),
                                                    ("country", u"Italy"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"the Randall Division of Cell and Molecular Biophysics and Institute of Mathematical and Molecular Biomedicine",
                                    u"King\u2019s College London",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"London", u"United Kingdom"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"London"]),
                                                    ("country", u"United Kingdom"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            ("emailAddresses", [u"attila.csikasz-nagy@fmach.it"]),
            ("equalContributionGroups", [1]),
        ]
    ),
]
