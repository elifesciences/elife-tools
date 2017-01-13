# coding=utf-8

import unittest
import os
import time
from ddt import ddt, data, unpack

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser
import json_rewrite

@ddt
class TestJsonRewrite(unittest.TestCase):

    def setUp(self):
        pass

    @unpack
    @data(
        ('', None, None, None),
        
        ('', '<root><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta></root>', None, None),

        ('not_a_rewrite_function',
        '<root><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="doi">10.7554/eLife.00051</article-id></article-meta></root>',
        None,
        None)

        )
    def test_rewrite_json(self, rewrite_type, xml_content, json_content, expected):
        soup = None
        if xml_content:
            soup = parser.parse_xml(xml_content)
        self.assertEqual(json_rewrite.rewrite_json(rewrite_type, soup, json_content), expected)

    @unpack
    @data(
        (None, None, None),
        ('elife', 'func', 'rewrite_elife_func'),
        ('eLife', 'func', 'rewrite_elife_func'),
        ('other_journal', 'func', 'rewrite_other_journal_func'),

        )
    def test_rewrite_function_name(self, journal_id, rewrite_type, expected):
        self.assertEqual(json_rewrite.rewrite_function_name(journal_id, rewrite_type), expected)



if __name__ == '__main__':
    unittest.main()
