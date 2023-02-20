# coding=utf-8

import unittest
import os
import time
from collections import OrderedDict
from ddt import ddt, data, unpack
from elifetools import utils
from elifetools import parseJATS as parser
from elifetools.utils_html import allowed_xml_tag_fragments
from tests import soup_body


@ddt
class TestUtils(unittest.TestCase):
    def setUp(self):
        self.mock_tag = type("", (object,), {})
        setattr(self.mock_tag, "name", "foo")

    @unpack
    @data((None, None), ([], None), (["bees"], "bees"), (["bees", "knees"], "bees"))
    def test_first(self, value, expected):
        self.assertEqual(utils.first(value), expected)

    @unpack
    @data(
        (None, None),
        ("this and that", "this-that"),
        ("six of one and half a dozen", "six-one-half-a-dozen"),
    )
    def test_subject_slug_default(self, value, expected):
        "subject_slug with the default stopwords"
        self.assertEqual(utils.subject_slug(value), expected)

    @unpack
    @data(
        (None, None, None),
        ("this and that", [], "this-and-that"),
        ("this and that", ["this", "and", "that"], ""),
    )
    def test_subject_slug_stopwords(self, value, stopwords, expected):
        "subject_slug specifying alternate stopwords"
        self.assertEqual(utils.subject_slug(value, stopwords), expected)

    @unpack
    @data(
        (None, None),
        ("An : ( example ) .", "An: (example)."),
        (["bees .", "( knees )"], ["bees.", "(knees)"]),
    )
    def test_strip_punctuation_space(self, value, expected):
        self.assertEqual(utils.strip_punctuation_space(value), expected)

    @unpack
    @data(
        (None, None, ".", None),
        ("", None, ".", None),
        ("Something", None, ".", "Something"),
        ("Short sentence", "Another", ".", "Short sentence. Another"),
        ("Short sentence ", " Another", ".", "Short sentence. Another"),
        ("Short sentence.", "Another", ".", "Short sentence. Another"),
        ("Short sentence. ", "Another", ".", "Short sentence. Another"),
        # use a comma as the glue just to check it works
        ("Short sentence", "Another", ",", "Short sentence, Another"),
    )
    def test_join_sentences(self, value1, value2, glue, expected):
        self.assertEqual(utils.join_sentences(value1, value2, glue), expected)

    @unpack
    @data(
        (None, None, None),
        ("1", 0xDEADBEEF, 1),
        ("1", "moo", 1),
        ("two", 0xDEADBEEF, "two"),
        ("two", "moo", "moo"),
    )
    def test_coerce_to_int(self, value, default, expected):
        self.assertEqual(utils.coerce_to_int(value, default), expected)

    @unpack
    @data(
        (2015, 6, 22, "UTC", "%Y-%m-%d %Z", "2015-06-22 UTC"),
        ("2015", "06", "22", "UTC", "%Y-%m-%d %Z", "2015-06-22 UTC"),
        ("2015", "06", "31", "UTC", "%Y-%m-%d %Z", None),
        ("2015", "06", "0", "UTC", "%Y-%m-%d %Z", None),
        (None, "06", "22", "UTC", "%Y-%m-%d %Z", None),
    )
    def test_date_struct(self, year, month, day, tz, date_format, date_string_expected):
        expected_date_struct = None
        if date_string_expected:
            expected_date_struct = time.strptime(date_string_expected, date_format)
        self.assertEqual(utils.date_struct(year, month, day, tz), expected_date_struct)

    def test_tag_media_sibling_ordinal_bad_input(self):
        self.assertEqual(utils.tag_media_sibling_ordinal(self.mock_tag), None)

    def test_tag_supplementary_material_sibling_ordinal_bad_input(self):
        self.assertEqual(
            utils.tag_supplementary_material_sibling_ordinal(self.mock_tag), None
        )

    @unpack
    @data(
        ("<p><bold>A</bold> c</p>", None, "<p><bold>A</bold> c</p>"),
        ("<p><bold>A</bold> c</p>", "bold", "<p> c</p>"),
        (
            "<p>A <bold>c</bold> <italic>d</italic> <fig>e</fig></p>",
            ["bold", "fig"],
            "<p>A  <italic>d</italic> </p>",
        ),
    )
    def test_remove_tag_from_tag(self, xml, unwanted_tag_names, expected_xml):
        soup = parser.parse_xml(xml)
        tag = soup.find_all()[0]
        modified_tag = utils.remove_tag_from_tag(tag, unwanted_tag_names)
        self.assertEqual(str(modified_tag), expected_xml)

    def test_convert_testing_doi(self):
        cases = [
            ("10.7554/eLife.00666", "10.7554/eLife.00666"),
            ("10.7554/eLife.507424566981410635", "10.7554/eLife.10635"),
            # component
            ('10.7554/eLife.09560.sa0', '10.7554/eLife.09560.sa0'),
            # versioned
            ('10.7554/eLife.09560.1', '10.7554/eLife.09560.1'),
            ('10.7554/eLife.09560.1.sa0', '10.7554/eLife.09560.1.sa0'),
            # case preserved
            ('10.7554/ELIFE.09560', '10.7554/ELIFE.09560'),
            # unlikely cases
            ('10.7554/eLife.0', '10.7554/eLife.0'),
            ('10.7554/eLife.0.1', '10.7554/eLife.0.1'),
            ('10.7554/eLife.0.1.2.3.4', '10.7554/eLife.0.1.2.3.4'),

            # preserves unparseable strings
            ('', ''),
            ('not_a_doi', 'not_a_doi'),

            # no match cases
            (None, None),
            ([], None),
            ({}, None),
        ]
        for given, expected in cases:
            self.assertEqual(utils.convert_testing_doi(given), expected, "failed case %r" % given)

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
        ("<root><p><bold>A</bold> c</p></root>", u"[<p><bold>A</bold> c</p>]"),
        (
            "<root><p><bold>A</bold> c</p><p>DOI:</p></root>",
            u"[<p><bold>A</bold> c</p>]",
        ),
        # example based on unwanted tag in elife 00049
        (
            '<root><p>First paragraph</p><p><bold>A</bold> c</p><p><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00049.011">http://dx.doi.org/10.7554/eLife.00049.011</ext-link></p></root>',
            u"[<p>First paragraph</p>, <p><bold>A</bold> c</p>]",
        ),
        # example to keep the DOI looking paragraph because there is more content
        (
            '<root><p><bold>A</bold> c</p><p><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00049.011">http://dx.doi.org/10.7554/eLife.00049.011</ext-link><bold>Content to test.</bold></p></root>',
            u'[<p><bold>A</bold> c</p>, <p><ext-link ext-link-type="doi" href="10.7554/eLife.00049.011">http://dx.doi.org/10.7554/eLife.00049.011</ext-link><bold>Content to test.</bold></p>]',
        ),
    )
    def test_remove_doi_paragraph(self, xml, expected_xml):
        soup = parser.parse_xml(xml)
        modified_tag = utils.remove_doi_paragraph(soup_body(soup))
        self.assertEqual(str(modified_tag), expected_xml)

    @unpack
    @data(
        (None, None),
        ("http://orcid.org/0000-0003-3523-4408", "0000-0003-3523-4408"),
        ("https://orcid.org/0000-0003-3523-4408", "0000-0003-3523-4408"),
    )
    def test_orcid_uri_to_orcid(self, orcid_uri, expected_doi):
        self.assertEqual(utils.orcid_uri_to_orcid(orcid_uri), expected_doi)

    @unpack
    @data(
        (None, None),
        ("A simple example ", u"A simple example"),
        ("Testing one, two, three. Is this thing on?", u"Testing one, two, three"),
        (
            "Predation of <italic>M. sexta</italic> larvae and eggs by <italic>Geocoris</italic> spp. (<bold>A</bold>) Examples of predated <italic>M. sexta</italic> larva (left panel) and egg (right panel).",
            "Predation of <italic>M. sexta</italic> larvae and eggs by <italic>Geocoris</italic> spp.",
        ),
        (
            "Predation of <i>M. sexta</i> larvae and eggs by <i>Geocoris</i> spp. (<b>A</b>) Examples of predated <i>M. sexta</i> larva (left panel) and egg (right panel).",
            "Predation of <i>M. sexta</i> larvae and eggs by <i>Geocoris</i> spp.",
        ),
        (
            "The wild tobacco plant <italic>N. attenuata</italic> relies on both direct and indirect mechanisms to defend it against <italic>M. sexta</italic> caterpillars. Indirect defence involves the release of volatile chemicals that attract <italic>Geocoris</italic> bugs that prey on the caterpillars. This photograph shows a <italic>Geocoris</italic> bug (bottom left) about to attack a caterpillar and two of its larvae.",
            "The wild tobacco plant <italic>N. attenuata</italic> relies on both direct and indirect mechanisms to defend it against <italic>M. sexta</italic> caterpillars",
        ),
        (
            "The unfolded protein response in <italic>S. pombe</italic> and other species. (<bold>A</bold>) The accumulation unfolded proteins in the endoplasmic reticulum (ER) of <italic>S. pombe</italic> leads to activation of IRE1 (presumably by nucleotide binding (green), auto-phosphorylation (red) and the formation of dimers), which is turn leads to the cleavage of mRNAs in the cytosol. The subsequent degradation of the cleaved mRNAs (known as RIDD) and explusion from the cell (via the exosome) reduced the protein-folding load on the ER. However, as described in the text, the mRNA that encodes for the molecular chaperone <italic>Bip1</italic> escapes this fate:",
            "The unfolded protein response in <italic>S. pombe</italic> and other species",
        ),
        (
            'Table summarizing the weights (<italic>w</italic><sub><italic>N</italic></sub>) and performance (expressed as Pearson\'s coefficient <italic>R</italic> and RMSE) of the fourfold cross-validation, repeated 10 times, of the following binding affinity regression model: <disp-formula id="equ4"><mml:math id="m4"><mml:mi>Δ</mml:mi><mml:msub><mml:mtext>G</mml:mtext><mml:mrow><mml:mtext>calc</mml:mtext></mml:mrow></mml:msub><mml:mo>=</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>1</mml:mn></mml:msub><mml:msub><mml:mtext>ICs</mml:mtext><mml:mrow><mml:mtext>charged</mml:mtext><mml:mo>/</mml:mo><mml:mtext>charged</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>2</mml:mn></mml:msub><mml:msub><mml:mtext> ICs</mml:mtext><mml:mrow><mml:mtext>charged_apolar</mml:mtext></mml:mrow></mml:msub><mml:mo>−</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>3</mml:mn></mml:msub><mml:msub><mml:mtext> ICs</mml:mtext><mml:mrow><mml:mtext>polar</mml:mtext><mml:mo>/</mml:mo><mml:mtext>polar</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mtext>4</mml:mtext></mml:msub><mml:msub><mml:mtext> ICs</mml:mtext><mml:mrow><mml:mtext>polar</mml:mtext><mml:mo>/</mml:mo><mml:mtext>apolar</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>5</mml:mn></mml:msub><mml:msub><mml:mtext> %NIS</mml:mtext><mml:mrow><mml:mtext>apolar</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:msub><mml:mtext>w</mml:mtext><mml:mn>6</mml:mn></mml:msub><mml:msub><mml:mtext> %NIS</mml:mtext><mml:mrow><mml:mtext>charged</mml:mtext></mml:mrow></mml:msub><mml:mo>+</mml:mo><mml:mtext>Q</mml:mtext><mml:mo>.</mml:mo></mml:math></disp-formula>Each coefficient has been reported as average on the four models trained on the respective folds.',
            "Table summarizing the weights (<italic>w</italic><sub><italic>N</italic></sub>) and performance (expressed as Pearson's coefficient <italic>R</italic> and RMSE) of the fourfold cross-validation, repeated 10 times, of the following binding affinity regression model",
        ),
    )
    def test_text_to_title(self, value, expected_title):
        self.assertEqual(utils.text_to_title(value), expected_title)

    @unpack
    @data(
        (None, None),
        (u"", u""),
        (u"\nText\n ", u"Text"),
        (
            u"\nAn example <ext-link>link</i>\n<ext-link>link 2</ext-link>\n",
            u"An example <ext-link>link</i> <ext-link>link 2</ext-link>",
        ),
    )
    def test_clean_whitespace(self, value, expected):
        self.assertEqual(expected, utils.clean_whitespace(value))

    @unpack
    @data(
        (None, None),
        (u"Figure 8", u"Figure 8"),
        (u"Reviewers’ figure 1", u"Reviewers’ figure 1"),
        (u"Figure 7—figure supplement 1:", u"Figure 7—figure supplement 1"),
        (
            u"Appendix 1—figure 3—figure supplement 1.",
            u"Appendix 1—figure 3—figure supplement 1",
        ),
    )
    def test_rstrip_punctuation(self, value, expected):
        self.assertEqual(expected, utils.rstrip_punctuation(value))

    @unpack
    @data(
        (None, None),
        (
            "<p><italic><bold><sup><sub><sc><underline><bold>superstyling</bold></underline></sc></sub></sup></bold></italic></p>",
            "<p><italic><bold><sup><sub><sc><underline><bold>superstyling</bold></underline></sc></sub></sup></bold></italic></p>",
        ),
        ("<", "&lt;"),
        (
            "< T << G << C >> A <<italic>m</italic>",
            "&lt; T &lt;&lt; G &lt;&lt; C &gt;&gt; A &lt;<italic>m</italic>",
        ),
        (
            "<p>**p<0.01; ***p<0.001. SI, aged mice >5 months old.</p>",
            "<p>**p&lt;0.01; ***p&lt;0.001. SI, aged mice &gt;5 months old.</p>",
        ),
    )
    def test_escape_unmatched_angle_brackets(self, value, expected):
        """
        Test some additional examples of unmatched angle brackets specifically
        """
        self.assertEqual(
            utils.escape_unmatched_angle_brackets(value, allowed_xml_tag_fragments()),
            expected,
        )

    @unpack
    @data(
        (None, None),
        ("", ""),
        ("a", "a"),
        ("another & another & another", "another &amp; another &amp; another"),
        ("a&a", "a&amp;a"),
        ("a&amp;&a", "a&amp;&amp;a"),
        ("a&#x0117;a", "a&#x0117;a"),
        (
            "fake link http://example.org/?a=b&amp",
            "fake link http://example.org/?a=b&amp;amp",
        ),
        ("CUT&RUN is performed", "CUT&amp;RUN is performed"),
        ("&#8220;&what?;&#8221; &#169; Anon", "&#8220;&amp;what?;&#8221; &#169; Anon"),
    )
    def test_escape_ampersand(self, value, expected):
        self.assertEqual(utils.escape_ampersand(value), expected)

    @unpack
    @data(
        (None, None, ""),
        ("p", '<p class="p1">Paragraph.</p>', "Paragraph."),
        ("bold", "<p>\n<bold>One<bold> <bold>two</bold>\n</p>", "<p>One two</p>"),
        (
            "italic",
            "<p><italic><italic>Very italic.</italic></italic></p>",
            "<p>Very italic.</p>",
        ),
    )
    def test_remove_tag(self, tag_name, string, expected):
        self.assertEqual(utils.remove_tag(tag_name, string), expected)

    @unpack
    @data(
        (None, None, ""),
        ("p", '<p class="p1">Paragraph.</p>', ""),
        ("italic", "<p><italic><italic>Very italic.</italic></italic></p>", "<p></p>"),
    )
    def test_remove_tag_and_text(self, tag_name, string, expected):
        self.assertEqual(utils.remove_tag_and_text(tag_name, string), expected)

    @unpack
    @data(
        (None, None),
        ("", None),
        ("<root></root>", None),
        (
            "<root><p>Content <!-- comments --></p></root>",
            "<p>Content <!-- comments --></p>",
        ),
    )
    def test_node_contents_str(self, xml, expected):
        if not xml:
            # to test with blank values
            tag = xml
        else:
            # parse the XML into tags to test with
            soup = parser.parse_xml(xml)
            tag = soup_body(soup)
        self.assertEqual(utils.node_contents_str(tag), expected)

    @unpack
    @data(
        (None, "none"),
        ("alpha-lower", "alpha-lower"),
        ("alpha-upper", "alpha-upper"),
        ("bullet", "bullet"),
        ("order", "number"),
        ("roman-lower", "roman-lower"),
        ("roman-upper", "roman-upper"),
        ("simple", "none"),
    )
    def test_list_type_prefix(self, list_type, expected):
        self.assertEqual(utils.list_type_prefix(list_type), expected)


