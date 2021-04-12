from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"par-1"),
            ("source", OrderedDict([("name", [u"Laura and John Arnold foundation"])])),
            (
                "recipients",
                [
                    OrderedDict(
                        [
                            ("type", "group"),
                            ("name", u"Reproducibility Project: Cancer Biology"),
                        ]
                    )
                ],
            ),
        ]
    )
]
