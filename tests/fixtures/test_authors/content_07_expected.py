# output from elife-00666.xml
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
        "person_id": 1,
        "author": "Melissa Harrison",
        "affiliations": [
            {
                "dept": "Department of Production",
                "institution": "eLife",
                "country": "United Kingdom",
                "city": "Cambridge",
            }
        ],
        "notes-fn": [
            "\n†\nThese authors contributed equally to this work\n",
            "\n§\nDepartment of Wellcome Trust, Sanger Institute, London, United Kingdom\n",
            "\n#\nDeceased (not really!!)\n",
            '\n¶\nThis footnote text must work in isolation as nothing is processed on the html view to make it "work"\n',
            "\nChair of JATS4R\n",
            "\nCompleted the XML mapping exercise and wrote this XML example\n",
        ],
        "article_doi": "10.7554/eLife.00666",
        "position": 1,
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
        "person_id": 2,
        "author": "James F Gilbert",
        "affiliations": [
            {
                "dept": "Department of Production",
                "institution": "eLife",
                "country": "United Kingdom",
                "city": "Cambridge",
            }
        ],
        "notes-fn": [
            "\n†\nThese authors contributed equally to this work\n",
            "\nNo competing interests declared\n",
            "\nContributed to the XML mapping exercise and quality checked all the tagging and content\n",
        ],
        "article_doi": "10.7554/eLife.00666",
        "position": 2,
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
        "affiliations": [
            {
                "dept": "Department of Production",
                "institution": "eLife",
                "country": "United Kingdom",
                "city": "Cambridge",
            }
        ],
        "notes-fn": [
            "\n‡\nThese authors also contributed equally to this work\n",
            "\nReviewed the PDF product\n",
            "\nNo competing interests declared\n",
        ],
        "article_doi": "10.7554/eLife.00666",
        "position": 3,
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
        "affiliations": [
            {
                "dept": "Department of Technology",
                "institution": "eLife",
                "country": "United Kingdom",
                "city": "Cambridge",
            }
        ],
        "notes-fn": [
            "\n‡\nThese authors also contributed equally to this work\n",
            "\nGraham Nott is not an eLife employee\n",
            "\nChris Wilkinson, Performed the XML mapping exercise and generated the JSON Schema\nGraham Nott, Wrote the JATSscraper\nLuke Skibinski, Identified missing components from the JATSscraper\n",
        ],
        "article_doi": "10.7554/eLife.00666",
        "position": 4,
    },
]
