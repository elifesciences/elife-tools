# coding=utf-8

import unittest
import os
import time
from ddt import ddt, data, unpack

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils
import parseJATS as parser



@ddt
class TestUtils(unittest.TestCase):

    def setUp(self):
        self.mock_tag = type('', (object,), {})
        setattr(self.mock_tag, 'name', 'foo')

    @unpack
    @data((None, None),
        ([], None),
        (["bees"], "bees"),
        (["bees","knees"], "bees"))
    def test_first(self, value, expected):
        self.assertEqual(utils.first(value), expected)

    @unpack
    @data((None, None),
        ("An : ( example ) .", "An: (example)."),
        (["bees .","( knees )"], ["bees.","(knees)"]))
    def test_strip_punctuation_space(self, value, expected):
        self.assertEqual(utils.strip_punctuation_space(value), expected)

    @unpack
    @data((None, None, None),
        ("1", 0xDEADBEEF, 1),
        ("1", "moo", 1),
        ("two", 0xDEADBEEF, "two"),
        ("two", "moo", "moo"))
    def test_coerce_to_int(self, value, default, expected):
        self.assertEqual(utils.coerce_to_int(value, default), expected)

    @unpack
    @data((2015, 6, 22, "UTC", "%Y-%m-%d %Z", "2015-06-22 UTC"),
        ("2015", "06", "22", "UTC", "%Y-%m-%d %Z", "2015-06-22 UTC"),
        ("2015", "06", "31", "UTC", "%Y-%m-%d %Z", None),
        ("2015", "06", "0", "UTC", "%Y-%m-%d %Z", None),
        (None, "06", "22", "UTC", "%Y-%m-%d %Z", None))
    def test_date_struct(self, year, month, day, tz, date_format, date_string_expected):
        expected_date_struct = None
        if date_string_expected:
            expected_date_struct = time.strptime(date_string_expected, date_format)
        self.assertEqual(utils.date_struct(year, month, day, tz), expected_date_struct)

    def test_tag_media_sibling_ordinal_bad_input(self):
        self.assertEqual(utils.tag_media_sibling_ordinal(self.mock_tag), None)

    def test_tag_supplementary_material_sibling_ordinal_bad_input(self):
        self.assertEqual(utils.tag_supplementary_material_sibling_ordinal(self.mock_tag), None)

    @unpack
    @data(
        ("<p><bold>A</bold> c</p>", None, "<p><bold>A</bold> c</p>"),
        ("<p><bold>A</bold> c</p>", "bold", "<p> c</p>"),
        ("<p>A <bold>c</bold> <italic>d</italic> <fig>e</fig></p>", ["bold", "fig"],
            "<p>A  <italic>d</italic> </p>"),
        )
    def test_remove_tag_from_tag(self, xml, unwanted_tag_names, expected_xml):
        soup = parser.parse_xml(xml)
        tag = soup.find_all()[0]
        modified_tag = utils.remove_tag_from_tag(tag, unwanted_tag_names)
        self.assertEqual(unicode(modified_tag), expected_xml)

    @unpack
    @data(
        (None, None),
        ("http://dx.doi.org/10.7554/eLife.00666", "10.7554/eLife.00666"),
        ("https://dx.doi.org/10.7554/eLife.00666", "10.7554/eLife.00666"),
        ("http://doi.org/10.7554/eLife.00666", "10.7554/eLife.00666"),
        ("https://doi.org/10.7554/eLife.00666", "10.7554/eLife.00666"),
        )
    def test_doi_uri_to_doi(self, doi_uri, expected_doi):
        self.assertEqual(utils.doi_uri_to_doi(doi_uri), expected_doi)

    @unpack
    @data(
        (None, None),
        ("10.7554/eLife.00666", "https://doi.org/10.7554/eLife.00666"),
        )
    def test_doi_to_doi_uri(self, doi_uri, expected_doi):
        self.assertEqual(utils.doi_to_doi_uri(doi_uri), expected_doi)

    @unpack
    @data(
        ('<root><p><bold>A</bold> c</p></root>', u'[<p><bold>A</bold> c</p>]'),
        ('<root><p><bold>A</bold> c</p><p>DOI:</p></root>', u'[<p><bold>A</bold> c</p>]'),

        # example based on unwanted tag in elife 00049
        ('<root><p>First paragraph</p><p><bold>A</bold> c</p><p><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00049.011">http://dx.doi.org/10.7554/eLife.00049.011</ext-link></p></root>',
         u'[<p>First paragraph</p>, <p><bold>A</bold> c</p>]'),

        # example to keep the DOI looking paragraph because there is more content
        ('<root><p><bold>A</bold> c</p><p><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00049.011">http://dx.doi.org/10.7554/eLife.00049.011</ext-link><bold>Content to test.</bold></p></root>',
         u'[<p><bold>A</bold> c</p>, <p><ext-link ext-link-type="doi" href="10.7554/eLife.00049.011">http://dx.doi.org/10.7554/eLife.00049.011</ext-link><bold>Content to test.</bold></p>]'),

        )
    def test_remove_doi_paragraph(self, xml, expected_xml):
        soup = parser.parse_xml(xml)
        modified_tag = utils.remove_doi_paragraph(soup.contents[0])
        self.assertEqual(unicode(modified_tag), expected_xml)

    @unpack
    @data(
        (None, None),
        ('A simple example ', u'A simple example'),
        ('Testing one, two, three. Is this thing on?', u'Testing one, two, three'),
        ('Predation of <italic>M. sexta</italic> larvae and eggs by <italic>Geocoris</italic> spp. (<bold>A</bold>) Examples of predated <italic>M. sexta</italic> larva (left panel) and egg (right panel).', 'Predation of <italic>M. sexta</italic> larvae and eggs by <italic>Geocoris</italic> spp.'),
        ('Predation of <i>M. sexta</i> larvae and eggs by <i>Geocoris</i> spp. (<b>A</b>) Examples of predated <i>M. sexta</i> larva (left panel) and egg (right panel).', 'Predation of <i>M. sexta</i> larvae and eggs by <i>Geocoris</i> spp.'),
        ('The wild tobacco plant <italic>N. attenuata</italic> relies on both direct and indirect mechanisms to defend it against <italic>M. sexta</italic> caterpillars. Indirect defence involves the release of volatile chemicals that attract <italic>Geocoris</italic> bugs that prey on the caterpillars. This photograph shows a <italic>Geocoris</italic> bug (bottom left) about to attack a caterpillar and two of its larvae.', 'The wild tobacco plant <italic>N. attenuata</italic> relies on both direct and indirect mechanisms to defend it against <italic>M. sexta</italic> caterpillars'),
        ('The unfolded protein response in <italic>S. pombe</italic> and other species. (<bold>A</bold>) The accumulation unfolded proteins in the endoplasmic reticulum (ER) of <italic>S. pombe</italic> leads to activation of IRE1 (presumably by nucleotide binding (green), auto-phosphorylation (red) and the formation of dimers), which is turn leads to the cleavage of mRNAs in the cytosol. The subsequent degradation of the cleaved mRNAs (known as RIDD) and explusion from the cell (via the exosome) reduced the protein-folding load on the ER. However, as described in the text, the mRNA that encodes for the molecular chaperone <italic>Bip1</italic> escapes this fate:', 'The unfolded protein response in <italic>S. pombe</italic> and other species'),
        ('Table summarizing the weights (<italic>w</italic><sub><italic>N</italic></sub>) and performance (expressed as Pearson\'s coefficient <italic>R</italic> and RMSE) of the fourfold cross-validation, repeated 10 times, of the following binding affinity regression model: <disp-formula id="equ4"><mml:math id="m4"><mml:mi>Δ</mml:mi><mml:msub><mml:mtext>G</mml:mtext><mml:mrow><mml:mtext>calc</mml:mtext></mml:mrow></mml:msub><mml:mo>=</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>1</mml:mn></mml:msub><mml:msub><mml:mtext>ICs</mml:mtext><mml:mrow><mml:mtext>charged</mml:mtext><mml:mo>/</mml:mo><mml:mtext>charged</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>2</mml:mn></mml:msub><mml:msub><mml:mtext> ICs</mml:mtext><mml:mrow><mml:mtext>charged_apolar</mml:mtext></mml:mrow></mml:msub><mml:mo>−</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>3</mml:mn></mml:msub><mml:msub><mml:mtext> ICs</mml:mtext><mml:mrow><mml:mtext>polar</mml:mtext><mml:mo>/</mml:mo><mml:mtext>polar</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mtext>4</mml:mtext></mml:msub><mml:msub><mml:mtext> ICs</mml:mtext><mml:mrow><mml:mtext>polar</mml:mtext><mml:mo>/</mml:mo><mml:mtext>apolar</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>5</mml:mn></mml:msub><mml:msub><mml:mtext> %NIS</mml:mtext><mml:mrow><mml:mtext>apolar</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>6</mml:mn></mml:msub><mml:msub><mml:mtext> %NIS</mml:mtext><mml:mrow><mml:mtext>charged</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:mtext>Q</mml:mtext><mml:mo>.</mml:mo></mml:math></disp-formula>Each coefficient has been reported as average on the four models trained on the respective folds.', 'Table summarizing the weights (<italic>w</italic><sub><italic>N</italic></sub>) and performance (expressed as Pearson\'s coefficient <italic>R</italic> and RMSE) of the fourfold cross-validation, repeated 10 times, of the following binding affinity regression model'),

        )
    def test_text_to_title(self, value, expected_title):
        self.assertEqual(utils.text_to_title(value), expected_title)


if __name__ == '__main__':
    unittest.main()
