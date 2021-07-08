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
                        ("preferred", u"Silvestro Micera"),
                        ("index", u"Micera, Silvestro"),
                    ]
                ),
            ),
            ("orcid", u"0000-0003-4396-8217"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"The BioRobotics Institute",
                                    u"Scuola Superiore Sant'Anna",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Pisa", u"Italy"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Pisa"]),
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
                                    u"Center for Neuroprosthetics",
                                    u"\xc9cole Polytechnique F\xe9d\xe9rale de Lausanne",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Lausanne", u"Switzerland"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Lausanne"]),
                                                    ("country", u"Switzerland"),
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
                                    u"Bertarelli Foundation Chair in Translational NeuroEngineering, Institute of Bioengineering, School of Engineering",
                                    u"\xc9cole Polytechnique F\xe9d\xe9rale de Lausanne",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Lausanne", u"Switzerland"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Lausanne"]),
                                                    ("country", u"Switzerland"),
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
            (
                "emailAddresses",
                [u"silvestro.micera@epfl.ch", u"silvestro.micera@sssup.it"],
            ),
        ]
    )
]
