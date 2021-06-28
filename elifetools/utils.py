import time
import calendar
import re
from collections import OrderedDict
from slugify import slugify
from bs4 import Comment


def subject_slug(subject, stopwords=None):
    "create a slug for a subject value"
    if stopwords is None:
        stopwords = ["and", "of"]
    if not subject:
        return subject
    return slugify(subject, stopwords=stopwords)


def first(value):
    if value is None:
        return None
    "returns the first element of an iterable, swallowing index errors and returning None"
    try:
        return value[0]
    except IndexError:
        return None


def firstnn(value):
    "returns the first non-nil value within given iterable"
    return first(list(filter(None, value)))


def strip_strings(value):
    def strip_string(value):
        if hasattr(value, "strip"):
            return value.strip()
        return value

    if isinstance(value, list):
        return list(map(strip_string, value))
    return strip_string(value)


def strip_punctuation_space(value):
    "Strip excess whitespace prior to punctuation."

    def strip_punctuation(string):
        replacement_list = (
            (" .", "."),
            (" :", ":"),
            ("( ", "("),
            (" )", ")"),
        )
        for match, replacement in replacement_list:
            string = string.replace(match, replacement)
        return string

    if value is None:
        return None
    if isinstance(value, list):
        return [strip_punctuation(v) for v in value]
    return strip_punctuation(value)


def join_sentences(string1, string2, glue="."):
    "concatenate two sentences together with punctuation glue"
    if not string1 or string1 == "":
        return string2
    if not string2 or string2 == "":
        return string1
    # both are strings, continue joining them together with the glue and whitespace
    new_string = string1.rstrip()
    if not new_string.endswith(glue):
        new_string += glue
    new_string += " " + string2.lstrip()
    return new_string


def coerce_to_int(val, default=0xDEADBEEF):
    """
    Attempts to cast given value to an integer, return the original value if
    failed or the default if one provided.
    """
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
        if isinstance(value, list) and len(value) == 0:
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


def clean_whitespace(value):
    if not value:
        return value
    if hasattr(value, "lstrip"):
        value = value.lstrip("\n ")
    if hasattr(value, "rstrip"):
        value = value.rstrip("\n ")
    value = value.replace("\n", " ")
    return value


def date_struct(year, month, day, tz="UTC"):
    """
    Given year, month and day numeric values and a timezone
    convert to structured date object
    """
    ymdtz = (year, month, day, tz)
    if None in ymdtz:
        # logger.debug("a year, month, day or tz value was empty: %s" % str(ymdtz))
        return None  # return early if we have a bad value
    try:
        return time.strptime("%s-%s-%s %s" % ymdtz, "%Y-%m-%d %Z")
    except (TypeError, ValueError):
        # logger.debug("date failed to convert: %s" % str(ymdtz))
        return None


def date_struct_nn(year, month, day, tz="UTC"):
    """
    Assemble a date object but if day or month is none set them to 1
    to make it easier to deal with partial dates
    """
    if not day:
        day = 1
    if not month:
        month = 1
    return date_struct(year, month, day, tz)


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
        return None


def paragraphs(tags):
    "Given a list of tags, only return the paragraph tags"
    return list(filter(lambda tag: tag.name == "p", tags))


def convert_testing_doi(doi):
    if doi is None:
        return doi
    parts = doi.split(".")
    new_msid = parts[-1][-5:]
    return ".".join(parts[0:-1] + [new_msid])


def starts_with_doi(tag):
    return bool(node_text(tag).strip().startswith("DOI:"))


def paragraph_is_only_doi(tag):
    return bool(
        node_text(tag).strip().startswith("http://dx.doi.org")
        and " " not in node_text(tag).strip()
        and node_contents_str(tag).startswith('<ext-link ext-link-type="doi"')
    )


def doi_uri_to_doi(value):
    "Strip the uri schema from the start of DOI URL strings"
    if value is None:
        return value
    replace_values = [
        "http://dx.doi.org/",
        "https://dx.doi.org/",
        "http://doi.org/",
        "https://doi.org/",
    ]
    for replace_value in replace_values:
        value = value.replace(replace_value, "")
    return value


def doi_to_doi_uri(value):
    "Turn DOI into a valid uri"
    if value is None:
        return value
    value = "https://doi.org/" + value
    return value


def remove_doi_paragraph(tags):
    "Given a list of tags, only return those whose text doesn't start with 'DOI:'"
    p_tags = list(filter(lambda tag: not starts_with_doi(tag), tags))
    p_tags = list(filter(lambda tag: not paragraph_is_only_doi(tag), p_tags))
    return p_tags


def orcid_uri_to_orcid(value):
    "Strip the uri schema from the start of ORCID URL strings"
    if value is None:
        return value
    replace_values = ["http://orcid.org/", "https://orcid.org/"]
    for replace_value in replace_values:
        value = value.replace(replace_value, "")
    return value


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
        if len(tag.find_previous_siblings("fig")) > 0:
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


