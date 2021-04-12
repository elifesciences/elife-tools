from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"fund1"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100000011"),
                        ("name", [u"Howard Hughes Medical Institute"]),
                    ]
                ),
            ),
            ("awardId", u"F32 GM089018"),
            (
                "recipients",
                [
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
                        ]
                    )
                ],
            ),
        ]
    )
]
