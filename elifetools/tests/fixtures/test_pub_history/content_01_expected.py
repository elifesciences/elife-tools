from collections import OrderedDict
from elifetools.utils import date_struct


expected = [
    OrderedDict(
        [
            ("event_type", "preprint-publication"),
            (
                "event_desc",
                'This article was originally published as a <ext-link ext-link-type="uri" xlink:href="https://www.biorxiv.org/content/early/2017/03/24/118356">preprint on bioRxiv</ext-link>',
            ),
            (
                "event_desc_html",
                'This article was originally published as a <a href="https://www.biorxiv.org/content/early/2017/03/24/118356">preprint on bioRxiv</a>',
            ),
            ("uri", "https://www.biorxiv.org/content/early/2017/03/24/118356"),
            ("uri_text", "preprint on bioRxiv"),
            ("day", "24"),
            ("month", "03"),
            ("year", "2017"),
            ("date", date_struct(2017, 3, 24)),
            ("iso-8601-date", "2017-03-24"),
        ]
    )
]
