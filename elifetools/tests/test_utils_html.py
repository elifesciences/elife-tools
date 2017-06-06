# coding=utf-8

import unittest
import os
import time
from ddt import ddt, data, unpack

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils_html


@ddt
class TestUtilsHtml(unittest.TestCase):

    def setUp(self):
        self.mock_tag = type('', (object,), {})
        setattr(self.mock_tag, 'name', 'foo')

    @unpack
    @data(
        (False, None, None, None),
        (True, None, None, None),
        (True, u'<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>', None,
         u'<p><b>A</b> <i>α</i> <span class="underline">c</span></p>'),

        (False, u'<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>', None,
         u'<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>'),

        (True, u'<p><bold>A</bold> 1 &lt; 2 &gt; 1 <xref rid="bib1">&gt;α&lt;</xref>&gt;</p>', None,
         u'<p><b>A</b> 1 &lt; 2 &gt; 1 <a href="#bib1">&gt;α&lt;</a>&gt;</p>'),

        (True, u'A bad xref <xref>&gt;α&lt;</xref>', None,
         u'A bad xref <xref>&gt;α&lt;</xref>'),

        (True, u'Link 1 <ext-link ext-link-type="uri" xlink:href="http://example.org/example.html">http://example.org/example.html</ext-link>', None,
         u'Link 1 <a href="http://example.org/example.html">http://example.org/example.html</a>'),

        (True, u'Link 2 <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>', None,
         u'Link 2 <a href="https://doi.org/10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</a>'),

        (True, u'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>', None,
         u'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>'),

        (True, u'<p>The Panda database (<ext-link ext-link-type="uri" xlink:href="http://circadian.salk.edu/about.html)%20does%20not%20indicate%20restoration%20of%20Cyp2b10">http://circadian.salk.edu/about.html) does not indicate restoration of <italic>Cyp2b10</italic></ext-link> cycling by restricted feeding of clockless mice.</p>', None,
         u'<p>The Panda database (<a href="http://circadian.salk.edu/about.html)%20does%20not%20indicate%20restoration%20of%20Cyp2b10">http://circadian.salk.edu/about.html) does not indicate restoration of <i>Cyp2b10</i></a> cycling by restricted feeding of clockless mice.</p>'),

        (True, u'<p>An empty tag <italic/></p>', None,
         u'<p>An empty tag <i></i></p>'),

        (True, u'<p><email>email@example.org</email></p>', None,
         u'<p><a href="mailto:email@example.org">email@example.org</a></p>'),

        (True, u'<p>A first <email>email@example.org</email> and second <email>another@example.org</email></p>', None,
         u'<p>A first <a href="mailto:email@example.org">email@example.org</a> and second <a href="mailto:another@example.org">another@example.org</a></p>'),

        (True, u'<p><inline-graphic xlink:href="elife-00240-inf1-v1"/></p>', None,
         u'<p><img src="elife-00240-inf1-v1.jpg"/></p>'),

        (True, u'<p><inline-graphic xlink:href="elife-00240-inf1-v1.tiff"/></p>', None,
         u'<p><img src="elife-00240-inf1-v1.jpg"/></p>'),

        (True, u'<p><inline-graphic xlink:href="elife-00240-inf1-v1.tif"/>Some text <inline-graphic xlink:href="elife-00240-inf2-v1.jpg"/>><inline-graphic xlink:href="elife-00240-inf3-v1.gif"></inline-graphic></p>', 'https://example.org/',
         u'<p><img src="https://example.org/elife-00240-inf1-v1.jpg"/>Some text <img src="https://example.org/elife-00240-inf2-v1.jpg"/>&gt;<img src="https://example.org/elife-00240-inf3-v1.gif"/></p>'),

        (True, u'<p>Bad inline-graphic for test coverage <inline-graphic/></p>', None,
         u'<p>Bad inline-graphic for test coverage <inline-graphic></inline-graphic></p>'),

        (True, u'<p>Xref tag with multiple rid from 09561 v1 to <xref ref-type="fig" rid="fig3 fig4">Figures 3, 4</xref></p>', None,
         u'<p>Xref tag with multiple rid from 09561 v1 to <a href="#fig3">Figures 3, 4</a></p>'),

        (True, u'<break></break>', None,
         u'<br/>'),

        (True, u'<monospace>m</monospace>', None,
         u'<span class="monospace">m</span>'),

        (True, u'<table><thead><!--  Header row  --><tr><!-- This header row ... --><th></th></tr></thead><tbody><!--  Table body  --><tr><td>Genotype</td></tr></tbody></table>', None,
         u'<table><thead><tr><th></th></tr></thead><tbody><tr><td>Genotype</td></tr></tbody></table>'),

        # Replace a particular style pattern with a class name
        (True, u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8">RS19</td></tr></tbody></table>', None,
         u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8">RS19</td></tr></tbody></table>'),
        (True, u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8"/></tr></tbody></table>', None,
         u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8"/></tr></tbody></table>'),
        (True, u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="author-callout-style-b8" valign="top">RS19</td></tr></tbody></table>', None,
         u'<table><thead><tr><th></th></tr></thead><tbody><tr><td class="author-callout-style-b8" valign="top">RS19</td></tr></tbody></table>'),
        (True, u'<table><thead><tr><th></th></tr></thead><tbody><tr><td valign="top" style="author-callout-style-b8">RS19</td></tr></tbody></table>', None,
         u'<table><thead><tr><th></th></tr></thead><tbody><tr><td valign="top" class="author-callout-style-b8">RS19</td></tr></tbody></table>'),

        # Do not replace general styles with a class name
        (True, u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="width:51.5pt;border-top:none;border-left:none; border-bottom:dashed; padding:0in 5.4pt 0in 5.4pt">CAP-Gly domain</td></tr></tbody></table>', None,
         u'<table><thead><tr><th></th></tr></thead><tbody><tr><td style="width:51.5pt;border-top:none;border-left:none; border-bottom:dashed; padding:0in 5.4pt 0in 5.4pt">CAP-Gly domain</td></tr></tbody></table>'),

        (True, u'<named-content content-type="author-callout-style-a1">author-callout-style-a1</named-content>', None,
         u'<span class="author-callout-style-a1">author-callout-style-a1</span>'),

        (True, u'<p>Bad named-content for test coverage <named-content/></p>', None,
         u'<p>Bad named-content for test coverage <named-content></named-content></p>'),

        )
    def test_xml_to_html(self, html_flag, xml_string, base_url, expected):
        self.assertEqual(utils_html.xml_to_html(html_flag, xml_string, base_url), expected)

if __name__ == '__main__':
    unittest.main()
