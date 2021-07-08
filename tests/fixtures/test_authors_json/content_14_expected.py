# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Randy Schekman"), ("index", u"Schekman, Randy")]
                ),
            ),
            ("role", u"Editor-in-Chief"),
            (
                "biography",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                u"Randy Schekman is eLife's Editor-In-Chief and a Howard Hughes Medical Institute investigator.",
                            ),
                        ]
                    )
                ],
            ),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"Department of Biology",
                                    u"University of North Carolina",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        (
                                            "formatted",
                                            [u"Chapel Hill", u"United States"],
                                        ),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Chapel Hill"]),
                                                    ("country", u"United States"),
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
                "competingInterests",
                u"The other authors declare that no competing interests exist.",
            ),
            ("equalContributionGroups", [1]),
        ]
    )
]
