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
                        ("id", "fig1video3"),
                        ("label", "Figure 1—Animation 1"),
                        ("title", "Animation associated with a main figure."),
                        (
                            "caption",
                            [
                                OrderedDict(
                                    [
                                        ("type", "paragraph"),
                                        (
                                            "text",
                                            "Note that file naming and ID for videos and animations is sequential regardless of labelling (e.g. videos and animations are counted together).",
                                        ),
                                    ]
                                )
                            ],
                        ),
                        (
                            "attribution",
                            [
                                "© 2004, American Society for Cell Biology, All Rights Reserved. video is reproduced from  with permission. It is not covered by the CC-BY 4.0 licence and further reproduction of this panel would need permission from the copyright holder."
                            ],
                        ),
                    ]
                )
            ],
        ),
    ]
)
