from collections import OrderedDict
from elifetools.utils import date_struct
expected = [
    OrderedDict([
        ('version', u'v1'),
        ('day', u'25'),
        ('month', u'04'),
        ('year', u'2016'),
        ('date', date_struct(2016, 4, 25)),
        ('xlink_href', u'https://elifesciences.org/articles/e00666v1')
        ]),
    OrderedDict([
        ('version', u'v2'),
        ('day', u'12'),
        ('month', u'06'),
        ('year', u'2016'),
        ('date', date_struct(2016, 6, 12)),
        ('xlink_href', u'https://elifesciences.org/articles/e00666v2'),
        ('comment', u'The first version of this article was enhanced considerably between versions of the XML instance. These changes can bee seen on <a href="https://github.com/elifesciences/XML-mapping/blob/master/eLife00666.xml">Github</a>.')
        ]),
    OrderedDict([
        ('version', u'v3'),
        ('day', u'27'),
        ('month', u'06'),
        ('year', u'2016'),
        ('date', date_struct(2016, 6, 27)),
        ('xlink_href', u'https://elifesciences.org/articles/e00666v3'),
        ('comment', u'The author Christoph Wuelfing requested has surname was converted to the German spelling of "W\xfclfing".')
        ])
    ]
