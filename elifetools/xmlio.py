from io import BytesIO
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom


"""
xmlio can do input and output of XML, allowing it to be edited using ElementTree library
"""


# namespaces for when reparsing XML strings
REPARSING_NAMESPACES = (
    'xmlns:ali="http://www.niso.org/schemas/ali/1.0/" '
    + 'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
    + 'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
    + 'xmlns:xlink="http://www.w3.org/1999/xlink"'
)


class CustomTreeBuilder(ElementTree.TreeBuilder):
    doctype_dict = {}

    def doctype(self, name, pubid, system):
        self.doctype_dict["name"] = name
        self.doctype_dict["pubid"] = pubid
        self.doctype_dict["system"] = system


def register_xmlns():
    """
    Register namespaces globally
    """
    ElementTree.register_namespace("ali", "http://www.niso.org/schemas/ali/1.0/")
    ElementTree.register_namespace("mml", "http://www.w3.org/1998/Math/MathML")
    ElementTree.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def parse(filename, return_doctype_dict=False, return_processing_instructions=False):
    """
    to extract the doctype details from the file when parsed and return the data
    for later use, set return_doctype_dict to True
    """
    doctype_dict = {}
    processing_instructions = []

    # support BytesIO or actual files
    try:
        xml_bytes = filename.getvalue()
    except AttributeError:
        with open(filename, "rb") as open_file:
            xml_bytes = open_file.read()

    # collect processing instruction nodes using minidom
    with minidom.parseString(xml_bytes) as dom:
        for node in dom.childNodes:
            if isinstance(node, minidom.ProcessingInstruction):
                processing_instructions.append(node)

    # Assume greater than Python 3.2, get the doctype from the TreeBuilder
    tree_builder = CustomTreeBuilder()
    parser = ElementTree.XMLParser(target=tree_builder, encoding="utf-8")
    new_file = BytesIO(xml_bytes)
    tree = ElementTree.parse(new_file, parser)

    root = tree.getroot()

    doctype_dict = tree_builder.doctype_dict

    if return_doctype_dict is True and return_processing_instructions is True:
        return root, doctype_dict, processing_instructions
    if return_doctype_dict is True:
        return root, doctype_dict
    return root


def add_tag_before(tag_name, tag_text, parent_tag, before_tag_name):
    """
    Helper function to refactor the adding of new tags
    especially for when converting text to role tags
    """
    new_tag = Element(tag_name)
    new_tag.text = tag_text
    if get_first_element_index(parent_tag, before_tag_name):
        parent_tag.insert(
            get_first_element_index(parent_tag, before_tag_name) - 1, new_tag
        )
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

    xpath_list = [
        ".//graphic",
        ".//media",
        ".//inline-graphic",
        ".//self-uri",
        ".//ext-link",
    ]
    count = 0
    for xpath in xpath_list:
        for tag in root.findall(xpath):

            if tag.get("{http://www.w3.org/1999/xlink}href"):

                for key, value in name_map.items():
                    # Try to match the exact name first, and if not then
                    #  try to match it without the file extension
                    if tag.get("{http://www.w3.org/1999/xlink}href") == key:
                        tag.set("{http://www.w3.org/1999/xlink}href", value)
                        count += 1
                    elif (
                        tag.get("{http://www.w3.org/1999/xlink}href")
                        == key.split(".")[0]
                    ):
                        tag.set(
                            "{http://www.w3.org/1999/xlink}href", value.split(".")[0]
                        )
                        count += 1
    return count


def rewrite_subject_group(root, subjects, subject_group_type, overwrite=True):
    "add or rewrite subject tags inside subj-group tags"
    parent_tag_name = "subj-group"
    tag_name = "subject"
    wrap_tag_name = "article-categories"
    tag_attribute = "subj-group-type"
    # the parent tag where it should be found
    xpath_parent = ".//front/article-meta/article-categories"
    # the wraping tag in case article-categories does not exist
    xpath_article_meta = ".//front/article-meta"
    # the xpath to find the subject tags we are interested in
    xpath = './/{parent_tag_name}[@{tag_attribute}="{group_type}"]'.format(
        parent_tag_name=parent_tag_name,
        tag_attribute=tag_attribute,
        group_type=subject_group_type,
    )

    count = 0
    # get the parent tag
    parent_tag = root.find(xpath_parent)
    if parent_tag is None:
        # parent tag not found, add one
        wrap_tag = root.find(xpath_article_meta)
        article_categories_tag = SubElement(wrap_tag, wrap_tag_name)
        parent_tag = article_categories_tag
    insert_index = 0
    # iterate all tags to find the index of the first tag we are interested in
    if parent_tag is not None:
        for tag_index, tag in enumerate(parent_tag.findall("*")):
            if (
                tag.tag == parent_tag_name
                and tag.get(tag_attribute) == subject_group_type
            ):
                insert_index = tag_index
                if overwrite is True:
                    # if overwriting use the first one found
                    break
            # if not overwriting, use the last one found + 1
            if overwrite is not True:
                insert_index += 1
    # remove the tag if overwriting the existing values
    if overwrite is True:
        # remove all the tags
        for tag in root.findall(xpath):
            parent_tag.remove(tag)
    # add the subjects
    for subject in subjects:
        subj_group_tag = Element(parent_tag_name)
        subj_group_tag.set(tag_attribute, subject_group_type)
        subject_tag = SubElement(subj_group_tag, tag_name)
        subject_tag.text = subject
        parent_tag.insert(insert_index, subj_group_tag)
        count += 1
        insert_index += 1
    return count


