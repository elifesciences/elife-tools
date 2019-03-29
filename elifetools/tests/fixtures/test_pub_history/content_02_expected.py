from collections import OrderedDict
from elifetools.utils import date_struct


expected = [
    OrderedDict([
        ('event_type', 'preprint-publication'),
        ('event_desc', 'This article was originally published as a <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1101/118356">preprint</ext-link> on bioRxiv.'),
        ('event_desc_html', 'This article was originally published as a <a href="https://doi.org/10.1101/118356">preprint</a> on bioRxiv.'),
        ('uri', 'https://doi.org/10.1101/118356'),
        ('uri_text', 'preprint'),
        ('id_list', [
            OrderedDict([
                ('type', 'doi'),
                ('value', '10.1101/118356'),
                ('assigning-authority', 'crossref')
                ])
        ]),
        ('day', '24'),
        ('month', '03'),
        ('year', '2017'),
        ('date', date_struct(2017, 3, 24)),
        ('iso-8601-date', '2017-03-24')
        ])
    ]