def extract_nodes(soup, nodename, attr=None, value=None):
    """
    Returns a list of tags (nodes) from the given soup matching the given nodename.
    If an optional attribute and value are given, these are used to filter the results
    further."""
    tags = soup.find_all(nodename)
    if attr is not None and value is not None:
        return list(filter(lambda tag: tag.get(attr) == value, tags))
    return list(tags)


def node_text(tag):
    "Returns the text contents of a tag"
    return getattr(tag, "text", None)


def node_contents_str(tag):
    """
    Return the contents of a tag, including it's children, as a string.
    Does not include the root/parent of the tag.
    """
    if not tag:
        return None
    tag_string = ""
    for child_tag in tag.children:
        if isinstance(child_tag, Comment):
            # BeautifulSoup does not preserve comment tags, add them back
            tag_string += "<!--%s-->" % str(child_tag)
        else:
            tag_string += str(child_tag)
    return tag_string if tag_string != "" else None


def first_parent(tag, nodename):
    """
    Given a beautiful soup tag, look at its parents and return the first
    tag name that matches nodename or the list nodename
    """
    if nodename is not None and isinstance(nodename, str):
        nodename = [nodename]
    if tag and tag.parents:
        return first(list(filter(lambda tag: tag.name in nodename, tag.parents)))
    return None


def tag_ordinal(tag):
    """
    Given a beautiful soup tag, look at the tags of the same name that come before it
    to get the tag ordinal. For example, if it is tag name fig
    and two fig tags are before it, then it is the third fig (3)
    """
    return len(tag.find_all_previous(tag.name)) + 1


def tag_fig_ordinal(tag):
    """
    Meant for finding the position of fig tags with respect to whether
    they are for a main figure or a child figure
    """
    if "specific-use" not in tag.attrs:
        # Look for tags with no "specific-use" attribute
        return (
            len(
                list(
                    filter(
                        lambda tag: "specific-use" not in tag.attrs,
                        tag.find_all_previous(tag.name),
                    )
                )
            )
            + 1
        )
    return None


def tag_sibling_ordinal(tag):
    """
    Given a beautiful soup tag, count the same tags in its siblings
    to get a sibling "local" ordinal value. This is useful in counting
    child figures within a fig-group, for example
    """
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
    return tag_limit_sibling_ordinal(tag, "sub-article")


def tag_appendix_sibling_ordinal(tag):
    return tag_limit_sibling_ordinal(tag, "app")


def tag_media_sibling_ordinal(tag):
    """
    Count sibling ordinal differently depending on if the
    mimetype is video or not
    """
    if hasattr(tag, "name") and tag.name != "media":
        return None

    nodenames = ["fig", "supplementary-material", "sub-article"]
    first_parent_tag = first_parent(tag, nodenames)

    sibling_ordinal = None

    if first_parent_tag:
        # Start counting at 0
        sibling_ordinal = 0
        for media_tag in first_parent_tag.find_all(tag.name):
            if "mimetype" in tag.attrs and tag["mimetype"] == "video":
                # Count all video type media tags
                if "mimetype" in media_tag.attrs and tag["mimetype"] == "video":
                    sibling_ordinal += 1
                if media_tag == tag:
                    break

            else:
                # Count all non-video type media tags
                if ("mimetype" not in media_tag.attrs) or (
                    "mimetype" in media_tag.attrs and tag["mimetype"] != "video"
                ):
                    sibling_ordinal += 1
                if media_tag == tag:
                    break
    else:
        # Start counting at 1
        sibling_ordinal = 1
        for prev_tag in tag.find_all_previous(tag.name):
            if not first_parent(prev_tag, nodenames):
                if "mimetype" in tag.attrs and tag["mimetype"] == "video":
                    # Count all video type media tags
                    if (
                        supp_asset(prev_tag) == supp_asset(tag)
                        and "mimetype" in prev_tag.attrs
                    ):
                        sibling_ordinal += 1
                else:
                    if (
                        supp_asset(prev_tag) == supp_asset(tag)
                        and "mimetype" not in prev_tag.attrs
                    ):
                        sibling_ordinal += 1

    return sibling_ordinal


def tag_supplementary_material_sibling_ordinal(tag):
    """
    Strategy is to count the previous supplementary-material tags
    having the same asset value to get its sibling ordinal.
    The result is its position inside any parent tag that
    are the same asset type
    """
    if hasattr(tag, "name") and tag.name != "supplementary-material":
        return None

    nodenames = ["fig", "media", "sub-article"]
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
    asset = "supp"
    if first(extract_nodes(tag, "label")):
        label_text = node_text(first(extract_nodes(tag, "label"))).lower()
        # Keyword match the label
        if label_text.find("code") > 0:
            asset = "code"
        elif label_text.find("data") > 0:
            asset = "data"
    return asset


def copy_attribute(source, source_key, destination, destination_key=None):
    if destination_key is None:
        destination_key = source_key
    if source is not None:
        if source is not None and destination is not None and source_key in source:
            destination[destination_key] = source[source_key]


def first_node_str_contents(soup, nodename, attr=None, value=None):
    return node_contents_str(
        first(extract_nodes(soup, nodename, attr=attr, value=value))
    )


