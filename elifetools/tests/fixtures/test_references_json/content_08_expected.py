from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"web"),
            ("id", u"bib45"),
            ("date", u"2014"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"Mikheyev AS"),
                                        ("index", u"Mikheyev, AS"),
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
                                        ("preferred", u"Linksvayer TA"),
                                        ("index", u"Linksvayer, TA"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "title",
                u"Data from: genes associated with ant social behavior show distinct transcriptional and evolutionary patterns",
            ),
            ("website", u"Dryad Digital Repository."),
            ("uri", u"https://doi.org/10.5061/dryad.cv0q3"),
        ]
    )
]
