from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "unknown"),
            ("id", u"bib42"),
            ("date", u"2015"),
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
                                        ("preferred", u"World Health Organization"),
                                        ("index", u"World Health Organization"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("title", u"WHO Glocal Tuberculosis Report 2015"),
            ("details", u"WHO Glocal Tuberculosis Report 2015"),
        ]
    )
]
