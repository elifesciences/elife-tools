from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "excerpt"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                "2) The competition term χ <sub>i</sub> requires renormalization, ... such as",
                            ),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "mathml"),
                            ("id", u"equ2"),
                            ("label", u"(2)"),
                            ("mathml", "<math><mrow/></math>"),
                        ]
                    ),
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            ("text", "which does not need renormalization."),
                        ]
                    ),
                ],
            ),
        ]
    )
]
