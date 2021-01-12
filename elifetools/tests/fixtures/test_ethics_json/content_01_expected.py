from collections import OrderedDict

expected = [
    OrderedDict(
        [
            ("type", "paragraph"),
            (
                "text",
                u"Human subjects: This study was approved by the Institutional Review Board (IRB) of National Institute of Biological Sciences (IRBS030901) and consent was obtained; see the Materials and Methods section for details. The Helsinki guidelines were followed.",
            ),
        ]
    ),
    OrderedDict(
        [
            ("type", "paragraph"),
            (
                "text",
                u"Animal experimentation: The institutional animal care and use committee (IACUC) of the National Institute of Biological Sciences and the approved animal protocol is 09001T. The institutional guidelines for the care and use of laboratory animals were followed.",
            ),
        ]
    ),
    OrderedDict([("type", "paragraph"), ("text", u"Clinical trial Registry: NCT.")]),
    OrderedDict([("type", "paragraph"), ("text", u"Registration ID: NCT00912041.")]),
    OrderedDict(
        [("type", "paragraph"), ("text", u"Clinical trial Registry: EudraCT.")]
    ),
    OrderedDict(
        [("type", "paragraph"), ("text", u"Registration ID: EudraCT2004-000446-20.")]
    ),
]
