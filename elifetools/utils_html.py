import re
from bs4 import BeautifulSoup

def xml_to_html(html_flag, xml_string):
    "For formatting json output into HTML friendly format"
    if not xml_string or not html_flag is True:
        return xml_string
    html_string = xml_string
    html_string = replace_xref_tags(html_string)
    html_string = replace_simple_tags(html_string, 'italic', 'i')
    html_string = replace_simple_tags(html_string, 'bold', 'b')
    html_string = replace_simple_tags(html_string, 'underline', 'span', '<span class="underline">')
    html_string = replace_simple_tags(html_string, 'sc', 'span', '<span class="small-caps">')
    html_string = replace_simple_tags(html_string, 'inline-formula', None)
    html_string = replace_simple_tags(html_string)
    # Run it through BeautifulSoup as HTML, this encodes unmatched angle brackets
    soup = BeautifulSoup(html_string, 'html.parser')
    html_string = soup.encode()
    return html_string

def replace_simple_tags(s, from_tag='italic', to_tag='i', to_open_tag=None):
    """
    Replace tags such as <italic> to <i>
    This does not validate markup
    """
    if to_open_tag:
        s = s.replace('<' + from_tag + '>', to_open_tag)
    elif to_tag:
        s = s.replace('<' + from_tag + '>', '<' + to_tag + '>')
    else:
        s = s.replace('<' + from_tag + '>', '')

    if to_tag:
        s = s.replace('</' + from_tag + '>', '</' + to_tag + '>')
    else:
        s = s.replace('</' + from_tag + '>', '')

    return s

def replace_xref_tags(s):
    for tag_match in re.finditer("<(xref.*?)>", s):
        rid_match = re.finditer('rid="(.*)"', tag_match.group())
        if rid_match:
            rid = rid_match.next().group(1)
            new_tag = '<a href="#' + rid + '">'
            p = re.compile('<' + tag_match.group(1) + '>')
            s = p.sub(new_tag, s)
    s = replace_simple_tags(s, 'xref', 'a')
    return s