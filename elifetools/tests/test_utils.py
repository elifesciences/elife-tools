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

if __name__ == '__main__':
    unittest.main()
