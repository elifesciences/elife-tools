# coding=utf-8
from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "person"),
            (
                "name",
                OrderedDict(
                    [("preferred", u"Indira M Raman"), ("index", u"Raman, Indira M")]
                ),
            ),
            ("orcid", u"0000-0001-5245-8177"),
            ("role", "<i>eLife</i> Reviewing Editor"),
            (
                "affiliations",
                [
                    OrderedDict(
                        [
                            (
                                "name",
                                [
                                    u"Department of Neurobiology",
                                    u"Northwestern University",
                                ],
                            ),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", [u"Evanston", u"United States"]),
                                        (
                                            "components",
                                            OrderedDict(
                                                [
                                                    ("locality", [u"Evanston"]),
                                                    ("country", u"United States"),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            ("emailAddresses", [u"i-raman@northwestern.edu"]),
            (
                "competingInterests",
                u"The author declares that no competing interests exist.",
            ),
        ]
    )
]
