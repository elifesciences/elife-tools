from collections import OrderedDict

expected = OrderedDict(
    [
        ("title", "eLife assessment"),
        ("id", "sa0"),
        ("doi", "10.7554/eLife.1234567890.4.sa0"),
        (
            "content",
            [
                OrderedDict(
                    [
                        ("type", "paragraph"),
                        (
                            "text",
                            'This is an eLife assessment, which is a summary of the peer reviews provided by the BRE. It will only contain one or more paragraphs, no figures, tables or videos. It might say something like, "with respect to blah blah, this study is <b>valuable</b> backed up by data that is <b>compelling</b>, however the model design for blah is only <b>useful</b> and the evidence <b>incomplete</b>.',
                        ),
                    ]
                )
            ],
        ),
        ("significance", ["valuable", "useful"]),
        ("strength", ["compelling", "incomplete"]),
    ]
)
