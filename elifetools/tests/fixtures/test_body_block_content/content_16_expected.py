from collections import OrderedDict

expected = OrderedDict(
    [
        ("type", "figure"),
        (
            "assets",
            [
                OrderedDict(
                    [
                        ("type", "image"),
                        ("doi", u"10.7554/eLife.27041.006"),
                        ("id", u"fig3"),
                        ("label", u"Figure 3"),
                        ("title", u"Developmental trajectories."),
                        (
                            "caption",
                            [
                                OrderedDict(
                                    [
                                        ("type", "paragraph"),
                                        (
                                            "text",
                                            u"Each plot shows single cells (dots; colored by trajectory assignment, sampled time point, or developmental stage) embedded in low-dimensional space based on their RNA (<b>A-C</b>) or protein (<b>D</b>) profiles, using different methods for dimensionality reduction and embedding: Gaussian process patent variable model (<b>A</b>); t-stochastic neighborhood embedding (<b>B</b>, <b>D</b>); diffusion maps (<b>C</b>). Computational methods then identify trajectories of pseudo-temporal progression in each case. (<b>A</b>) Myoblast differentiation in vitro. (<b>B</b>) Neurogenesis in the mouse brain dentate gyrus. (<b>C</b>) Embryonic stem cell differentiation in vitro. (<b>D</b>) Early hematopoiesis.",
                                        ),
                                    ]
                                )
                            ],
                        ),
                        (
                            "image",
                            OrderedDict(
                                [
                                    ("uri", u"elife-27041-fig3-v2"),
                                    ("alt", ""),
                                    (
                                        "attribution",
                                        [
                                            u'\xa9 2017 AAAS. <a href="#fig3">Figure 3A</a> reprinted from <a href="#bib109">L\xf6nnberg et al., 2017</a> with permission.',
                                            u'\xa9 2016 AAAS. <a href="#fig3">Figure 3B</a> reprinted from <a href="#bib67">Habib et al., 2016a</a> with permission.',
                                            u'\xa9 2016 Macmillan Publishers Limited. <a href="#fig3">Figure 3C</a> adapted from <a href="#bib70">Haghverdi et al., 2016</a> with permission.',
                                            u'\xa9 2016 Macmillan Publishers Limited. <a href="#fig3">Figure 3D</a> adapted from <a href="#bib157">Setty et al., 2016</a> with permission.',
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ]
                )
            ],
        ),
    ]
)
