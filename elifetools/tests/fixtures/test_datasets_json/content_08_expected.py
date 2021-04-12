from collections import OrderedDict

expected = OrderedDict(
    [
        (
            "availability",
            [
                OrderedDict(
                    [
                        ("type", "paragraph"),
                        (
                            "text",
                            u'A data availability statement will generally describe how the authors have provided the source data for their work. This can list the source data files accompanying their figures, supplementary files, and/or external dataasets. Hyperlinks can be included here, for example: <a href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE102999">https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE102999</a>',
                        ),
                    ]
                )
            ],
        ),
        (
            "generated",
            [
                OrderedDict(
                    [
                        ("id", u"dataset1"),
                        ("date", u"2018"),
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
                                                    ("preferred", u"D\xfcsterwald KM"),
                                                    ("index", u"D\xfcsterwald, KM"),
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
                                                    ("preferred", u"Currin CB"),
                                                    ("index", u"Currin, CB"),
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
                                                    ("preferred", u"Burman RJ"),
                                                    ("index", u"Burman, RJ"),
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
                                                    ("preferred", u"Akerman CJ"),
                                                    ("index", u"Akerman, CJ"),
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
                                                    ("preferred", u"Kay AR"),
                                                    ("index", u"Kay, AR"),
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
                                                    ("preferred", u"Raimondo JV"),
                                                    ("index", u"Raimondo, JV"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        ("title", u"Dryad Digital Repository"),
                        (
                            "details",
                            u"Data from: Biophysical models reveal the relative importance of transporter proteins and impermeant anions in chloride homeostasis",
                        ),
                        ("doi", u"10.5061/dryad.kj1f3v4"),
                        ("assigningAuthority", u"Dryad"),
                    ]
                )
            ],
        ),
        (
            "used",
            [
                OrderedDict(
                    [
                        ("id", u"dataset2"),
                        ("date", u"2013"),
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
                                                    ("preferred", u"Rau CD"),
                                                    ("index", u"Rau, CD"),
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
                                                    ("preferred", u"Wang J"),
                                                    ("index", u"Wang, J"),
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
                                                    ("preferred", u"Wang Y"),
                                                    ("index", u"Wang, Y"),
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
                                                    ("preferred", u"Lusis AJ"),
                                                    ("index", u"Lusis, AJ"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        ("title", u"NCBI Gene Expression Omnibus"),
                        (
                            "details",
                            u"Transcriptomes of the hybrid mouse diversity panel subjected to Isoproterenol challenge",
                        ),
                        (
                            "uri",
                            u"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE48760",
                        ),
                        ("dataId", u"GSE48760"),
                        ("assigningAuthority", u"NCBI"),
                    ]
                ),
                OrderedDict(
                    [
                        ("id", u"dataset3"),
                        ("date", u"2018"),
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
                                                    ("preferred", u"Garcia Miguel A"),
                                                    ("index", u"Garcia, Miguel A"),
                                                ]
                                            ),
                                        ),
                                    ]
                                )
                            ],
                        ),
                        ("title", u"Open Science Framework"),
                        ("details", u"Shear Manuscript"),
                        ("uri", u"https://osf.io/kvu5j/"),
                        ("assigningAuthority", u"other"),
                    ]
                ),
            ],
        ),
    ]
)
