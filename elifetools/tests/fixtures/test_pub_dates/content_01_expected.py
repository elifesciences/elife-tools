from collections import OrderedDict
from elifetools.utils import date_struct

expected = [
    OrderedDict(
        [
            ("publication-format", u"electronic"),
            ("date-type", u"update"),
            ("day", u"11"),
            ("month", u"08"),
            ("year", u"2016"),
            (u"date", date_struct(2016, 8, 11)),
        ]
    ),
    OrderedDict(
        [
            ("publication-format", u"electronic"),
            ("date-type", u"publication"),
            ("day", u"25"),
            ("month", u"04"),
            ("year", u"2016"),
            (u"date", date_struct(2016, 4, 25)),
        ]
    ),
    OrderedDict(
        [
            ("pub-type", u"collection"),
            ("day", None),
            ("month", None),
            ("year", u"2016"),
            (u"date", date_struct(2016, 1, 1)),
        ]
    ),
]
