# coding=utf-8

import unittest
import os
import json
from ddt import ddt, data, unpack
from bs4 import BeautifulSoup

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser
import rawJATS as raw_parser
from utils import date_struct, node_contents_str
from collections import OrderedDict

from file_utils import sample_xml, json_expected_folder, json_expected_file




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
            with open(json_file, 'rb') as json_file_fp:
                json_expected = json.loads(json_file_fp.read())
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
        ("elife-kitchen-sink.xml", None, OrderedDict()),
        ("elife_poa_e06828.xml", OrderedDict(), None))
    def test_decision_letter(self, filename, expected, not_expected):
        sub_article_content = parser.decision_letter(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, sub_article_content)
        if not_expected is not None:
            self.assertNotEqual(not_expected, sub_article_content)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, OrderedDict()),
        ("elife_poa_e06828.xml", OrderedDict(), None))
    def test_author_response(self, filename, expected, not_expected):
        sub_article_content = parser.author_response(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, sub_article_content)
        if not_expected is not None:
            self.assertNotEqual(not_expected, sub_article_content)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, []),
        ("elife_poa_e06828.xml", [], None))
    def test_body(self, filename, expected, not_expected):
        body = parser.body(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, body)
        if not_expected is not None:
            self.assertNotEqual(not_expected, body)

    @unpack
    @data(
        ('<root><sec sec-type="intro" id="s1"><title>Introduction</title><p>content</p></sec></root>',
         OrderedDict([('type', 'section'), ('title', u'Introduction')])
         ),

        ('<root><boxed-text id="box1"><object-id pub-id-type="doi">10.7554/eLife.00013.009</object-id><label>Box 1.</label><caption><title>Box title</title><p>content</p></caption></boxed-text></root>',
         OrderedDict([('type', 'box'), ('doi', u'10.7554/eLife.00013.009'), ('id', u'box1'), ('label', u'Box 1.'), ('title', u'Box title')])
         ),

        ('<root><p>content</p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<table-wrap><table><thead><tr><th/><th></tr><tbody><tr><td></td></tr></tbody></table></table-wrap></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<disp-formula><mml:math><mml:mtext>Body\u2009Mass</mml:mtext></mml:mtext></disp-formula></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<fig-group><fig></fig><fig></fig></fig-group></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<fig></fig></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig3s1" position="float" specific-use="child-fig"><object-id pub-id-type="doi">10.7554/eLife.00666.012</object-id><label>Figure 3—figure supplement 1.</label><caption><title>Title of the figure supplement</title><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00666.013</object-id><label>Figure 3—figure supplement 1—Source data 1.</label><caption><title>Title of the figure supplement source data.</title><p>Legend of the figure supplement source data.</p></caption><media mime-subtype="xlsx" mimetype="application" xlink:href="elife-00666-fig3-figsupp1-data1-v1.xlsx"/></supplementary-material></p></caption><graphic xlink:href="elife-00666-fig3-figsupp1-v1.tiff"/></fig></root>',
        OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.012'), ('id', u'fig3s1'), ('label', u'Figure 3\u2014figure supplement 1.'), ('title', u'Title of the figure supplement'), ('caption', []), ('alt', ''), ('uri', u'elife-00666-fig3-figsupp1-v1.tiff'), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.00666.013'), ('id', u'SD1-data'), ('label', u'Figure 3\u2014figure supplement 1\u2014Source data 1.'), ('title', u'Title of the figure supplement source data.'), ('mediaType', u'application/xlsx'), ('uri', u'elife-00666-fig3-figsupp1-data1-v1.xlsx')])])])
         ),

        ('<root><table-wrap id="tbl2" position="float"><object-id pub-id-type="doi">10.7554/eLife.00013.011</object-id><label>Table 2.</label><caption><p>Caption <xref ref-type="table-fn" rid="tblfn2">*</xref>content</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00013.011">http://dx.doi.org/10.7554/eLife.00013.011</ext-link></p></caption><table frame="hsides" rules="groups"><thead><tr><th>Species</th><th>Reference<xref ref-type="table-fn" rid="tblfn3">*</xref></th></tr></thead><tbody><tr><td><italic>Algoriphagus machipongonensis</italic> PR1</td><td><xref ref-type="bibr" rid="bib3">Alegado et al. (2012)</xref></td></tr></tbody></table><table-wrap-foot><fn id="tblfn1"><label>*</label><p>Footnote 1</p></fn><fn id="tblfn3"><label>§</label><p>CM = conditioned medium;</p></fn></table-wrap-foot></table-wrap></root>',
         OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.00013.011'), ('id', u'tbl2'), ('label', u'Table 2.'), ('title', u'Caption <xref ref-type="table-fn" rid="tblfn2">*</xref>content'), ('tables', [u'<table><thead><tr><th>Species</th><th>Reference<xref ref-type="table-fn" rid="tblfn3">*</xref></th></tr></thead><tbody><tr><td><italic>Algoriphagus machipongonensis</italic> PR1</td><td><xref ref-type="bibr" rid="bib3">Alegado et al. (2012)</xref></td></tr></tbody></table>']), ('footer', [OrderedDict([('type', 'paragraph'), ('text', u'Footnote 1')]), OrderedDict([('type', 'paragraph'), ('text', u'CM = conditioned medium;')])])])
            ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML"><disp-formula id="equ7"><label>(3)</label><mml:math id="m7"><mml:mrow><mml:msub><mml:mi>P</mml:mi><mml:mrow><mml:mi>k</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:msub><mml:mrow><mml:mo>(</mml:mo><mml:mi>I</mml:mi><mml:mi>O</mml:mi><mml:mo>)</mml:mo></mml:mrow><mml:mo>=</mml:mo><mml:mn>0.1</mml:mn><mml:mo>+</mml:mo><mml:mfrac><mml:mrow><mml:mn>0.5</mml:mn></mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:msup><mml:mi>e</mml:mi><mml:mrow><mml:mo>-</mml:mo><mml:mn>0.3</mml:mn><mml:mrow><mml:mo>(</mml:mo><mml:mi>I</mml:mi><mml:msub><mml:mi>N</mml:mi><mml:mrow><mml:mi>k</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:msub><mml:mo>-</mml:mo><mml:mn>100</mml:mn><mml:mo>)</mml:mo></mml:mrow></mml:mrow></mml:msup><mml:mo>)</mml:mo></mml:mrow></mml:mfrac></mml:mrow></mml:math></disp-formula></root>',
        OrderedDict([('type', 'mathml'), ('id', u'equ7'), ('label', u'(3)'), ('mathml', u'<mml:mrow><mml:msub><mml:mi>P</mml:mi><mml:mrow><mml:mi>k</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:msub><mml:mrow><mml:mo>(</mml:mo><mml:mi>I</mml:mi><mml:mi>O</mml:mi><mml:mo>)</mml:mo></mml:mrow><mml:mo>=</mml:mo><mml:mn>0.1</mml:mn><mml:mo>+</mml:mo><mml:mfrac><mml:mrow><mml:mn>0.5</mml:mn></mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:msup><mml:mi>e</mml:mi><mml:mrow><mml:mo>-</mml:mo><mml:mn>0.3</mml:mn><mml:mrow><mml:mo>(</mml:mo><mml:mi>I</mml:mi><mml:msub><mml:mi>N</mml:mi><mml:mrow><mml:mi>k</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:msub><mml:mo>-</mml:mo><mml:mn>100</mml:mn><mml:mo>)</mml:mo></mml:mrow></mml:mrow></mml:msup><mml:mo>)</mml:mo></mml:mrow></mml:mfrac></mml:mrow>')])
        )

    )
    def test_body_block_content(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.body_block_content(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ('<root><sec><boxed-text><title>Strange content for test coverage</title><table-wrap><label>A label</label></table-wrap><fig></fig><fig><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id></fig></boxed-text></sec></root>',
        OrderedDict([('content', [OrderedDict([('type', 'section'), ('content', [OrderedDict([('type', 'box'), ('title', u'Strange content for test coverage'), ('content', [OrderedDict([('type', 'table'), ('label', u'A label'), ('tables', [])]), OrderedDict([('type', 'image'), ('alt', '')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('alt', '')])])])])])])])
         ),

        ('<root><p>content <italic>test</italic></p></root>',
OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'content <italic>test</italic>')])])])
         ),
        
        ('<root><p>content<table-wrap><table><thead><tr><th/><th></tr><tbody><tr><td></td></tr></tbody></table></table-wrap></p></root>',
OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'content')]), OrderedDict([('type', 'table'), ('tables', [u'<table><thead><tr><th/><th/><tbody><tr><td/></tr></tbody></tr></thead></table>'])])])])
         ),

        ('<root><p>content</p><table-wrap><table><thead><tr><th/><th></tr><tbody><tr><td></td></tr></tbody></table></table-wrap></root>',
OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'content')]), OrderedDict([('type', 'table'), ('tables', [u'<table><thead><tr><th/><th/><tbody><tr><td/></tr></tbody></tr></thead></table>'])])])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig></p><p>More content</p></root>',
         OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.</p><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig><p>More content</p></root>',
         OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group></p><p>More content</p></root>',
        OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.</p><fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group><p>More content</p></root>',
        OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])
         ),

        )
    def test_body_block_content_render(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_block_content_render(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="s1"><title>Section title</title><p>Content.<fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group></p><p>More content</p></sec></root>',
        [OrderedDict([('type', 'section'), ('title', u'Section title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="s1"><title>Section title</title><p>Content.</p><fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group><p>More content</p></sec></root>',
        [OrderedDict([('type', 'section'), ('title', u'Section title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])]
         ),

        )
    def test_render_raw_body(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.render_raw_body(soup.contents[0])
        self.assertEqual(expected, tag_content)

    """
    Unit test small or special cases
    """
    @unpack
    @data(("", ""),
        ("<email>test@example.org</email>", "test@example.org"))
    def test_get_email(self, text, expected):
        self.assertEqual(expected, parser.get_email(text))

    @unpack
    @data(("elife-kitchen-sink.xml", "pub", ('28', '02', '2014')))
    def test_ymd(self, filename, test_date_type, expected):
        soup = self.soup(filename)
        date_tag = raw_parser.pub_date(soup, date_type=test_date_type)
        self.assertEqual(expected, parser.ymd(date_tag))

    @unpack
    @data(("elife-kitchen-sink.xml", "received", date_struct(2012, 6, 22)),
        ("elife-kitchen-sink.xml", None, None),
        ("elife-kitchen-sink.xml", "not_a_date_type", None))
    def test_history_date(self, filename, date_type, expected):
        self.assertEqual(expected, parser.history_date(self.soup(filename), date_type))

    @unpack
    @data(("<p></p>", "paragraph", "<p/>"),
        ("<p>§ <italic>*</italic></p>", "paragraph", u"<p>§ <italic>*</italic></p>"),)
    def test_duplicate_tag(self, xml, parser_function, expected_xml):
        # To test, first parse the XML into a tag, then duplicate it, then check the contents
        soup = parser.parse_xml(xml)
        tags = getattr(raw_parser, parser_function)(soup)
        tag_copy = parser.duplicate_tag(tags[0])
        self.assertEqual(expected_xml, unicode(tag_copy))

    """
    Functions that require more than one argument to test against json output
    """

    @data("elife-kitchen-sink.xml")
    def test_journal_issn(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_issn"),
                         parser.journal_issn(self.soup(filename), "electronic"))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_author_contributions(self, filename):
        self.assertEqual(self.json_expected(filename, "author_contributions"),
                         parser.author_contributions(self.soup(filename), "con"))

    @data("elife-kitchen-sink.xml", "elife00190.xml")
    def test_competing_interests(self, filename):
        self.assertEqual(self.json_expected(filename, "competing_interests"),
                         parser.competing_interests(self.soup(filename), "conflict"))

    @data("elife-kitchen-sink.xml")
    def test_full_author_notes(self, filename):
        self.assertEqual(self.json_expected(filename, "full_author_notes"),
                         parser.full_author_notes(self.soup(filename), None))

    """
    Functions that only need soup to test them against json output
    """

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_abstract(self, filename):
        self.assertEqual(self.json_expected(filename, "abstract"),
                         parser.abstract(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml")
    def test_abstracts(self, filename):
        self.assertEqual(self.json_expected(filename, "abstracts"),
                         parser.abstracts(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_date"),
                         parser.accepted_date_date(self.soup(filename)))


    @data("elife-kitchen-sink.xml")
    def test_accepted_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_day"),
                         parser.accepted_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_month"),
                         parser.accepted_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_timestamp"),
                         parser.accepted_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_year"),
                         parser.accepted_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_ack(self, filename):
        self.assertEqual(self.json_expected(filename, "ack"),
                         parser.ack(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_acknowledgements(self, filename):
        self.assertEqual(self.json_expected(filename, "acknowledgements"),
                         parser.acknowledgements(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_article_type(self, filename):
        self.assertEqual(self.json_expected(filename, "article_type"),
                         parser.article_type(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml")
    def test_author_notes(self, filename):
        self.assertEqual(self.json_expected(filename, "author_notes"),
                         parser.author_notes(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml",
          "elife02935.xml", "elife00270.xml", "elife00351.xml")
    def test_authors(self, filename):
        self.assertEqual(self.json_expected(filename, "authors"),
                         parser.authors(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_authors_non_byline(self, filename):
        self.assertEqual(self.json_expected(filename, "authors_non_byline"),
                         parser.authors_non_byline(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00013.xml")
    def test_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "award_groups"),
                         parser.award_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_category(self, filename):
        self.assertEqual(self.json_expected(filename, "category"),
                         parser.category(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_collection_year(self, filename):
        self.assertEqual(self.json_expected(filename, "collection_year"),
                         parser.collection_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_component_doi(self, filename):
        self.assertEqual(self.json_expected(filename, "component_doi"),
                         parser.component_doi(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife05502.xml", "elife04490.xml",
          "elife-14093-v1.xml")
    def test_components(self, filename):
        self.assertEqual(self.json_expected(filename, "components"),
                         parser.components(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_conflict(self, filename):
        self.assertEqual(self.json_expected(filename, "conflict"),
                         parser.conflict(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_contributors(self, filename):
        self.assertEqual(self.json_expected(filename, "contributors"),
                         parser.contributors(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_holder(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_holder"),
                         parser.copyright_holder(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_statement"),
                         parser.copyright_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_year(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_year"),
                         parser.copyright_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "correspondence"),
                         parser.correspondence(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_digest(self, filename):
        self.assertEqual(self.json_expected(filename, "digest"),
                         parser.digest(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_display_channel(self, filename):
        self.assertEqual(self.json_expected(filename, "display_channel"),
                         parser.display_channel(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_doi(self, filename):
        self.assertEqual(self.json_expected(filename, "doi"),
                         parser.doi(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_elocation_id(self, filename):
        self.assertEqual(self.json_expected(filename, "elocation_id"),
                         parser.elocation_id(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml", "elife00013.xml")
    def test_full_abstract(self, filename):
        self.assertEqual(self.json_expected(filename, "full_abstract"),
                         parser.full_abstract(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_affiliation(self, filename):
        self.assertEqual(self.json_expected(filename, "full_affiliation"),
                         parser.full_affiliation(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_award_group_funding_source(self, filename):
        self.assertEqual(self.json_expected(filename, "full_award_group_funding_source"),
                         parser.full_award_group_funding_source(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "full_award_groups"),
                         parser.full_award_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "full_correspondence"),
                         parser.full_correspondence(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_full_digest(self, filename):
        self.assertEqual(self.json_expected(filename, "full_digest"),
                         parser.full_digest(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_keyword_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "full_keyword_groups"),
                         parser.full_keyword_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_license(self, filename):
        self.assertEqual(self.json_expected(filename, "full_license"),
                         parser.full_license(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_subject_area(self, filename):
        self.assertEqual(self.json_expected(filename, "full_subject_area"),
                         parser.full_subject_area(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_title(self, filename):
        self.assertEqual(self.json_expected(filename, "full_title"),
                         parser.full_title(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_funding_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "funding_statement"),
                         parser.funding_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml",
          "elife04953.xml", "elife00133.xml")
    def test_graphics(self, filename):
        self.assertEqual(self.json_expected(filename, "graphics"),
                         parser.graphics(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_impact_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "impact_statement"),
                         parser.impact_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_inline_graphics(self, filename):
        self.assertEqual(self.json_expected(filename, "inline_graphics"),
                         parser.inline_graphics(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_is_poa(self, filename):
        self.assertEqual(self.json_expected(filename, "is_poa"),
                         parser.is_poa(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_journal_id(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_id"),
                         parser.journal_id(self.soup(filename)))



    @data("elife-kitchen-sink.xml")
    def test_journal_title(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_title"),
                         parser.journal_title(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_keywords(self, filename):
        self.assertEqual(self.json_expected(filename, "keywords"),
                         parser.keywords(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_license(self, filename):
        self.assertEqual(self.json_expected(filename, "license"),
                         parser.license(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_license_url(self, filename):
        self.assertEqual(self.json_expected(filename, "license_url"),
                         parser.license_url(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife00007.xml", "elife04953.xml",
          "elife00005.xml", "elife05031.xml", "elife04493.xml", "elife06726.xml")
    def test_media(self, filename):
        self.assertEqual(self.json_expected(filename, "media"),
                         parser.media(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_timestamp"),
                         parser.pub_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_date"),
                         parser.pub_date_date(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_day"),
                         parser.pub_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_month"),
                         parser.pub_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_year"),
                         parser.pub_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_publisher(self, filename):
        self.assertEqual(self.json_expected(filename, "publisher"),
                         parser.publisher(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_publisher_id(self, filename):
        self.assertEqual(self.json_expected(filename, "publisher_id"),
                         parser.publisher_id(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_date"),
                         parser.received_date_date(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_day"),
                         parser.received_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_month"),
                         parser.received_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_timestamp"),
                         parser.received_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_year"),
                         parser.received_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_references(self, filename):
        # Alias of refs
        self.assertEqual(self.json_expected(filename, "refs"),
                         parser.references(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife02935.xml", "elife00051.xml",
          "elife_poa_e06828.xml")
    def test_refs(self, filename):
        self.assertEqual(self.json_expected(filename, "refs"),
                         parser.refs(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_related_article(self, filename):
        self.assertEqual(self.json_expected(filename, "related_article"),
                         parser.related_article(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_related_object_ids(self, filename):
        self.assertEqual(self.json_expected(filename, "related_object_ids"),
                         parser.related_object_ids(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_research_organism(self, filename):
        self.assertEqual(self.json_expected(filename, "research_organism"),
                         parser.research_organism(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_self_uri(self, filename):
        self.assertEqual(self.json_expected(filename, "self_uri"),
                         parser.self_uri(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_subject_area(self, filename):
        self.assertEqual(self.json_expected(filename, "subject_area"),
                         parser.subject_area(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife02304.xml")
    def test_supplementary_material(self, filename):
        self.assertEqual(self.json_expected(filename, "supplementary_material"),
                         parser.supplementary_material(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title(self, filename):
        self.assertEqual(self.json_expected(filename, "title"),
                         parser.title(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title_short(self, filename):
        self.assertEqual(self.json_expected(filename, "title_short"),
                         parser.title_short(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title_slug(self, filename):
        self.assertEqual(self.json_expected(filename, "title_slug"),
                         parser.title_slug(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_volume(self, filename):
        self.assertEqual(self.json_expected(filename, "volume"),
                         parser.volume(self.soup(filename)))








if __name__ == '__main__':
    unittest.main()
