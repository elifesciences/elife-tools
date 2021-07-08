# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"par-1"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100006978"),
                        (
                            "name",
                            [
                                u"University of California Berkeley (University of California, Berkeley)"
                            ],
                        ),
                    ]
                ),
            ),
            ("awardId", u"AWS in Education grant"),
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
                                        ("preferred", u"Eric Jonas"),
                                        ("index", u"Jonas, Eric"),
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
            ("id", u"par-2"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100000001"),
                        ("name", [u"National Science Foundation"]),
                    ]
                ),
            ),
            ("awardId", u"NSF CISE Expeditions Award CCF-1139158"),
            (
                "recipients",
                [
                    {
                        "type": "person",
                        "name": {"index": "Jonas, Eric", "preferred": "Eric Jonas"},
                    }
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("id", u"par-3"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100006235"),
                        ("name", [u"Lawrence Berkely National Laboratory"]),
                    ]
                ),
            ),
            ("awardId", u"Award 7076018"),
            (
                "recipients",
                [
                    {
                        "type": "person",
                        "name": {"index": "Jonas, Eric", "preferred": "Eric Jonas"},
                    }
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("id", u"par-4"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100000185"),
                        ("name", [u"Defense Advanced Research Projects Agency"]),
                    ]
                ),
            ),
            ("awardId", u"XData Award FA8750-12-2-0331"),
            (
                "recipients",
                [
                    {
                        "type": "person",
                        "name": {"index": "Jonas, Eric", "preferred": "Eric Jonas"},
                    }
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("id", u"par-5"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100000002"),
                        ("name", [u"National Institutes of Health"]),
                    ]
                ),
            ),
            ("awardId", u"R01NS074044"),
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
                                        ("preferred", u"Konrad Kording"),
                                        ("index", u"Kording, Konrad"),
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
            ("id", u"par-6"),
            (
                "source",
                OrderedDict(
                    [
                        ("funderId", u"10.13039/100000002"),
                        ("name", [u"National Institutes of Health"]),
                    ]
                ),
            ),
            ("awardId", u"R01NS063399"),
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
                                        ("preferred", u"Konrad Kording"),
                                        ("index", u"Kording, Konrad"),
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
