# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Randy Schekman"), ("index", u"Schekman, Randy")]
                ),
            ),
            ("orcid", u"0000-0001-8615-6409"),
            ("role", u"Editor-in-Chief"),
            (
                "competingInterests",
                u"Receives funding from the Howard Hughes Medical Institute",
            ),
        ]
    ),
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Mark Patterson"), ("index", u"Patterson, Mark")]
                ),
            ),
            ("orcid", u"0000-0001-7237-0797"),
            ("role", u"Executive Director"),
            ("emailAddresses", [u"m.patterson@elifesciences.org"]),
            ("competingInterests", u"No competing interests declared."),
        ]
    ),
]
