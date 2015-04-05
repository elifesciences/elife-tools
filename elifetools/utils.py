import cgi
import htmlentitydefs

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





def extract_nodes(soup, nodename, attr = None, value = None):
    tags = soup.find_all(nodename)
    if attr != None and value != None:
        # refine nodes further by their attributes
        return filter(lambda tag: tag.get(attr) == value, tags)
    return tags

# deprecate?
def extract_first_node(soup, nodename):
    return first(extract_nodes(soup, nodename))

#@strippen
#@revert_entities
def node_text(tag):
    return getattr(tag, 'text', None)



#
# deprecated
#

# double handling and mixing responsibilities.
# use `extract_nodes` and `node_text`
def extract_node_text(soup, nodename, attr = None, value = None):
    """
    Extract node text by nodename, unless attr is supplied
    If attr and value is specified, find all the nodes and search
      by attr and value for the first node
    """
    tag_text = None
    if(attr == None):
        tag = extract_first_node(soup, nodename)
        try:
            tag_text = tag.text
        except(AttributeError):
            # Tag text not found
            return None
    else:
        tags = extract_nodes(soup, nodename, attr, value)
        for tag in tags:
            try:
                if tag[attr] == value:
                    tag_text = tag.text
            except KeyError:
                continue
    return tag_text
