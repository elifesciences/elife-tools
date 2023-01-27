import os
import unittest
import bs4
from ddt import ddt, data, unpack
from elifetools import parseJATS as parser
from elifetools import rawJATS as raw_parser
from tests.file_utils import sample_xml, read_fixture


CACHED_SOUP_MAP = {}


def get_cached_soup(filename):
    if filename not in CACHED_SOUP_MAP:
        CACHED_SOUP_MAP[filename] = parser.parse_document(sample_xml(filename))
    return CACHED_SOUP_MAP[filename]


@ddt
class TestJatsParser(unittest.TestCase):
    def setUp(self):
        self.kitchen_sink_xml = sample_xml("elife-kitchen-sink.xml")
        self.xml = sample_xml("elife00013.xml")

    def tearDown(self):
        pass

    def test_quickly(self):
        struct = [
            (parser.doi, u"10.7554/eLife.00013"),
            (parser.journal_id, u"eLife"),
            (parser.journal_title, u"eLife"),
            (parser.journal_issn, u"2050-084X"),
            (parser.publisher, u"eLife Sciences Publications, Ltd"),
        ]
        for func, expected in struct:
            soup = parser.parse_document(self.kitchen_sink_xml)
            got = func(soup)
            try:

                self.assertEqual(got, expected)
            except AssertionError:
                print("failed on", func, "expected", expected, "got", got)
                raise
        soup = parser.parse_document(self.kitchen_sink_xml)
        self.assertEqual(
            parser.journal_issn(soup, pub_format="electronic"), u"2050-084X"
        )

    def test_quickly2(self):
        soup = parser.parse_document(self.xml)
        self.assertEqual(raw_parser.article_type(soup), "research-article")

    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", bs4.element.Tag),
        ("elife07586.xml", bs4.element.Tag),
    )
    def test_back(self, filename, expected_type):
        soup = get_cached_soup(filename)
        self.assertEqual(type(raw_parser.back(soup)), expected_type)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 2),
        ("elife_poa_e06828.xml", 1),
        ("elife07586.xml", 0),
    )
    def test_abstract(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.abstract(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 4),
        ("elife_poa_e06828.xml", 2),
        ("elife07586.xml", 2),
    )
    def test_article_id(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.article_id(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 1),
        ("elife_poa_e06828.xml", 1),
        ("elife07586.xml", 1),
    )
    def test_meta_article_id(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.meta_article_id(soup, "doi")), expected_len)

    @unpack
    @data(
        (
            "elife-kitchen-sink.xml",
            '<article-id pub-id-type="doi">10.7554/eLife.00013</article-id>',
        ),
        (
            "elife_poa_e06828.xml",
            '<article-id pub-id-type="doi">10.7554/eLife.06828</article-id>',
        ),
        (
            "elife07586.xml",
            '<article-id pub-id-type="doi">10.7554/eLife.07586</article-id>',
        ),
    )
    def test_doi(self, filename, expected):
        soup = get_cached_soup(filename)
        self.assertEqual(str(raw_parser.doi(soup)), expected)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", "None"),
        ("elife_poa_e06828.xml", "None"),
        ("elife07586.xml", "None"),
    )
    def test_version_doi(self, filename, expected):
        soup = get_cached_soup(filename)
        self.assertEqual(str(raw_parser.version_doi(soup)), expected)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 3),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 1),
    )
    def test_body(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.body(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", type(None)),
        ("elife07586.xml", bs4.element.Tag),
    )
    def test_article_body(self, filename, expected_type):
        soup = get_cached_soup(filename)
        self.assertEqual(type(raw_parser.article_body(soup)), expected_type)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 2),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0),
    )
    def test_sub_article(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.sub_article(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", type(None)),
        ("elife07586.xml", type(None)),
        ("elife-00666.xml", bs4.element.Tag),
    )
    def test_decision_letter(self, filename, expected_type):
        soup = get_cached_soup(filename)
        self.assertEqual(type(raw_parser.decision_letter(soup)), expected_type)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", bs4.element.Tag),
        ("elife_poa_e06828.xml", type(None)),
        ("elife07586.xml", type(None)),
    )
    def test_author_response(self, filename, expected_type):
        soup = get_cached_soup(filename)
        self.assertEqual(type(raw_parser.author_response(soup)), expected_type)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 25),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0),
    )
    def test_section(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.section(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 177),
        ("elife_poa_e06828.xml", 3),
        ("elife07586.xml", 5),
    )
    def test_paragraph(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.paragraph(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 4),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0),
    )
    def test_table(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.table(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 2),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0),
    )
    def test_table_wrap_foot(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.table_wrap_foot(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 6),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0),
    )
    def test_disp_formula(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.disp_formula(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 20),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 0),
    )
    def test_math(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.math(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", 4),
        ("elife_poa_e06828.xml", 0),
        ("elife07586.xml", 1),
    )
    def test_boxed_text(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.boxed_text(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 25), ("elife_poa_e06828.xml", 0))
    def test_fig(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.fig(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 3), ("elife_poa_e06828.xml", 0))
    def test_fig_group(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.fig_group(soup)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, 2),
        ("elife-kitchen-sink.xml", "executive-summary", 1),
        ("elife_poa_e06828.xml", None, 1),
        ("elife_poa_e06828.xml", "executive-summary", 0),
    )
    def test_abstract_with_abstract_type(self, filename, abstract_type, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.abstract(soup, abstract_type)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 0), ("elife-02833-v2.xml", 1))
    def test_list(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.list(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 0), ("elife-02833-v2.xml", 4))
    def test_list_item(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.list_item(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", "doi", 78), ("elife-kitchen-sink.xml", None, 79))
    def test_pub_id_doi(self, filename, pub_id_type, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.pub_id(soup, pub_id_type)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", "uri", 7), ("elife-kitchen-sink.xml", None, 47))
    def test_pub_id_uri(self, filename, ext_link_type, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.ext_link(soup, ext_link_type)), expected_len)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", "ethics-information", 1),
        ("elife-kitchen-sink.xml", None, 3),
    )
    def test_fn_group(self, filename, content_type, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.fn_group(soup, content_type)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 1))
    def test_app_group(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.app_group(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 2))
    def test_app(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.app(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 1))
    def test_funding_group(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.funding_group(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 7))
    def test_award_group(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.award_group(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 7))
    def test_principal_award_recipient(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.principal_award_recipient(soup)), expected_len)

    @unpack
    @data(("elife-kitchen-sink.xml", 1))
    def test_mixed_citations(self, filename, expected_len):
        soup = get_cached_soup(filename)
        self.assertEqual(len(raw_parser.mixed_citations(soup)), expected_len)

    @unpack
    @data(
        (read_fixture("test_pub_history", "content_01.xml"), 1),
    )
    def test_pub_history(self, xml_content, expected_len):
        soup = parser.parse_xml(xml_content)
        self.assertEqual(len(raw_parser.pub_history(soup)), expected_len)

    @unpack
    @data(
        (read_fixture("test_pub_history", "content_01.xml"), 1),
    )
    def test_raw_event(self, xml_content, expected_len):
        soup = parser.parse_xml(xml_content)
        self.assertEqual(len(raw_parser.event(soup)), expected_len)

    @unpack
    @data(
        (read_fixture("test_pub_history", "content_01.xml"), 1),
    )
    def test_event_desc(self, xml_content, expected_len):
        soup = parser.parse_xml(xml_content)
        self.assertEqual(len(raw_parser.event_desc(soup)), expected_len)


