expected = [
    {
        "type": "author",
        "equal-contrib": "yes",
        "corresp": "yes",
        "deceased": "yes",
        "id": "author-00001",
        "orcid": "https://orcid.org/0000-0003-3523-4408",
        "email": ["m.harrison@elifesciences.org"],
        "surname": "Harrison",
        "given-names": "Melissa",
        "suffix": "Jnr",
        "references": {
            "affiliation": ["aff1"],
            "equal-contrib": ["equal-contrib1"],
            "present-address": ["pa1"],
            "foot-note": ["fn1", "fn2"],
            "funding": ["fund1"],
            "competing-interest": ["conf1"],
            "contribution": ["con1"],
            "related-object": ["dataset1", "dataset2"],
        },
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "id": "author-00002",
        "surname": "Gilbert",
        "given-names": "James F",
        "references": {
            "affiliation": ["aff1"],
            "equal-contrib": ["equal-contrib1"],
            "competing-interest": ["conf2"],
            "contribution": ["con2"],
        },
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "group-author-key": "group-author-id1",
        "collab": "eLife Editorial Production Group",
        "references": {
            "equal-contrib": ["equal-contrib2"],
            "contribution": ["con3"],
            "competing-interest": ["conf2"],
            "affiliation": ["aff1"],
        },
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id1",
        "surname": "Shearer",
        "given-names": "Alistair",
        "sub-group": "Writing group",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id1",
        "surname": "Caton",
        "given-names": "Hannah",
        "sub-group": "Writing group",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id1",
        "surname": "Chan",
        "given-names": "Wei Mun",
        "sub-group": "Editing group",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id1",
        "surname": "Drury",
        "given-names": "Hannah",
        "sub-group": "Editing group",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id1",
        "surname": "Guerreiro",
        "given-names": "Maria",
        "sub-group": "Editing group",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id1",
        "surname": "Richmond",
        "given-names": "Susanna",
        "sub-group": "Editing group",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "corresp": "yes",
        "group-author-key": "group-author-id2",
        "collab": "eLife Technology Group",
        "email": ["c.wilkinson@elifesciences.org"],
        "references": {
            "affiliation": ["aff2"],
            "equal-contrib": ["equal-contrib2"],
            "funding": ["fund2"],
            "competing-interest": ["conf3"],
            "contribution": ["con4"],
        },
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id2",
        "surname": "Nott",
        "given-names": "Graham",
        "affiliations": [
            {
                "institution": "Graham Nott Enterprises",
                "country": "Canada",
                "city": "Victoria",
            }
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id2",
        "orcid": "https://orcid.org/0000-0003-4921-6155",
        "email": ["c.wilkinson@elifesciences.org"],
        "surname": "Wilkinson",
        "given-names": "Chris",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author non-byline",
        "group-author-key": "group-author-id2",
        "surname": "Skibinski",
        "given-names": "Luke",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {"type": "on-behalf-of", "on-behalf-of": "for the eLife Staff Team"},
    {
        "type": "editor",
        "id": "author-10",
        "role": "Reviewing Editor",
        "surname": "Collings",
        "given-names": "Andrew",
        "affiliations": [
            {"institution": "eLife Sciences", "country": "United Kingdom"}
        ],
    },
]
