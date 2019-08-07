from collections import OrderedDict
expected = [
    OrderedDict([
        ('doi', '10.7554/eLife.00666.DL'),
        ('article_type', 'decision-letter'),
        ('id', 'SA1'),
        ('article_title', 'Decision letter'),
        ('contributors', [{
            'affiliations': [{
                'country': 'United Kingdom',
                'institution': 'eLife'
                }],
            'given-names': 'Andy',
            'role': 'Reviewing editor',
            'surname': 'Collings',
            'type': 'editor'
            }]
        ),
        ('parent_doi', '10.7554/eLife.00666'),
        ('parent_article_type', 'research-article'),
        ('parent_article_title', 'The eLife research article'),
        ('parent_license_url', 'http://creativecommons.org/licenses/by/4.0/')
    ]),
    OrderedDict([
        ('doi', '10.7554/eLife.00666.AR'),
        ('article_type', 'reply'),
        ('id', 'SA2'),
        ('article_title', 'Author response'),
        ('parent_doi', '10.7554/eLife.00666'),
        ('parent_article_type', 'research-article'),
        ('parent_article_title', 'The eLife research article'),
        ('parent_license_url', 'http://creativecommons.org/licenses/by/4.0/')
    ])
]
