import unittest
import os
import StringIO
from ddt import ddt, data, unpack
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xmlio

from file_utils import sample_xml


@ddt
class TestXmlio(unittest.TestCase):

    def setUp(self):
        pass

    @data("elife-kitchen-sink.xml")
    def test_parse(self, filename):
        root = xmlio.parse(sample_xml(filename))
        self.assertEqual(type(root), Element)

    @unpack
    @data(("xmlio_input.xml", "inline-graphic", 2),
        ("xmlio_input.xml", "italic", None))
    def test_get_first_element_index(self, filename, tag_name, index):
        root = xmlio.parse(sample_xml(filename))
        self.assertEqual(xmlio.get_first_element_index(root, tag_name), index)

    @unpack
    @data(("<a><b/></a>", "c", "see", "b", "<a><c>see</c><b /></a>"))
    def test_add_tag_before(self, xml, tag_name, tag_text, before, expected_string):
        xml_element = ElementTree.fromstring(xml)
        element = xmlio.add_tag_before(tag_name, tag_text, xml_element, before)
        self.assertEqual(ElementTree.tostring(element), expected_string)

    @unpack
    @data(({"doc1.pdf":"doc-1.pdf", "img2.tif":"img-2.tif"},
        "xmlio_input.xml", "xmlio_output_convert_xlink.xml"))
    def test_convert_xlink_href(self, name_map, xml_input_filename, xml_expected_filename):
        xmlio.register_xmlns()
        root = xmlio.parse(sample_xml(xml_input_filename))
        xlink_count = xmlio.convert_xlink_href(root, name_map)
        xml_output = xmlio.output(root)
        xml_output_expected = None
        with open(sample_xml(xml_expected_filename), "rb") as xml_file:
            xml_output_expected = xml_file.read()
        self.assertEqual(xml_output, xml_output_expected)

    @unpack
    @data(("<article/>", "JATS", '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Archiving and Interchange DTD v1.1d3 20150301//EN"  "JATS-archivearticle1.dtd"><article/>'),
        ("<article/>", None, '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article><article/>'))
    def test_output(self, xml, type, xml_expected):
        root = xmlio.parse(StringIO.StringIO(xml))
        xml_output = xmlio.output(root, type)
        self.assertEqual(xml_output, xml_expected)

    @unpack
    @data(("<article/>", "", "", None,
           '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article><article/>'),
        ("<article/>", "-//a", "a", None,
         '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "-//a"  "a"><article/>'),
        ("<article/>", None, "b", "",
         '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article SYSTEM "b"><article/>'),
        ("<article/>", "c", "", "subset",
         '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "c"  "" [subset]><article/>'))
    def test_output_root(self, xml, publicId, systemId, internalSubset, xml_expected):
        encoding = 'UTF-8'
        qualifiedName = "article"
        root = xmlio.parse(StringIO.StringIO(xml))
        doctype = xmlio.build_doctype(qualifiedName, publicId, systemId, internalSubset)
        xml_output = xmlio.output_root(root, doctype, encoding)
        self.assertEqual(xml_output, xml_expected)


if __name__ == '__main__':
    unittest.main()
