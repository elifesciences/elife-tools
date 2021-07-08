from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "figure"),
        (
            "assets",
            [
                OrderedDict(
                    [
                        ("type", "image"),
                        ("doi", u"10.7554/eLife.00666.012"),
                        ("id", u"fig3s1"),
                        ("label", u"Figure 3\u2014figure supplement 1"),
                        ("title", u"Title of the figure supplement"),
                        (
                            "image",
                            {"alt": "", "uri": u"elife-00666-fig3-figsupp1-v1.tiff"},
                        ),
                        (
                            "sourceData",
                            [
                                OrderedDict(
                                    [
                                        ("doi", u"10.7554/eLife.00666.013"),
                                        ("id", u"SD1-data"),
                                        (
                                            "label",
                                            u"Figure 3\u2014figure supplement 1\u2014Source data 1",
                                        ),
                                        (
                                            "title",
                                            u"Title of the figure supplement source data.",
                                        ),
                                        (
                                            "caption",
                                            [
                                                OrderedDict(
                                                    [
                                                        ("type", "paragraph"),
                                                        (
                                                            "text",
                                                            u"Legend of the figure supplement source data.",
                                                        ),
                                                    ]
                                                )
                                            ],
                                        ),
                                        ("mediaType", u"application/xlsx"),
                                        (
                                            "uri",
                                            u"elife-00666-fig3-figsupp1-data1-v1.xlsx",
                                        ),
                                        (
                                            "filename",
                                            u"elife-00666-fig3-figsupp1-data1-v1.xlsx",
                                        ),
                                    ]
                                )
                            ],
                        ),
                    ]
                )
            ],
        ),
    ]
)
