from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "excerpt"),
        (
            "content",
            [
                OrderedDict([("type", "code"), ("code", "<Code>")]),
                OrderedDict(
                    [
                        ("type", "list"),
                        ("prefix", "bullet"),
                        (
                            "items",
                            [
                                [
                                    OrderedDict(
                                        [
                                            ("type", "paragraph"),
                                            ("text", "<i>L. braziliensis</i>"),
                                        ]
                                    )
                                ]
                            ],
                        ),
                    ]
                ),
                OrderedDict(
                    [
                        ("type", "mathml"),
                        (
                            "mathml",
                            "<math>\n&lt;mtext&gt;Body\\u2009Mass&lt;/mtext&gt;\n</math>",
                        ),
                    ]
                ),
                OrderedDict([("type", "paragraph"), ("text", "Paragraph content.")]),
                OrderedDict(
                    [
                        ("type", "table"),
                        (
                            "tables",
                            [
                                "<table>\n<thead>\n<tr>\n<th>\n</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td/>\n</tr>\n</tbody>\n</table>"
                            ],
                        ),
                    ]
                ),
            ],
        ),
    ]
)
