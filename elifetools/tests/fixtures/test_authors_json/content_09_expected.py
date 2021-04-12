# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Yukiko Eguchi"), ("index", u"Eguchi, Yukiko")]
                ),
            ),
            ("deceased", True),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"National Institute for Basic Biology",
                                    u"National Institutes for Natural Sciences",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Okazaki", u"Japan"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Okazaki"]),
                                                    ("country", u"Japan"),
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
            ("contribution", u"YE, Contributed reagents"),
            (
                "competingInterests",
                u"The authors declare that no competing interests exist.",
            ),
        ]
    )
]
