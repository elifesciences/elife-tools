import xml
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

"""
xmlio can do input and output of XML, allowing it to be edited using ElementTree library
"""

def register_xmlns():
    """
    Register namespaces globally
    """
    ElementTree.register_namespace("mml","http://www.w3.org/1998/Math/MathML")
    ElementTree.register_namespace("xlink","http://www.w3.org/1999/xlink")

def parse(filename):
    parser = ElementTree.XMLParser(html=0, target=None, encoding='utf-8')

    tree = ElementTree.parse(filename, parser)
    root = tree.getroot()
    
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
    
    xpath_list = ['.//graphic', './/media', './/inline-graphic', './/self-uri']
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




def output(root, type = 'JATS'):

    if type == 'JATS':
        publicId = "-//NLM//DTD JATS (Z39.96) Journal Archiving and Interchange DTD v1.1d1 20130915//EN"
        systemId = 'JATS-archivearticle1.dtd'
    encoding = 'UTF-8'

    namespaceURI = None
    qualifiedName = "article"

    doctype = ElifeDocumentType(qualifiedName)
    doctype._identified_mixin_init(publicId, systemId)

    rough_string = ElementTree.tostring(root, encoding)

    reparsed = minidom.parseString(rough_string)
    if doctype:
        reparsed.insertBefore(doctype, reparsed.documentElement)

    #reparsed_string =  reparsed.toprettyxml(indent="\t", encoding = encoding)
    reparsed_string = reparsed.toxml(encoding = encoding)

    return reparsed_string


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

if __name__ == '__main__':
    
    # Sample usage
    article_xml_filenames = ["sample-xml/elife-kitchen-sink.xml"]
                           
    for filename in article_xml_filenames:
        print "converting " + filename
        
        register_xmlns()
    
        root = parse(filename)
    
        reparsed_string = output(root)
    
        print reparsed_string
