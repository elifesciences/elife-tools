# coding=utf-8

import json
import os
import unittest
from collections import OrderedDict
from bs4 import BeautifulSoup
from ddt import ddt, data, unpack
from elifetools import parseJATS as parser
from elifetools import rawJATS as raw_parser
from elifetools.utils import date_struct
from elifetools.file_utils import sample_xml, json_expected_file, read_fixture
from elifetools.tests import soup_body


@ddt
class TestParseJats(unittest.TestCase):
    def setUp(self):
        pass

    def soup(self, filename):
        # return soup
        return parser.parse_document(sample_xml(filename))

    def json_expected(self, filename, function_name):
        json_expected = None
        json_file = json_expected_file(filename, function_name)
        try:
            with open(json_file, "rb") as json_file_fp:
                json_expected = json.loads(json_file_fp.read().decode("utf-8"))
        except IOError:
            # file may not exist or the value is None for this article
            pass
        return json_expected

    @data("elife-kitchen-sink.xml")
    def test_parse_document(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertTrue(isinstance(soup, BeautifulSoup))

    """
    Quick test cases during development checking syntax errors and coverage
    """

    @unpack
    @data(
        (
            "elife04493.xml",
            "Neuron hemilineages provide the functional ground plan for the <i>Drosophila</i> ventral nervous system",
        )
    )
    def test_full_title_json(self, filename, expected):
        full_title_json = parser.full_title_json(self.soup(filename))
        self.assertEqual(expected, full_title_json)

    @unpack
    @data(
        (
            "elife04490.xml",
            "Both the frequency of sesquiterpene-emitting individuals and the defense capacity of individual plants determine the consequences of sesquiterpene volatile emission for individuals and their neighbors in populations of the wild tobacco <i>Nicotiana attenuata</i>.",
        ),
        ("elife_poa_e06828.xml", ""),
    )
    def test_impact_statement_json(self, filename, expected):
        impact_statement_json = parser.impact_statement_json(self.soup(filename))
        self.assertEqual(expected, impact_statement_json)

    @unpack
    @data(("elife-kitchen-sink.xml", 6), ("elife-02833-v2.xml", 0))
    def test_ethics_json_by_file(self, filename, expected_length):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(parser.ethics_json(soup)), expected_length)

    @unpack
    @data(
        (
            read_fixture("test_ethics_json", "content_01.xml"),
            read_fixture("test_ethics_json", "content_01_expected.py"),
        ),
    )
    def test_ethics_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.ethics_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(("elife-kitchen-sink.xml", list), ("elife_poa_e06828.xml", None))
    def test_acknowledgements_json_by_file(self, filename, expected):
        acknowledgements_json = parser.acknowledgements_json(self.soup(filename))
        if expected is None:
            self.assertEqual(expected, acknowledgements_json)
        else:
            self.assertEqual(expected, type(acknowledgements_json))

    @unpack
    @data(("elife04490.xml", 3))
    def test_appendices_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.appendices_json(soup)
        self.assertEqual(len(tag_content), expected_len)

    @unpack
    @data(
        # example based on 14093 v1 with many sections and content
        (
            read_fixture("test_appendices_json", "content_01.xml"),
            read_fixture("test_appendices_json", "content_01_expected.py"),
        ),
        # example based on 14022 v3 having a section with no title in it, with some additional scenarios
        (
            read_fixture("test_appendices_json", "content_02.xml"),
            read_fixture("test_appendices_json", "content_02_expected.py"),
        ),
        # appendix with no sections, based on 00666 kitchen sink
        (
            read_fixture("test_appendices_json", "content_03.xml"),
            read_fixture("test_appendices_json", "content_03_expected.py"),
        ),
        # appendix with a section and a box, also based on 00666 kitchen sink
        (
            read_fixture("test_appendices_json", "content_04.xml"),
            read_fixture("test_appendices_json", "content_04_expected.py"),
        ),
        # appendix with a boxed-text in a subsequent section based on article
        (
            read_fixture("test_appendices_json", "content_05.xml"),
            read_fixture("test_appendices_json", "content_05_expected.py"),
        ),
    )
    def test_appendices_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.appendices_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # appendix with inline-graphic, based on 17092 v1
        (
            read_fixture("test_appendices_json_base_url", "content_01.xml"),
            None,
            read_fixture("test_appendices_json_base_url", "content_01_expected.py"),
        ),
        # appendix with inline-graphic, based on 17092 v1
        (
            read_fixture("test_appendices_json_base_url", "content_02.xml"),
            "https://example.org/",
            read_fixture("test_appendices_json_base_url", "content_02_expected.py"),
        ),
    )
    def test_appendices_json_with_base_url(self, xml_content, base_url, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.appendices_json(soup_body(soup), base_url)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "elife04490.xml",
            [
                "<i>Nicotiana attenuata</i>",
                "<i>Manduca sexta</i>",
                u"Geocoris spp.",
                "<i>Trichobaris mucorea</i>",
                u"direct and indirect defense",
                u"diversity",
            ],
        ),
        ("elife07586.xml", []),
    )
    def test_keywords_json(self, filename, expected):
        keywords_json = parser.keywords_json(self.soup(filename))
        self.assertEqual(expected, keywords_json)

    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"/>', []),
        (
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><kwd-group kwd-group-type="research-organism"><title>Research organism</title><kwd><italic>A. thaliana</italic></kwd><kwd>Other</kwd></kwd-group></root>',
            ["<i>A. thaliana</i>"],
        ),
        (
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><kwd-group kwd-group-type="research-organism"><title>Research organism</title><kwd>None</kwd></kwd-group></root>',
            [],
        ),
    )
    def test_research_organism_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.research_organism_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("<root></root>", None),
        ("<root><ack></ack></root>", None),
        (
            "<root><ack><title>Acknowledgements</title><p>Paragraph</p></ack></root>",
            [OrderedDict([("type", "paragraph"), ("text", u"Paragraph")])],
        ),
        (
            "<root><ack><title>Acknowledgements</title><p>Paragraph</p><p><italic>italic</italic></p></ack></root>",
            [
                OrderedDict([("type", "paragraph"), ("text", u"Paragraph")]),
                OrderedDict([("type", "paragraph"), ("text", u"<i>italic</i>")]),
            ],
        ),
    )
    def test_acknowledgements_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.acknowledgements_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("elife02304.xml", 2),
        ("elife02935.xml", 2),
    )
    def test_datasets_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.datasets_json(soup)
        self.assertEqual(len(tag_content), expected_len)

    @unpack
    @data(
        # Datasets from 00825 v1, has generated, used, etal and italic tags
        (
            read_fixture("test_datasets_json", "content_01.xml"),
            read_fixture("test_datasets_json", "content_01_expected.py"),
        ),
        # Datasets from 00666 kitchen sink, includes a DOI
        (
            read_fixture("test_datasets_json", "content_02.xml"),
            read_fixture("test_datasets_json", "content_02_expected.py"),
        ),
        # 10856 v2, excerpt, for adding dates to datasets missing a year value
        (
            read_fixture("test_datasets_json", "content_03.xml"),
            read_fixture("test_datasets_json", "content_03_expected.py"),
        ),
        # Datasets example with section sec-type data-availability
        (
            read_fixture("test_datasets_json", "content_04.xml"),
            read_fixture("test_datasets_json", "content_04_expected.py"),
        ),
        # Datasets example with a blank paragraph on some PoA XML files based 33420 v1
        (
            read_fixture("test_datasets_json", "content_05.xml"),
            read_fixture("test_datasets_json", "content_05_expected.py"),
        ),
        # Datasets example with section sec-type data-availability and using element-citation tag
        (
            read_fixture("test_datasets_json", "content_06.xml"),
            read_fixture("test_datasets_json", "content_06_expected.py"),
        ),
        # Datasets example for PoA XML in new style tagging, based 33420 v1
        (
            read_fixture("test_datasets_json", "content_07.xml"),
            read_fixture("test_datasets_json", "content_07_expected.py"),
        ),
        # Datasets example with new pub-id uri tagging
        (
            read_fixture("test_datasets_json", "content_08.xml"),
            read_fixture("test_datasets_json", "content_08_expected.py"),
        ),
        # Datasets example with multiple datasets availability paragraphs
        (
            read_fixture("test_datasets_json", "content_09.xml"),
            read_fixture("test_datasets_json", "content_09_expected.py"),
        ),
    )
    def test_datasets_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.datasets_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("elife02304.xml", 2),
        ("elife02935.xml", 6),
    )
    def test_supplementary_files_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.supplementary_files_json(soup)
        self.assertEqual(len(tag_content), expected_len)

    @unpack
    @data(
        # Datasets from 16996 v1 PoA
        (
            read_fixture("test_supplementary_files_json", "content_01.xml"),
            read_fixture("test_supplementary_files_json", "content_01_expected.py"),
        ),
        # Datasets from 08477 v1 VoR
        (
            read_fixture("test_supplementary_files_json", "content_02.xml"),
            read_fixture("test_supplementary_files_json", "content_02_expected.py"),
        ),
        # 02184 v1, older style PoA has supplementary files directly in the article-meta
        (
            read_fixture("test_supplementary_files_json", "content_03.xml"),
            read_fixture("test_supplementary_files_json", "content_03_expected.py"),
        ),
        # 04493 v1 PoA, multiple old style supplementary files
        (
            read_fixture("test_supplementary_files_json", "content_04.xml"),
            read_fixture("test_supplementary_files_json", "content_04_expected.py"),
        ),
        # 10110 v1 excerpt, should only extract the supplementary-material from the back matter
        (
            read_fixture("test_supplementary_files_json", "content_05.xml"),
            read_fixture("test_supplementary_files_json", "content_05_expected.py"),
        ),
        # 03405 v1, label and no title tag
        (
            read_fixture("test_supplementary_files_json", "content_06.xml"),
            read_fixture("test_supplementary_files_json", "content_06_expected.py"),
        ),
        # 00333 v1, mimetype contains a slash so ignore sub-mimetype
        (
            read_fixture("test_supplementary_files_json", "content_07.xml"),
            read_fixture("test_supplementary_files_json", "content_07_expected.py"),
        ),
        # 26759 v2, example of title tag and no label tag
        (
            read_fixture("test_supplementary_files_json", "content_08.xml"),
            read_fixture("test_supplementary_files_json", "content_08_expected.py"),
        ),
    )
    def test_supplementary_files_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.supplementary_files_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "elife02304.xml",
            "The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.",
        )
    )
    def test_funding_statement_json_by_file(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.funding_statement_json(soup)
        self.assertEqual(tag_content, expected)

    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"></root>', None),
        (
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><funding-statement>Funding statement</funding-statement></root>',
            "Funding statement",
        ),
        (
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><funding-statement><italic>Special</italic> funding statement</funding-statement></root>',
            "<i>Special</i> funding statement",
        ),
    )
    def test_funding_statement_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.funding_statement_json(soup)
        self.assertEqual(tag_content, expected)

    @unpack
    @data(
        ("elife02304.xml", 3),
        ("elife02935.xml", 16),
    )
    def test_funding_awards_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.funding_awards_json(soup)
        self.assertEqual(len(tag_content), expected_len)

    @unpack
    @data(
        # 07383 v1 has an institution as the recipient
        (
            read_fixture("test_funding_awards_json", "content_01.xml"),
            read_fixture("test_funding_awards_json", "content_01_expected.py"),
        ),
        # Funding from new kitchen sink
        (
            read_fixture("test_funding_awards_json", "content_02.xml"),
            read_fixture("test_funding_awards_json", "content_02_expected.py"),
        ),
        # 08245 v1 edge case, unusual principal-award-recipient
        (
            read_fixture("test_funding_awards_json", "content_03.xml"),
            read_fixture("test_funding_awards_json", "content_03_expected.py"),
        ),
        # 00801 v1 edge case, rewrite funding award
        (
            read_fixture("test_funding_awards_json", "content_04.xml"),
            read_fixture("test_funding_awards_json", "content_04_expected.py"),
        ),
        # 04250 v1 edge case, rewrite to add funding award recipients
        (
            read_fixture("test_funding_awards_json", "content_05.xml"),
            read_fixture("test_funding_awards_json", "content_05_expected.py"),
        ),
        # 06412 v2 edge case, rewrite to add funding award recipients
        (
            read_fixture("test_funding_awards_json", "content_06.xml"),
            read_fixture("test_funding_awards_json", "content_06_expected.py"),
        ),
        # 03609 v1 example funding award with multiple recipients
        (
            read_fixture("test_funding_awards_json", "content_07.xml"),
            read_fixture("test_funding_awards_json", "content_07_expected.py"),
        ),
    )
    def test_funding_awards_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.funding_awards_json(soup)
        self.assertEqual(tag_content, expected)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, OrderedDict()),
        ("elife_poa_e06828.xml", OrderedDict(), None),
    )
    def test_decision_letter(self, filename, expected, not_expected):
        sub_article_content = parser.decision_letter(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, sub_article_content)
        if not_expected is not None:
            self.assertNotEqual(not_expected, sub_article_content)

    @unpack
    @data(
        # 04871 v2, excerpt, remove unwanted sections
        (
            read_fixture("test_decision_letter", "content_01.xml"),
            read_fixture("test_decision_letter", "content_01_expected.py"),
        ),
        # 10856 v2, excerpt, add missing description via a rewrite
        (
            read_fixture("test_decision_letter", "content_02.xml"),
            read_fixture("test_decision_letter", "content_02_expected.py"),
        ),
    )
    def test_decision_letter_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.decision_letter(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, OrderedDict()),
        ("elife_poa_e06828.xml", OrderedDict(), None),
    )
    def test_author_response(self, filename, expected, not_expected):
        sub_article_content = parser.author_response(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, sub_article_content)
        if not_expected is not None:
            self.assertNotEqual(not_expected, sub_article_content)

    @unpack
    @data(
        # 04871 v2, excerpt, remove unwanted sections
        (
            read_fixture("test_author_response", "content_01.xml"),
            read_fixture("test_author_response", "content_01_expected.py"),
        ),
    )
    def test_author_response_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.author_response(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(("elife-kitchen-sink.xml", None, []), ("elife_poa_e06828.xml", [], None))
    def test_body(self, filename, expected, not_expected):
        body = parser.body(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, body)
        if not_expected is not None:
            self.assertNotEqual(not_expected, body)

    @unpack
    @data(
        # very simple body, wrap in a section
        (
            read_fixture("test_body_json", "content_01.xml"),
            read_fixture("test_body_json", "content_01_expected.py"),
        ),
        # normal boxed-text and section, keep these
        (
            read_fixture("test_body_json", "content_02.xml"),
            read_fixture("test_body_json", "content_02_expected.py"),
        ),
        # boxed-text paragraphs inside the caption tag, based on 05519 v2
        (
            read_fixture("test_body_json", "content_03.xml"),
            read_fixture("test_body_json", "content_03_expected.py"),
        ),
        # 00301 v1 do not keep boxed-text and wrap in section
        (
            read_fixture("test_body_json", "content_04.xml"),
            read_fixture("test_body_json", "content_04_expected.py"),
        ),
        # 00646 v1 boxed text to keep, and wrap in section
        (
            read_fixture("test_body_json", "content_05.xml"),
            read_fixture("test_body_json", "content_05_expected.py"),
        ),
        # 02945 v1, correction article keep the boxed-text
        (
            read_fixture("test_body_json", "content_06.xml"),
            read_fixture("test_body_json", "content_06_expected.py"),
        ),
        # 12844 v1, based on, edge case to rewrite unacceptable sections that have no titles
        (
            read_fixture("test_body_json", "content_07.xml"),
            read_fixture("test_body_json", "content_07_expected.py"),
        ),
        # 09977 v2, based on, edge case to remove a specific section with no content
        (
            read_fixture("test_body_json", "content_08.xml"),
            read_fixture("test_body_json", "content_08_expected.py"),
        ),
        # 09977 v3, based on, edge case to keep a specific section that does have content
        (
            read_fixture("test_body_json", "content_09.xml"),
            read_fixture("test_body_json", "content_09_expected.py"),
        ),
        # 05519 v2, based on, edge case to remove an unwanted section
        (
            read_fixture("test_body_json", "content_10.xml"),
            read_fixture("test_body_json", "content_10_expected.py"),
        ),
        # 00013 v1, excerpt, add an id to a section
        (
            read_fixture("test_body_json", "content_11.xml"),
            read_fixture("test_body_json", "content_11_expected.py"),
        ),
        # 04232 v2, excerpt, remove an unwanted section
        (
            read_fixture("test_body_json", "content_12.xml"),
            read_fixture("test_body_json", "content_12_expected.py"),
        ),
        # 07157 v1, add title to a section
        (
            read_fixture("test_body_json", "content_13.xml"),
            read_fixture("test_body_json", "content_13_expected.py"),
        ),
        # excerpt of 23383 v1 where there is a boxed-text that was formerly stripped away, check it remains
        (
            read_fixture("test_body_json", "content_14.xml"),
            read_fixture("test_body_json", "content_14_expected.py"),
        ),
    )
    def test_body_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_json(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_body_json_base_url", "content_01.xml"),
            None,
            read_fixture("test_body_json_base_url", "content_01_expected.py"),
        ),
        (
            read_fixture("test_body_json_base_url", "content_02.xml"),
            "https://example.org/",
            read_fixture("test_body_json_base_url", "content_02_expected.py"),
        ),
        (
            read_fixture("test_body_json_base_url", "content_03.xml"),
            None,
            read_fixture("test_body_json_base_url", "content_03_expected.py"),
        ),
        (
            read_fixture("test_body_json_base_url", "content_04.xml"),
            "https://example.org/",
            read_fixture("test_body_json_base_url", "content_04_expected.py"),
        ),
    )
    def test_body_json_with_base_url(self, xml_content, base_url, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_json(soup, base_url=base_url)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # 08647 v1 PoA editor has blank string in the affiliation tags
        (
            read_fixture("test_editors_json", "content_01.xml"),
            read_fixture("test_editors_json", "content_01_expected.py"),
        ),
        # 09560 v1 example, has two editors
        (
            read_fixture("test_editors_json", "content_02.xml"),
            read_fixture("test_editors_json", "content_02_expected.py"),
        ),
        # 23804 v3 example, has no role tag and is rewritten
        (
            read_fixture("test_editors_json", "content_03.xml"),
            read_fixture("test_editors_json", "content_03_expected.py"),
        ),
        # 22028 v1 example, has a country but no institution
        (
            read_fixture("test_editors_json", "content_04.xml"),
            read_fixture("test_editors_json", "content_04_expected.py"),
        ),
        # kitchen sink example, has senior editor and reviewers
        (
            read_fixture("test_editors_json", "content_05.xml"),
            read_fixture("test_editors_json", "content_05_expected.py"),
        ),
        # kitchen sink example, reviewing editor and senior editor is the same person
        (
            read_fixture("test_editors_json", "content_06.xml"),
            read_fixture("test_editors_json", "content_06_expected.py"),
        ),
        # reviewing editor and senior editor is the same person in both mentions plus a reviewer
        (
            read_fixture("test_editors_json", "content_07.xml"),
            read_fixture("test_editors_json", "content_07_expected.py"),
        ),
    )
    def test_editors_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.editors_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data(
        "elife-kitchen-sink.xml",
        "elife-02833-v2.xml",
        "elife00351.xml",
        "elife-00666.xml",
    )
    def test_authors_json(self, filename):
        """note elife00351.xml has email inside an inline aff tag, very irregular"""
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.authors_json(soup), None)

    @unpack
    @data(
        # Author with phone number, 02833 v2
        (
            read_fixture("test_authors_json", "content_01.xml"),
            read_fixture("test_authors_json", "content_01_expected.py"),
        ),
        # 02935 v1, group authors (collab) but no members of those groups
        (
            read_fixture("test_authors_json", "content_02.xml"),
            read_fixture("test_authors_json", "content_02_expected.py"),
        ),
        # 02935 v2, excerpt for group author parsing
        (
            read_fixture("test_authors_json", "content_03.xml"),
            read_fixture("test_authors_json", "content_03_expected.py"),
        ),
        # 09376 v1, excerpt to rewrite an author ORCID
        (
            read_fixture("test_authors_json", "content_04.xml"),
            read_fixture("test_authors_json", "content_04_expected.py"),
        ),
        # 06956 v1, excerpt, add an affiliation name to an author
        (
            read_fixture("test_authors_json", "content_05.xml"),
            read_fixture("test_authors_json", "content_05_expected.py"),
        ),
        # 21337 v1, example to pick up the email of corresponding authors from authors notes
        (
            read_fixture("test_authors_json", "content_06.xml"),
            read_fixture("test_authors_json", "content_06_expected.py"),
        ),
        # 00007 v1, example with a present address
        (
            read_fixture("test_authors_json", "content_07.xml"),
            read_fixture("test_authors_json", "content_07_expected.py"),
        ),
        # 00666 kitchen sink (with extra whitespace removed), example to pick up the email of corresponding author
        (
            read_fixture("test_authors_json", "content_08.xml"),
            read_fixture("test_authors_json", "content_08_expected.py"),
        ),
        # 09594 v2 example of non-standard footnote fn-type other and id starting with 'fn'
        (
            read_fixture("test_authors_json", "content_09.xml"),
            read_fixture("test_authors_json", "content_09_expected.py"),
        ),
        # 21230 v1 example of author role to parse
        (
            read_fixture("test_authors_json", "content_10.xml"),
            read_fixture("test_authors_json", "content_10_expected.py"),
        ),
        # 21230 v1 as an example of competing interests rewrite rule for elife
        (
            read_fixture("test_authors_json", "content_11.xml"),
            read_fixture("test_authors_json", "content_11_expected.py"),
        ),
        # 00351 v1 example of author role to parse
        (
            read_fixture("test_authors_json", "content_12.xml"),
            read_fixture("test_authors_json", "content_12_expected.py"),
        ),
        # 21723 v1 another example of author role
        (
            read_fixture("test_authors_json", "content_13.xml"),
            read_fixture("test_authors_json", "content_13_expected.py"),
        ),
        # author with a bio based on kitchen sink 00777
        (
            read_fixture("test_authors_json", "content_14.xml"),
            read_fixture("test_authors_json", "content_14_expected.py"),
        ),
        # 02273 v1 example, equal contribution to parse
        (
            read_fixture("test_authors_json", "content_15.xml"),
            read_fixture("test_authors_json", "content_15_expected.py"),
        ),
        # 09148 v1 example, and author with two email addresses
        (
            read_fixture("test_authors_json", "content_16.xml"),
            read_fixture("test_authors_json", "content_16_expected.py"),
        ),
        # example of new kitchen sink group authors with multiple email addresses, based on 17044 v1
        (
            read_fixture("test_authors_json", "content_17.xml"),
            read_fixture("test_authors_json", "content_17_expected.py"),
        ),
        # example of inline email address
        (
            read_fixture("test_authors_json", "content_18.xml"),
            read_fixture("test_authors_json", "content_18_expected.py"),
        ),
    )
    def test_authors_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.authors_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # 00855 v1, example of just person authors
        (
            read_fixture("test_author_line", "content_01.xml"),
            u"Randy Schekman, Mark Patterson",
        ),
        # 08714 v1, group authors only
        (
            read_fixture("test_author_line", "content_02.xml"),
            u"MalariaGEN Plasmodium falciparum Community Project",
        ),
    )
    def test_author_line_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.author_line(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (None, None),
        (["Randy Schekman"], "Randy Schekman"),
        (["Randy Schekman", "Mark Patterson"], "Randy Schekman, Mark Patterson"),
        (["Randy Schekman", "Mark Patterson", "eLife"], "Randy Schekman et al."),
    )
    def test_format_author_line(self, author_names, expected):
        self.assertEqual(parser.format_author_line(author_names), expected)

    @data(
        # aff tag linked via an rid to id attribute
        (
            read_fixture("test_format_aff", "content_01.xml"),
            read_fixture("test_format_aff", "content_01_expected.py"),
        ),
        # inline aff tag example, no id attribute
        (
            read_fixture("test_format_aff", "content_02.xml"),
            read_fixture("test_format_aff", "content_02_expected.py"),
        ),
        # aff example mostly just text with no subtags
        (
            read_fixture("test_format_aff", "content_03.xml"),
            read_fixture("test_format_aff", "content_03_expected.py"),
        ),
        # edge case, no aff tag or the rid idoes not match an aff id
        (None, (None, {})),
    )
    @unpack
    def test_format_aff_edge_cases(self, xml_content, expected):
        if xml_content:
            soup = parser.parse_xml(xml_content)
            aff_tag = soup_body(soup)
        else:
            # where the tag is None
            aff_tag = xml_content
        tag_content = parser.format_aff(aff_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (None, []),
        (
            [
                {"name": {"preferred": "Randy Schekman"}},
                {"name": {"preferred": "Mark Patterson"}},
                {"name": "eLife"},
            ],
            ["Randy Schekman", "Mark Patterson", "eLife"],
        ),
    )
    def test_extract_author_line_names(self, authors_json, expected):
        self.assertEqual(parser.extract_author_line_names(authors_json), expected)

    @unpack
    @data(
        ("elife_poa_e06828.xml", "Michael S Fleming et al."),
        ("elife00351.xml", "Richard Smith"),
    )
    def test_author_line(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(parser.author_line(soup), expected)

    @data(
        # standard expected author with name tag
        (
            read_fixture("test_format_contributor", "content_01.xml"),
            read_fixture("test_format_contributor", "content_01_expected.py"),
        ),
        # edge case, no valid contrib tags
        (
            read_fixture("test_format_contributor", "content_02.xml"),
            read_fixture("test_format_contributor", "content_02_expected.py"),
        ),
        # edge case, string-name wrapper
        (
            read_fixture("test_format_contributor", "content_03.xml"),
            read_fixture("test_format_contributor", "content_03_expected.py"),
        ),
        # edge case, incorrect aff tag xref values will not cause an error if aff tag is not found
        (
            read_fixture("test_format_contributor", "content_04.xml"),
            read_fixture("test_format_contributor", "content_04_expected.py"),
        ),
    )
    @unpack
    def test_format_contributor_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        contrib_tag = raw_parser.article_contributors(soup)[0]
        tag_content = parser.format_contributor(contrib_tag, soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(("(+1) 800-555-5555", "+18005555555"))
    def test_phone_number_json(self, phone, expected):
        self.assertEqual(parser.phone_number_json(phone), expected)

    @unpack
    @data(
        (None, OrderedDict(), OrderedDict()),
        # example of clinical trial contributors
        (
            read_fixture("test_references_json_authors", "content_01.py"),
            OrderedDict([("type", u"clinical-trial")]),
            read_fixture("test_references_json_authors", "content_01_expected.py"),
        ),
        # example of patent contributors
        (
            read_fixture("test_references_json_authors", "content_02.py"),
            OrderedDict([("type", u"patent")]),
            read_fixture("test_references_json_authors", "content_02_expected.py"),
        ),
        # example of thesis contributors
        (
            read_fixture("test_references_json_authors", "content_03.py"),
            OrderedDict([("type", u"thesis")]),
            read_fixture("test_references_json_authors", "content_03_expected.py"),
        ),
    )
    def test_references_json_authors(self, ref_authors, ref_content, expected):
        references_json = parser.references_json_authors(ref_authors, ref_content)
        self.assertEqual(expected, references_json)

    @data(
        "elife-kitchen-sink.xml",
        "elife-09215-v1.xml",
        "elife00051.xml",
        "elife-10421-v1.xml",
        "elife-00666.xml",
    )
    def test_references_json(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.references_json(soup), None)

    @data(
        # Web reference with no title, use the uri from 01892
        (
            read_fixture("test_references_json", "content_01.xml"),
            read_fixture("test_references_json", "content_01_expected.py"),
        ),
        # Thesis title from 00626, also in converted to unknown because of its comment tag
        (
            read_fixture("test_references_json", "content_02.xml"),
            read_fixture("test_references_json", "content_02_expected.py"),
        ),
        # fpage value with usual characters from 00170
        (
            read_fixture("test_references_json", "content_03.xml"),
            read_fixture("test_references_json", "content_03_expected.py"),
        ),
        # fpage contains dots, 00569
        (
            read_fixture("test_references_json", "content_04.xml"),
            read_fixture("test_references_json", "content_04_expected.py"),
        ),
        # pages value of in press, 00109
        (
            read_fixture("test_references_json", "content_05.xml"),
            read_fixture("test_references_json", "content_05_expected.py"),
        ),
        # year value of in press, 02535
        (
            read_fixture("test_references_json", "content_06.xml"),
            read_fixture("test_references_json", "content_06_expected.py"),
        ),
        # conference, 03532 v3
        (
            read_fixture("test_references_json", "content_07.xml"),
            read_fixture("test_references_json", "content_07_expected.py"),
        ),
        # web with doi but no uri, 04775 v2
        (
            read_fixture("test_references_json", "content_08.xml"),
            read_fixture("test_references_json", "content_08_expected.py"),
        ),
        # Clinical trial example, from new kitchen sink 00666
        (
            read_fixture("test_references_json", "content_09.xml"),
            read_fixture("test_references_json", "content_09_expected.py"),
        ),
        # Journal reference with no article-title, 05462 v3
        (
            read_fixture("test_references_json", "content_10.xml"),
            read_fixture("test_references_json", "content_10_expected.py"),
        ),
        # book reference, gets converted to book-chapter, and has no editors, 16412 v1
        (
            read_fixture("test_references_json", "content_11.xml"),
            read_fixture("test_references_json", "content_11_expected.py"),
        ),
        # journal reference with no article title and no lpage, 11282 v2
        (
            read_fixture("test_references_json", "content_12.xml"),
            read_fixture("test_references_json", "content_12_expected.py"),
        ),
        # reference with no title uses detail as the titel, 00311 v1
        (
            read_fixture("test_references_json", "content_13.xml"),
            read_fixture("test_references_json", "content_13_expected.py"),
        ),
        # reference of type other with no details, 15266 v1
        (
            read_fixture("test_references_json", "content_14.xml"),
            read_fixture("test_references_json", "content_14_expected.py"),
        ),
        # reference of type journal with no journal name, 00340 v1
        (
            read_fixture("test_references_json", "content_15.xml"),
            read_fixture("test_references_json", "content_15_expected.py"),
        ),
        # reference of type book with no source, 00051 v1
        (
            read_fixture("test_references_json", "content_16.xml"),
            read_fixture("test_references_json", "content_16_expected.py"),
        ),
        # reference of type book with no publisher, 00031 v1
        (
            read_fixture("test_references_json", "content_17.xml"),
            read_fixture("test_references_json", "content_17_expected.py"),
        ),
        # reference of type book with no bookTitle, 03069 v2
        (
            read_fixture("test_references_json", "content_18.xml"),
            read_fixture("test_references_json", "content_18_expected.py"),
        ),
        # reference with unicode in collab tag, also gets turned into unknown type, 18023 v1
        (
            read_fixture("test_references_json", "content_19.xml"),
            read_fixture("test_references_json", "content_19_expected.py"),
        ),
        # data reference with no source, 16800 v2
        (
            read_fixture("test_references_json", "content_20.xml"),
            read_fixture("test_references_json", "content_20_expected.py"),
        ),
        # reference with an lpage and not fpage still gets pages value set, 13905 v2
        (
            read_fixture("test_references_json", "content_21.xml"),
            read_fixture("test_references_json", "content_21_expected.py"),
        ),
        # Reference with a collab using italic tag, from 05423 v2
        (
            read_fixture("test_references_json", "content_22.xml"),
            read_fixture("test_references_json", "content_22_expected.py"),
        ),
        # Reference with a non-numeric year, from 09215 v1
        (
            read_fixture("test_references_json", "content_23.xml"),
            read_fixture("test_references_json", "content_23_expected.py"),
        ),
        # no year value, 00051, with json rewriting enabled by adding elife XML metadata
        (
            read_fixture("test_references_json", "content_24.xml"),
            read_fixture("test_references_json", "content_24_expected.py"),
        ),
        # elife 12125 v3 bib11 will get deleted in the JSON rewriting
        (
            read_fixture("test_references_json", "content_25.xml"),
            read_fixture("test_references_json", "content_25_expected.py"),
        ),
        # 19532 v2 bib27 has a date-in-citation and no year tag, will get rewritten
        (
            read_fixture("test_references_json", "content_26.xml"),
            read_fixture("test_references_json", "content_26_expected.py"),
        ),
        # 00666 kitchen sink reference of type patent
        (
            read_fixture("test_references_json", "content_27.xml"),
            read_fixture("test_references_json", "content_27_expected.py"),
        ),
        # 20352 v2 reference of type patent, with a rewrite of the country value
        (
            read_fixture("test_references_json", "content_28.xml"),
            read_fixture("test_references_json", "content_28_expected.py"),
        ),
        # 20492 v3, report type reference with no publisher-name gets converted to unknown
        (
            read_fixture("test_references_json", "content_29.xml"),
            read_fixture("test_references_json", "content_29_expected.py"),
        ),
        # 15504 v2, reference with a pmid
        (
            read_fixture("test_references_json", "content_30.xml"),
            read_fixture("test_references_json", "content_30_expected.py"),
        ),
        # 15504 v2, reference with an isbn
        (
            read_fixture("test_references_json", "content_31.xml"),
            read_fixture("test_references_json", "content_31_expected.py"),
        ),
        # 18296 v3, reference of type preprint
        (
            read_fixture("test_references_json", "content_32.xml"),
            read_fixture("test_references_json", "content_32_expected.py"),
        ),
        # 16394 v2, reference of type thesis with no publisher, convert to unknown
        (
            read_fixture("test_references_json", "content_33.xml"),
            read_fixture("test_references_json", "content_33_expected.py"),
        ),
        # 09672 v2, reference of type conference-proceeding with no conference
        (
            read_fixture("test_references_json", "content_34.xml"),
            read_fixture("test_references_json", "content_34_expected.py"),
        ),
        # 07460 v1, reference rewriting test, rewrites date and authors
        (
            read_fixture("test_references_json", "content_35.xml"),
            read_fixture("test_references_json", "content_35_expected.py"),
        ),
        # 20522 v1, reference rewriting year value in json output
        (
            read_fixture("test_references_json", "content_36.xml"),
            read_fixture("test_references_json", "content_36_expected.py"),
        ),
        # 09520 v2, reference rewriting conference data
        (
            read_fixture("test_references_json", "content_37.xml"),
            read_fixture("test_references_json", "content_37_expected.py"),
        ),
        # from 00666 kitchen sink example, will add a uri to the references json from the doi value
        (
            read_fixture("test_references_json", "content_38.xml"),
            read_fixture("test_references_json", "content_38_expected.py"),
        ),
        # from 00666 kitchen sink example, reference of type periodical
        (
            read_fixture("test_references_json", "content_39.xml"),
            read_fixture("test_references_json", "content_39_expected.py"),
        ),
        # 00666 kitchen sink example with a version tag
        (
            read_fixture("test_references_json", "content_40.xml"),
            read_fixture("test_references_json", "content_40_expected.py"),
        ),
        # 23193 v2 book references has editors and no authors
        (
            read_fixture("test_references_json", "content_41.xml"),
            read_fixture("test_references_json", "content_41_expected.py"),
        ),
        # example of data citation with a pub-id accession, based on article 07836
        (
            read_fixture("test_references_json", "content_42.xml"),
            read_fixture("test_references_json", "content_42_expected.py"),
        ),
        # example of data citation with a object-id tag accession, gets converted to unknown because of the comment tag, based on article 07048
        (
            read_fixture("test_references_json", "content_43.xml"),
            read_fixture("test_references_json", "content_43_expected.py"),
        ),
        # example of data citation with a pub-id pub-id-type="archive", parse it as an accession number, based on 00666 kitchen sink example
        (
            read_fixture("test_references_json", "content_44.xml"),
            read_fixture("test_references_json", "content_44_expected.py"),
        ),
        # example of ref of type webpage, based on article 10.5334/sta.606, note: does not parse author names
        (
            read_fixture("test_references_json", "content_45.xml"),
            read_fixture("test_references_json", "content_45_expected.py"),
        ),
        # example of ref of type report, with a doi but no uri, uri gets filled in
        (
            read_fixture("test_references_json", "content_46.xml"),
            read_fixture("test_references_json", "content_46_expected.py"),
        ),
        # example of ref of type journal with no pages
        (
            read_fixture("test_references_json", "content_47.xml"),
            read_fixture("test_references_json", "content_47_expected.py"),
        ),
        # example of ref author having a suffix from the elife 00666 kitchen sink XML
        (
            read_fixture("test_references_json", "content_48.xml"),
            read_fixture("test_references_json", "content_48_expected.py"),
        ),
    )
    @unpack
    def test_references_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.references_json(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data((None, None, None))
    def test_references_publisher(self, publisher_name, publisher_loc, expected):
        self.assertEqual(
            parser.references_publisher(publisher_name, publisher_loc), expected
        )

    @unpack
    @data(
        (None, 0),
        ("<root><italic></italic></root>", 0),
        ("<root><sec><p>Content</p></sec></root>", 1),
    )
    def test_body_blocks(self, xml_content, expected_len):
        if xml_content:
            soup = parser.parse_xml(xml_content)
            body_tag = soup_body(soup_body(soup))
        else:
            body_tag = xml_content
        body_block_tags = parser.body_blocks(body_tag)
        self.assertEqual(len(body_block_tags), expected_len)

    @unpack
    @data(
        (None, None, None, None, None, None, None, None, None),
        ("title", None, None, None, None, None, "title", None, None),
        (None, "label", None, None, None, None, None, "label", None),
        ("title", "label", "caption", None, None, None, "title", "label", None),
        ("title", "label", "caption", True, None, None, "title", "label", "caption"),
        (None, "label", None, None, True, None, "label", None, None),
        (None, "label", None, None, True, True, "label", None, None),
        ("title", None, None, None, True, True, None, "title", None),
        ("title", None, None, None, None, True, None, "title", None),
        ("title", "label", None, None, True, None, "title", "label", None),
        ("title.", None, None, None, None, True, None, "title", None),
        (None, "label:", None, None, True, None, "label:", None, None),
    )
    def test_body_block_title_label_caption(
        self,
        title_value,
        label_value,
        caption_content,
        set_caption,
        prefer_title,
        prefer_label,
        expected_title,
        expected_label,
        expected_caption,
    ):
        tag_content = OrderedDict()
        parser.body_block_title_label_caption(
            tag_content,
            title_value,
            label_value,
            caption_content,
            set_caption,
            prefer_title,
            prefer_label,
        )
        self.assertEqual(tag_content.get("label"), expected_label)
        self.assertEqual(tag_content.get("title"), expected_title)
        self.assertEqual(tag_content.get("caption"), expected_caption)

    @unpack
    @data(
        (
            read_fixture("test_body_block_content", "content_01.xml"),
            read_fixture("test_body_block_content", "content_01_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_02.xml"),
            read_fixture("test_body_block_content", "content_02_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_03.xml"),
            read_fixture("test_body_block_content", "content_03_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_04.xml"),
            read_fixture("test_body_block_content", "content_04_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_05.xml"),
            read_fixture("test_body_block_content", "content_05_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_06.xml"),
            read_fixture("test_body_block_content", "content_06_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_07.xml"),
            read_fixture("test_body_block_content", "content_07_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_08.xml"),
            read_fixture("test_body_block_content", "content_08_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_09.xml"),
            read_fixture("test_body_block_content", "content_09_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_10.xml"),
            read_fixture("test_body_block_content", "content_10_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_11.xml"),
            read_fixture("test_body_block_content", "content_11_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_12.xml"),
            read_fixture("test_body_block_content", "content_12_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_13.xml"),
            read_fixture("test_body_block_content", "content_13_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_14.xml"),
            read_fixture("test_body_block_content", "content_14_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_15.xml"),
            read_fixture("test_body_block_content", "content_15_expected.py"),
        ),
        # example of copyright statements ending in a full stop, based on article 27041
        (
            read_fixture("test_body_block_content", "content_16.xml"),
            read_fixture("test_body_block_content", "content_16_expected.py"),
        ),
        # example of video with attributions, based on article 17243
        (
            read_fixture("test_body_block_content", "content_17.xml"),
            read_fixture("test_body_block_content", "content_17_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_18.xml"),
            read_fixture("test_body_block_content", "content_18_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_19.xml"),
            read_fixture("test_body_block_content", "content_19_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_20.xml"),
            read_fixture("test_body_block_content", "content_20_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_21.xml"),
            read_fixture("test_body_block_content", "content_21_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_22.xml"),
            read_fixture("test_body_block_content", "content_22_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_23.xml"),
            read_fixture("test_body_block_content", "content_23_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_24.xml"),
            read_fixture("test_body_block_content", "content_24_expected.py"),
        ),
        # media tag that is not a video
        (
            read_fixture("test_body_block_content", "content_25.xml"),
            read_fixture("test_body_block_content", "content_25_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_26.xml"),
            read_fixture("test_body_block_content", "content_26_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_27.xml"),
            read_fixture("test_body_block_content", "content_27_expected.py"),
        ),
        (
            read_fixture("test_body_block_content", "content_28.xml"),
            read_fixture("test_body_block_content", "content_28_expected.py"),
        ),
        # disp-quote content-type="editor-comment" is turned into an excerpt block
        (
            read_fixture("test_body_block_content", "content_29.xml"),
            read_fixture("test_body_block_content", "content_29_expected.py"),
        ),
        # 00109 v1, figure with a supplementary file that has multiple caption paragraphs
        (
            read_fixture("test_body_block_content", "content_30.xml"),
            read_fixture("test_body_block_content", "content_30_expected.py"),
        ),
        # code block, based on elife 20352 v2, contains new lines too
        (
            read_fixture("test_body_block_content", "content_31.xml"),
            read_fixture("test_body_block_content", "content_31_expected.py"),
        ),
        # example of a table with a break tag, based on 7141 v1
        (
            read_fixture("test_body_block_content", "content_32.xml"),
            read_fixture("test_body_block_content", "content_32_expected.py"),
        ),
        # example of a figure, based on 00007 v1
        (
            read_fixture("test_body_block_content", "content_33.xml"),
            read_fixture("test_body_block_content", "content_33_expected.py"),
        ),
        # example table with a caption and no title needs a title added, based on 05604 v1
        (
            read_fixture("test_body_block_content", "content_34.xml"),
            read_fixture("test_body_block_content", "content_34_expected.py"),
        ),
        # example video with only the DOI in the caption paragraph, based on 02277 v1
        (
            read_fixture("test_body_block_content", "content_35.xml"),
            read_fixture("test_body_block_content", "content_35_expected.py"),
        ),
        # example animated gif as a video in 00666 kitchen sink
        (
            read_fixture("test_body_block_content", "content_36.xml"),
            read_fixture("test_body_block_content", "content_36_expected.py"),
        ),
        # example of named-content to be converted to HTML from new kitchen sink 00666
        (
            read_fixture("test_body_block_content", "content_37.xml"),
            read_fixture("test_body_block_content", "content_37_expected.py"),
        ),
        # example of table author-callout-style styles to replace as a class attribute, based on 24231 v1
        (
            read_fixture("test_body_block_content", "content_38.xml"),
            read_fixture("test_body_block_content", "content_38_expected.py"),
        ),
        # example inline table adapted from 00666 kitchen sink
        (
            read_fixture("test_body_block_content", "content_39.xml"),
            read_fixture("test_body_block_content", "content_39_expected.py"),
        ),
        # example key resources inline table that has a label will be turned into a figure block
        (
            read_fixture("test_body_block_content", "content_40.xml"),
            read_fixture("test_body_block_content", "content_40_expected.py"),
        ),
        # test for stripping out comment tag content when it is inside a paragraph tag
        (
            read_fixture("test_body_block_content", "content_41.xml"),
            read_fixture("test_body_block_content", "content_41_expected.py"),
        ),
        # test ignoring nested fig title as a box-text title
        (
            read_fixture("test_body_block_content", "content_42.xml"),
            read_fixture("test_body_block_content", "content_42_expected.py"),
        ),
    )
    def test_body_block_content(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        # find the first tag in the root with a name
        for child in soup.root.children:
            if child.name:
                body_tag = child
                break
        tag_content = parser.body_block_content(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_body_block_content_render", "content_01.xml"),
            read_fixture("test_body_block_content_render", "content_01_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_02.xml"),
            read_fixture("test_body_block_content_render", "content_02_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_03.xml"),
            read_fixture("test_body_block_content_render", "content_03_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_04.xml"),
            read_fixture("test_body_block_content_render", "content_04_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_05.xml"),
            read_fixture("test_body_block_content_render", "content_05_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_06.xml"),
            read_fixture("test_body_block_content_render", "content_06_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_07.xml"),
            read_fixture("test_body_block_content_render", "content_07_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_08.xml"),
            read_fixture("test_body_block_content_render", "content_08_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_09.xml"),
            read_fixture("test_body_block_content_render", "content_09_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_10.xml"),
            read_fixture("test_body_block_content_render", "content_10_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_11.xml"),
            read_fixture("test_body_block_content_render", "content_11_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_12.xml"),
            read_fixture("test_body_block_content_render", "content_12_expected.py"),
        ),
        (
            read_fixture("test_body_block_content_render", "content_13.xml"),
            read_fixture("test_body_block_content_render", "content_13_expected.py"),
        ),
        # disp-quote content-type="editor-comment" is turned into an excerpt block
        (
            read_fixture("test_body_block_content_render", "content_14.xml"),
            read_fixture("test_body_block_content_render", "content_14_expected.py"),
        ),
        # Boxed text with no title tag uses the first sentence of the caption paragraph, 00288 v1
        (
            read_fixture("test_body_block_content_render", "content_15.xml"),
            read_fixture("test_body_block_content_render", "content_15_expected.py"),
        ),
        # Example of boxed-text with content inside its caption tag
        (
            read_fixture("test_body_block_content_render", "content_16.xml"),
            read_fixture("test_body_block_content_render", "content_16_expected.py"),
        ),
        # code block, based on elife 20352 v2, contains new lines too
        (
            read_fixture("test_body_block_content_render", "content_17.xml"),
            read_fixture("test_body_block_content_render", "content_17_expected.py"),
        ),
        # Example of monospace tags
        (
            read_fixture("test_body_block_content_render", "content_18.xml"),
            read_fixture("test_body_block_content_render", "content_18_expected.py"),
        ),
        # example of a table to not pickup a child element title, based on 22264 v2
        (
            read_fixture("test_body_block_content_render", "content_19.xml"),
            read_fixture("test_body_block_content_render", "content_19_expected.py"),
        ),
        # example table: a label, no title, no caption
        (
            read_fixture("test_body_block_content_render", "content_20.xml"),
            read_fixture("test_body_block_content_render", "content_20_expected.py"),
        ),
        # example table: a label, a title, no caption
        (
            read_fixture("test_body_block_content_render", "content_21.xml"),
            read_fixture("test_body_block_content_render", "content_21_expected.py"),
        ),
        # example table: a label, no title, a caption
        (
            read_fixture("test_body_block_content_render", "content_22.xml"),
            read_fixture("test_body_block_content_render", "content_22_expected.py"),
        ),
        # example table: a label, a title, and a caption
        (
            read_fixture("test_body_block_content_render", "content_23.xml"),
            read_fixture("test_body_block_content_render", "content_23_expected.py"),
        ),
        # example table: no label, no title, and a caption
        (
            read_fixture("test_body_block_content_render", "content_24.xml"),
            read_fixture("test_body_block_content_render", "content_24_expected.py"),
        ),
        # example fig with a caption and no title, based on 00281 v1
        (
            read_fixture("test_body_block_content_render", "content_25.xml"),
            read_fixture("test_body_block_content_render", "content_25_expected.py"),
        ),
        # example media with a label and no title, based on 00007 v1
        (
            read_fixture("test_body_block_content_render", "content_26.xml"),
            read_fixture("test_body_block_content_render", "content_26_expected.py"),
        ),
        # example test from 02935 v2 of list within a list to not add child list-item to the parent list twice
        (
            read_fixture("test_body_block_content_render", "content_27.xml"),
            read_fixture("test_body_block_content_render", "content_27_expected.py"),
        ),
        # example list from 00666 kitchen sink with paragraphs and list inside a list-item
        (
            read_fixture("test_body_block_content_render", "content_28.xml"),
            read_fixture("test_body_block_content_render", "content_28_expected.py"),
        ),
        # example of a video inside a fig group based on 00666 kitchen sink
        (
            read_fixture("test_body_block_content_render", "content_29.xml"),
            read_fixture("test_body_block_content_render", "content_29_expected.py"),
        ),
        # example of a video as supplementary material inside a fig-group based on 06726 v2
        (
            read_fixture("test_body_block_content_render", "content_30.xml"),
            read_fixture("test_body_block_content_render", "content_30_expected.py"),
        ),
        # example of fig supplementary-material with only a title tag, based on elife-26759-v1.xml except
        #  this example is fixed so the caption tag wraps the entire caption, and values are abbreviated
        #  to test how the punctuation is stripped from the end of the supplementary-material title value
        #  when it is converted to a label
        (
            read_fixture("test_body_block_content_render", "content_31.xml"),
            read_fixture("test_body_block_content_render", "content_31_expected.py"),
        ),
        # example of disp-formula inside a disp-quote based on 55588
        (
            read_fixture("test_body_block_content_render", "content_32.xml"),
            read_fixture("test_body_block_content_render", "content_32_expected.py"),
        ),
    )
    def test_body_block_content_render(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_block_content_render(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_render_raw_body", "content_01.xml"),
            read_fixture("test_render_raw_body", "content_01_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_02.xml"),
            read_fixture("test_render_raw_body", "content_02_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_03.xml"),
            read_fixture("test_render_raw_body", "content_03_expected.py"),
        ),
        # Below when there is a space between paragraph tags, it should not render as a paragraph
        (
            read_fixture("test_render_raw_body", "content_04.xml"),
            read_fixture("test_render_raw_body", "content_04_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_05.xml"),
            read_fixture("test_render_raw_body", "content_05_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_06.xml"),
            read_fixture("test_render_raw_body", "content_06_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_07.xml"),
            read_fixture("test_render_raw_body", "content_07_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_08.xml"),
            read_fixture("test_render_raw_body", "content_08_expected.py"),
        ),
        (
            read_fixture("test_render_raw_body", "content_09.xml"),
            read_fixture("test_render_raw_body", "content_09_expected.py"),
        ),
        # excerpt from 00646 v1 with a boxed-text inline-graphic
        (
            read_fixture("test_render_raw_body", "content_10.xml"),
            read_fixture("test_render_raw_body", "content_10_expected.py"),
        ),
    )
    def test_render_raw_body(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.render_raw_body(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_abstract_json", "content_01.xml"),
            read_fixture("test_abstract_json", "content_01_expected.py"),
        ),
        # executive-summary will return None
        (
            read_fixture("test_abstract_json", "content_02.xml"),
            read_fixture("test_abstract_json", "content_02_expected.py"),
        ),
        # test lots of inline tagging
        (
            read_fixture("test_abstract_json", "content_03.xml"),
            read_fixture("test_abstract_json", "content_03_expected.py"),
        ),
        # structured abstract example based on BMJ Open bmjopen-4-e003269.xml
        (
            read_fixture("test_abstract_json", "content_04.xml"),
            read_fixture("test_abstract_json", "content_04_expected.py"),
        ),
        # structured abstract elife example
        (
            read_fixture("test_abstract_json", "content_05.xml"),
            read_fixture("test_abstract_json", "content_05_expected.py"),
        ),
    )
    def test_abstract_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstract_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_digest_json", "content_01.xml"),
            read_fixture("test_digest_json", "content_01_expected.py"),
        ),
    )
    def test_digest_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.digest_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    """
    Unit test small or special cases
    """

    @unpack
    @data(("elife-kitchen-sink.xml", "pub", ("28", "02", "2014")))
    def test_ymd(self, filename, test_date_type, expected):
        soup = self.soup(filename)
        date_tag = raw_parser.pub_date(soup, date_type=test_date_type)[0]
        self.assertEqual(expected, parser.ymd(date_tag))

    @unpack
    @data(
        ("elife-kitchen-sink.xml", "received", date_struct(2012, 6, 22)),
        ("elife-kitchen-sink.xml", None, None),
        ("elife-kitchen-sink.xml", "not_a_date_type", None),
    )
    def test_history_date(self, filename, date_type, expected):
        self.assertEqual(expected, parser.history_date(self.soup(filename), date_type))

    """
    Functions that require more than one argument to test against json output
    """

    @unpack
    @data(
        # typical eLife format
        (
            read_fixture("test_journal_issn", "content_01.xml"),
            "electronic",
            None,
            "2050-084X",
        ),
        # eLife format with specifying the publication format
        (read_fixture("test_journal_issn", "content_02.xml"), None, None, "2050-084X"),
        # a non-eLife format
        (
            read_fixture("test_journal_issn", "content_03.xml"),
            None,
            "epub",
            "2057-4991",
        ),
    )
    def test_journal_issn_edge_cases(self, xml_content, pub_format, pub_type, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.journal_issn(
            soup_body(soup), pub_format=pub_format, pub_type=pub_type
        )
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_journal_issn(self, filename):
        self.assertEqual(
            self.json_expected(filename, "journal_issn"),
            parser.journal_issn(self.soup(filename), "electronic"),
        )

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_author_contributions(self, filename):
        self.assertEqual(
            self.json_expected(filename, "author_contributions"),
            parser.author_contributions(self.soup(filename), "con"),
        )

    @data("elife-kitchen-sink.xml", "elife00190.xml")
    def test_competing_interests(self, filename):
        self.assertEqual(
            self.json_expected(filename, "competing_interests"),
            parser.competing_interests(self.soup(filename), "conflict"),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_author_notes(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_author_notes"),
            parser.full_author_notes(self.soup(filename), None),
        )

    """
    Functions that only need soup to test them against json output
    """

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_abstract(self, filename):
        self.assertEqual(
            self.json_expected(filename, "abstract"),
            parser.abstract(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml")
    def test_abstracts(self, filename):
        self.assertEqual(
            self.json_expected(filename, "abstracts"),
            parser.abstracts(self.soup(filename)),
        )

    @unpack
    @data(
        # example based on eLife format
        (
            read_fixture("test_abstract", "content_01.xml"),
            read_fixture("test_abstract", "content_01_expected.py"),
        ),
        # example based on BMJ Open bmjopen-4-e003269.xml
        (
            read_fixture("test_abstract", "content_02.xml"),
            read_fixture("test_abstract", "content_02_expected.py"),
        ),
    )
    def test_abstract_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstract(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            # very basic abstract
            read_fixture("test_abstract_xml", "content_01.xml"),
            read_fixture("test_abstract_xml", "content_01_expected.py"),
        ),
        (
            # abstract tag with id attribute and mathml tags
            read_fixture("test_abstract_xml", "content_02.xml"),
            read_fixture("test_abstract_xml", "content_02_expected.py"),
        ),
        (
            # structured abstract example
            read_fixture("test_abstract_xml", "content_03.xml"),
            read_fixture("test_abstract_xml", "content_03_expected.py"),
        ),
        (
            # no abstract tag
            read_fixture("test_abstract_xml", "content_04.xml"),
            read_fixture("test_abstract_xml", "content_04_expected.py"),
        ),
    )
    def test_abstract_xml(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstract_xml(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_date(self, filename):
        self.assertEqual(
            self.json_expected(filename, "accepted_date_date"),
            parser.accepted_date_date(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_day(self, filename):
        self.assertEqual(
            self.json_expected(filename, "accepted_date_day"),
            parser.accepted_date_day(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_month(self, filename):
        self.assertEqual(
            self.json_expected(filename, "accepted_date_month"),
            parser.accepted_date_month(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_timestamp(self, filename):
        self.assertEqual(
            self.json_expected(filename, "accepted_date_timestamp"),
            parser.accepted_date_timestamp(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_year(self, filename):
        self.assertEqual(
            self.json_expected(filename, "accepted_date_year"),
            parser.accepted_date_year(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_ack(self, filename):
        self.assertEqual(
            self.json_expected(filename, "ack"), parser.ack(self.soup(filename))
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_acknowledgements(self, filename):
        self.assertEqual(
            self.json_expected(filename, "acknowledgements"),
            parser.acknowledgements(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_article_type(self, filename):
        self.assertEqual(
            self.json_expected(filename, "article_type"),
            parser.article_type(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml")
    def test_author_notes(self, filename):
        self.assertEqual(
            self.json_expected(filename, "author_notes"),
            parser.author_notes(self.soup(filename)),
        )

    @data(
        "elife-kitchen-sink.xml",
        "elife00013.xml",
        "elife_poa_e06828.xml",
        "elife02935.xml",
        "elife00270.xml",
        "elife00351.xml",
        "elife-00666.xml",
    )
    def test_authors(self, filename):
        self.assertEqual(
            self.json_expected(filename, "authors"), parser.authors(self.soup(filename))
        )

    @data("elife-kitchen-sink.xml", "elife-00666.xml")
    def test_authors_non_byline(self, filename):
        expected = self.json_expected(filename, "authors_non_byline")
        actual = parser.authors_non_byline(self.soup(filename))
        self.assertEqual(expected, actual)

    @data(
        "elife-kitchen-sink.xml",
        "elife-09215-v1.xml",
        "elife00013.xml",
        "elife-00666.xml",
    )
    def test_award_groups(self, filename):
        self.assertEqual(
            self.json_expected(filename, "award_groups"),
            parser.award_groups(self.soup(filename)),
        )

    @unpack
    @data(
        # 07383 v1 has a institution in the principal award recipient
        (
            read_fixture("test_award_groups", "content_01.xml"),
            read_fixture("test_award_groups", "content_01_expected.py"),
        ),
    )
    def test_award_groups_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.award_groups(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_category(self, filename):
        self.assertEqual(
            self.json_expected(filename, "category"),
            parser.category(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_collection_year(self, filename):
        self.assertEqual(
            self.json_expected(filename, "collection_year"),
            parser.collection_year(self.soup(filename)),
        )

    @unpack
    @data(
        ("<root></root>", None),
        (
            """
        <root>
            <pub-date pub-type="collection">
                <year>2016</year>
            </pub-date>
        </root>""",
            2016,
        ),
        (
            """
        <root>
            <pub-date date-type="collection">
                <year>2016</year>
            </pub-date>
        </root>""",
            2016,
        ),
    )
    def test_collection_year_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.collection_year(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_component_doi(self, filename):
        self.assertEqual(
            self.json_expected(filename, "component_doi"),
            parser.component_doi(self.soup(filename)),
        )

    @data(
        "elife-kitchen-sink.xml",
        "elife02304.xml",
        "elife05502.xml",
        "elife04490.xml",
        "elife-14093-v1.xml",
        "elife-00666.xml",
    )
    def test_components(self, filename):
        self.assertEqual(
            self.json_expected(filename, "components"),
            parser.components(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_conflict(self, filename):
        expected = self.json_expected(filename, "conflict")
        actual = parser.conflict(self.soup(filename))
        self.assertEqual(expected, actual)

    @data("elife-kitchen-sink.xml", "elife-02833-v2.xml", "elife-00666.xml")
    def test_contributors(self, filename):
        expected = self.json_expected(filename, "contributors")
        actual = parser.contributors(self.soup(filename))
        self.assertEqual(expected, actual)

    @data("elife-kitchen-sink.xml")
    def test_copyright_holder(self, filename):
        self.assertEqual(
            self.json_expected(filename, "copyright_holder"),
            parser.copyright_holder(self.soup(filename)),
        )

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_copyright_holder_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_holder(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", u"Alegado et al."),
        ("elife00240.xml", u"Pickett"),
        ("elife09853.xml", "Becker and Gitler"),
        ("elife02935.xml", None),
    )
    def test_copyright_holder_json(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(expected, parser.copyright_holder_json(soup))

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_copyright_holder_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_holder_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_copyright_statement(self, filename):
        self.assertEqual(
            self.json_expected(filename, "copyright_statement"),
            parser.copyright_statement(self.soup(filename)),
        )

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_copyright_statement_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_statement(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_copyright_year(self, filename):
        self.assertEqual(
            self.json_expected(filename, "copyright_year"),
            parser.copyright_year(self.soup(filename)),
        )

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_copyright_year_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_year(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_correspondence(self, filename):
        self.assertEqual(
            self.json_expected(filename, "correspondence"),
            parser.correspondence(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_digest(self, filename):
        self.assertEqual(
            self.json_expected(filename, "digest"), parser.digest(self.soup(filename))
        )

    @data("elife-kitchen-sink.xml")
    def test_display_channel(self, filename):
        self.assertEqual(
            self.json_expected(filename, "display_channel"),
            parser.display_channel(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_doi(self, filename):
        self.assertEqual(
            self.json_expected(filename, "doi"), parser.doi(self.soup(filename))
        )

    @data("elife-kitchen-sink.xml")
    def test_elocation_id(self, filename):
        self.assertEqual(
            self.json_expected(filename, "elocation_id"),
            parser.elocation_id(self.soup(filename)),
        )

    @data(
        "elife-kitchen-sink.xml",
        "elife07586.xml",
        "elife_poa_e06828.xml",
        "elife00013.xml",
    )
    def test_full_abstract(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_abstract"),
            parser.full_abstract(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_affiliation(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_affiliation"),
            parser.full_affiliation(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_award_group_funding_source(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_award_group_funding_source"),
            parser.full_award_group_funding_source(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_award_groups(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_award_groups"),
            parser.full_award_groups(self.soup(filename)),
        )

    @data(
        # edge case, no id attribute on award-group tag, and id will be generated, based on 10.1098/rsob.150230
        (
            read_fixture("test_full_award_groups", "content_01.xml"),
            read_fixture("test_full_award_groups", "content_01_expected.py"),
        ),
    )
    @unpack
    def test_full_award_groups_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_award_groups(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife-02833-v2.xml")
    def test_full_correspondence(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_correspondence"),
            parser.full_correspondence(self.soup(filename)),
        )

    @data(
        # edge case, no id attribute on corresp tag, will be empty but not cause an error, based on 10.2196/resprot.3838
        (
            "<root><article><author-notes><corresp>Corresponding Author: Elisa J Gordon<email>eg@example.org</email></corresp></author-notes></article></root>",
            {},
        ),
    )
    @unpack
    def test_full_correspondence_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup_body(soup_body(soup))
        tag_content = parser.full_correspondence(body_tag)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_full_digest(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_digest"),
            parser.full_digest(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_funding_statement(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_funding_statement"),
            parser.full_funding_statement(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_keyword_groups(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_keyword_groups"),
            parser.full_keyword_groups(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_full_keywords(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_keywords"),
            parser.full_keywords(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_license(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_license"),
            parser.full_license(self.soup(filename)),
        )

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_full_license_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_license(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_full_research_organism(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_research_organism"),
            parser.full_research_organism(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_full_subject_area(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_subject_area"),
            parser.full_subject_area(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_title(self, filename):
        self.assertEqual(
            self.json_expected(filename, "full_title"),
            parser.full_title(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_funding_statement(self, filename):
        self.assertEqual(
            self.json_expected(filename, "funding_statement"),
            parser.funding_statement(self.soup(filename)),
        )

    @data(
        "elife-kitchen-sink.xml",
        "elife00013.xml",
        "elife00240.xml",
        "elife04953.xml",
        "elife00133.xml",
    )
    def test_graphics(self, filename):
        self.assertEqual(
            self.json_expected(filename, "graphics"),
            parser.graphics(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_impact_statement(self, filename):
        self.assertEqual(
            self.json_expected(filename, "impact_statement"),
            parser.impact_statement(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_inline_graphics(self, filename):
        self.assertEqual(
            self.json_expected(filename, "inline_graphics"),
            parser.inline_graphics(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_is_poa(self, filename):
        self.assertEqual(
            self.json_expected(filename, "is_poa"), parser.is_poa(self.soup(filename))
        )

    @data("elife-kitchen-sink.xml")
    def test_journal_id(self, filename):
        self.assertEqual(
            self.json_expected(filename, "journal_id"),
            parser.journal_id(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_journal_title(self, filename):
        self.assertEqual(
            self.json_expected(filename, "journal_title"),
            parser.journal_title(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_keywords(self, filename):
        self.assertEqual(
            self.json_expected(filename, "keywords"),
            parser.keywords(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_license(self, filename):
        self.assertEqual(
            self.json_expected(filename, "license"), parser.license(self.soup(filename))
        )

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_license_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.license(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example license from 00666
        (
            read_fixture("test_license_json", "content_01.xml"),
            read_fixture("test_license_json", "content_01_expected.py"),
        ),
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
    )
    def test_license_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.license_json(soup)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_license_url(self, filename):
        self.assertEqual(
            self.json_expected(filename, "license_url"),
            parser.license_url(self.soup(filename)),
        )

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None)
    )
    @unpack
    def test_license_url_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.license_url(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data(
        "elife-kitchen-sink.xml",
        "elife02304.xml",
        "elife00007.xml",
        "elife04953.xml",
        "elife00005.xml",
        "elife05031.xml",
        "elife04493.xml",
        "elife06726.xml",
    )
    def test_media(self, filename):
        self.assertEqual(
            self.json_expected(filename, "media"), parser.media(self.soup(filename))
        )

    @unpack
    @data(
        # pub-date values from 00666 kitchen sink
        (
            read_fixture("test_pub_dates", "content_01.xml"),
            read_fixture("test_pub_dates", "content_01_expected.py"),
        ),
        # example from cstp77
        (
            read_fixture("test_pub_dates", "content_02.xml"),
            read_fixture("test_pub_dates", "content_02_expected.py"),
        ),
        # example from bmjopen-2013-003269
        (
            read_fixture("test_pub_dates", "content_03.xml"),
            read_fixture("test_pub_dates", "content_03_expected.py"),
        ),
    )
    def test_pub_dates_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_dates(soup)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_timestamp(self, filename):
        self.assertEqual(
            self.json_expected(filename, "pub_date_timestamp"),
            parser.pub_date_timestamp(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_date(self, filename):
        self.assertEqual(
            self.json_expected(filename, "pub_date_date"),
            parser.pub_date_date(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_day(self, filename):
        self.assertEqual(
            self.json_expected(filename, "pub_date_day"),
            parser.pub_date_day(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_month(self, filename):
        self.assertEqual(
            self.json_expected(filename, "pub_date_month"),
            parser.pub_date_month(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_year(self, filename):
        self.assertEqual(
            self.json_expected(filename, "pub_date_year"),
            parser.pub_date_year(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_publisher(self, filename):
        self.assertEqual(
            self.json_expected(filename, "publisher"),
            parser.publisher(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_publisher_id(self, filename):
        self.assertEqual(
            self.json_expected(filename, "publisher_id"),
            parser.publisher_id(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_received_date_date(self, filename):
        self.assertEqual(
            self.json_expected(filename, "received_date_date"),
            parser.received_date_date(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_received_date_day(self, filename):
        self.assertEqual(
            self.json_expected(filename, "received_date_day"),
            parser.received_date_day(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_received_date_month(self, filename):
        self.assertEqual(
            self.json_expected(filename, "received_date_month"),
            parser.received_date_month(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_received_date_timestamp(self, filename):
        self.assertEqual(
            self.json_expected(filename, "received_date_timestamp"),
            parser.received_date_timestamp(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_received_date_year(self, filename):
        self.assertEqual(
            self.json_expected(filename, "received_date_year"),
            parser.received_date_year(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_references(self, filename):
        # Alias of refs
        self.assertEqual(
            self.json_expected(filename, "refs"), parser.references(self.soup(filename))
        )

    @data(
        "elife-kitchen-sink.xml",
        "elife00013.xml",
        "elife02935.xml",
        "elife00051.xml",
        "elife_poa_e06828.xml",
        "elife02304.xml",
        "elife-14093-v1.xml",
    )
    def test_refs(self, filename):
        self.assertEqual(
            self.json_expected(filename, "refs"), parser.refs(self.soup(filename))
        )

    @unpack
    @data(
        # non-elife example with issue tag from cstp77
        (
            read_fixture("test_refs", "content_01.xml"),
            read_fixture("test_refs", "content_01_expected.py"),
        ),
        # mixed-citation example 1 from bmjopen
        (
            read_fixture("test_refs", "content_02.xml"),
            read_fixture("test_refs", "content_02_expected.py"),
        ),
        # mixed-citation example 2 from bmjopen
        (
            read_fixture("test_refs", "content_03.xml"),
            read_fixture("test_refs", "content_03_expected.py"),
        ),
        # mixed-citation example 3 from bmjopen
        (
            read_fixture("test_refs", "content_04.xml"),
            read_fixture("test_refs", "content_04_expected.py"),
        ),
        # citation example from redalyc - udea
        (
            read_fixture("test_refs", "content_05.xml"),
            read_fixture("test_refs", "content_05_expected.py"),
        ),
        # example of data citation with a pub-id accession, based on article 07836
        (
            read_fixture("test_refs", "content_06.xml"),
            read_fixture("test_refs", "content_06_expected.py"),
        ),
        # example of data citation with a object-id tag accession, based on article 07048
        (
            read_fixture("test_refs", "content_07.xml"),
            read_fixture("test_refs", "content_07_expected.py"),
        ),
        # example of mixed-citation with string-name, based on non-elife article
        (
            read_fixture("test_refs", "content_08.xml"),
            read_fixture("test_refs", "content_08_expected.py"),
        ),
        # example of data citation with a pub-id pub-id-type="archive", parse it as an accession number, based on 00666 kitchen sink example
        (
            read_fixture("test_refs", "content_09.xml"),
            read_fixture("test_refs", "content_09_expected.py"),
        ),
    )
    def test_refs_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.refs(soup)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_related_article(self, filename):
        self.assertEqual(
            self.json_expected(filename, "related_article"),
            parser.related_article(self.soup(filename)),
        )

    @unpack
    @data(
        (
            read_fixture("test_sub_articles", "content_01.xml"),
            read_fixture("test_sub_articles", "content_01_expected.py"),
        ),
    )
    def test_sub_articles(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.sub_articles(soup)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_related_object_ids(self, filename):
        self.assertEqual(
            self.json_expected(filename, "related_object_ids"),
            parser.related_object_ids(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_research_organism(self, filename):
        self.assertEqual(
            self.json_expected(filename, "research_organism"),
            parser.research_organism(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_self_uri(self, filename):
        self.assertEqual(
            self.json_expected(filename, "self_uri"),
            parser.self_uri(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_subject_area(self, filename):
        self.assertEqual(
            self.json_expected(filename, "subject_area"),
            parser.subject_area(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife02304.xml")
    def test_supplementary_material(self, filename):
        self.assertEqual(
            self.json_expected(filename, "supplementary_material"),
            parser.supplementary_material(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_title(self, filename):
        self.assertEqual(
            self.json_expected(filename, "title"), parser.title(self.soup(filename))
        )

    @data(
        "elife-kitchen-sink.xml", "elife00240.xml", "elife00270.xml", "elife00351.xml"
    )
    def test_title_prefix(self, filename):
        self.assertEqual(
            self.json_expected(filename, "title_prefix"),
            parser.title_prefix(self.soup(filename)),
        )

    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"></root>', None),
        (read_fixture("test_title_prefix_json", "content_01.xml"), u"Breast Cancer"),
        (
            read_fixture("test_title_prefix_json", "content_02.xml"),
            u"The Natural History of Model Organisms",
        ),
        (
            read_fixture("test_title_prefix_json", "content_03.xml"),
            u"p53 Family Proteins",
        ),
        (read_fixture("test_title_prefix_json", "content_04.xml"), u"TOR Signaling"),
        # example from elife-27438-v1.xml has no sub-display-channel and title_prefix is None
        (read_fixture("test_title_prefix_json", "content_05.xml"), None),
        # example from elife-27438-v2.xml which does have a title_prefix and it rewritten
        (read_fixture("test_title_prefix_json", "content_06.xml"), "Point of View"),
    )
    def test_title_prefix_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.title_prefix_json(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_title_short(self, filename):
        self.assertEqual(
            self.json_expected(filename, "title_short"),
            parser.title_short(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml")
    def test_title_slug(self, filename):
        self.assertEqual(
            self.json_expected(filename, "title_slug"),
            parser.title_slug(self.soup(filename)),
        )

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_volume(self, filename):
        self.assertEqual(
            self.json_expected(filename, "volume"), parser.volume(self.soup(filename))
        )

    @unpack
    @data(
        # example issue from a non-eLife article
        (read_fixture("test_issue", "content_01.xml"), "1"),
        # example of no article issue
        (read_fixture("test_issue", "content_02.xml"), None),
    )
    def test_issue(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.issue(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example fpage from a non-eLife article
        (read_fixture("test_fpage", "content_01.xml"), "1"),
        # example of no article fpage
        (read_fixture("test_fpage", "content_02.xml"), None),
    )
    def test_fpage(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.fpage(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example lpage from a non-eLife article
        (read_fixture("test_lpage", "content_01.xml"), "2"),
        # example of no article lpage
        (read_fixture("test_lpage", "content_02.xml"), None),
    )
    def test_lpage(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.lpage(soup)
        self.assertEqual(expected, tag_content)

    def test_parse_mixed_citations(self):
        data = parser.mixed_citations(self.soup("elife-kitchen-sink.xml"))
        expected = read_fixture("test_parse_mixed_citations", "content_01_expected.py")
        self.assertEqual(expected, data)

    @unpack
    @data(
        # example with no history
        (
            read_fixture("test_version_history", "content_01.xml"),
            read_fixture("test_version_history", "content_01_expected.py"),
        ),
        # example based on 00666 kitchen sink
        (
            read_fixture("test_version_history", "content_02.xml"),
            read_fixture("test_version_history", "content_02_expected.py"),
        ),
    )
    def test_version_history(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.version_history(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_clinical_trials", "content_01.xml"),
            read_fixture("test_clinical_trials", "content_01_expected.py"),
        ),
        # eLife example
        (
            read_fixture("test_clinical_trials", "content_02.xml"),
            read_fixture("test_clinical_trials", "content_02_expected.py"),
        ),
        # example with all tag attributes and a related-object tag to ignore
        (
            read_fixture("test_clinical_trials", "content_03.xml"),
            read_fixture("test_clinical_trials", "content_03_expected.py"),
        ),
    )
    def test_clinical_trials(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.clinical_trials(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("", []),
        (
            read_fixture("test_pub_history", "content_01.xml"),
            read_fixture("test_pub_history", "content_01_expected.py"),
        ),
        (
            read_fixture("test_pub_history", "content_02.xml"),
            read_fixture("test_pub_history", "content_02_expected.py"),
        ),
    )
    def test_pub_history(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_history(soup)
        self.assertEqual(expected, tag_content)


if __name__ == "__main__":
    unittest.main()
