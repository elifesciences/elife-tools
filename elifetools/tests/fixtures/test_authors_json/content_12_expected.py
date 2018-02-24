# coding=utf-8
from collections import OrderedDict
expected = [
    OrderedDict([
        ('type', 'person'),
        ('name', OrderedDict([
            ('preferred', u'Richard Smith'),
            ('index', u'Smith, Richard')
            ])),
        ('role', u'Chair of Patients Know Best'),
        ('emailAddresses', [u'richardswsmith@yahoo.co.uk']),
        ('competingInterests', "The author reviewed Goldacre's first book for the BMJ, and is mentioned briefly in Bad Pharma. Over the years he has had some meals paid for by drug companies and spoken at meetings sponsored by drug companies (as has Goldacre), which is hard to avoid if you speak at all as a doctor. 30 years ago he won an award from the Medical Journalists' Association that was sponsored by Eli Lilly, and discovered that the company thought it had bought him. Since then he has avoided prizes awarded by drug companies.")
        ])
    ]
