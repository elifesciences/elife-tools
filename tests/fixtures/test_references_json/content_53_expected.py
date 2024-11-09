from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "data"),
            ("id", "bib8"),
            ("date", "2015"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", "Kok K"), ("index", "Kok, K")]
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
                                    [("preferred", "Ay A"), ("index", "Ay, A")]
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
                                    [("preferred", "Li L"), ("index", "Li, L")]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            ("title", "Genome-wide errant targeting by Hairy"),
            ("source", "Dryad Digital Repository"),
            ("specificUse", "analyzed"),
            ("doi", "10.5061/dryad.cv323"),
            ("uri", "https://doi.org/10.5061/dryad.cv323"),
        ]
    ),
    OrderedDict(
        [
            ("type", "data"),
            ("id", "bib5"),
            ("date", "2020"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", "Hao Q"), ("index", "Hao, Q")]
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
                                        ("preferred", "Prasanth KV"),
                                        ("index", "Prasanth, KV"),
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
                                    [("preferred", "Sun Q"), ("index", "Sun, Q")]
                                ),
                            ),
                        ]
                    ),
                ],
            ),
            (
                "title",
                "poly A+ RNA sequencing of cell cycle-synchronized RNA from U2OS cells",
            ),
            ("source", "NCBI Gene Expression Omnibus"),
            ("dataId", "GSE143275"),
            ("specificUse", "generated"),
            ("uri", "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE143275"),
        ]
    ),
]
