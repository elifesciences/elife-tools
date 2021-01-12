from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "figure"),
            (
                "assets",
                [
                    OrderedDict(
                        [
                            ("type", "image"),
                            ("doi", u"10.7554/eLife.06726.003"),
                            ("id", u"fig1"),
                            ("label", u"Figure 1"),
                            ("title", u"Angioblast migration ...."),
                            (
                                "caption",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", u"(<b>A</b>\u2013<b>F</b>)"),
                                        ]
                                    )
                                ],
                            ),
                            (
                                "sourceData",
                                [
                                    OrderedDict(
                                        [
                                            ("doi", u"10.7554/eLife.06726.004"),
                                            ("id", u"SD1-data"),
                                            ("label", u"Figure 1\u2014source movie 1"),
                                            ("title", u"Time-lapse movie ...."),
                                            ("mediaType", u"video/avi"),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "image"),
                            ("doi", u"10.7554/eLife.06726.005"),
                            ("id", u"fig1s1"),
                            ("label", u"Figure 1\u2014figure supplement 1"),
                            ("title", u"Inhibition of Vegfa signaling ...."),
                            (
                                "caption",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", u"(<b>A</b>\u2013<b>J</b>)"),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )
]