# some XML content for testing sub-article parsing functions
SUB_ARTICLE_XML_CONTENT = read_fixture("", "sub_articles.xml")


class TestFilterSubArticles(unittest.TestCase):
    def setUp(self):
        # sample data with a variety of XML data with an abbreviated structure for testing
        soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)
        self.nodes = raw_parser.sub_article(soup)

    def test_filter_none(self):
        expected_len = 0
        self.assertEqual(
            len(raw_parser.filter_sub_articles_by_title(None)), expected_len
        )

    def test_filter_blank(self):
        expected_len = 0
        self.assertEqual(len(raw_parser.filter_sub_articles_by_title([])), expected_len)

    def test_filter_no_article_title(self):
        "test when a node has no article title"
        xml_content = "<root><sub-article/></root>"
        expected_len = 1
        soup = parser.parse_xml(xml_content)
        nodes = raw_parser.sub_article(soup)
        self.assertEqual(
            len(raw_parser.filter_sub_articles_by_title(nodes)), expected_len
        )

    def test_filter_default(self):
        expected_len = len(self.nodes)
        self.assertEqual(
            len(raw_parser.filter_sub_articles_by_title(self.nodes)), expected_len
        )

    def test_filter_include_title(self):
        include_title = "recommendations"
        expected_len = 1
        self.assertEqual(
            len(
                raw_parser.filter_sub_articles_by_title(
                    self.nodes, include_title=include_title
                )
            ),
            expected_len,
        )

    def test_filter_exclude_title(self):
        exclude_title = "recommendations"
        expected_len = len(self.nodes) - 1
        self.assertEqual(
            len(
                raw_parser.filter_sub_articles_by_title(
                    self.nodes, exclude_title=exclude_title
                )
            ),
            expected_len,
        )

    def test_filter_include_and_exclude(self):
        include_title = "evaluation"
        exclude_title = "assessment"
        expected_len = 1
        self.assertEqual(
            len(
                raw_parser.filter_sub_articles_by_title(
                    self.nodes, include_title=include_title, exclude_title=exclude_title
                )
            ),
            expected_len,
        )


