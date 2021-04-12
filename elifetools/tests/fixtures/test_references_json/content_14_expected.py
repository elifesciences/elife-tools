from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "unknown"),
            ("id", u"bib12"),
            ("date", u"2006"),
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
                                        ("preferred", u"Blench R"),
                                        ("index", u"Blench, R"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("title", u"Archaeology-Language-and-the-African-Past"),
        ]
    )
]