def output(root, output_type="JATS", doctype_dict=None, processing_instructions=None):

    if doctype_dict is not None:
        publicId = doctype_dict.get("pubid")
        systemId = doctype_dict.get("system")
        qualifiedName = doctype_dict.get("name")
    elif output_type == "JATS":
        publicId = (
            "-//NLM//DTD JATS (Z39.96) Journal Archiving and Interchange "
            "DTD v1.1d3 20150301//EN"
        )
        systemId = "JATS-archivearticle1.dtd"
        qualifiedName = "article"
    else:
        publicId = None
        systemId = None
        qualifiedName = "article"

    encoding = "UTF-8"

    doctype = build_doctype(qualifiedName, publicId, systemId)

    return output_root(root, doctype, encoding, processing_instructions)


def output_root(root, doctype, encoding, processing_instructions=None):
    rough_string = ElementTree.tostring(root, encoding)

    reparsed = minidom.parseString(rough_string)
    if doctype:
        reparsed.insertBefore(doctype, reparsed.documentElement)

    if processing_instructions:
        for pi_node in processing_instructions:
            reparsed.insertBefore(pi_node, reparsed.documentElement)

    # reparsed_string =  reparsed.toprettyxml(indent="\t", encoding = encoding)
    reparsed_string = reparsed.toxml(encoding=encoding)

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
        assert self.name is not None, "the `minidom.DocumentType.name` property has not been set. see `output` and `build_doctype`."

        writer.write("<!DOCTYPE ")

        # Throws TypeError if self.name is None. only happens in Python 3.
        writer.write(self.name)

        if self.publicId:
            writer.write(
                '%s PUBLIC "%s"%s  "%s"' % (newl, self.publicId, newl, self.systemId)
            )
        elif self.systemId:
            writer.write('%s SYSTEM "%s"' % (newl, self.systemId))

        if self.internalSubset is not None:
            writer.write(" [")
            writer.write(self.internalSubset)
            writer.write("]")
        writer.write(">" + newl)


def append_minidom_xml_to_elementtree_xml(
    parent, xml, recursive=False, attributes=None, child_attributes=False
):
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
                if xml.documentElement.hasAttribute(attribute):
                    new_elem.set(attribute, xml.documentElement.getAttribute(attribute))
    else:
        node = xml
        tag_name = node.tagName
        new_elem = parent
        # copy child tag attributes if present
        if child_attributes and node.hasAttributes():
            for name, value in node.attributes.items():
                new_elem.set(name, value)

    new_elem_sub = None
    i = 0
    for child_node in node.childNodes:
        if child_node.nodeName == "#text":
            if not new_elem.text and i <= 0:
                new_elem.text = child_node.nodeValue
            elif new_elem_sub is not None and (not new_elem.text and i > 0):
                new_elem_sub.tail = child_node.nodeValue
            elif new_elem_sub is not None:
                new_elem_sub.tail = child_node.nodeValue

        elif child_node.childNodes is not None:
            new_elem_sub = SubElement(new_elem, child_node.tagName)
            new_elem_sub = append_minidom_xml_to_elementtree_xml(
                new_elem_sub, child_node, True, attributes, child_attributes
            )

        i = i + 1

    # Debug
    # encoding = 'utf-8'
    # rough_string = ElementTree.tostring(parent, encoding)
    # print rough_string

    return parent


if __name__ == "__main__":

    # Sample usage
    article_xml_filenames = ["sample-xml/elife-kitchen-sink.xml"]

    for filename in article_xml_filenames:
        print("converting " + filename)

        register_xmlns()

        root = parse(filename)

        reparsed_string = output(root)

        print(reparsed_string)


def reparsed_tag(
    tag_name, tag_string, namespaces=REPARSING_NAMESPACES, attributes_text=""
):
    """given tag content and attributes, reparse to a minidom tag"""
    open_tag_parts = [
        value for value in [tag_name, namespaces, attributes_text] if value
    ]
    open_tag = "<%s>" % " ".join(open_tag_parts)
    close_tag = "</%s>" % tag_name
    tagged_string = "%s%s%s" % (open_tag, tag_string, close_tag)
    return minidom.parseString(tagged_string.encode("utf-8"))
