from collections import OrderedDict

expected = [
    {
        "type": "author",
        "equal-contrib": "yes",
        "corresp": "yes",
        "orcid": "https://orcid.org/0000-0002-6048-1470",
        "email": ["f.atherden@elifesciences.org"],
        "surname": "Atherden",
        "given-names": "Frederick Peter",
        "suffix": "III",
        "references": {
            "affiliation": ["aff1"],
            "equal-contrib": ["equal-contrib1"],
            "foot-note": ["fn1"],
            "contribution": ["con1"],
            "competing-interest": ["conf1"],
        },
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "corresp": "yes",
        "orcid": "https://orcid.org/0000-0002-4932-938X",
        "email": ["...@elifesciences.org"],
        "surname": "Harrison",
        "given-names": "Melissa",
        "references": {
            "affiliation": ["aff1"],
            "equal-contrib": ["equal-contrib1"],
            "foot-note": ["fn1"],
            "contribution": ["con2"],
            "competing-interest": ["conf2"],
        },
    },
    {
        "type": "author",
        "corresp": "yes",
        "group-author-key": "group-author-id1",
        "collab": "Example Group author",
        "email": ["...@elifesciences.org"],
        "references": {"contribution": ["con3"], "competing-interest": ["conf2"]},
    },
    {
        "type": "author",
        "orcid": "https://orcid.org/0000-1002-4932-938X",
        "surname": "Gilbert",
        "given-names": "James",
        "group-author-key": "group-author-id1",
        "affiliations": [
            {"institution": "eLife", "country": "United Kingdom", "city": "Cambridge"}
        ],
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "deceased": "yes",
        "surname": "Claus",
        "given-names": "Santa",
        "references": {
            "affiliation": ["aff1"],
            "equal-contrib": ["equal-contrib2"],
            "contribution": ["con4"],
            "competing-interest": ["conf2"],
            "foot-note": ["fn2"],
        },
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "surname": "West",
        "given-names": "Cornel",
        "suffix": "Jnr",
        "references": {
            "affiliation": ["aff2"],
            "equal-contrib": ["equal-contrib2"],
            "contribution": ["con5"],
            "competing-interest": ["conf2"],
        },
    },
    {
        "type": "on-behalf-of",
        "on-behalf-of": "on behalf of whoever finds this interesting",
    },
    {
        "type": "senior_editor",
        "role": "Senior Editor",
        "surname": "Behrens",
        "given-names": "Timothy",
        "affiliations": [
            {
                "institution": "University of Oxford",
                "country": "United Kingdom",
                "city": "Oxford",
                "ror": "https://ror.org/052gg0110",
            }
        ],
    },
    {
        "type": "editor",
        "role": "Reviewing Editor",
        "surname": "Helaine",
        "given-names": "Sophie",
        "affiliations": [
            {"institution": "Imperial College London", "country": "United Kingdom"}
        ],
    },
]
