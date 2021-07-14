# output from elife-kitchen-sink.xml
expected = [
    {
        "type": "author",
        "equal-contrib": "yes",
        "id": "author-23",
        "surname": "Alegado",
        "given-names": "Rosanna A",
        "suffix": "Jnr",
        "references": {
            "affiliation": ["aff1", "aff2"],
            "equal-contrib": ["equal-contrib"],
            "funding": ["par-1", "par-2"],
            "contribution": ["con1"],
            "competing-interest": ["conf2"],
            "present-address": ["pa1"],
            "related-object": ["dataro1", "dataro2"],
        },
        "person_id": 23,
        "author": "Rosanna A Alegado",
        "affiliations": [
            {
                "dept": "Department of Molecular and Cell Biology",
                "institution": "University of California, Berkeley",
                "country": "United States",
                "city": "Berkeley",
            },
            {
                "dept": "Department of Biological Chemistry and Molecular Pharmacology",
                "institution": "Harvard Medical School",
                "country": "United States",
                "city": "Boston",
            },
        ],
        "notes-fn": [
            "\n†\nThese authors contributed equally to this work\n",
            "\nRAA, Conception and design, Acquisition of data, Analysis and interpretation\n                        of data, Drafting or revising the article\n",
            "\nThe other authors declare that no competing interests exist.\n",
            "\n¶\nDepartment of Wellcome Trust, Sanger Institute, London, United Kingdom\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 1,
    },
    {
        "type": "author",
        "equal-contrib": "yes",
        "id": "author-17",
        "orcid": "http://orcid.org/0000-0002-7361-560X",
        "surname": "Brown",
        "given-names": "Laura W",
        "references": {
            "affiliation": ["aff2"],
            "equal-contrib": ["equal-contrib"],
            "funding": ["par-1", "par-3"],
            "contribution": ["con2"],
            "competing-interest": ["conf2"],
            "present-address": ["pa2"],
        },
        "person_id": 17,
        "author": "Laura W Brown",
        "affiliations": [
            {
                "dept": "Department of Biological Chemistry and Molecular Pharmacology",
                "institution": "Harvard Medical School",
                "country": "United States",
                "city": "Boston",
            }
        ],
        "notes-fn": [
            "\n†\nThese authors contributed equally to this work\n",
            "\nLWB, Conception and design, Acquisition of data, Analysis and interpretation\n                        of data, Drafting or revising the article\n",
            "\nThe other authors declare that no competing interests exist.\n",
            "\n‖\nDepartment of Biological Chemistry and Molecular Pharmacology, Harvard\n                        Medical School, Boston, United States\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 2,
    },
    {
        "type": "author",
        "id": "author-3",
        "surname": "Cao",
        "given-names": "Shugeng",
        "references": {
            "affiliation": ["aff2"],
            "equal-contrib": ["equal-contrib2"],
            "contribution": ["con3"],
            "competing-interest": ["conf2"],
        },
        "person_id": 3,
        "author": "Shugeng Cao",
        "affiliations": [
            {
                "dept": "Department of Biological Chemistry and Molecular Pharmacology",
                "institution": "Harvard Medical School",
                "country": "United States",
                "city": "Boston",
            }
        ],
        "notes-fn": [
            "\n‡\nThese authors also contributed equally to this work\n",
            "\nCS, Acquisition of data, Analysis and interpretation of data, Drafting or\n                        revising the article\n",
            "\nThe other authors declare that no competing interests exist.\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 3,
    },
    {
        "type": "author",
        "id": "author-4",
        "surname": "Dermenjian",
        "given-names": "Renee Kathryn",
        "references": {
            "affiliation": ["aff2"],
            "equal-contrib": ["equal-contrib2"],
            "contribution": ["con4"],
            "competing-interest": ["conf2"],
            "present-address": ["pa3"],
        },
        "person_id": 4,
        "author": "Renee Kathryn Dermenjian",
        "affiliations": [
            {
                "dept": "Department of Biological Chemistry and Molecular Pharmacology",
                "institution": "Harvard Medical School",
                "country": "United States",
                "city": "Boston",
            }
        ],
        "notes-fn": [
            "\n‡\nThese authors also contributed equally to this work\n",
            "\nRKD, Acquisition of data, Analysis and interpretation of data\n",
            "\nThe other authors declare that no competing interests exist.\n",
            "\neLife Sciences editorial Office, eLife Sciences, Cambridge, United\n                        Kingdom\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 4,
    },
    {
        "type": "author",
        "deceased": "yes",
        "id": "author-5",
        "surname": "Zuzow",
        "given-names": "Richard",
        "references": {
            "affiliation": ["aff3"],
            "contribution": ["con5"],
            "competing-interest": ["conf2"],
            "present-address": ["pa3"],
            "foot-note": ["fn1"],
        },
        "person_id": 5,
        "author": "Richard Zuzow",
        "affiliations": [
            {
                "dept": "Department of Biochemistry",
                "institution": "Stanford University School of Medicine",
                "country": "United States",
                "city": "Stanford",
            }
        ],
        "notes-fn": [
            "\nRZ, Acquisition of data, Analysis and interpretation of data\n",
            "\nThe other authors declare that no competing interests exist.\n",
            "\neLife Sciences editorial Office, eLife Sciences, Cambridge, United\n                        Kingdom\n",
            "\n**\nDeceased\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 5,
    },
    {
        "type": "author",
        "id": "author-6",
        "surname": "Fairclough",
        "given-names": "Stephen R",
        "references": {
            "affiliation": ["aff1"],
            "funding": ["par-6"],
            "contribution": ["con6"],
            "competing-interest": ["conf2"],
        },
        "person_id": 6,
        "author": "Stephen R Fairclough",
        "affiliations": [
            {
                "dept": "Department of Molecular and Cell Biology",
                "institution": "University of California, Berkeley",
                "country": "United States",
                "city": "Berkeley",
            }
        ],
        "notes-fn": [
            "\nSRF, Acquisition of data, Analysis and interpretation of data\n",
            "\nThe other authors declare that no competing interests exist.\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 6,
    },
    {
        "type": "author",
        "corresp": "yes",
        "id": "author-7",
        "surname": "Clardy",
        "given-names": "Jon",
        "references": {
            "affiliation": ["aff2"],
            "email": ["cor1"],
            "funding": ["par-4", "par-5"],
            "contribution": ["con7"],
            "competing-interest": ["conf1"],
        },
        "person_id": 7,
        "author": "Jon Clardy",
        "affiliations": [
            {
                "dept": "Department of Biological Chemistry and Molecular Pharmacology",
                "institution": "Harvard Medical School",
                "country": "United States",
                "city": "Boston",
            }
        ],
        "notes-corresp": [
            "\n*For\n                        correspondence: jon_clardy@hms.harvard.edu(JC);"
        ],
        "notes-fn": [
            "\nJC, Conception and design, Analysis and interpretation of data, Drafting or\n                        revising the article\n",
            "\nJC: Reviewing editor, eLife.\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 7,
    },
    {
        "type": "author",
        "corresp": "yes",
        "id": "author-8",
        "surname": "King",
        "given-names": "Nicole",
        "references": {
            "affiliation": ["aff1"],
            "email": ["cor2"],
            "funding": ["par-1", "par-2", "par-3", "par-4", "par-5"],
            "contribution": ["con8"],
            "competing-interest": ["conf2"],
        },
        "person_id": 8,
        "author": "Nicole King",
        "affiliations": [
            {
                "dept": "Department of Molecular and Cell Biology",
                "institution": "University of California, Berkeley",
                "country": "United States",
                "city": "Berkeley",
            }
        ],
        "notes-corresp": ["\nnking@berkeley.edu(NK);"],
        "notes-fn": [
            "\nNK, Conception and design, Analysis and interpretation of data, Drafting or\n                        revising the article\n",
            "\nThe other authors declare that no competing interests exist.\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 8,
    },
    {
        "type": "author",
        "corresp": "yes",
        "group-author-key": "group-author-id1",
        "collab": "NISC Comparative Sequencing Program",
        "references": {
            "email": ["cor3"],
            "affiliation": ["aff3"],
            "contribution": ["con9"],
            "competing-interest": ["conf2"],
            "funding": ["par-7"],
        },
        "affiliations": [
            {
                "dept": "Department of Biochemistry",
                "institution": "Stanford University School of Medicine",
                "country": "United States",
                "city": "Stanford",
            }
        ],
        "notes-corresp": ["\nmharrison@elifesciences.org(MH)"],
        "notes-fn": [
            "\nNISC Comparative Sequencing Program: JM did X, IM did Y and JB did Z and Y\n",
            "\nThe other authors declare that no competing interests exist.\n",
        ],
        "article_doi": "10.7554/eLife.00013",
        "position": 9,
    },
    {
        "type": "author",
        "group-author-key": "group-author-id2",
        "collab": "eLife staff group",
        "article_doi": "10.7554/eLife.00013",
        "position": 10,
    },
]
