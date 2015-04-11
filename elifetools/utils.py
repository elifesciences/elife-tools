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
    title = textHTMLEntities.replace("&#8211;", "&#x02013;")#.encode('ascii', 'xmlcharrefreplace')
    return title

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    returnText = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return returnText

def format_text(title_text):
    textHTMLEntities = unicodeToHTMLEntities(title_text)
    textHTMLEntitiesReverted = swap_en_dashes(textHTMLEntities)
    return textHTMLEntitiesReverted

def nullify(function):
    """
    If list length is zero then return None,
    otherwise return the list as given
    """
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        if(type(value) == list and len(value) == 0):
            return None
        return value
    return wrapper

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
    """
    Strip excess whitespace, on strings, and simple lists
    using recursion
    """
    if (value == None):
        return None
    elif (type(value) == list):
        # List, so recursively strip elements
        for i in range(0, len(value)):
            value[i] = strip_strings(value[i])
        return value
    else:
        try:
            value = value.strip()
            return value
        except(AttributeError):
            return value

def strip_punctuation_space(value):
    """
    Strip excess whitespace prior to punctuation
    using recursion
    """
    if (value == None):
        return None
    elif (type(value) == list):
        # List, so recursively strip elements
        for i in range(0, len(value)):
            value[i] = strip_punctuation_space(value[i])
        return value
    else:
        try:
            value = value.replace(" .", ".")
            value = value.replace(" :", ":")
            value = value.replace("( ", "(")
            value = value.replace(" )", ")")
            return value
        except(AttributeError):
            return value

def strippen(function):
    """
    Strip excess whitespace as a decorator
    """
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        return strip_strings(value)
    return wrapper

def inten(function):
    """
    Try to convert to int as a decorator
    """
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        if (value == None):
            return None
        else:
            try:
                return int(value)
            except(TypeError):
                return value
    return wrapper

def revert_entities(function):
    "this is the decorator"
    def wrapper(*args, **kwargs):
        text = function(*args, **kwargs)
        formatted_text = format_text(text)
        return formatted_text
    return wrapper

def date_struct(year, month, day, tz = "UTC"):
    """
    Given year, month and day numeric values and a timezone
    convert to structured date object
    """
    date_struct = None
    
    for item in year, month, day:
        if item is None:
            return None
    
    try:
        date_struct = time.strptime(year + "-" + month + "-" + day + " " + tz, "%Y-%m-%d %Z")
    except(TypeError, ValueError):
        # Date did not convert due to None variables, or the date does not exist
        pass

    return date_struct

def date_format(format, date_struct):
    """
    Convert a structured date to the given date format
    but can return None if it fails to happen
    """
    date_string = None
    if date_struct:
        date_string = time.strftime(format, date_struct)
    return date_string

def date_text(date_struct):
    return date_format("%B %d, %Y", date_struct)

def day_text(date_struct):
    try:
        return int(date_format("%d", date_struct))
    except TypeError:
        return None
    
def month_text(date_struct):
    try:
        return int(date_format("%m", date_struct))
    except TypeError:
        return None

def year_text(date_struct):
    try:
        return int(date_format("%Y", date_struct))
    except TypeError:
        return None

def date_timestamp(date_struct):
    timestamp = None
    try:
        timestamp = calendar.timegm(date_struct)
    except:
        # Date did not convert
        pass
    return timestamp



def extract_nodes(soup, nodename, attr = None, value = None):
    tags = soup.find_all(nodename)
    if attr != None and value != None:
        # refine nodes further by their attributes
        return filter(lambda tag: tag.get(attr) == value, tags)
    return tags


#@strippen
#@revert_entities
def node_text(tag):
    return getattr(tag, 'text', None)

def node_content(tag):
    """
    Given a tag, return a string of its children including the tags
    In other words, do not include the root or parent tag of the tag
    """
    content = ""
    for ch in tag.children:
        content = content + unicode(ch)
        
    if content == "":
        return None
    else:
        return content
    
def paragraphs(tags):
    """
    Given a list of tags only return the paragraph tags
    """
    
    paragraphs = []
    for tag in tags:
        if tag.name == "p":
            paragraphs.append(tag)
            
    return paragraphs

def remove_doi_paragraph(tags):
    """
    Some paragraphs start with the text "DOI:" and we do not always want them
    and this can filter them out of a list of paragraphs
    """
    match_text = "DOI:"
    start_index = 0
    end_index = len(match_text)
    
    good_tags = []
    for tag in tags:
        if node_text(tag).strip()[start_index:end_index] != match_text:
            good_tags.append(tag)
    return good_tags
