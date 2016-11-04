import cgi
import htmlentitydefs
import time
import calendar

def first(x):
    if x is None:
        return None
    "returns the first element of an iterable, swallowing index errors and returning None"
    try:
        return x[0]
    except IndexError:
        return None

def firstnn(x):
    "returns the first non-nil value within given iterable"
    return first(filter(None, x))

def strip_strings(value):
    def strip_string(value):
        if hasattr(value, 'strip'):
            return value.strip()
        return value
    if type(value) == list:
        return map(strip_string, value)
    return strip_string(value)

def strip_punctuation_space(value):
    "Strip excess whitespace prior to punctuation."
    def strip_punctuation(string):
        replacement_list = (
            (' .',  '.'),
            (' :',  ':'),
            ('( ',  '('),
            (' )',  ')'),
        )
        for match, replacement in replacement_list:
            string = string.replace(match, replacement)
        return string
    if value == None:
        return None
    if type(value) == list:
        return map(strip_punctuation, value)
    return strip_punctuation(value)

def coerce_to_int(val, default=0xDEADBEEF):
    """Attempts to cast given value to an integer, return the original value if failed or the default if one provided."""
    try:
        return int(val)
    except (TypeError, ValueError):
        if default != 0xDEADBEEF:
            return default
        return val


def nullify(function):
    "Decorator. If empty list, returns None, else list."
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        if(type(value) == list and len(value) == 0):
            return None
        return value
    return wrapper

def strippen(function):
    "Decorator. Strip excess whitespace from return value."
    def wrapper(*args, **kwargs):
        return strip_strings(function(*args, **kwargs))
    return wrapper

def inten(function):
    "Decorator. Attempts to convert return value to int"
    def wrapper(*args, **kwargs):
        return coerce_to_int(function(*args, **kwargs))
    return wrapper

def date_struct(year, month, day, tz = "UTC"):
    """
    Given year, month and day numeric values and a timezone
    convert to structured date object
    """
    ymdtz = (year, month, day, tz)
    if None in ymdtz:
        #logger.debug("a year, month, day or tz value was empty: %s" % str(ymdtz))
        return None # return early if we have a bad value
    try:
        return time.strptime("%s-%s-%s %s" % ymdtz,  "%Y-%m-%d %Z")
    except(TypeError, ValueError):
        #logger.debug("date failed to convert: %s" % str(ymdtz))
        pass

def date_text(date_struct):
    # looks like: January 01, 2015
    return time.strftime("%B %d, %Y", date_struct) if date_struct else None


# TODO: if these are being converted to integers perhaps they shouldn't end with '_text' ?

@inten
def day_text(date_struct):
    return time.strftime("%d", date_struct) if date_struct else None

@inten
def month_text(date_struct):
    return time.strftime("%m", date_struct) if date_struct else None

@inten
def year_text(date_struct):
    return time.strftime("%Y", date_struct) if date_struct else None

def date_timestamp(date_struct):
    try:
        return calendar.timegm(date_struct)
    except (TypeError, ValueError):
        pass

def paragraphs(tags):
    "Given a list of tags, only return the paragraph tags"
    return filter(lambda tag: tag.name == "p", tags)

def starts_with_doi(tag):
    if node_text(tag).strip().startswith("DOI:"):
        return True
    else:
        return False

def remove_doi_paragraph(tags):
    "Given a list of tags, only return those whose text doesn't start with 'DOI:'"
    return filter(lambda tag: not starts_with_doi(tag), tags)

def remove_tag_from_tag(tag, nodename):
    if not nodename:
        return tag
    unwanted_tags = extract_nodes(tag, nodename)
    for unwanted_tag in unwanted_tags:
        unwanted_tag.decompose()
    return tag

def component_acting_parent_tag(parent_tag, tag):
    """
    Only intended for use in getting components, look for tag name of fig-group
    and if so, find the first fig tag inside it as the acting parent tag
    """
    if parent_tag.name == "fig-group":
        if (len(tag.find_previous_siblings("fig")) > 0):
            acting_parent_tag = first(extract_nodes(parent_tag, "fig"))
        else:
            # Do not return the first fig as parent of itself
            return None
    else:
        acting_parent_tag = parent_tag
    return acting_parent_tag

#
#
#

def extract_nodes(soup, nodename, attr = None, value = None):
    """
    Returns a list of tags (nodes) from the given soup matching the given nodename.
    If an optional attribute and value are given, these are used to filter the results
    further."""
    tags = soup.find_all(nodename)
    if attr != None and value != None:
        return filter(lambda tag: tag.get(attr) == value, tags)
    return tags

def node_text(tag):
    "Returns the text contents of a tag"
    return getattr(tag, 'text', None)

def node_contents_str(tag):
    """
    Return the contents of a tag, including it's children, as a string.
    Does not include the root/parent of the tag.
    """
    if tag is None:
        return None
    return "".join(map(unicode, tag.children)) or None
    
def first_parent(tag, nodename):
    """
    Given a beautiful soup tag, look at its parents and return the first
    tag name that matches nodename or the list nodename
    """
    if nodename is not None and type(nodename) == str:
        nodename = [nodename]
    return first(filter(lambda tag: tag.name in nodename, tag.parents))
        
def tag_ordinal(tag):
    """
    Given a beautiful soup tag, look at the tags of the same name that come before it
    to get the tag ordinal. For example, if it is tag name fig
    and two fig tags are before it, then it is the third fig (3)
    """
    tag_count = 0
    return len(tag.find_all_previous(tag.name)) + 1

