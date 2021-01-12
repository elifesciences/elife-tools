from collections import OrderedDict

expected = OrderedDict(
    [
        (
            "generated",
            [
                OrderedDict(
                    [
                        ("id", u"dataset1"),
                        ("date", u"2018"),
                        (
                            "authors",
                            [OrderedDict([("type", "group"), ("name", u"Liu et al")])],
                        ),
                        ("title", u"Xenopus Brain Proteome"),
                        ("details", u"ftp://MSV000081728@massive.ucsd.edu"),
                        ("uri", u"www.proteomexchange.org"),
                    ]
                )
            ],
        ),
        (
            "used",
            [
                OrderedDict(
                    [
                        ("id", u"dataset2"),
                        ("date", u"2014"),
                        (
                            "authors",
                            [OrderedDict([("type", "group"), ("name", u"Xenbase")])],
                        ),
                        ("title", u"Xenbase_Xenopus_laevis_05-29-2014"),
                        ("details", u"RRID:SCR_003280"),
                        ("uri", u"http://www.xenbase.org"),
                    ]
                ),
                OrderedDict(
                    [
                        ("id", u"dataset3"),
                        ("date", u"2014"),
                        (
                            "authors",
                            [OrderedDict([("type", "group"), ("name", u"Wuhr et al")])],
                        ),
                        ("title", u"Molecular Atlas of Development"),
                        ("details", u"accession no. PXD000926"),
                        ("uri", u"http://kirschner.med.harvard.edu/MADX.html"),
                    ]
                ),
                OrderedDict(
                    [
                        ("id", u"dataset4"),
                        ("date", u"2015"),
                        (
                            "authors",
                            [OrderedDict([("type", "group"), ("name", u"Xenbase")])],
                        ),
                        ("title", u"UniProt_Xenopus_laevis_01-23-2015"),
                        ("details", u"Proteome ID: UP000186698"),
                        ("uri", u"http://www.xenbase.org"),
                    ]
                ),
                OrderedDict(
                    [
                        ("id", u"dataset5"),
                        ("date", u"2014"),
                        (
                            "authors",
                            [OrderedDict([("type", "group"), ("name", u"Shen et al")])],
                        ),
                        ("title", u"Xenopus brain"),
                        ("details", u"ProteomeExchange number: PXD008659"),
                        (
                            "uri",
                            u"http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD008659",
                        ),
                    ]
                ),
            ],
        ),
    ]
)
