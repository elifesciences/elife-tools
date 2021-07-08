from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "image"),
            ("id", u"B1"),
            ("image", {"alt": "", "uri": u"elife-00646-inf1-v1"}),
            (
                "caption",
                [
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                'This article by Emma Pewsey (pictured) was the winning entry in the <a href="http://europepmc.org/ScienceWritingCompetition">Access to Understanding science-writing competition</a> for PhD students and early career post-doctoral researchers organized by Europe PubMed Central in partnership with The British Library. Entrants were asked to explain to a non-scientific audience, in fewer than 800 words, the research reported in a scientific article and why it mattered.',
                            ),
                        ]
                    )
                ],
            ),
        ]
    )
]
