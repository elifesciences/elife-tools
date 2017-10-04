import xml
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

"""
xmlio can do input and output of XML, allowing it to be edited using ElementTree library
"""

class CustomXMLParser(ElementTree.XMLParser):
    doctype_dict = {}
    def doctype(self, name, pubid, system):
        self.doctype_dict["name"] = name
        self.doctype_dict["pubid"] = pubid
        self.doctype_dict["system"] = system

def register_xmlns():
    """
    Register namespaces globally
    """
    ElementTree.register_namespace("mml","http://www.w3.org/1998/Math/MathML")
    ElementTree.register_namespace("xlink","http://www.w3.org/1999/xlink")
    ElementTree.register_namespace("ali","http://www.niso.org/schemas/ali/1.0/")

def parse(filename, return_doctype_dict=False):
    """
    to extract the doctype details from the file when parsed and return the data
    for later use, set return_doctype_dict to True
    """
    parser = CustomXMLParser(html=0, target=None, encoding='utf-8')

    tree = ElementTree.parse(filename, parser)
    root = tree.getroot()

    if return_doctype_dict is True:
        return root, parser.doctype_dict
    else:
        return root

def add_tag_before(tag_name, tag_text, parent_tag, before_tag_name):
    """
    Helper function to refactor the adding of new tags
    especially for when converting text to role tags
    """
    new_tag = Element(tag_name)
    new_tag.text = tag_text
    parent_tag.insert( get_first_element_index(parent_tag, before_tag_name) - 1, new_tag)
    return parent_tag
    

def get_first_element_index(root, tag_name):
    """
    In order to use Element.insert() in a convenient way,
    this function will find the first child tag with tag_name
    and return its index position
    The index can then be used to insert an element before or after the
    found tag using Element.insert() 
    """
    tag_index = 1
    for tag in root:
        if tag.tag == tag_name:
            # Return the first one found if there is a match
            return tag_index
        tag_index = tag_index + 1
    # Default
    return None


def convert_xlink_href(root, name_map):
    
    xpath_list = ['.//graphic', './/media', './/inline-graphic', './/self-uri', './/ext-link']
    count = 0
    for xpath in xpath_list:
        for tag in root.findall(xpath):
            
            if tag.get('{http://www.w3.org/1999/xlink}href'):
                
                for k,v in name_map.iteritems():
                    # Try to match the exact name first, and if not then
                    #  try to match it without the file extension
                    if tag.get('{http://www.w3.org/1999/xlink}href') == k:
                        tag.set('{http://www.w3.org/1999/xlink}href', v)
                        count += 1
                    elif tag.get('{http://www.w3.org/1999/xlink}href') == k.split('.')[0]:
                        tag.set('{http://www.w3.org/1999/xlink}href', v.split('.')[0])
                        count += 1
    return count




def output(root, type='JATS', doctype_dict=None):

    if doctype_dict is not None:
        publicId = doctype_dict.get('pubid')
        systemId = doctype_dict.get('system')
        qualifiedName = doctype_dict.get('name')
    elif type == 'JATS':
        publicId = "-//NLM//DTD JATS (Z39.96) Journal Archiving and Interchange DTD v1.1d3 20150301//EN"
        systemId = 'JATS-archivearticle1.dtd'
        qualifiedName = "article"
    else:
        publicId = None
        systemId = None
        qualifiedName = "article"

    encoding = 'UTF-8'

    namespaceURI = None

    doctype = build_doctype(qualifiedName, publicId, systemId)

    return output_root(root, doctype, encoding)


def output_root(root, doctype, encoding):
    rough_string = ElementTree.tostring(root, encoding)

    reparsed = minidom.parseString(rough_string)
    if doctype:
        reparsed.insertBefore(doctype, reparsed.documentElement)

    #reparsed_string =  reparsed.toprettyxml(indent="\t", encoding = encoding)
    reparsed_string = reparsed.toxml(encoding = encoding)

    return reparsed_string


def build_doctype(qualifiedName, publicId=None, systemId=None, internalSubset=None):
    """
    Instantiate an ElifeDocumentType, a subclass of minidom.DocumentType, with
    some properties so it is more testable
    """
    doctype = ElifeDocumentType(qualifiedName)
    doctype._identified_mixin_init(publicId, systemId)
    if internalSubset:
        doctype.internalSubset = internalSubset
    return doctype


class ElifeDocumentType(minidom.DocumentType):
    """
    Override minidom.DocumentType in order to get
    double quotes in the DOCTYPE rather than single quotes
    """
    def writexml(self, writer, indent="", addindent="", newl=""):
        writer.write("<!DOCTYPE ")
        writer.write(self.name)
        if self.publicId:
            writer.write('%s PUBLIC "%s"%s  "%s"'
                         % (newl, self.publicId, newl, self.systemId))
        elif self.systemId:
            writer.write('%s SYSTEM "%s"' % (newl, self.systemId))
        if self.internalSubset is not None:
            writer.write(" [")
            writer.write(self.internalSubset)
            writer.write("]")
        writer.write(">"+newl)


def append_minidom_xml_to_elementtree_xml(parent, xml, recursive=False, attributes=None):
    """
    Recursively,
    Given an ElementTree.Element as parent, and a minidom instance as xml,
    append the tags and content from xml to parent
    Used primarily for adding a snippet of XML with <italic> tags
    attributes: a list of attribute names to copy
    """

    # Get the root tag name
    if recursive is False:
        tag_name = xml.documentElement.tagName
        node = xml.getElementsByTagName(tag_name)[0]
        new_elem = SubElement(parent, tag_name)
        if attributes:
            for attribute in attributes:
                if xml.documentElement.getAttribute(attribute):
                    new_elem.set(attribute, xml.documentElement.getAttribute(attribute))
    else:
        node = xml
        tag_name = node.tagName
        new_elem = parent

    i = 0
    for child_node in node.childNodes:
        if child_node.nodeName == '#text':
            if not new_elem.text and i <= 0:
                new_elem.text = child_node.nodeValue
            elif not new_elem.text and i > 0:
                new_elem_sub.tail = child_node.nodeValue
            else:
                new_elem_sub.tail = child_node.nodeValue

        elif child_node.childNodes is not None:
            new_elem_sub = SubElement(new_elem, child_node.tagName)
            new_elem_sub = append_minidom_xml_to_elementtree_xml(new_elem_sub, child_node,
                                                                 True, attributes)

        i = i + 1

    # Debug
    #encoding = 'utf-8'
    #rough_string = ElementTree.tostring(parent, encoding)
    #print rough_string

    return parent


if __name__ == '__main__':
    
    # Sample usage
    article_xml_filenames = ["sample-xml/elife-kitchen-sink.xml"]
                           
    for filename in article_xml_filenames:
        print "converting " + filename
        
        register_xmlns()
    
        root = parse(filename)
    
        reparsed_string = output(root)
    
        print reparsed_string
