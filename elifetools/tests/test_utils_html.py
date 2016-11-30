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
        (False, None, None),
        (True, None, None),
        (True, u'<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>',
         u'<p><b>A</b> <i>α</i> <span class="underline">c</span></p>'),
        (False, u'<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>',
         u'<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>'),
        (True, u'<p><bold>A</bold> 1 &lt; 2 &gt; 1 <xref rid="bib1">&gt;α&lt;</xref>&gt;</p>',
         u'<p><b>A</b> 1 &lt; 2 &gt; 1 <a href="#bib1">&gt;α&lt;</a>&gt;</p>'),
        (True, u'A bad xref <xref>&gt;α&lt;</xref>',
         u'A bad xref <xref>&gt;α&lt;</xref>'),
        (True, u'Link 1 <ext-link ext-link-type="uri" xlink:href="http://example.org/example.html">http://example.org/example.html</ext-link>',
         u'Link 1 <a href="http://example.org/example.html">http://example.org/example.html</a>'),
        (True, u'Link 2 <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
         u'Link 2 <a href="https://doi.org/10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</a>'),
        (True, u'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
         u'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>'),
        (True, u'<p>The Panda database (<ext-link ext-link-type="uri" xlink:href="http://circadian.salk.edu/about.html)%20does%20not%20indicate%20restoration%20of%20Cyp2b10">http://circadian.salk.edu/about.html) does not indicate restoration of <italic>Cyp2b10</italic></ext-link> cycling by restricted feeding of clockless mice.</p>',
         u'<p>The Panda database (<a href="http://circadian.salk.edu/about.html)%20does%20not%20indicate%20restoration%20of%20Cyp2b10">http://circadian.salk.edu/about.html) does not indicate restoration of <i>Cyp2b10</i></a> cycling by restricted feeding of clockless mice.</p>'),
        (True, u'<p>An empty tag <italic/></p>',
         u'<p>An empty tag <i></i></p>'),
        (True, u'<p><email>email@example.org</email></p>',
         u'<p><a href="mailto:email@example.org">email@example.org</a></p>'),
        (True, u'<p>A first <email>email@example.org</email> and second <email>another@example.org</email></p>',
         u'<p>A first <a href="mailto:email@example.org">email@example.org</a> and second <a href="mailto:another@example.org">another@example.org</a></p>'),
        )
    def test_xml_to_html(self, html_flag, xml_string, expected):
        self.assertEqual(utils_html.xml_to_html(html_flag, xml_string), expected)

if __name__ == '__main__':
    unittest.main()
