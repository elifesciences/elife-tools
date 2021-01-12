from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Wenying Shou"), ("index", u"Shou, Wenying")]
                ),
            ),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"Fred Hutchinson Cancer Research Center"]),
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
            ("role", u"Reviewing Editor"),
        ]
    )
]
