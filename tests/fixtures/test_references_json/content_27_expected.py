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
                                        ("preferred", u"Patterson JB"),
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
                                        ("preferred", u"Lonergan DG"),
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
                                        ("preferred", u"Flynn GA"),
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
                                        ("preferred", u"Qingpeng Z"),
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
                                        ("preferred", u"Pallai PV"),
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
