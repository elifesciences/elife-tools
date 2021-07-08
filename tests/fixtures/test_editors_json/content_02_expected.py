from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Johannes Krause"), ("index", u"Krause, Johannes")]
                ),
            ),
            ("role", u"Reviewing editor"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"University of T\xfcbingen"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Germany"]),
                                        (
                                            "components",
                                            OrderedDict([("country", u"Germany")]),
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
                        ("preferred", u"Nicholas J Conard"),
                        ("index", u"Conard, Nicholas J"),
                    ]
                ),
            ),
            ("role", u"Reviewing editor"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            ("name", [u"University of T\xfcbingen"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Germany"]),
                                        (
                                            "components",
                                            OrderedDict([("country", u"Germany")]),
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
