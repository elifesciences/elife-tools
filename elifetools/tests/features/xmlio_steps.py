# -*- coding: utf-8 -*-
from lettuce import *
import xmlio
import os
from xml.etree import ElementTree
from parse_steps import set_file_location

@step(u'I have run register_xmlns')
def i_have_run_register_xmlns(step):
    xmlio.register_xmlns()
    
@step(u'I use xmlio to parse the (\S+)')
def i_use_xmlio_to_parse_the_document(step, document):
    file_location = set_file_location(document)
    world.root = xmlio.parse(file_location)

@step(u'I output the xml root')
def i_output_the_xml_root(step):
    world.string = xmlio.output(world.root)

@step(u'I get the first element index of (\S+)')
def and_i_get_the_first_element_index_of_tag(step, tag_name):
    world.string = xmlio.get_first_element_index(world.root, tag_name)

@step(u'I have the xml (.*)')
def i_have_the_xml_xml(step, xml):
    world.xml = xml

@step(u'I turn the xml into an element')
def i_turn_the_xml_into_an_element(step):
    world.element = ElementTree.fromstring(world.xml)

@step(u'I add tag (\S+) with text (\S+) before tag name (\S+)')
def i_add_tag_tag_name_with_text(step, tag_name, tag_text, before):
    world.element = xmlio.add_tag_before(tag_name, tag_text, world.element, before)

@step(u'I convert the element to string')
def i_convert_the_element_to_string(step):
    world.string = ElementTree.tostring(world.element)

@step(u'I convert the xlink href')
def i_convert_the_xlink_href(step):
    world.count = xmlio.convert_xlink_href(world.root, world.list)

@step(u'I compare the string to the document (\S+)')
def i_compare_the_string_to_the_document_output_document(step, document):
    file_location = set_file_location(document)
    file_contents = open(file_location).read()
    assert world.string == file_contents, \
        "Got %s" % world.string