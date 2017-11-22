import re
from utils import escape_unmatched_angle_brackets, escape_ampersand

def xml_to_html(html_flag, xml_string, base_url=None):
    "For formatting json output into HTML friendly format"
    if not xml_string or not html_flag is True:
        return xml_string
    html_string = xml_string
    html_string = remove_comment_tags(html_string)
    #  Escape unmatched angle brackets
    if '<' in html_string or '>' in html_string:
        html_string = escape_html(html_string)
    # Replace more tags
    html_string = replace_xref_tags(html_string)
    html_string = replace_ext_link_tags(html_string)
    html_string = replace_email_tags(html_string)
    html_string = replace_inline_graphic_tags(html_string, base_url)
    html_string = replace_named_content_tags(html_string)
    html_string = replace_mathml_tags(html_string)
    html_string = replace_table_style_author_callout(html_string)
    html_string = replace_simple_tags(html_string, 'italic', 'i')
    html_string = replace_simple_tags(html_string, 'bold', 'b')
    html_string = replace_simple_tags(html_string, 'underline', 'span', '<span class="underline">')
    html_string = replace_simple_tags(html_string, 'sc', 'span', '<span class="small-caps">')
    html_string = replace_simple_tags(html_string, 'monospace', 'span', '<span class="monospace">')
    html_string = replace_simple_tags(html_string, 'inline-formula', None)
    html_string = replace_simple_tags(html_string, 'break', 'br')
    return html_string


def allowed_xml_tag_fragments():
    """
    tuples of whitelisted tag startswith values for matching tags found in inline text
    prior to being converted to HTML
    values can be a complete tag for exact matching just the first few characters of a tag
    such as the case would be for mml: or table td tags
    """
    return (
        '<p>', '</p>', '<p/>',
        '<break>', '</break>', '<break/>',
        '<underline>', '</underline>', '<underline/>',
        '<italic>', '</italic>','<italic/>',
        '<bold>', '</bold>', '<bold/>',
        '<monospace>', '</monospace>', '<monospace/>',
        '<sc>', '</sc>', '<sc/>',
        '<sup>', '</sup>',
        '<sub>', '</sub>',
        '<email', '</email',
        '<ext-link', '</ext-link',
        '<xref', '</xref',
        '<inline-graphic', '</inline-graphic',
        '<inline-formula', '</inline-formula',
        '<math', '</math',
        '<mml:', '</mml:',
        '<named-content', '</named-content',
        '<table', '</table',
        '<thead', '</thead',
        '<tbody', '</tbody',
        '<th', '</th',
        '<tr', '</tr',
        '<td', '</td',
        )

def escape_html(html_string):
    "escape ampersands and unmatched angle brackets in HTML string allowing some whitelisted tags"
    html_string = escape_ampersand(html_string)
    return escape_unmatched_angle_brackets(html_string, allowed_xml_tag_fragments())

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
                all_rid = next(rid_match).group(1)
                # Take only the first rid value if separated by spaces
                rid = all_rid.split(' ')[0]
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
                xlink = next(xlink_match).group(1)
                ext_link_type = next(ext_link_type_match).group(1)
                if ext_link_type.startswith('uri'):
                    # Compare the start of the unicode string and prepend incomplete URL values
                    if not xlink[0:4] in ['http', 'ftp:']:
                        xlink = 'http://' + xlink
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

def replace_inline_graphic_tags(s, base_url=None):
    from_file_extension = ['.tif', '.tiff']
    to_file_extension = '.jpg'
    for tag_match in re.finditer("<(inline-graphic.*?)>", s):
        xlink_match = re.finditer('xlink:href="(.*)"', tag_match.group())
        if xlink_match:
            try:
                xlink = next(xlink_match).group(1)
                # Add or change file extension
                if '.' not in xlink:
                    xlink = xlink + to_file_extension
                else:
                    for extension in from_file_extension:
                        if xlink.endswith(extension):
                            xlink = xlink.replace(extension, to_file_extension)
                # Add base_url if given
                if base_url:
                    xlink = base_url + xlink
                new_tag = '<img src="' + xlink + '"/>'
                old_tag = '<' + tag_match.group(1) + '>'
                s = s.replace(old_tag, new_tag)
                # Replace close tag if present
                s = s.replace('</inline-graphic>', '')
            except StopIteration:
                pass
    return s

def replace_named_content_tags(s):
    for tag_match in re.finditer("<(named-content.*?)>", s):
        content_type_match = re.finditer('content-type="(.*)"', tag_match.group())
        try:
            all_match = next(content_type_match).group(1)
            # Take only the first value
            span_class = all_match.split(' ')[0]
            new_tag = '<span class="' + span_class + '">'
            old_tag = '<' + tag_match.group(1) + '>'
            s = s.replace(old_tag, new_tag)
            # Replace all close tags even if one open tag gets replaced
            s = replace_simple_tags(s, 'named-content', 'span')
        except StopIteration:
            pass
    return s

def remove_comment_tags(s):
    for tag_match in re.finditer("<!--(.*?)-->", s):
        old_tag = '<!--' + tag_match.group(1) + '-->'
        s = s.replace(old_tag, '')
    return s

def replace_table_style_author_callout(s):
    for tag_match in re.finditer('<(td[^>]*style="author-callout-style[^>]*?")/?>', s):
        for style_match in re.finditer('(.*)style="(.*)"(.*)', tag_match.group()):
            tag_start = style_match.group(1)
            class_name = style_match.group(2)
            tag_end = style_match.group(3)
            new_tag = tag_start +  'class="' + class_name + '"' + tag_end
            old_tag = tag_start + 'style="' + class_name + '"' + tag_end
            s = s.replace(old_tag, new_tag)
    return s
