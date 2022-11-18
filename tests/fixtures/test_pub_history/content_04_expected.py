from collections import OrderedDict
from elifetools.utils import date_struct

expected = [
    OrderedDict(
        [
            ("event_type", "preprint"),
            ("event_desc", "This manuscript was published as a preprint."),
            ("event_desc_html", "This manuscript was published as a preprint."),
            ("uri", "https://doi.org/10.1101/2021.11.09.467796"),
            ("day", "15"),
            ("month", "02"),
            ("year", "2023"),
            (
                "date",
                date_struct(2023, 2, 15),
            ),
            ("iso-8601-date", "2023-02-15"),
        ]
    ),
    OrderedDict(
        [
            ("event_type", "reviewed-preprint"),
            ("event_desc", "This manuscript was published as a reviewed preprint."),
            (
                "event_desc_html",
                "This manuscript was published as a reviewed preprint.",
            ),
            ("uri", "https://doi.org/10.7554/eLife.1234567890.1"),
            ("day", "15"),
            ("month", "04"),
            ("year", "2023"),
            (
                "date",
                date_struct(2023, 4, 15),
            ),
            ("iso-8601-date", "2023-04-15"),
        ]
    ),
    OrderedDict(
        [
            ("event_type", "reviewed-preprint"),
            ("event_desc", "The reviewed preprint was revised."),
            ("event_desc_html", "The reviewed preprint was revised."),
            ("uri", "https://doi.org/10.7554/eLife.1234567890.2"),
            ("day", "10"),
            ("month", "09"),
            ("year", "2023"),
            (
                "date",
                date_struct(2023, 9, 10),
            ),
            ("iso-8601-date", "2023-09-10"),
        ]
    ),
    OrderedDict(
        [
            ("event_type", "reviewed-preprint"),
            ("event_desc", "The reviewed preprint was revised."),
            ("event_desc_html", "The reviewed preprint was revised."),
            ("uri", "https://doi.org/10.7554/eLife.1234567890.3"),
            ("day", "10"),
            ("month", "11"),
            ("year", "2023"),
            (
                "date",
                date_struct(2023, 11, 10),
            ),
            ("iso-8601-date", "2023-11-10"),
        ]
    ),
]
