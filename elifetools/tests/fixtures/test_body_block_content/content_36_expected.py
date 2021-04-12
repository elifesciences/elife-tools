from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "figure"),
        (
            "assets",
            [
                OrderedDict(
                    [
                        ("type", "video"),
                        ("doi", u"10.7554/eLife.00666.038"),
                        ("id", u"video2"),
                        ("label", u"Animation 1"),
                        (
                            "title",
                            u"A demonstration of how to tag an animated gif file to ensure it is autolooped when on the eLife website.",
                        ),
                        ("uri", u"elife-00666-video2.gif"),
                        ("autoplay", True),
                        ("loop", True),
                    ]
                )
            ],
        ),
    ]
)
