from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "software"),
            ("id", "bib61"),
            ("date", "2008"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "group"),
                            ("name", "R Development Core Team, R. F. F. S. C"),
                        ]
                    )
                ],
            ),
            (
                "title",
                "\n<i>R: A Language and Environment for Statistical Computing</i>\n",
            ),
            (
                "publisher",
                OrderedDict(
                    [
                        ("name", ["R Foundation for Statistical Computing"]),
                        (
                            "address",
                            OrderedDict(
                                [
                                    ("formatted", ["Vienna, Austria"]),
                                    (
                                        "components",
                                        OrderedDict(
                                            [("locality", ["Vienna, Austria"])]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            ("doi", "10.1007/978-3-540-74686-7"),
            ('uri', 'https://doi.org/10.1007/978-3-540-74686-7'),
        ]
    )
]
