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
                            ("doi", u"10.7554/eLife.00666.011"),
                            ("id", u"fig3"),
                            ("label", u"Figure 3"),
                            (
                                "title",
                                'Figure with figure supplements and figure supplement with source data and a video (see <a href="#bib25">Koch, 1959</a>) .',
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "image"),
                            ("doi", u"10.7554/eLife.00666.012"),
                            ("id", u"fig3s1"),
                            ("label", u"Figure 3\u2014figure supplement 1"),
                            ("title", u"Title of the figure supplement"),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "video"),
                            ("doi", u"10.7554/eLife.00666.035"),
                            ("id", u"fig3video1"),
                            ("label", u"Figure 3\u2014Video 1"),
                            (
                                "title",
                                u" A description of the eLife editorial process. ",
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )
]
