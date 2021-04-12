from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "unknown"),
            ("id", u"bib4"),
            ("date", u"2005"),
            (
                "authors",
                [
                    OrderedDict(
                        [
                            ("type", "person"),
                            (
                                "name",
                                OrderedDict(
                                    [("preferred", u"Engel W"), ("index", u"Engel, W")]
                                ),
                            ),
                        ]
                    )
                ],
            ),
            (
                "title",
                u"SHADERX3: Advanced Rendering with DirectX and OpenGL: Charles River Media",
            ),
            (
                "details",
                "SHADERX3: Advanced Rendering with DirectX and OpenGL: Charles River Media, Hingham, MA, USA",
            ),
        ]
    )
]
