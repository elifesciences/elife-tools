from collections import OrderedDict

expected = [
    {
        "id": "fn1-1",
        "title": "1.",
        "type": "section",
        "content": [OrderedDict([("type", "paragraph"), ("text", "First footnote.")])],
    },
    {
        "id": "fn1-2",
        "title": "2.",
        "type": "section",
        "content": [
            OrderedDict(
                [
                    ("type", "paragraph"),
                    (
                        "text",
                        "See abstract in <i>Econometrica</i>, XXIV (July I956); I. Blumen, M. Kogan, and J. McCarthy.",
                    ),
                ]
            )
        ],
    },
]
