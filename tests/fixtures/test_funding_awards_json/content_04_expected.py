# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("id", u"par-1"),
            ("source", OrderedDict([("name", [u"Wellcome Trust"])])),
            ("awardId", u"094874/Z/10/Z"),
            (
                "recipients",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"Jörn Diedrichsen"),
                                        ("index", u"Diedrichsen, Jörn"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
        ]
    ),
    OrderedDict(
        [
            ("id", u"par-3"),
            ("source", OrderedDict([("name", [u"James S McDonnell Foundation"])])),
            ("awardId", u"Understanding Human Cognition Scholar Award 2012"),
            (
                "recipients",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"Jörn Diedrichsen"),
                                        ("index", u"Diedrichsen, Jörn"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
        ]
    ),
]
