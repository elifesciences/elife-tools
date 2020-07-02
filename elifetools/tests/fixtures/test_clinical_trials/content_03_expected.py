from collections import OrderedDict

expected = [
    OrderedDict([
        ('id', 'CT1'),
        ('content-type', 'post-result'),
        ('document-id', 'NCT02836002'),
        ('document-id-type', 'clinical-trial-number'),
        ('source-id', 'ClinicalTrials.gov'),
        ('source-id-type', 'registry-name'),
        ('source-type', 'clinical-trials-registry'),
        ('text', 'NCT02836002'),
        ('xlink_href', 'https://clinicaltrials.gov/show/NCT02836002'),
        ]),
    OrderedDict([
        ('id', 'CT1'),
        ('content-type', 'preResult'),
        ('document-id', 'NCT04094727'),
        ('document-id-type', 'clinical-trial-number'),
        ('source-id', '10.18810/clinical-trials-gov'),
        ('source-id-type', 'crossref-doi'),
        ('source-type', 'clinical-trials-registry'),
        ('text', 'NCT04094727'),
        ('xlink_href', 'https://clinicaltrials.gov/show/NCT04094727'),
        ])
    ]