def tag_fig_ordinal(tag):
    """
    Meant for finding the position of fig tags with respect to whether
    they are for a main figure or a child figure
    """
    tag_count = 0
    if 'specific-use' not in tag.attrs:
        # Look for tags with no "specific-use" attribute
        return len(filter(lambda tag: 'specific-use' not in tag.attrs,
                          tag.find_all_previous(tag.name))) + 1

def tag_sibling_ordinal(tag):
    """
    Given a beautiful soup tag, count the same tags in its siblings
    to get a sibling "local" ordinal value. This is useful in counting
    child figures within a fig-group, for example
    """
    tag_count = 0
    return len(tag.find_previous_siblings(tag.name)) + 1
    
    
def tag_limit_sibling_ordinal(tag, stop_tag_name):
    """
    Count previous tags of the same name until it
    reaches a tag name of type stop_tag, then stop counting
    """
    tag_count = 1
    for prev_tag in tag.previous_elements:
        if prev_tag.name == tag.name:
            tag_count += 1
        if prev_tag.name == stop_tag_name:
            break

    return tag_count
    
def tag_subarticle_sibling_ordinal(tag):
    return tag_limit_sibling_ordinal(tag, 'sub-article')

def tag_appendix_sibling_ordinal(tag):
    return tag_limit_sibling_ordinal(tag, 'app')

def tag_media_sibling_ordinal(tag):
    """
    Count sibling ordinal differently depending on if the
    mimetype is video or not
    """
    if hasattr(tag, 'name') and tag.name != 'media':
        return None
    
    nodenames = ['fig','supplementary-material','sub-article']
    first_parent_tag = first_parent(tag, nodenames)
    
    sibling_ordinal = None
    
    if first_parent_tag:
        # Start counting at 0
        sibling_ordinal = 0
        for media_tag in first_parent_tag.find_all(tag.name):
            if 'mimetype' in tag.attrs and tag['mimetype'] == 'video':
                # Count all video type media tags
                if 'mimetype' in media_tag.attrs and tag['mimetype'] == 'video':
                    sibling_ordinal += 1
                if media_tag == tag:
                    break

            else:
                # Count all non-video type media tags
                if (('mimetype' not in media_tag.attrs)
                    or ('mimetype' in media_tag.attrs and tag['mimetype'] != 'video')):
                    sibling_ordinal += 1
                if media_tag == tag:
                    break
    else:
        # Start counting at 1
        sibling_ordinal = 1
        for prev_tag in tag.find_all_previous(tag.name):
            if not first_parent(prev_tag, nodenames):
                if 'mimetype' in tag.attrs and tag['mimetype'] == 'video':
                    # Count all video type media tags
                    if supp_asset(prev_tag) == supp_asset(tag) and 'mimetype' in prev_tag.attrs:
                        sibling_ordinal += 1
                else:
                    if supp_asset(prev_tag) == supp_asset(tag) and 'mimetype' not in prev_tag.attrs:
                        sibling_ordinal += 1
    
    return sibling_ordinal

def tag_supplementary_material_sibling_ordinal(tag):
    """
    Strategy is to count the previous supplementary-material tags
    having the same asset value to get its sibling ordinal.
    The result is its position inside any parent tag that
    are the same asset type
    """
    if hasattr(tag, 'name') and tag.name != 'supplementary-material':
        return None

    nodenames = ['fig','media','sub-article']
    first_parent_tag = first_parent(tag, nodenames)
    
    sibling_ordinal = 1
    
    if first_parent_tag:
        # Within the parent tag of interest, count the tags
        #  having the same asset value
        for supp_tag in first_parent_tag.find_all(tag.name):
            if tag == supp_tag:
                # Stop once we reach the same tag we are checking
                break
            if supp_asset(supp_tag) == supp_asset(tag):
                sibling_ordinal += 1
            
    else:
        # Look in all previous elements that do not have a parent
        #  and count the tags having the same asset value
        for prev_tag in tag.find_all_previous(tag.name):
            if not first_parent(prev_tag, nodenames):
                if supp_asset(prev_tag) == supp_asset(tag):
                    sibling_ordinal += 1
    
    return sibling_ordinal


def supp_asset(tag):
    """
    Given a supplementary-material tag, the asset value depends on
    its label text. This also informs in what order (its ordinal) it
    has depending on how many of each type is present
    """
    # Default
    asset = 'supp'
    if first(extract_nodes(tag, "label")):
        label_text = node_text(first(extract_nodes(tag, "label"))).lower()
        # Keyword match the label
        if label_text.find('code') > 0:
            asset = 'code'
        elif label_text.find('data') > 0:
            asset = 'data'
    return asset

def copy_attribute(source, source_key, destination, destination_key=None):
    if destination_key is None:
        destination_key = source_key
    if source is not None:
        if source is not None and destination is not None and source_key in source:
            destination[destination_key] = source[source_key]

def first_node_str_contents(soup, nodename, attr = None, value = None):
    return node_contents_str(first(extract_nodes(soup, nodename, attr=attr, value=value)))

def set_if_value(dictionary, key, value):
    if value is not None:
        dictionary[key] = value

def prune_dict_of_none_values(dictionary):
    # If a dict key value is none, then remove the key
    for key,value in dictionary.items():
        if value is None:
            del(dictionary[key])
