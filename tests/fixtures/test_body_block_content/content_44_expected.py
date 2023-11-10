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
                        ("id", "video2"),
                        ("label", "Animation 1"),
                        (
                            "title",
                            "A demonstration of how to tag an mp4 animation file to ensure it is autolooped when on the eLife website.",
                        ),
                        ("uri", "elife-1234567890-video2.mp4"),
                        ("autoplay", True),
                        ("loop", True),
                    ]
                )
            ],
        ),
    ]
)
