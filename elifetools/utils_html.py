import re
from bs4 import BeautifulSoup

def xml_to_html(html_flag, xml_string):
    "For formatting json output into HTML friendly format"
    if not xml_string or not html_flag is True:
        return xml_string
    html_string = xml_string
    html_string = replace_xref_tags(html_string)
    html_string = replace_ext_link_tags(html_string)
    html_string = replace_email_tags(html_string)
    html_string = replace_mathml_tags(html_string)
    html_string = replace_simple_tags(html_string, 'italic', 'i')
    html_string = replace_simple_tags(html_string, 'bold', 'b')
    html_string = replace_simple_tags(html_string, 'underline', 'span', '<span class="underline">')
    html_string = replace_simple_tags(html_string, 'sc', 'span', '<span class="small-caps">')
    html_string = replace_simple_tags(html_string, 'inline-formula', None)
    html_string = replace_simple_tags(html_string)
    # Run it through BeautifulSoup as HTML if it contains tags, this
    #  encodes unmatched angle brackets
    if '<' in html_string or '>' in html_string:
        soup = BeautifulSoup(html_string, 'html.parser')
        html_string = soup.encode('utf8')
        try:
            html_string.encode('utf8')
        except UnicodeDecodeError:
            html_string = html_string.decode('utf8')
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
        s = s.replace('<' + from_tag + '/>', '<' + to_tag + '/>')
    else:
        s = s.replace('<' + from_tag + '>', '')
        s = s.replace('<' + from_tag + '/>', '')

    if to_tag:
        s = s.replace('</' + from_tag + '>', '</' + to_tag + '>')
    else:
        s = s.replace('</' + from_tag + '>', '')

    return s

def replace_xref_tags(s):
    for tag_match in re.finditer("<(xref.*?)>", s):
        rid_match = re.finditer('rid="(.*)"', tag_match.group())
        if rid_match:
            try:
                rid = rid_match.next().group(1)
                new_tag = '<a href="#' + rid + '">'
                old_tag = '<' + tag_match.group(1) + '>'
                s = s.replace(old_tag, new_tag)
                # Replace all close tags even if one open tag gets replaced
                s = replace_simple_tags(s, 'xref', 'a')
            except StopIteration:
                pass
            
    return s

def replace_mathml_tags(s):
    p = re.compile('<mml:')
    s = p.sub('<', s)
    p = re.compile('</mml:')
    s = p.sub('</', s)
    return s

def replace_ext_link_tags(s):
    for tag_match in re.finditer("<(ext-link.*?)>", s):
        xlink_match = re.finditer('xlink:href="(.*)"', tag_match.group())
        ext_link_type_match = re.finditer('ext-link-type="(.*)"', tag_match.group())
        if xlink_match and ext_link_type_match:
            try:
                xlink = xlink_match.next().group(1)
                ext_link_type = ext_link_type_match.next().group(1)
                if ext_link_type.startswith('uri'):
                    new_tag = '<a href="' + xlink + '">'
                elif ext_link_type.startswith('doi'):
                    new_tag = '<a href="https://doi.org/' + xlink + '">'
                old_tag = '<' + tag_match.group(1) + '>'
                s = s.replace(old_tag, new_tag)
                # Replace all close tags even if one open tag gets replaced
                s = replace_simple_tags(s, 'ext-link', 'a')
            except StopIteration:
                pass
    return s

def replace_email_tags(s):
    for tag_match in re.finditer("<email>(.*?)</email>", s):
        email = tag_match.group(1)
        old_tag = '<email>' + email + '</email>'
        new_tag = '<a href="mailto:' + email + '">' + email + '</a>'
        s = s.replace(old_tag, new_tag)
    return s