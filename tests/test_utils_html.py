# coding=utf-8

import unittest
import os
from ddt import ddt, data, unpack
from elifetools import utils_html


@ddt
class TestUtilsHtml(unittest.TestCase):
    def setUp(self):
        self.mock_tag = type("", (object,), {})
        setattr(self.mock_tag, "name", "foo")

    @unpack
    @data(
        (False, None, None, None),
        (True, None, None, None),
        (
            True,
            u"<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>",
            None,
            u'<p><b>A</b> <i>α</i> <span class="underline">c</span></p>',
        ),
        (
            False,
            u"<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>",
            None,
            u"<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>",
        ),
        (
            True,
            u'<p><bold>A</bold> 1 &lt; 2 &gt; 1 <xref rid="bib1">&gt;α&lt;</xref>&gt;</p>',
            None,
            u'<p><b>A</b> 1 &lt; 2 &gt; 1 <a href="#bib1">&gt;α&lt;</a>&gt;</p>',
        ),
        (
            True,
            u"A bad xref <xref>&gt;α&lt;</xref>",
            None,
            u"A bad xref <xref>&gt;α&lt;</xref>",
        ),
        (
            True,
            u'Link 1 <ext-link ext-link-type="uri" xlink:href="http://example.org/example.html">http://example.org/example.html</ext-link>',
            None,
            u'Link 1 <a href="http://example.org/example.html">http://example.org/example.html</a>',
        ),
        (
            True,
            u'Link 2 <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
            None,
            u'Link 2 <a href="https://doi.org/10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</a>',
        ),
        (
            True,
            u'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
            None,
            u'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
        ),
        (
            True,
            u'External link rewrite 1 <ext-link ext-link-type="uri" xlink:href="www.r-project.org">www.r-project.org</ext-link>',
            None,
            u'External link rewrite 1 <a href="http://www.r-project.org">www.r-project.org</a>',
        ),
        (
            True,
            u'External link rewrite 2 <ext-link ext-link-type="uri" xlink:href="http://www.r-project.org">www.r-project.org</ext-link>',
            None,
            u'External link rewrite 2 <a href="http://www.r-project.org">www.r-project.org</a>',
        ),
        (
            True,
            u'External link rewrite 3 <ext-link ext-link-type="uri" xlink:href="ftp://example.org">ftp://example.org</ext-link>',
            None,
            u'External link rewrite 3 <a href="ftp://example.org">ftp://example.org</a>',
        ),
        (
            True,
            u'<p>The Panda database (<ext-link ext-link-type="uri" xlink:href="http://circadian.salk.edu/about.html)%20does%20not%20indicate%20restoration%20of%20Cyp2b10">http://circadian.salk.edu/about.html) does not indicate restoration of <italic>Cyp2b10</italic></ext-link> cycling by restricted feeding of clockless mice.</p>',
            None,
            u'<p>The Panda database (<a href="http://circadian.salk.edu/about.html)%20does%20not%20indicate%20restoration%20of%20Cyp2b10">http://circadian.salk.edu/about.html) does not indicate restoration of <i>Cyp2b10</i></a> cycling by restricted feeding of clockless mice.</p>',
        ),
        (True, u"<p>An empty tag <italic/></p>", None, u"<p>An empty tag <i/></p>"),
        (
            True,
            u"<p><email>email@example.org</email></p>",
            None,
            u'<p><a href="mailto:email@example.org">email@example.org</a></p>',
        ),
        (
            True,
            u"<p>A first <email>email@example.org</email> and second <email>another@example.org</email></p>",
            None,
            u'<p>A first <a href="mailto:email@example.org">email@example.org</a> and second <a href="mailto:another@example.org">another@example.org</a></p>',
        ),
        (
            True,
            u'<p><inline-graphic xlink:href="elife-00240-inf1-v1"/></p>',
            None,
            u'<p><img src="elife-00240-inf1-v1.jpg"/></p>',
        ),
        (
            True,
            u'<p><inline-graphic xlink:href="elife-00240-inf1-v1.tiff"/></p>',
            None,
            u'<p><img src="elife-00240-inf1-v1.jpg"/></p>',
        ),
        (
            True,
            u'<p><inline-graphic xlink:href="elife-00240-inf1-v1.tif"/>Some text <inline-graphic xlink:href="elife-00240-inf2-v1.jpg"/>><inline-graphic xlink:href="elife-00240-inf3-v1.gif"></inline-graphic></p>',
            "https://example.org/",
            u'<p><img src="https://example.org/elife-00240-inf1-v1.jpg"/>Some text <img src="https://example.org/elife-00240-inf2-v1.jpg"/>&gt;<img src="https://example.org/elife-00240-inf3-v1.gif"/></p>',
        ),
        (
            True,
            u"<p>Bad inline-graphic for test coverage <inline-graphic/></p>",
            None,
            u"<p>Bad inline-graphic for test coverage <inline-graphic/></p>",
        ),
        (
            True,
            u'<p>Xref tag with multiple rid from 09561 v1 to <xref ref-type="fig" rid="fig3 fig4">Figures 3, 4</xref></p>',
            None,
            u'<p>Xref tag with multiple rid from 09561 v1 to <a href="#fig3">Figures 3, 4</a></p>',
        ),
        (True, u"<break></break>", None, u"<br></br>"),
        (True, u"<monospace>m</monospace>", None, u'<span class="monospace">m</span>'),
        (
            True,
            u"<table><thead><!--  Header row  --><tr><!-- This header row ... --><th></th></tr></thead><tbody><!--  Table body  --><tr><td>Genotype</td></tr></tbody></table>",
            None,
            u"<table><thead><tr><th></th></tr></thead><tbody><tr><td>Genotype</td></tr></tbody></table>",
        ),
        # Replace a particular style pattern with a class name
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8">RS19</td></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8">RS19</td></tr></tbody></table>',
        ),
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8"/></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8"/></tr></tbody></table>',
        ),
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8" valign="top">RS19</td></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8" valign="top">RS19</td></tr></tbody></table>',
        ),
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td valign="top" style="author-callout-style-b8">RS19</td></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td valign="top" class="author-callout-style-b8">RS19</td></tr></tbody></table>',
        ),
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td valign="top"><bold>R143Q</bold></td><td valign="top"/><td style="author-callout-style-b8" valign="top"/><td style="author-callout-style-b8" valign="top"/><td style="author-callout-style-b8" valign="top"/><td style="author-callout-style-b8" valign="top"/><td><bold>-2</bold></td><td valign="top"/></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td valign="top"><b>R143Q</b></td><td valign="top"/><td class="author-callout-style-b8" valign="top"/><td class="author-callout-style-b8" valign="top"/><td class="author-callout-style-b8" valign="top"/><td class="author-callout-style-b8" valign="top"/><td><b>-2</b></td><td valign="top"/></tr></tbody></table>',
        ),
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8">RS19</td><td style="author-callout-style-b8">RS19</td></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8">RS19</td><td class="author-callout-style-b8">RS19</td></tr></tbody></table>',
        ),
        # Do not replace general styles with a class name
        (
            True,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="width:51.5pt;border-top:none;border-left:none; border-bottom:dashed; padding:0in 5.4pt 0in 5.4pt">CAP-Gly domain</td></tr></tbody></table>',
            None,
            u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="width:51.5pt;border-top:none;border-left:none; border-bottom:dashed; padding:0in 5.4pt 0in 5.4pt">CAP-Gly domain</td></tr></tbody></table>',
        ),
        (
            True,
            u'<named-content content-type="author-callout-style-a1">author-callout-style-a1</named-content>',
            None,
            u'<span class="author-callout-style-a1">author-callout-style-a1</span>',
        ),
        (
            True,
            u"<p>Bad named-content for test coverage <named-content/></p>",
            None,
            u"<p>Bad named-content for test coverage <named-content/></p>",
        ),
        # Edge case based on elife article 24634
        (
            True,
            u"<p>Regional analyses identified portions of ... (p<e-200) <italic>MYH7</italic></p>",
            None,
            u"<p>Regional analyses identified portions of ... (p&lt;e-200) <i>MYH7</i></p>",
        ),
        # Edge case with a greater than tag, based on elife article 28862
        (
            True,
            u"<p>We observed significant colocalization (>74%) of <italic>Clensor</italic> with LMP-1-GFP labeled lysosomes ....</p>",
            None,
            u"<p>We observed significant colocalization (&gt;74%) of <i>Clensor</i> with LMP-1-GFP labeled lysosomes ....</p>",
        ),
        # Ampersand test
        (True, u"<p>&</p>", None, u"<p>&amp;</p>"),
        # related-object tag, can be found in a structured abstract
        (
            True,
            (
                '<related-object id="CT1" source-type="clinical-trials-registry" '
                'source-id="ClinicalTrials.gov" source-id-type="registry-name" '
                'document-id="NCT02968459" document-id-type="clinical-trial-number" '
                'xlink:href="https://clinicaltrials.gov/show/NCT02968459">NCT02968459.'
                "</related-object>"
            ),
            None,
            '<a href="https://clinicaltrials.gov/show/NCT02968459">NCT02968459.</a>',
        ),
        # table containing a list
        (
            True,
            u"<table><thead><tr><th></th></tr></thead><tbody><tr><td>Genotype<list></list></td></tr>"
            u"</tbody></table>",
            None,
            u"<table><thead><tr><th></th></tr></thead><tbody><tr><td>Genotype<ul></ul></td></tr>"
            u"</tbody></table>",
        ),
        # table with inline styles and styled-content
        (
            True,
            "<table><thead><tr><th></th><th></th></tr></thead><tbody><tr>"
            '<td><styled-content style="color: #D50000;">400</styled-content></td>'
            '<td style="background-color: #FFB74D;">30503.40</td>'
            "</tr></tbody></table>",
            None,
            "<table><thead><tr><th></th><th></th></tr></thead><tbody><tr>"
            '<td><span style="color: #D50000;">400</span></td>'
            '<td style="background-color: #FFB74D;">30503.40</td>'
            "</tr></tbody></table>",
        ),
    )
    def test_xml_to_html(self, html_flag, xml_string, base_url, expected):
        self.assertEqual(
            utils_html.xml_to_html(html_flag, xml_string, base_url), expected
        )

    def test_replace_related_object_tagsl(self):
        """test when link is not prefaced with an internet scheme prefix"""
        tag_string = (
            '<related-object xlink:href="clinicaltrials.gov/show/NCT02968459">NCT02968459.'
            "</related-object>"
        )
        expected = (
            '<a href="http://clinicaltrials.gov/show/NCT02968459">NCT02968459.</a>'
        )
        self.assertEqual(utils_html.replace_related_object_tags(tag_string), expected)

    @unpack
    @data(
        ("", ""),
        ("<list/>", "<ul/>"),
        ("<list><list-item/></list>", "<ul><li/></ul>"),
        ("<list><list-item>One</list-item></list>", "<ul><li>One</li></ul>"),
        (
            '<list list-type="alpha-lower"><list-item>One</list-item></list>',
            '<ol class="list list--alpha-lower"><li>One</li></ol>',
        ),
        (
            '<list list-type="alpha-upper"><list-item>One</list-item></list>',
            '<ol class="list list--alpha-upper"><li>One</li></ol>',
        ),
        (
            '<list list-type="bullet"><list-item>One</list-item></list>',
            '<ul class="list list--bullet"><li>One</li></ul>',
        ),
        (
            '<list list-type="order"><list-item>One</list-item></list>',
            '<ol class="list list--number"><li>One</li></ol>',
        ),
        (
            '<list list-type="roman-lower"><list-item>One</list-item></list>',
            '<ol class="list list--roman-lower"><li>One</li></ol>',
        ),
        (
            '<list list-type="roman-upper"><list-item>One</list-item></list>',
            '<ol class="list list--roman-upper"><li>One</li></ol>',
        ),
        (
            '<list list-type="simple"><list-item>One</list-item></list>',
            '<ul class="list"><li>One</li></ul>',
        ),
    )
    def test_replace_list_tags(self, xml_string, expected):
        self.assertEqual(utils_html.replace_list_tags(xml_string), expected)


if __name__ == "__main__":
    unittest.main()
