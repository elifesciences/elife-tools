from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"app1"),
            (
                "title",
                u"Appendix 1: Details of the automated linear stability analysis",
            ),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                u"We consider a reaction-diffusion system of the form",
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "mathml"),
                            ("id", u"equ5"),
                            ("label", u"(1)"),
                            (
                                "mathml",
                                '<math><mrow><mi mathvariant="bold">c</mi></mrow></math>',
                            ),
                        ]
                    ),
                    OrderedDict([("type", "paragraph"), ("text", u"where etc.")]),
                    OrderedDict(
                        [
                            ("type", "section"),
                            ("id", u"s16"),
                            ("title", u"Step 1. Possible networks of size ..."),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            (
                                                "text",
                                                u"We first generate a list of possible networks with ...",
                                            ),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            ("text", u"Test another section with no title"),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "section"),
                            ("id", u"test2"),
                            ("title", u"Section with title"),
                            (
                                "content",
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", u"Section content"),
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            ("text", u"Second section with no title"),
                        ]
                    ),
                ],
            ),
        ]
    )
]
