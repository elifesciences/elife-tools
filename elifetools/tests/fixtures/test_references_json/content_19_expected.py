from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"software"),
            ("id", u"bib55"),
            ("date", u"2014"),
            (
                "authors",
                [OrderedDict([("type", "group"), ("name", u"Schr\xf6dinger, LLC")])],
            ),
            ("title", u"The PyMOL Molecular Graphics System"),
            ("source", u"The PyMOL Molecular Graphics System"),
            ("publisher", OrderedDict([("name", [u"Schrodinger, LLC"])])),
            ("version", u"Version 1.7.2"),
        ]
    )
]