class TestUtilsNameFormatting(unittest.TestCase):
    def setUp(self):
        self.surname = "Doe"
        self.given_names = "Jane"
        self.suffix = "Jnr"

    def test_references_author_person(self):
        author = {
            "surname": self.surname,
            "given-names": self.given_names,
            "suffix": self.suffix,
        }
        expected = OrderedDict(
            [
                ("type", "person"),
                (
                    "name",
                    OrderedDict(
                        [("preferred", "Doe Jane Jnr"), ("index", "Doe, Jane, Jnr")]
                    ),
                ),
            ]
        )
        self.assertEqual(utils.references_author_person(author), expected)

    def test_reference_author_preferred_name(self):
        expected = "Doe Jane Jnr"
        self.assertEqual(
            utils.reference_author_preferred_name(
                self.surname, self.given_names, self.suffix
            ),
            expected,
        )

    def test_author_preferred_name(self):
        expected = "Jane Doe Jnr"
        self.assertEqual(
            utils.author_preferred_name(self.surname, self.given_names, self.suffix),
            expected,
        )

    def test_author_index_name(self):
        expected = "Doe, Jane, Jnr"
        self.assertEqual(
            utils.author_index_name(self.surname, self.given_names, self.suffix),
            expected,
        )


if __name__ == "__main__":
    unittest.main()
