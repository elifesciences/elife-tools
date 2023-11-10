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
from tests.file_utils import (
    sample_xml,
    json_expected_file,
    read_fixture,
    read_sample_xml,
)
from tests import soup_body


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
        # example of an appendix with no boxed-content tag wrapping the content
        (
            read_fixture("test_appendices_json", "content_06.xml"),
            read_fixture("test_appendices_json", "content_06_expected.py"),
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
        # Example of fn-group and fn tags included and ignored in footnotes_json output
        (
            read_fixture("test_footnotes_json", "content_01.xml"),
            read_fixture("test_footnotes_json", "content_01_expected.py"),
        ),
        # Test for no back tag
        ("<article/>", None),
        # Test for no fn-group tags
        ("<article><back/></article>", None),
        # Only fn-group tag with a content-type
        (
            '<article><back><fn-group content-type="competing-interest"/></back></article>',
            None,
        ),
    )
    def test_footnotes_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.footnotes_json(soup_body(soup))
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
        # test for no sub-article
        (
            "<root/>",
            OrderedDict(),
        ),
        # example from elife 00666 kitchen sink XML
        (
            read_fixture("test_editor_evaluation", "content_01.xml"),
            read_fixture("test_editor_evaluation", "content_01_expected.py"),
        ),
        # example from eLife kitchen sink 3.0
        (
            read_fixture("test_editor_evaluation", "content_02.xml"),
            read_fixture("test_editor_evaluation", "content_02_expected.py"),
        ),
    )
    def test_editor_evaluation(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.editor_evaluation(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # test for no sub-article
        (
            "<root/>",
            OrderedDict(),
        ),
        # example from elife 00666 kitchen sink XML
        (
            read_fixture("test_elife_assessment", "content_01.xml"),
            read_fixture("test_elife_assessment", "content_01_expected.py"),
        ),
        # example from eLife kitchen sink 3.0
        (
            read_fixture("test_elife_assessment", "content_02.xml"),
            read_fixture("test_elife_assessment", "content_02_expected.py"),
        ),
    )
    def test_elife_assessment(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.elife_assessment(soup)
        self.assertEqual(expected, tag_content)

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
        # test for no sub-article
        (
            "<root/>",
            [],
        ),
        # example from elife 00666 kitchen sink XML
        (
            read_fixture("test_public_reviews", "content_01.xml"),
            read_fixture("test_public_reviews", "content_01_expected.py"),
        ),
        # example from eLife kitchen sink 3.0
        (
            read_fixture("test_public_reviews", "content_02.xml"),
            read_fixture("test_public_reviews", "content_02_expected.py"),
        ),
    )
    def test_public_reviews(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.public_reviews(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # test for no sub-article
        (
            "<root/>",
            OrderedDict(),
        ),
        # example from elife 00666 kitchen sink XML
        (
            read_fixture("test_recommendations_for_authors", "content_01.xml"),
            read_fixture("test_recommendations_for_authors", "content_01_expected.py"),
        ),
        # example from eLife kitchen sink 3.0
        (
            read_fixture("test_recommendations_for_authors", "content_02.xml"),
            read_fixture("test_recommendations_for_authors", "content_02_expected.py"),
        ),
    )
    def test_recommendations_for_authors(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.recommendations_for_authors(soup)
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
        # example from eLife kitchen sink 3.0
        (
            read_fixture("test_author_response", "content_02.xml"),
            read_fixture("test_author_response", "content_02_expected.py"),
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
        # example of collab inside collab
        (
            read_fixture("test_authors_json", "content_19.xml"),
            read_fixture("test_authors_json", "content_19_expected.py"),
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
        # elife00351.xml, one author
        (
            read_fixture("test_author_line", "content_03.xml"),
            "Richard Smith",
        ),
        # elife_poa_e06828.xml, multiple authors adds et al.
        (
            read_fixture("test_author_line", "content_04.xml"),
            "Michael S Fleming, Anna Vysochan ... Wenqin Luo",
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

    @unpack
    @data(
        (None, None, None),
        (["Randy Schekman"], 2, "Randy Schekman"),
        (["Randy Schekman", "Mark Patterson"], 2, "Randy Schekman, Mark Patterson"),
        (["Randy Schekman", "Mark Patterson", "eLife"], 2, "Randy Schekman et al."),
        (["Randy Schekman", "Mark Patterson", "eLife"], 1, "Randy Schekman et al."),
        (
            ["Randy Schekman", "Mark Patterson", "eLife"],
            3,
            "Randy Schekman, Mark Patterson, eLife",
        ),
    )
    def test_format_author_line_etal(self, author_names, max_names, expected):
        self.assertEqual(
            parser.format_author_line_etal(author_names, max_names), expected
        )

    @unpack
    @data(
        (None, None, None),
        (["Randy Schekman"], 3, "Randy Schekman"),
        (["Randy Schekman", "Mark Patterson"], 3, "Randy Schekman, Mark Patterson"),
        (
            ["Randy Schekman", "Mark Patterson", "eLife"],
            3,
            "Randy Schekman, Mark Patterson, eLife",
        ),
        (["One", "Two", "Three", "Four"], 1, "One, Two ... Four"),
        (["One", "Two", "Three", "Four"], 4, "One, Two, Three, Four"),
    )
    def test_format_author_line_ellipsis(self, author_names, max_names, expected):
        self.assertEqual(
            parser.format_author_line_ellipsis(author_names, max_names), expected
        )

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
        # aff example with ror institution-id
        (
            read_fixture("test_format_aff", "content_04.xml"),
            read_fixture("test_format_aff", "content_04_expected.py"),
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
        # edge case, a group author in a sub-article
        (
            read_fixture("test_format_contributor", "content_05.xml"),
            read_fixture("test_format_contributor", "content_05_expected.py"),
        ),
        # example of anonymous author
        (
            read_fixture("test_format_contributor", "content_06.xml"),
            read_fixture("test_format_contributor", "content_06_expected.py"),
        ),
    )
    @unpack
    def test_format_contributor_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        contrib_tag = raw_parser.contributors(soup)[0]
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
        # example of ref with an elocation-id, no pages, from elife-kitchen-sink.xml
        (
            read_fixture("test_references_json", "content_49.xml"),
            read_fixture("test_references_json", "content_49_expected.py"),
        ),
        # example of ref with a strange year tag value, json_rewrite invoked, from elife-09215-v1.xml
        (
            read_fixture("test_references_json", "content_50.xml"),
            read_fixture("test_references_json", "content_50_expected.py"),
        ),
        # example of thesis ref with a doi, its uri will be populated from the doi
        (
            read_fixture("test_references_json", "content_51.xml"),
            read_fixture("test_references_json", "content_51_expected.py"),
        ),
        # example of software ref with a doi, its uri will be populated from the doi
        (
            read_fixture("test_references_json", "content_52.xml"),
            read_fixture("test_references_json", "content_52_expected.py"),
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
        # disp-quote content-type="editor-comment" excerpt block with non-paragraph blocks
        (
            read_fixture("test_body_block_content", "content_43.xml"),
            read_fixture("test_body_block_content", "content_43_expected.py"),
        ),
        # mp4 animation example
        (
            read_fixture("test_body_block_content", "content_44.xml"),
            read_fixture("test_body_block_content", "content_44_expected.py"),
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
        (
            read_fixture("test_digest_json", "content_02.xml"),
            read_fixture("test_digest_json", "content_02_expected.py"),
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
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (read_fixture("", "article_dates.xml"), "pub", ("28", "02", "2014")),
    )
    def test_ymd(self, xml_content, test_date_type, expected):
        soup = parser.parse_xml(xml_content)
        date_tag = raw_parser.pub_date(soup, date_type=test_date_type)[0]
        self.assertEqual(expected, parser.ymd(date_tag))

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (read_fixture("", "article_dates.xml"), "received", date_struct(2012, 6, 22)),
        (read_fixture("", "article_dates.xml"), None, None),
        (read_fixture("", "article_dates.xml"), "not_a_date_type", None),
    )
    def test_history_date(self, xml_content, date_type, expected):
        soup = parser.parse_xml(xml_content)
        self.assertEqual(expected, parser.history_date(soup, date_type))

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
    def test_journal_issn(self, xml_content, pub_format, pub_type, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.journal_issn(
            soup_body(soup), pub_format=pub_format, pub_type=pub_type
        )
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            None,
        ),
        (
            read_fixture("test_author_contributions", "content_01.xml"),
            read_fixture("test_author_contributions", "content_01_expected.py"),
        ),
    )
    def test_author_contributions(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.author_contributions(soup, "con")
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            # snippet from elife-kitchen-sink.xml
            read_fixture("test_competing_interests", "content_01.xml"),
            read_fixture("test_competing_interests", "content_01_expected.py"),
        ),
        (
            # snippet from elife00190.xml
            read_fixture("test_competing_interests", "content_02.xml"),
            read_fixture("test_competing_interests", "content_02_expected.py"),
        ),
        (
            # snippet from elife-00666.xml
            read_fixture("test_competing_interests", "content_03.xml"),
            read_fixture("test_competing_interests", "content_03_expected.py"),
        ),
    )
    def test_competing_interests(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.competing_interests(soup, ["conflict", "COI-statement"])
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no author notes
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_author_notes.xml"),
            read_fixture("test_full_author_notes", "content_01_expected.py"),
        ),
    )
    def test_full_author_notes(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_author_notes(soup)
        self.assertEqual(expected, tag_content)

    """
    Functions that only need soup to test them against json output
    """

    @unpack
    @data(
        # example with no abstracts, such as a correction article
        (
            "<article/>",
            [],
        ),
        # example with an empty abstract, a correction article in accepted submission format
        (
            "<article><abstract><p/></abstract></article>",
            [{"abstract_type": None, "content": "", "full_content": ""}],
        ),
        # example from elife00013.xml
        (
            read_sample_xml("elife00013.xml"),
            read_fixture("test_abstracts", "content_02_expected.py"),
        ),
        # example from elife_poa_e06828.xml
        (
            read_sample_xml("elife_poa_e06828.xml"),
            read_fixture("test_abstracts", "content_03_expected.py"),
        ),
    )
    def test_abstracts(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstracts(soup)
        self.assertEqual(expected, tag_content)

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
        # example with no abstract, such as a correction article
        (
            "<article/>",
            None,
        ),
        # example with an empty abstract, a correction article in accepted submission format
        (
            "<article><abstract><p/></abstract></article>",
            "",
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

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            "July 18, 2012",
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_accepted_date_date(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.accepted_date_date(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            18,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_accepted_date_day(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.accepted_date_day(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            7,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_accepted_date_month(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.accepted_date_month(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            1342569600,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_accepted_date_timestamp(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.accepted_date_timestamp(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            2012,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_accepted_date_year(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.accepted_date_year(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no data
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            """Acknowledgements
We thank Michael Fischbach, Richard Losick, and Russell Vance for critical reading of
                the manuscript. NK is a Fellow in the Integrated Microbial Biodiversity Program of
                the Canadian Institute for Advanced Research.""",
        ),
    )
    def test_ack(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.ack(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no data
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            """Acknowledgements
We thank Michael Fischbach, Richard Losick, and Russell Vance for critical reading of
                the manuscript. NK is a Fellow in the Integrated Microbial Biodiversity Program of
                the Canadian Institute for Advanced Research.""",
        ),
    )
    def test_acknowledgements(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.acknowledgements(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            (
                '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                'xmlns:xlink="http://www.w3.org/1999/xlink" '
                'article-type="research-article" dtd-version="1.1d3">'
            ),
            "research-article",
        ),
    )
    def test_article_type(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.article_type(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no author notes
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_author_notes.xml"),
            [
                "\n†\nThese authors contributed equally to this work\n",
                "\n‡\nThese authors also contributed equally to this work\n",
                "\n**\nDeceased\n",
            ],
        ),
    )
    def test_author_notes(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.author_notes(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_authors", "content_01_expected.py"),
        ),
        (
            sample_xml("elife00013.xml"),
            read_fixture("test_authors", "content_02_expected.py"),
        ),
        (
            sample_xml("elife_poa_e06828.xml"),
            read_fixture("test_authors", "content_03_expected.py"),
        ),
        (
            sample_xml("elife02935.xml"),
            read_fixture("test_authors", "content_04_expected.py"),
        ),
        (
            sample_xml("elife00270.xml"),
            read_fixture("test_authors", "content_05_expected.py"),
        ),
        (
            sample_xml("elife00351.xml"),
            read_fixture("test_authors", "content_06_expected.py"),
        ),
        (
            sample_xml("elife-00666.xml"),
            read_fixture("test_authors", "content_07_expected.py"),
        ),
    )
    def test_authors(self, filename, expected):
        soup = parser.parse_document(filename)
        tag_content = parser.authors(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_authors_non_byline", "content_01_expected.py"),
        ),
        (
            read_sample_xml("elife-00666.xml"),
            read_fixture("test_authors_non_byline", "content_02_expected.py"),
        ),
    )
    def test_authors_non_byline(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.authors_non_byline(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # 07383 v1 has a institution in the principal award recipient
        (
            read_fixture("test_award_groups", "content_01.xml"),
            read_fixture("test_award_groups", "content_01_expected.py"),
        ),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("test_award_groups", "content_02.xml"),
            read_fixture("test_award_groups", "content_02_expected.py"),
        ),
        # example from elife-09215-v1.xml
        (
            read_fixture("test_award_groups", "content_03.xml"),
            read_fixture("test_award_groups", "content_03_expected.py"),
        ),
        # example from elife00013.xml
        (
            read_fixture("test_award_groups", "content_04.xml"),
            read_fixture("test_award_groups", "content_04_expected.py"),
        ),
        # example from elife-00666.xml
        (
            read_fixture("test_award_groups", "content_05.xml"),
            read_fixture("test_award_groups", "content_05_expected.py"),
        ),
        # funding DOI example
        (
            read_fixture("test_award_groups", "content_06.xml"),
            read_fixture("test_award_groups", "content_06_expected.py"),
        ),
    )
    def test_award_groups(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.award_groups(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            ["Cell biology", "Computational and systems biology"],
        ),
    )
    def test_category(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.category(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            2014,
        ),
        # poa XML has no collection date
        (
            "<article/>",
            None,
        ),
    )
    def test_collection_year(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.collection_year(soup)
        self.assertEqual(expected, tag_content)

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

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_component_doi", "content_01_expected.py"),
        ),
    )
    def test_component_doi(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.component_doi(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_components", "content_01_expected.py"),
        ),
        (
            sample_xml("elife02304.xml"),
            read_fixture("test_components", "content_02_expected.py"),
        ),
        (
            sample_xml("elife05502.xml"),
            read_fixture("test_components", "content_03_expected.py"),
        ),
        (
            sample_xml("elife04490.xml"),
            read_fixture("test_components", "content_04_expected.py"),
        ),
        (
            sample_xml("elife-14093-v1.xml"),
            read_fixture("test_components", "content_05_expected.py"),
        ),
        (
            sample_xml("elife-00666.xml"),
            read_fixture("test_components", "content_06_expected.py"),
        ),
    )
    def test_components(self, filename, expected):
        soup = parser.parse_document(filename)
        tag_content = parser.components(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("test_conflict", "content_01.xml"),
            read_fixture("test_conflict", "content_01_expected.py"),
        ),
    )
    def test_conflict(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.conflict(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_contributors", "content_01_expected.py"),
        ),
        # example from elife-02833-v2.xml
        (
            read_sample_xml("elife-02833-v2.xml"),
            read_fixture("test_contributors", "content_02_expected.py"),
        ),
        # example from elife-00666.xml
        (
            read_sample_xml("elife-00666.xml"),
            read_fixture("test_contributors", "content_03_expected.py"),
        ),
    )
    def test_contributors(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.contributors(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_contributors", "content_04.xml"),
            read_fixture("test_contributors", "content_04_expected.py"),
        ),
    )
    def test_contributors_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.contributors(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            "Alegado et al",
        ),
    )
    @unpack
    def test_copyright_holder(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_holder(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            "Alegado et al.",
        ),
        # example from elife00240.xml
        (
            read_fixture("test_copyright_holder_json", "content_01.xml"),
            "Pickett",
        ),
        # example from elife09853.xml
        (
            read_fixture("test_copyright_holder_json", "content_02.xml"),
            "Becker and Gitler",
        ),
        # example from elife02935.xml which is CC0 license
        (
            read_fixture("test_copyright_holder_json", "content_03.xml"),
            None,
        ),
    )
    @unpack
    def test_copyright_holder_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_holder_json(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            "© 2012, Alegado et al",
        ),
    )
    @unpack
    def test_copyright_statement(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_statement(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            2012,
        ),
    )
    @unpack
    def test_copyright_year_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.copyright_year(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no author notes
        (
            "<article/>",
            [],
        ),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_author_notes.xml"),
            [
                "*For correspondence: jon_clardy@hms.harvard.edu(JC);",
                "nking@berkeley.edu(NK);",
                "mharrison@elifesciences.org(MH)",
            ],
        ),
    )
    def test_correspondence(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.correspondence(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no abstracts, such as a correction article
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_digest", "content_01_expected.py"),
        ),
        # example from elife_poa_e06828.xml
        (read_sample_xml("elife_poa_e06828.xml"), None),
        # example of plain-language-summary
        (
            (
                "<article>"
                '<abstract abstract-type="plain-language-summary">'
                "<title>eLife digest</title><p>Paragraph.</p>"
                "</abstract>"
                "</article>"
            ),
            "Paragraph.",
        ),
    )
    def test_digest(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.digest(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            ["Research article"],
        ),
    )
    def test_display_channel(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.display_channel(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (read_fixture("", "article_meta.xml"), "10.7554/eLife.00013"),
        # example from elife-1234567890-v2.xml
        (read_fixture("", "article_meta_v2.xml"), "10.7554/eLife.1234567890"),
    )
    def test_doi(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.doi(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (read_fixture("", "article_meta.xml"), None),
        # example from elife-1234567890-v2.xml
        (read_fixture("", "article_meta_v2.xml"), "10.7554/eLife.1234567890.4"),
    )
    def test_version_doi(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.version_doi(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (read_fixture("", "article_meta.xml"), "e00013"),
    )
    @data("elife-kitchen-sink.xml")
    def test_elocation_id(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.elocation_id(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no abstracts, such as a correction article
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_full_abstract", "content_01_expected.py"),
        ),
        # example from elife00013.xml
        (
            read_sample_xml("elife00013.xml"),
            read_fixture("test_full_abstract", "content_02_expected.py"),
        ),
        # example from elife_poa_e06828.xml
        (
            read_sample_xml("elife_poa_e06828.xml"),
            read_fixture("test_full_abstract", "content_03_expected.py"),
        ),
    )
    def test_full_abstract(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_abstract(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no affs
        (
            "<article/>",
            [],
        ),
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_full_affiliation", "content_01_expected.py"),
        ),
    )
    def test_full_affiliation(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_affiliation(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # elife-kitchen-sink.xml example
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture(
                "test_full_award_group_funding_source", "content_01_expected.py"
            ),
        ),
    )
    @unpack
    def test_full_award_group_funding_source(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_award_group_funding_source(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no id attribute on award-group tag, and id will be generated, based on 10.1098/rsob.150230
        (
            read_fixture("test_full_award_groups", "content_01.xml"),
            read_fixture("test_full_award_groups", "content_01_expected.py"),
        ),
        # elife-kitchen-sink.xml example
        (
            read_fixture("test_full_award_groups", "content_02.xml"),
            read_fixture("test_full_award_groups", "content_02_expected.py"),
        ),
        # funding DOI example
        (
            read_fixture("test_full_award_groups", "content_03.xml"),
            read_fixture("test_full_award_groups", "content_03_expected.py"),
        ),
    )
    @unpack
    def test_full_award_groups(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_award_groups(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no id attribute on corresp tag, will be empty but not cause an error, based on 10.2196/resprot.3838
        (
            "<article><author-notes><corresp>Corresponding Author: Elisa J Gordon<email>eg@example.org</email></corresp></author-notes></article>",
            {},
        ),
        # example with no author notes
        (
            "<article/>",
            {},
        ),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_author_notes.xml"),
            {
                "cor1": ["jon_clardy@hms.harvard.edu"],
                "cor2": ["nking@berkeley.edu"],
                "cor3": ["mharrison@elifesciences.org"],
            },
        ),
        # example elife-02833-v2.xml
        (
            read_sample_xml("elife-02833-v2.xml"),
            {
                "cor1": ["kingston@molbio.mgh.harvard.edu"],
                "cor2": ["(+1) 617-432-1906"],
            },
        ),
    )
    @unpack
    def test_full_correspondence(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_correspondence(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no abstracts, such as a correction article
        (
            "<article/>",
            None,
        ),
        # example from elife-kitchen-sink.xml
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_full_digest", "content_01_expected.py"),
        ),
        # example from elife_poa_e06828.xml
        (read_sample_xml("elife_poa_e06828.xml"), None),
        # example of plain-language-summary
        (
            (
                "<article>"
                '<abstract abstract-type="plain-language-summary">'
                "<title>eLife digest</title><p>Paragraph.</p>"
                "</abstract>"
                "</article>"
            ),
            "<p>Paragraph.</p>",
        ),
    )
    def test_full_digest(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_digest(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("test_full_funding_statement", "content_01.xml"),
            read_fixture("test_full_funding_statement", "content_01_expected.py"),
        ),
    )
    def test_full_funding_statement(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_funding_statement(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            {},
        ),
        (
            read_fixture("", "article_meta.xml"),
            {
                "author-keywords": [
                    "<italic>Salpingoeca rosetta</italic>",
                    "Algoriphagus",
                    "bacterial sulfonolipid",
                    "multicellular development",
                ],
                "research-organism": ["Mouse", "<italic>C. elegans</italic>", "Other"],
            },
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            {
                "author-keywords": [
                    "neurotrophins",
                    "RET signaling",
                    "DRG neuron development",
                    "cis and trans activation",
                ],
                "research-organism": ["Mouse"],
            },
        ),
    )
    def test_full_keyword_groups(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_keyword_groups(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            [
                "<italic>Salpingoeca rosetta</italic>",
                "Algoriphagus",
                "bacterial sulfonolipid",
                "multicellular development",
            ],
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            [
                "neurotrophins",
                "RET signaling",
                "DRG neuron development",
                "cis and trans activation",
            ],
        ),
    )
    def test_full_keywords(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_keywords(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            (
                "This article is distributed under the terms of the "
                '<ext-link ext-link-type="uri" '
                'xlink:href="http://creativecommons.org/licenses/by/4.0/">'
                "Creative Commons Attribution License</ext-link>, which permits "
                "unrestricted use and redistribution provided that the original "
                "author and source are credited."
            ),
        ),
    )
    @unpack
    def test_full_license(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_license(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            ["Mouse", "<italic>C. elegans</italic>", "Other"],
        ),
    )
    def test_full_research_organism(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_research_organism(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            {},
        ),
        (
            read_fixture("", "article_meta.xml"),
            {
                "display-channel": ["Research article"],
                "heading": ["Cell biology", "Computational and systems biology"],
            },
        ),
    )
    def test_full_subject_area(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_subject_area(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            (
                "Bacterial regulation of colony development in the closest "
                "living relatives of animals"
            ),
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            (
                "<italic>Cis</italic> and <italic>trans</italic> RET signaling control the "
                "survival and central projection growth of rapidly adapting mechanoreceptors"
            ),
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_full_title(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.full_title(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("test_funding_statement", "content_01.xml"),
            read_fixture("test_funding_statement", "content_01_expected.py"),
        ),
    )
    def test_funding_statement(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.funding_statement(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_graphics", "content_01_expected.py"),
        ),
        (
            sample_xml("elife00013.xml"),
            read_fixture("test_graphics", "content_02_expected.py"),
        ),
        (
            sample_xml("elife00240.xml"),
            read_fixture("test_graphics", "content_03_expected.py"),
        ),
        (
            sample_xml("elife04953.xml"),
            read_fixture("test_graphics", "content_04_expected.py"),
        ),
        (
            sample_xml("elife00133.xml"),
            read_fixture("test_graphics", "content_05_expected.py"),
        ),
    )
    def test_graphics(self, filename, expected):
        soup = parser.parse_document(filename)
        tag_content = parser.graphics(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            "",
        ),
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            "The chemical nature of RIF-1 may reveal a new class of bacterial signaling molecules.",
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            "",
        ),
    )
    def test_impact_statement(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.impact_statement(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_inline_graphics", "content_01_expected.py"),
        ),
        (
            sample_xml("elife00240.xml"),
            read_fixture("test_inline_graphics", "content_02_expected.py"),
        ),
    )
    def test_inline_graphics(self, filename, expected):
        soup = parser.parse_document(filename)
        tag_content = parser.inline_graphics(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            True,
        ),
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            False,
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            True,
        ),
    )
    def test_is_poa(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.is_poa(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            "eLife",
        ),
    )
    def test_journal_id(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.journal_id(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            "eLife",
        ),
    )
    def test_journal_title(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.journal_title(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            [
                "Salpingoeca rosetta",
                "Algoriphagus",
                "bacterial sulfonolipid",
                "multicellular development",
            ],
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            [
                "neurotrophins",
                "RET signaling",
                "DRG neuron development",
                "cis and trans activation",
            ],
        ),
    )
    def test_keywords(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.keywords(soup)
        self.assertEqual(expected, tag_content)

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            (
                "This article is distributed under the terms of the "
                "Creative Commons Attribution License, which permits "
                "unrestricted use and redistribution provided that "
                "the original author and source are credited."
            ),
        ),
    )
    @unpack
    def test_license(self, xml_content, expected):
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

    @data(
        # edge case, no permissions tag
        ("<root><article></article></root>", None),
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_permissions.xml"),
            ("http://creativecommons.org/licenses/by/4.0/"),
        ),
    )
    @unpack
    def test_license_url(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.license_url(soup_body(soup))
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_media", "content_01_expected.py"),
        ),
        (
            sample_xml("elife02304.xml"),
            read_fixture("test_media", "content_02_expected.py"),
        ),
        (
            sample_xml("elife00007.xml"),
            read_fixture("test_media", "content_03_expected.py"),
        ),
        (
            sample_xml("elife04953.xml"),
            read_fixture("test_media", "content_04_expected.py"),
        ),
        (
            sample_xml("elife00005.xml"),
            read_fixture("test_media", "content_05_expected.py"),
        ),
        (
            sample_xml("elife05031.xml"),
            read_fixture("test_media", "content_06_expected.py"),
        ),
        (
            sample_xml("elife04493.xml"),
            read_fixture("test_media", "content_07_expected.py"),
        ),
        (
            sample_xml("elife06726.xml"),
            read_fixture("test_media", "content_08_expected.py"),
        ),
    )
    def test_media(self, filename, expected):
        soup = parser.parse_document(filename)
        tag_content = parser.media(soup)
        self.assertEqual(expected, tag_content)

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

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            1393545600,
        ),
        # poa XML before pub-date is added
        (
            "<article/>",
            None,
        ),
    )
    def test_pub_date_timestamp(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_date_timestamp(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            "February 28, 2014",
        ),
        # poa XML before pub-date is added
        (
            "<article/>",
            None,
        ),
    )
    def test_pub_date_date(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_date_date(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            28,
        ),
        # poa XML before pub-date is added
        (
            "<article/>",
            None,
        ),
    )
    def test_pub_date_day(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_date_day(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            2,
        ),
        # poa XML before pub-date is added
        (
            "<article/>",
            None,
        ),
    )
    def test_pub_date_month(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_date_month(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            2014,
        ),
        # poa XML before pub-date is added
        (
            "<article/>",
            None,
        ),
    )
    def test_pub_date_year(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_date_year(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            "eLife Sciences Publications, Ltd",
        ),
    )
    def test_publisher(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.publisher(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            "00013",
        ),
    )
    def test_publisher_id(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.publisher_id(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            "June 22, 2012",
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_received_date_date(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.received_date_date(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            22,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_received_date_day(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.received_date_day(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            6,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_received_date_month(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.received_date_month(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            1340323200,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_received_date_timestamp(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.received_date_timestamp(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # snippet of XML from elife-kitchen-sink.xml
        (
            read_fixture("", "article_dates.xml"),
            2012,
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_received_date_year(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.received_date_year(soup)
        self.assertEqual(expected, tag_content)

    def test_references(self):
        # Alias of refs
        soup = parser.parse_xml("<article/>")
        self.assertEqual(parser.references(soup), [])

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
        # example of citation with a pub-id pub-id-type="pmid", from elife-kitchen-sink.xml
        (
            read_fixture("test_refs", "content_10.xml"),
            read_fixture("test_refs", "content_10_expected.py"),
        ),
        # example of person-group with a collab, from elife-kitchen-sink.xml
        (
            read_fixture("test_refs", "content_11.xml"),
            read_fixture("test_refs", "content_11_expected.py"),
        ),
    )
    def test_refs_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.refs(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            [
                {
                    "ext_link_type": "doi",
                    "related_article_type": "commentary",
                    "xlink_href": None,
                }
            ],
        ),
    )
    def test_related_article(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.related_article(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_fixture("test_sub_articles", "content_01.xml"),
            read_fixture("test_sub_articles", "content_01_expected.py"),
        ),
        # editor evaluation sub-article parsing
        (
            read_fixture("test_sub_articles", "content_02.xml"),
            read_fixture("test_sub_articles", "content_02_expected.py"),
        ),
    )
    def test_sub_articles(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.sub_articles(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            {"dataro1": {}, "dataro2": {}, "dataro3": {}},
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            {},
        ),
    )
    def test_related_object_ids(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.related_object_ids(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            ["Mouse", "C. elegans", "Other"],
        ),
    )
    def test_research_organism(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.research_organism(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            [{"content-type": "pdf", "type": "self-uri", "position": 1, "ordinal": 1}],
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            [],
        ),
    )
    def test_self_uri(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.self_uri(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (
            "<article/>",
            [],
        ),
        (
            read_fixture("", "article_meta.xml"),
            ["Research article", "Cell biology", "Computational and systems biology"],
        ),
    )
    def test_subject_area(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.subject_area(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no data
        (
            "<article/>",
            [],
        ),
        (
            read_sample_xml("elife-kitchen-sink.xml"),
            read_fixture("test_supplementary_material", "content_01_expected.py"),
        ),
        (
            read_sample_xml("elife02304.xml"),
            read_fixture("test_supplementary_material", "content_02_expected.py"),
        ),
    )
    def test_supplementary_material(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.supplementary_material(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            (
                "Bacterial regulation of colony development in the closest "
                "living relatives of animals"
            ),
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_title(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.title(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example with no title prefix
        (
            read_fixture("test_title_prefix", "content_01.xml"),
            read_fixture("test_title_prefix", "content_01_expected.py"),
        ),
        # example from elife00240.xml
        (
            read_fixture("test_title_prefix", "content_02.xml"),
            read_fixture("test_title_prefix", "content_02_expected.py"),
        ),
        # example from elife00270.xml
        (
            read_fixture("test_title_prefix", "content_03.xml"),
            read_fixture("test_title_prefix", "content_03_expected.py"),
        ),
        # example from elife00351.xml
        (
            read_fixture("test_title_prefix", "content_04.xml"),
            read_fixture("test_title_prefix", "content_04_expected.py"),
        ),
    )
    def test_title_prefix(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.title_prefix(soup)
        self.assertEqual(expected, tag_content)

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

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (read_fixture("", "article_meta.xml"), "Bacterial regulation"),
    )
    @data("elife-kitchen-sink.xml")
    def test_title_short(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.title_short(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            "bacterial-regulation-of-colony-development-in-the-closest-living-relatives-of-animals",
        ),
    )
    @data("elife-kitchen-sink.xml")
    def test_title_slug(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.title_slug(soup)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example from elife-kitchen-sink.xml
        (
            read_fixture("", "article_meta.xml"),
            "3",
        ),
        (
            read_sample_xml("elife_poa_e06828.xml"),
            None,
        ),
    )
    def test_volume(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.volume(soup)
        self.assertEqual(expected, tag_content)

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
        (
            read_fixture("test_pub_history", "content_03.xml"),
            read_fixture("test_pub_history", "content_03_expected.py"),
        ),
        (
            read_fixture("test_pub_history", "content_04.xml"),
            read_fixture("test_pub_history", "content_04_expected.py"),
        ),
    )
    def test_pub_history(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_history(soup)
        self.assertEqual(expected, tag_content)


if __name__ == "__main__":
    unittest.main()
