from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", u"unknown"),
            ("id", u"bib36"),
            ("date", u"2006"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [
                                        ("preferred", u"Schneider P"),
                                        ("index", u"Schneider, P"),
                                    ]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            (
                "title",
                u"Submicroscopic <i>Plasmodium falciparum</i> gametocytaemia and the contribution to malaria transmission",
            ),
            (
                "details",
                "PhD Thesis, Radboud University Nijmegen Medical Centre, Nijmegen, The Netherlands",
            ),
        ]
    )
]
