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
                        ("preferred", u"Melissa Harrison Jnr"),
                        ("index", u"Harrison, Melissa, Jnr"),
                    ]
                ),
            ),
            ("orcid", u"0000-0003-3523-4408"),
            ("deceased", True),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"Department of Production", u"eLife"]),
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
            (
                "additionalInformation",
                [
                    u'This footnote text must work in isolation as nothing is processed on the html view to make it "work"'
                ],
            ),
            ("emailAddresses", [u"m.harrison@elifesciences.org"]),
            (
                "contribution",
                u"Completed the XML mapping exercise and wrote this XML example",
            ),
            ("competingInterests", u"Chair of JATS4R"),
            ("equalContributionGroups", [1]),
            (
                "postalAddresses",
                [
                    OrderedDict(
                        [
                            (
                                "formatted",
                                [
                                    u"Department of Wellcome Trust, Sanger Institute, London, United Kingdom"
                                ],
                            ),
                            (
                                "components",
                                OrderedDict(
                                    [
                                        (
                                            "streetAddress",
                                            [
                                                u"Department of Wellcome Trust, Sanger Institute, London, United Kingdom"
                                            ],
                                        )
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
        ]
    )
]
