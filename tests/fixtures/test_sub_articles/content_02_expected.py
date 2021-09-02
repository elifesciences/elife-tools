from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("doi", "10.7554/eLife.00666.sa0"),
            ("article_type", "editor-report"),
            ("id", "sa0"),
            ("article_title", "Editor's evaluation"),
            (
                "contributors",
                [
                    {
                        "type": "author",
                        "role": "Reviewing Editor",
                        "surname": "Ma",
                        "given-names": "Yuting",
                        "affiliations": [
                            {
                                "institution": "Suzhou Institute of Systems Medicine",
                                "country": "China",
                            }
                        ],
                    }
                ],
            ),
            (
                "related_objects",
                [
                    OrderedDict(
                        [
                            ("id", "ro1"),
                            ("link_type", "continued-by"),
                            (
                                "xlink_href",
                                "https://sciety.org/articles/activity/10.1101/2020.11.21.391326",
                            ),
                        ]
                    )
                ],
            ),
            ("parent_doi", "10.7554/eLife.00666"),
            ("parent_article_title", "The eLife research article"),
        ]
    )
]
