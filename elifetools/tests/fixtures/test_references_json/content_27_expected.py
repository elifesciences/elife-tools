from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"patent"),
            ("id", u"bib32"),
            ("date", u"2011"),
            (
                "inventors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"JB Patterson"),
                                        ("index", u"Patterson, JB"),
                                    ]
                                ),
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
                                        ("preferred", u"DG Lonergan"),
                                        ("index", u"Lonergan, DG"),
                                    ]
                                ),
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
                                        ("preferred", u"GA Flynn"),
                                        ("index", u"Flynn, GA"),
                                    ]
                                ),
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
                                        ("preferred", u"Z Qingpeng"),
                                        ("index", u"Qingpeng, Z"),
                                    ]
                                ),
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
                                        ("preferred", u"PV Pallai"),
                                        ("index", u"Pallai, PV"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "assignees",
                [OrderedDict([("type", "group"), ("name", u"Mankind Corp")])],
            ),
            ("title", u"IRE-1alpha inhibitors"),
            ("patentType", u"United States patent"),
            ("number", u"US20100941530"),
            ("country", u"United States"),
            ("uri", u"http://europepmc.org/patents/PAT/US2011065162"),
        ]
    )
]
