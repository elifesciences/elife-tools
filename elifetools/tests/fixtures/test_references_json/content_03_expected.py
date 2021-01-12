from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"journal"),
            ("id", u"bib14"),
            ("date", u"2011"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", u"J Feng"), ("index", u"Feng, J")]
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
                                    [("preferred", u"T Liu"), ("index", u"Liu, T")]
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
                                    [("preferred", u"Y Zhang"), ("index", u"Zhang, Y")]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            ("articleTitle", u"Using MACS to identify peaks from ChIP-Seq data"),
            ("journal", u"Curr Protoc Bioinformatics"),
            ("volume", u"Chapter 2"),
            ("pages", u"Unit 2.14"),
        ]
    )
]
