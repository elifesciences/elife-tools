from collections import OrderedDict
from utils import date_struct
expected = [
    OrderedDict([
        ('publication-format', u'electronic'),
        ('date-type', u'pub'),
        ('day', u'04'),
        ('month', u'07'),
        ('year', u'2017'),
        (u'date', date_struct(2017, 7, 4))
        ])
    ]
