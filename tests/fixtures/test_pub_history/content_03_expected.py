from collections import OrderedDict
from elifetools.utils import date_struct


expected = [
    OrderedDict(
        [
            ("event_type", "preprint"),
            ("event_desc", "This manuscript was published as a preprint at bioRxiv."),
            (
                "event_desc_html",
                "This manuscript was published as a preprint at bioRxiv.",
            ),
            ("uri", "https://www.biorxiv.org/content/10.1101/2019.08.22.6666666v1"),
            ("day", "15"),
            ("month", "02"),
            ("year", "2019"),
            (
                "date",
                date_struct(2019, 2, 15),
            ),
            ("iso-8601-date", "2019-02-15"),
        ]
    )
]
