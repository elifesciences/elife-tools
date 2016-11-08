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
        (True, '<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>',
         '<p><b>A</b> <i>α</i> <span class="underline">c</span></p>'),
        (False, '<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>',
         '<p><bold>A</bold> <italic>α</italic> <underline>c</underline></p>'),
        (True, '<p><bold>A</bold> 1 &lt; 2 &gt; 1 <xref rid="bib1">&gt;α&lt;</xref>&gt;</p>',
         '<p><b>A</b> 1 &lt; 2 &gt; 1 <a href="#bib1">&gt;\xce\xb1&lt;</a>&gt;</p>'),
        (True, 'A bad xref <xref>&gt;α&lt;</xref>',
         'A bad xref <xref>&gt;α&lt;</xref>'),
        (True, 'Link 1 <ext-link ext-link-type="uri" xlink:href="http://example.org/example.html">http://example.org/example.html</ext-link>',
         'Link 1 <a href="http://example.org/example.html">http://example.org/example.html</a>'),
        (True, 'Link 2 <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
         'Link 2 <a href="https://doi.org/10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</a>'),
        (True, 'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>',
         'Bad link 1 <ext-link xlink:href="10.7554/eLife.00001.012">http://dx.doi.org/10.7554/eLife.00001.012</ext-link>'),
        )
    def test_xml_to_html(self, html_flag, xml_string, expected):
        self.assertEqual(utils_html.xml_to_html(html_flag, xml_string), expected)

if __name__ == '__main__':
    unittest.main()
