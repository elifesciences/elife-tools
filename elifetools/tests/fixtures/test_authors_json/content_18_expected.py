from collections import OrderedDict
expected = [OrderedDict([
    ('type', 'person'),
    ('name', OrderedDict([
        ('preferred', u'FirstName Surname'),
        ('index', u'Surname, FirstName')])),
    ('emailAddresses', [u'p@example.org'])
    ])
]