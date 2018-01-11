from __future__ import absolute_import

from io import BytesIO
import unittest

from ddt import ddt, data, unpack
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

from elifetools import xmlio
from elifetools.file_utils import sample_xml
from elifetools.utils import unicode_value


@ddt
class TestXmlio(unittest.TestCase):

    def setUp(self):
        pass

    @data("elife-kitchen-sink.xml")
    def test_parse(self, filename):
        root = xmlio.parse(sample_xml(filename))
        self.assertEqual(type(root), Element)

    @data("elife-02833-v2.xml", "simple-jats-doctype-1.1.xml", "simple-jats-doctype-1.1d3.xml")
    def test_input_output(self, filename):
        """test parsing a file while retaining the doctype"""
        with open(sample_xml(filename), "rb") as xml_file:
            xml_output_expected = xml_file.read()
        root, doctype_dict = xmlio.parse(sample_xml(filename), return_doctype_dict=True)
        self.assertEqual(xmlio.output(root, None, doctype_dict), xml_output_expected)

    @data("elife-02833-v2.xml")
    def test_input_output_forcing_jats_doctype(self, filename):
        with open(sample_xml(filename), "rb") as xml_file:
            xml_output_expected = xml_file.read()
        root, doctype_dict = xmlio.parse(sample_xml(filename), return_doctype_dict=True)
        self.assertEqual(xmlio.output(root, 'JATS'), xml_output_expected)

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
        self.assertEqual(ElementTree.tostring(element).decode('utf-8'), expected_string)

    @unpack
    @data(({"doc1.pdf":"doc-1.pdf", "img2.tif":"img-2.tif"}, "xmlio_input.xml", "xmlio_output_convert_xlink.xml"))
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
        root = xmlio.parse(BytesIO(xml))
        xml_output = xmlio.output(root, type)
        self.assertEqual(xml_output.decode('utf-8'), xml_expected)

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
        root = xmlio.parse(BytesIO(xml))
        doctype = xmlio.build_doctype(qualifiedName, publicId, systemId, internalSubset)
        xml_output = xmlio.output_root(root, doctype, encoding)
        self.assertEqual(xml_output.decode('utf-8'), xml_expected)

    def test_append_minidom_xml_to_elementtree_xml(self):
        "test coverage of an edge case"
        parent = Element('root')
        tag = SubElement(parent, 'i')
        tag.text = "Text"
        tag.tail = " and tail."
        attributes = ["class"]
        # Add a first example
        xml = '<span><i>and</i> some <i>XML</i>.</span>'
        reparsed = minidom.parseString(xml.encode('utf-8'))
        parent = xmlio.append_minidom_xml_to_elementtree_xml(parent, reparsed)
        # Add another example to test more lines of code
        xml = '<span class="span"> <i>more</i> text</span>'
        reparsed = minidom.parseString(xml.encode('utf-8'))
        parent = xmlio.append_minidom_xml_to_elementtree_xml(parent, reparsed, False, attributes)
        # Generate output and compare it
        rough_string = ElementTree.tostring(parent).decode('utf-8')
        self.assertEqual(rough_string, '<root><i>Text</i> and tail.<span><i>and</i> some <i>XML</i>.</span><span class="span"> <i>more</i> text</span></root>')

if __name__ == '__main__':
    unittest.main()
