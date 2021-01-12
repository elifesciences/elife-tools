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
                        ("doi", u"10.7554/eLife.00666.024"),
                        ("id", u"fig1"),
                        ("label", u"Figure 1"),
                        ("title", u"Figure title"),
                        (
                            "caption",
                            [
                                OrderedDict(
                                    [("type", "paragraph"), ("text", u"Figure caption")]
                                )
                            ],
                        ),
                        ("image", {"alt": "", "uri": u"elife-00666-fig1-v1.tif"}),
                    ]
                )
            ],
        ),
    ]
)
