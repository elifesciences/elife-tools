from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "section"),
            ("id", "s0"),
            ("title", "Main text"),
            (
                "content",
                [
                    OrderedDict(
                        [
                            ("type", "image"),
                            ("id", u"B1"),
                            (
                                "image",
                                OrderedDict(
                                    [("uri", u"elife-00646-inf1-v1"), ("alt", "")]
                                ),
                            ),
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
                    ),
                    OrderedDict(
                        [
                            ("type", "paragraph"),
                            (
                                "text",
                                u"Normal healthy bones can be thought of as nature's scaffold poles. The tightly packed minerals that make up the cortical bone form a sheath around an inner core of spongy bone and provide the strength that supports our bodies. Throughout our lives, our skeletons are kept strong by the continuous creation of new, fresh bone and the destruction of old, worn out bone. Unfortunately, as we become older, destruction becomes faster than creation, and so the cortical layer thins, causing the bone to weaken and break more easily. In severe cases, this is known as osteoporosis. As a result, simple trips or falls that would only bruise a younger person can cause serious fractures in the elderly. However, half of the elderly patients admitted to hospital with a broken hip do not suffer from osteoporosis.",
                            ),
                        ]
                    ),
                ],
            ),
        ]
    )
]
