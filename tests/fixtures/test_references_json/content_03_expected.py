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
                                    [("preferred", u"Feng J"), ("index", u"Feng, J")]
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
                                    [("preferred", u"Liu T"), ("index", u"Liu, T")]
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
                                    [("preferred", u"Zhang Y"), ("index", u"Zhang, Y")]
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
