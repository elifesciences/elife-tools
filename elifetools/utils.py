import cgi
import htmlentitydefs
import time
import calendar

def first(x):
    "returns the first element of an iterable, swallowing index errors and returning None"
    try:
        return x[0]
    except IndexError:
        return None

def firstnn(x):
    "returns the first non-nil value within given iterable"
    return first(filter(None, x))

def swap_en_dashes(textHTMLEntities):
    return textHTMLEntities.replace("&#8211;", "&#x02013;")#.encode('ascii', 'xmlcharrefreplace')

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    return cgi.escape(text).encode('ascii', 'xmlcharrefreplace')

def format_text(title_text):
    textHTMLEntities = unicodeToHTMLEntities(title_text)
    textHTMLEntitiesReverted = swap_en_dashes(textHTMLEntities)
    return textHTMLEntitiesReverted

def flatten(function):
    """
    Convert or flatten value; if list length is zero then return None,
    if length of a list is 1, convert to a string, otherwise return
    the list as given
    """
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        if(type(value) == list and len(value) == 0):
            return None
        elif(type(value) == list and len(value) == 1):
            # If there is only one list element, return a singleton
            return value[0]
        else:
            return value
        return value
    return wrapper

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

def revert_entities(function):
    def wrapper(*args, **kwargs):
        text = function(*args, **kwargs)
        return format_text(text)
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

def remove_doi_paragraph(tags):
    "Given a list of tags, only return those whose text doesn't start with 'DOI:'"
    return filter(lambda tag: not node_text(tag).strip().startswith("DOI:"), tags)

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
    return "".join(map(unicode, tag.children)) or None

def copy_attribute(source, source_key, destination, destination_key):
    if source is not None:
        if source is not None and destination is not None and source_key in source:
            destination[destination_key] = source[source_key]
