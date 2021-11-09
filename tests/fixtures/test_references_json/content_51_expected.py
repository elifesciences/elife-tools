from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "thesis"),
            ("id", "bib1"),
            ("date", "1967"),
            (
                "author",
                OrderedDict(
                    [
                        ("type", "person"),
                        (
                            "name",
                            OrderedDict(
                                [("preferred", "Arita GS"), ("index", "Arita, GS")]
                            ),
                        ),
                    ]
                ),
            ),
            (
                "title",
                "A Comparative Study of the Structure and Function of the Adhesive Apparatus of the Cyclopteridae and Gobiesocidae",
            ),
            (
                "publisher",
                OrderedDict([("name", ["The University of British Columbia"])]),
            ),
            ("doi", "10.14288/1.0104391"),
            ("uri", "https://doi.org/10.14288/1.0104391"),
        ]
    )
]
