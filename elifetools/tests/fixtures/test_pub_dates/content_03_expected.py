from collections import OrderedDict
from utils import date_struct
expected = [
    OrderedDict([
        ('pub-type', u'ppub'),
        ('day', None),
        ('month', u'1'),
        ('year', u'2014'),
        (u'date', date_struct(2014, 1, 1))
        ]),
    OrderedDict([
        ('pub-type', u'epub-original'),
        ('day', u'30'),
        ('month', u'1'),
        ('year', u'2014'),
        (u'date', date_struct(2014, 1, 30))
        ]),
    OrderedDict([
        ('pub-type', u'epub'),
        ('day',  u'31'),
        ('month', u'1'),
        ('year', u'2014'),
        (u'date', date_struct(2014, 1, 31))
        ]),
    ]
