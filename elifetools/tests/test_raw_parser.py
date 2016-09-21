import os, unittest
from ddt import ddt, data, unpack
import bs4

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser
import rawJATS as raw_parser

from file_utils import sample_xml

@ddt
class TestJatsParser(unittest.TestCase):
    def setUp(self):
        self.kitchen_sink_xml = sample_xml('elife-kitchen-sink.xml')
        self.xml = sample_xml('elife00013.xml')
        self.soup = parser.parse_document(self.kitchen_sink_xml)

    def tearDown(self):
        self.soup = None

    def test_quickly(self):
        struct = [
            (parser.doi, u"10.7554/eLife.00013"),
            (parser.journal_id, u"eLife"),
            (parser.journal_title, u"eLife"),
            #(parser.journal_issn, u"2050-084X"),
            (parser.publisher, u"eLife Sciences Publications, Ltd"),
        ]
        for func, expected in struct:
            soup = parser.parse_document(self.kitchen_sink_xml)
            got = func(soup)
            try:

                self.assertEqual(got, expected)
            except AssertionError:
                print 'failed on', func, 'expected', expected, 'got', got
                raise
        soup = parser.parse_document(self.kitchen_sink_xml)
        self.assertEqual(parser.journal_issn(soup, pub_format="electronic"), u"2050-084X")

    def test_quickly2(self):
        soup = parser.parse_document(self.xml)
        self.assertEqual(raw_parser.article_type(soup), "research-article")


    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", bs4.element.Tag),
        ("elife07586.xml", bs4.element.Tag)
    )
    def test_back(self, filename, expected_type):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(type(raw_parser.back(soup)), expected_type)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 2),
        ("elife_poa_e06828.xml", 1),
        ("elife07586.xml", 0)
    )
    def test_abstract(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.abstract(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 3),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 1)
    )
    def test_body(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.body(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", type(None)),
        ("elife07586.xml", bs4.element.Tag)
    )
    def test_article_body(self, filename, expected_type):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(type(raw_parser.article_body(soup)), expected_type)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 2),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0)
    )
    def test_sub_article(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.sub_article(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", type(None)),
        ("elife07586.xml", type(None))
    )
    def test_decision_letter(self, filename, expected_type):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(type(raw_parser.decision_letter(soup)), expected_type)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", type(None)),
        ("elife07586.xml", type(None))
    )
    def test_author_response(self, filename, expected_type):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(type(raw_parser.author_response(soup)), expected_type)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 25),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0)
    )
    def test_section(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.section(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 176),
        ("elife_poa_e06828.xml", 3),
        ("elife07586.xml", 5)
    )
    def test_paragraph(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.paragraph(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 4),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0)
    )
    def test_table(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.table(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 2),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0)
    )
    def test_table_wrap_foot(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.table_wrap_foot(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 6),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0)
    )
    def test_disp_formula(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.disp_formula(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 20),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0)
    )
    def test_math(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.math(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 4),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 1)
    )
    def test_boxed_text(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.boxed_text(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 25),
        ("elife_poa_e06828.xml", 0)
    )
    def test_fig(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.fig(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 3),
        ("elife_poa_e06828.xml", 0)
    )
    def test_fig_group(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.fig_group(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, 2),
        ("elife-kitchen-sink.xml", "executive-summary", 1),
        ("elife_poa_e06828.xml", None, 1),
        ("elife_poa_e06828.xml", "executive-summary", 0)
    )
    def test_abstract_with_abstract_type(self, filename, abstract_type, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.abstract(soup, abstract_type)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 0),
        ("elife-02833-v2.xml", 1)
    )
    def test_list(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.list(soup)), expected_len)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", 0),
        ("elife-02833-v2.xml", 4)
    )
    def test_list_item(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(raw_parser.list_item(soup)), expected_len)



if __name__ == '__main__':
    unittest.main()