class TestEditorEvaluation(unittest.TestCase):
    def setUp(self):
        self.soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)

    def test_editor_evaluation(self):
        node = raw_parser.editor_evaluation(self.soup)
        self.assertEqual(node.name, "sub-article")
        self.assertEqual(
            str(raw_parser.article_title(node)),
            "<article-title>Editor's evaluation</article-title>",
        )


class TestElifeAssessment(unittest.TestCase):
    def setUp(self):
        self.soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)

    def test_elife_assessment(self):
        node = raw_parser.elife_assessment(self.soup)
        self.assertEqual(node.name, "sub-article")
        self.assertEqual(
            str(raw_parser.article_title(node)),
            "<article-title>eLife assessment</article-title>",
        )


class TestDecisionLetter(unittest.TestCase):
    def setUp(self):
        self.soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)

    def test_decision_letter(self):
        node = raw_parser.decision_letter(self.soup)
        self.assertEqual(node.name, "sub-article")
        self.assertEqual(
            str(raw_parser.article_title(node)),
            "<article-title>Decision letter</article-title>",
        )


class TestAuthorResponse(unittest.TestCase):
    def setUp(self):
        self.soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)

    def test_author_response(self):
        node = raw_parser.author_response(self.soup)
        self.assertEqual(node.name, "sub-article")
        self.assertEqual(
            str(raw_parser.article_title(node)),
            "<article-title>Author response</article-title>",
        )


class TestRecommendationsForAuthors(unittest.TestCase):
    def setUp(self):
        self.soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)

    def test_recommendations_for_authors(self):
        node = raw_parser.recommendations_for_authors(self.soup)
        self.assertEqual(node.name, "sub-article")
        self.assertEqual(
            str(raw_parser.article_title(node)),
            "<article-title>Recommendations for authors</article-title>",
        )


class TestPublicReviews(unittest.TestCase):
    def setUp(self):
        self.soup = parser.parse_xml(SUB_ARTICLE_XML_CONTENT)

    def test_public_reviews(self):
        expected_len = 3
        nodes = raw_parser.public_reviews(self.soup)
        self.assertEqual(len(nodes), expected_len)
        self.assertEqual(
            str(raw_parser.article_title(nodes[0])),
            "<article-title>Reviewer #1 (public review)</article-title>",
        )


if __name__ == "__main__":
    unittest.main()