def set_if_value(dictionary, key, value):
    if value is not None:
        dictionary[key] = value


def prune_dict_of_none_values(dictionary):
    return dict((k, v) for k, v in dictionary.items() if v is not None)


def text_to_title(value):
    """when a title is required, generate one from the value"""
    title = None
    if not value:
        return title
    words = value.split(" ")
    keep_words = []
    for word in words:
        if word.endswith(".") or word.endswith(":"):
            keep_words.append(word)
            if len(word) > 1 and "<italic>" not in word and "<i>" not in word:
                break
        else:
            keep_words.append(word)
    if len(keep_words) > 0:
        title = " ".join(keep_words)
        if title.split(" ")[-1] != "spp.":
            title = title.rstrip(" .:")
    return title


def rstrip_punctuation(value):
    "strip punctuation from the end of a label or title"
    if not value:
        return value
    return value.rstrip(".:")


def escape_unmatched_angle_brackets(string, allowed_tag_fragments=()):
    """
    In order to make an XML string less malformed, escape
    unmatched less than tags that are not part of an allowed tag
    Note: Very, very basic, and do not try regex \1 style replacements
      on unicode ever again! Instead this uses string replace
    allowed_tag_fragments is a tuple of tag name matches for use with startswith()
    """
    if not string:
        return string

    # Split string on tags
    tags = re.split("(<.*?>)", string)
    # print tags

    for i, val in enumerate(tags):
        # Use angle bracket character counts to find unmatched tags
        #  as well as our allowed_tags list to ignore good tags

        if val.count("<") == val.count(">") and not val.startswith(
            allowed_tag_fragments
        ):
            val = val.replace("<", "&lt;")
            val = val.replace(">", "&gt;")
        else:
            # Count how many unmatched tags we have
            while val.count("<") != val.count(">"):
                if val.count("<") != val.count(">") and val.count("<") > 0:
                    val = val.replace("<", "&lt;", 1)
                elif val.count("<") != val.count(">") and val.count(">") > 0:
                    val = val.replace(">", "&gt;", 1)
            if val.count("<") == val.count(">") and not val.startswith(
                allowed_tag_fragments
            ):
                # Send it through again in case there are nested unmatched tags
                val = escape_unmatched_angle_brackets(val, allowed_tag_fragments)

        tags[i] = val

    return "".join(tags)


def escape_ampersand(string):
    """
    Quick convert unicode ampersand characters not associated with
    a numbered entity or not starting with allowed characters to a plain &amp;
    """
    if not string:
        return string
    start_with_match = r"(\#x(....);|lt;|gt;|amp;)"
    # The pattern below is match & that is not immediately followed by #
    string = re.sub(r"&(?!" + start_with_match + ")", "&amp;", string)
    return string


def remove_tag(tag_name, string):
    "remove open tag and its attributes and remove close tag from an XML string"
    pattern = r"\n*</?%s.*?>\n*" % tag_name
    return re.sub(pattern, "", string) if string else ""


def remove_tag_and_text(tag_name, string):
    "remove open tag and close tag and the contents between them from an XML string"
    pattern = r"\n*<%s.*?>.*?</%s>\n*" % (tag_name, tag_name)
    return remove_tag(tag_name, re.sub(pattern, "", string)) if string else ""


def article_author_person(ref_author):
    return generate_author_person(ref_author, "article_author")


def references_author_person(ref_author):
    return generate_author_person(ref_author, "reference_author")


def generate_author_person(ref_author, preferred_format):
    "Create a person data structure, its preferred value depends on the preferred_format type"
    author_json = OrderedDict()
    author_json["type"] = "person"
    author_name = OrderedDict()

    if preferred_format == "article_author":
        author_name["preferred"] = author_preferred_name(
            ref_author.get("surname"),
            ref_author.get("given-names"),
            ref_author.get("suffix"),
        )
    elif preferred_format == "reference_author":
        author_name["preferred"] = reference_author_preferred_name(
            ref_author.get("surname"),
            ref_author.get("given-names"),
            ref_author.get("suffix"),
        )

    author_name["index"] = author_index_name(
        ref_author.get("surname"),
        ref_author.get("given-names"),
        ref_author.get("suffix"),
    )
    author_json["name"] = author_name
    return author_json


def reference_author_preferred_name(surname, given_names, suffix):
    # join surname given_names suffix, in that order, with a space character
    return " ".join(
        [element for element in [surname, given_names, suffix] if element is not None]
    )


def author_preferred_name(surname, given_names, suffix):
    return " ".join(
        [element for element in [given_names, surname, suffix] if element is not None]
    )


def author_index_name(surname, given_names, suffix):
    index_name = ", ".join(
        [element for element in [surname, given_names, suffix] if element is not None]
    )
    return index_name


def list_type_prefix(list_type):
    """from a JATS list list-type attribute return a list style prefix"""
    if list_type:
        if list_type == "simple":
            return "none"
        if list_type == "order":
            return "number"
        return list_type
    return "none"
