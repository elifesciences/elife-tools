from bs4 import BeautifulSoup
import cgi
import htmlentitydefs
import os
import time
import calendar
from slugify import slugify
from utils import *
import rawJATS as raw_parser
import re
from collections import OrderedDict


import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(os.getcwd() + os.sep + 'test.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


def parse_xml(xml):
    return BeautifulSoup(xml, ["lxml", "xml"])

def parse_document(filelocation):
    return parse_xml(open(filelocation))

def duplicate_tag(tag):
    # Make a completely new copy of a tag by parsing its contents again
    soup_copy = parse_xml(unicode(tag))
    tag_copy = first(extract_nodes(soup_copy, tag.name))
    return tag_copy

def title(soup):
    return node_text(raw_parser.article_title(soup))
    
def full_title(soup):
    # The title including italic tags, etc.
    return node_contents_str(raw_parser.article_title(soup))

def title_short(soup):
    "'title' truncated to 20 chars"
    # TODO: 20 is arbitrary, 
    return title(soup)[:20]

def title_slug(soup):
    "'title' slugified"
    return slugify(title(soup))

def doi(soup):
    # the first non-nil value returned by the raw parser
    return node_text(raw_parser.doi(soup))

def publisher_id(soup):
    # aka the article_id, specified by the publisher
    return node_text(raw_parser.publisher_id(soup))

def journal_id(soup):
    return node_text(raw_parser.journal_id(soup))

def journal_title(soup):
    return node_text(raw_parser.journal_title(soup))

def journal_issn(soup, pub_format = None):
    if pub_format:
        return node_text(raw_parser.journal_issn(soup, pub_format))

def publisher(soup):
    return node_text(raw_parser.publisher(soup))

def article_type(soup):
    # no node text extraction required
    return raw_parser.article_type(soup)

def volume(soup):
    return node_text(first(raw_parser.volume(soup)))

def elocation_id(soup):
    return node_text(first(raw_parser.elocation_id(soup)))
    
def research_organism(soup):
    "Find the research-organism from the set of kwd-group tags"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return map(node_text, raw_parser.research_organism_keywords(soup))

def full_research_organism(soup):
    "research-organism list including inline tags, such as italic"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return map(node_contents_str, raw_parser.research_organism_keywords(soup))

def keywords(soup):
    """
    Find the keywords from the set of kwd-group tags
    which are typically labelled as the author keywords
    """
    if not raw_parser.author_keywords(soup):
        return []
    return map(node_text, raw_parser.author_keywords(soup))

def full_keywords(soup):
    "author keywords list including inline tags, such as italic"
    if not raw_parser.author_keywords(soup):
        return []
    return map(node_contents_str, raw_parser.author_keywords(soup))

def full_keyword_groups(soup):
    groups = {}
    for group_tag in raw_parser.keyword_group(soup):
        group = map(node_contents_str, extract_nodes(group_tag, "kwd"))
        group = map(lambda s: s.strip(), group)
        if 'kwd-group-type' in group_tag.attrs:
            groups[group_tag['kwd-group-type'].strip()] = group
    return groups

def full_custom_meta(soup, meta_name=None):
    return raw_parser.custom_meta(soup, meta_name)

def impact_statement(soup):
    tag = first(full_custom_meta(soup, "Author impact statement"))
    if tag is not None:
        return node_contents_str(first(extract_nodes(tag, "meta-value")))
    return ""


def format_related_object(related_object):
    return related_object["id"], {}


def related_object_ids(soup):
    tags = raw_parser.related_object(soup)
    return dict(map(format_related_object, tags))

@strippen
def acknowledgements(soup):
    return node_text(raw_parser.acknowledgements(soup))

# DEPRECATED: use `acknowledgements`. avoid unnecessary abbreviations
def ack(soup):
    return acknowledgements(soup)

@nullify
@strippen
def conflict(soup):
    return map(node_text, raw_parser.conflict(soup))

def copyright_statement(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    return node_text(raw_parser.copyright_statement(permissions_tag))

@inten
def copyright_year(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    return node_text(raw_parser.copyright_year(permissions_tag))

def copyright_holder(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    return node_text(raw_parser.copyright_holder(permissions_tag))

def license(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    return node_text(raw_parser.licence_p(permissions_tag))

def full_license(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    return node_contents_str(raw_parser.licence_p(permissions_tag))

def license_url(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    return raw_parser.licence_url(permissions_tag)

def funding_statement(soup):
    return node_text(raw_parser.funding_statement(soup))


#
# authors
#

#
# refs
#


def ref_text(tag):
    # ref - human readable full reference text
    ref_text = node_text(tag)
    ref_text = strip_strings(ref_text)
    # Remove excess space
    ref_text = ' '.join(ref_text.split())
    # Fix punctuation spaces and extra space
    ref_text = strip_punctuation_space(strip_strings(ref_text))
    return ref_text


def subject_area(soup):
    """
    Find the subject areas from article-categories subject tags
    """
    subject_area = []
    
    tags = raw_parser.subject_area(soup)
    for tag in tags:
        subject_area.append(node_text(tag))
        
    return subject_area

def full_subject_area(soup):
    subject_areas = raw_parser.full_subject_area(soup)
    areas = {}
    for tag in subject_areas:
        subj_type = tag['subj-group-type']
        if subj_type not in areas:
            areas[subj_type] = []
        areas[subj_type].append(tag.get_text().strip())
    return areas


def display_channel(soup):
    """
    Find the subject areas of type display-channel
    """
    display_channel = []
    
    tags = raw_parser.display_channel(soup)
    for tag in tags:
        display_channel.append(node_text(tag))
        
    return display_channel

def category(soup):
    """
    Find the category from subject areas
    """
    category = []
    
    tags = raw_parser.category(soup)
    for tag in tags:
        category.append(node_text(tag))
        
    return category

def ymd(soup):
    """
    Get the year, month and day from child tags
    """
    day = node_text(raw_parser.day(soup))
    month = node_text(raw_parser.month(soup))
    year = node_text(raw_parser.year(soup))
    return (day, month, year)

def pub_date(soup):
    """
    Return the publishing date in struct format
    pub_date_date, pub_date_day, pub_date_month, pub_date_year, pub_date_timestamp
    Default date_type is pub
    """
    pub_date = raw_parser.pub_date(soup, date_type = "pub")
    if pub_date is None:
        return None
    (day, month, year) = ymd(pub_date)
    return date_struct(year, month, day)

def history_date(soup, date_type = None):
    """
    Find a date in the history tag for the specific date_type
    typical date_type values: received, accepted
    """
    if(date_type == None):
        return None
    
    history_date = raw_parser.history_date(soup, date_type)
    if history_date is None:
        return None
    (day, month, year) = ymd(history_date)
    return date_struct(year, month, day)

def pub_date_date(soup):
    """
    Find the published date in human readable form
    """
    return date_text(pub_date(soup))

def pub_date_day(soup):
    """
    Find the published date day
    """
    return day_text(pub_date(soup))

def pub_date_month(soup):
    """
    Find the published date month
    """
    return month_text(pub_date(soup))
    
def pub_date_year(soup):
    """
    Find the published date year
    """
    return year_text(pub_date(soup))

def pub_date_timestamp(soup):
    """
    Find the published date timestamp, in UTC time
    """
    return date_timestamp(pub_date(soup))

def received_date_date(soup):
    """
    Find the received date in human readable form
    """
    return date_text(history_date(soup, date_type = "received"))
    
def received_date_day(soup):
    """
    Find the received date day
    """
    return day_text(history_date(soup, date_type = "received"))

def received_date_month(soup):
    """
    Find the received date month
    """
    return month_text(history_date(soup, date_type = "received"))
    
def received_date_year(soup):
    """
    Find the received date year
    """
    return year_text(history_date(soup, date_type = "received"))
    
def received_date_timestamp(soup):
    """
    Find the received date timestamp, in UTC time
    """
    return date_timestamp(history_date(soup, date_type = "received"))
    
def accepted_date_date(soup):
    """
    Find the accepted date in human readable form
    """
    return date_text(history_date(soup, date_type = "accepted"))
    
def accepted_date_day(soup):
    """
    Find the accepted date day
    """
    return day_text(history_date(soup, date_type = "accepted"))

def accepted_date_month(soup):
    """
    Find the accepted date month
    """
    return month_text(history_date(soup, date_type = "accepted"))
    
def accepted_date_year(soup):
    """
    Find the accepted date year
    """
    return year_text(history_date(soup, date_type = "accepted"))

def accepted_date_timestamp(soup):
    """
    Find the accepted date timestamp, in UTC time
    """
    return date_timestamp(history_date(soup, date_type = "accepted"))
    
def collection_year(soup):
    """
    Pub date of type collection will hold a year element for VOR articles
    """
    pub_date = raw_parser.pub_date_collection(soup, pub_type = "collection")
    if pub_date is None:
        return None
    
    year = None
    year_tag = raw_parser.year(pub_date)
    if year_tag:
        year = int(node_text(year_tag))
        
    return year

def is_poa(soup):
    """
    Test for whether is POA XML or not
    """
    if collection_year(soup) is None:
        return True
    else:
        return False


def abstracts(soup):
    """
    Find the article abstract and format it
    """

    abstracts = []

    abstract_tags = raw_parser.abstract(soup)

    for tag in abstract_tags:
        abstract = {}
        
        abstract["abstract_type"] = tag.get("abstract-type")
        title_tag = raw_parser.title(tag)
        if title_tag:    
            abstract["title"] = node_text(title_tag)
        
        abstract["content"] = None
        if len(paragraphs(tag)) > 0:
            abstract["content"] = ""
            abstract["full_content"] = ""
            
            good_paragraphs = remove_doi_paragraph(paragraphs(tag))
            
            # Plain text content
            glue = ""
            for p_tag in good_paragraphs:
                abstract["content"] += glue + node_text(p_tag)
                glue = " "
            
            # Content including markup tags
            # When more than one paragraph, wrap each in a <p> tag
            for p_tag in good_paragraphs:
                abstract["full_content"] += '<p>' + node_contents_str(p_tag) + '</p>'            
    
        abstracts.append(abstract)

    return abstracts


def abstract(soup):
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = first(filter(lambda tag: tag.get("abstract_type") is None, abstract_list))
    if abstract:
        return abstract.get("content")
    else:
        return None

def full_abstract(soup):
    """
    Return the abstract including inline tags
    """
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = first(filter(lambda tag: tag.get("abstract_type") is None, abstract_list))
    if abstract:
        return abstract.get("full_content")
    else:
        return None

def digest(soup):
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = first(filter(lambda tag: tag.get("abstract_type") == "executive-summary",
                                abstract_list))
    if abstract:
        return abstract.get("content")
    else:
        return None

def full_digest(soup):
    """
    Return the digest including inline tags
    """
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = first(filter(lambda tag: tag.get("abstract_type") == "executive-summary",
                                abstract_list))
    if abstract:
        return abstract["full_content"]
    else:
        return None

def related_article(soup):
    related_articles = []
    
    related_article_tags = raw_parser.related_article(soup)

    for tag in related_article_tags:
        related_article = {}
        related_article["ext_link_type"] = tag.get("ext-link-type")
        related_article["related_article_type"] =tag.get("related-article-type")
        related_article["xlink_href"] = tag.get("xlink:href")
        related_articles.append(related_article)
    
    return related_articles

def component_doi(soup):
    """
    Look for all object-id of pub-type-id = doi, these are the component DOI tags
    """
    component_doi = []
    
    object_id_tags = raw_parser.object_id(soup, pub_id_type = "doi")

    # Get components too for later
    component_list = components(soup)

    position = 1

    for tag in object_id_tags:
        component_object = {}
        component_object["doi"] = tag.text
        component_object["position"] = position
        
        # Try to find the type of component
        for component in component_list:
            if "doi" in component and component["doi"] == component_object["doi"]:
                component_object["type"] = component["type"] 

        component_doi.append(component_object)
        
        position = position + 1
    
    return component_doi

def tag_details_sibling_ordinal(tag):
    sibling_ordinal = None
    
    if ((tag.name == "fig" and 'specific-use' not in tag.attrs)
         or tag.name == "media"):
        # Fig that is not a child figure / figure supplement
        if first_parent(tag, 'sub-article'):
            # Sub-article sibling ordinal numbers work differently
            sibling_ordinal = tag_subarticle_sibling_ordinal(tag)
        elif first_parent(tag, 'app'):
            sibling_ordinal = tag_appendix_sibling_ordinal(tag)
        elif tag.name == "media":
            # Media video or non-video are different numbering
            sibling_ordinal = tag_media_sibling_ordinal(tag)
        else:
            sibling_ordinal = tag_fig_ordinal(tag)
    elif tag.name == "supplementary-material":
        sibling_ordinal = tag_supplementary_material_sibling_ordinal(tag)
    else:
        # Default
        sibling_ordinal = tag_sibling_ordinal(tag)
        
    return sibling_ordinal

def tag_details_asset(tag):
    asset = None
    
    if tag.name == "fig" and 'specific-use' in tag.attrs:
        # Child figure / figure supplement
        asset = 'figsupp'
    elif tag.name == "media":
        # Set media tag asset value, it is useful
        asset = 'media'
    elif tag.name == "app":
        asset = 'app'
    elif tag.name == "supplementary-material":
        # Default is supp
        asset = supp_asset(tag)
    elif tag.name == "sub-article":
        if (node_text(raw_parser.article_title(tag)) and
            node_text(raw_parser.article_title(tag)).lower() == 'decision letter'):
            asset = 'dec'
        elif (node_text(raw_parser.article_title(tag)) and
              node_text(raw_parser.article_title(tag)).lower() == 'author response'):
            asset = 'resp'
        
    return asset


def tag_details(tag, nodenames):
    """
    Used in media and graphics to extract data from their parent tags
    """
    details = {}

    details['type'] = tag.name
    details['ordinal'] = tag_ordinal(tag)
    
    # Ordinal value
    if tag_details_sibling_ordinal(tag):
        details['sibling_ordinal'] = tag_details_sibling_ordinal(tag)

    # Asset name
    if tag_details_asset(tag):
        details['asset'] = tag_details_asset(tag)
    
    object_id_tag = first(raw_parser.object_id(tag, pub_id_type= "doi"))
    if object_id_tag:
        details['component_doi'] = extract_component_doi(tag, nodenames)
    
    return details


def media(soup):
    """
    All media tags and some associated data about the related component doi
    and the parent of that doi (not always present)
    """
    media = []
    
    media_tags = raw_parser.media(soup)
    
    position = 1
    
    for tag in media_tags:
        media_item = {}
        
        copy_attribute(tag.attrs, 'mime-subtype', media_item)
        copy_attribute(tag.attrs, 'mimetype', media_item)
        copy_attribute(tag.attrs, 'xlink:href', media_item, 'xlink_href')
        copy_attribute(tag.attrs, 'content-type', media_item)
        
        nodenames = ["sub-article", "media", "fig-group", "fig", "supplementary-material"]

        details = tag_details(tag, nodenames)
        copy_attribute(details, 'component_doi', media_item)
        copy_attribute(details, 'type', media_item)
        copy_attribute(details, 'sibling_ordinal', media_item)

        # Try to get the component DOI of the parent tag
        parent_tag = first_parent(tag, nodenames)
        if parent_tag:
            acting_parent_tag = component_acting_parent_tag(parent_tag, tag)
            if acting_parent_tag:
                details = tag_details(acting_parent_tag, nodenames)
                copy_attribute(details, 'type', media_item, 'parent_type')
                copy_attribute(details, 'ordinal', media_item, 'parent_ordinal')
                copy_attribute(details, 'asset', media_item, 'parent_asset')
                copy_attribute(details, 'sibling_ordinal', media_item, 'parent_sibling_ordinal')
                copy_attribute(details, 'component_doi', media_item, 'parent_component_doi')
        
            # Try to get the parent parent
            p_parent_tag = first_parent(parent_tag, nodenames)
            if p_parent_tag:
                acting_p_parent_tag = component_acting_parent_tag(p_parent_tag, parent_tag)
                if acting_p_parent_tag:
                    details = tag_details(acting_p_parent_tag, nodenames)
                    copy_attribute(details, 'type', media_item, 'p_parent_type')
                    copy_attribute(details, 'ordinal', media_item, 'p_parent_ordinal')
                    copy_attribute(details, 'asset', media_item, 'p_parent_asset')
                    copy_attribute(details, 'sibling_ordinal', media_item, 'p_parent_sibling_ordinal')
                    copy_attribute(details, 'component_doi', media_item, 'p_parent_component_doi')
                
                # Try to get the parent parent parent
                p_p_parent_tag = first_parent(p_parent_tag, nodenames)
                if p_p_parent_tag:
                    acting_p_p_parent_tag = component_acting_parent_tag(p_p_parent_tag, p_parent_tag)
                    if acting_p_p_parent_tag:
                        details = tag_details(acting_p_p_parent_tag, nodenames)
                        copy_attribute(details, 'type', media_item, 'p_p_parent_type')
                        copy_attribute(details, 'ordinal', media_item, 'p_p_parent_ordinal')
                        copy_attribute(details, 'asset', media_item, 'p_p_parent_asset')
                        copy_attribute(details, 'sibling_ordinal', media_item, 'p_p_parent_sibling_ordinal')
                        copy_attribute(details, 'component_doi', media_item, 'p_p_parent_component_doi')

        # Increment the position
        media_item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        media_item['ordinal'] = tag_ordinal(tag)
        
        media.append(media_item)
        
        position += 1
    
    return media
    
    
def graphics(soup):
    """
    All graphic tags and some associated data about the related component doi
    and the parent of that doi (not always present), and whether it is
    part of a figure supplement
    """
    graphics = []
    
    graphic_tags = raw_parser.graphic(soup)
    
    position = 1
    
    for tag in graphic_tags:
        graphic_item = {}
        
        copy_attribute(tag.attrs, 'xlink:href', graphic_item, 'xlink_href')
        
        # Get the tag type
        nodenames = ["sub-article", "fig-group", "fig", "app"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', graphic_item)
        
        parent_tag = first_parent(tag, nodenames)
        if parent_tag:
            details = tag_details(parent_tag, nodenames)
            copy_attribute(details, 'type', graphic_item, 'parent_type')
            copy_attribute(details, 'ordinal', graphic_item, 'parent_ordinal')
            copy_attribute(details, 'asset', graphic_item, 'parent_asset')
            copy_attribute(details, 'sibling_ordinal', graphic_item, 'parent_sibling_ordinal')
            copy_attribute(details, 'component_doi', graphic_item, 'parent_component_doi')

            # Try to get the parent parent - special for looking at fig tags
            #  use component_acting_parent_tag
            p_parent_tag = first_parent(parent_tag, nodenames)
            if p_parent_tag:
                acting_p_parent_tag = component_acting_parent_tag(p_parent_tag, parent_tag)
                if acting_p_parent_tag:
                    details = tag_details(acting_p_parent_tag, nodenames)
                    copy_attribute(details, 'type', graphic_item, 'p_parent_type')
                    copy_attribute(details, 'ordinal', graphic_item, 'p_parent_ordinal')
                    copy_attribute(details, 'asset', graphic_item, 'p_parent_asset')
                    copy_attribute(details, 'sibling_ordinal', graphic_item, 'p_parent_sibling_ordinal')
                    copy_attribute(details, 'component_doi', graphic_item, 'p_parent_component_doi')
                            
        # Increment the position
        graphic_item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        graphic_item['ordinal'] = tag_ordinal(tag)
        
        graphics.append(graphic_item)
        
        position += 1
    
    return graphics

def inline_graphics(soup):
    """
    inline-graphic tags
    """
    inline_graphics = []
    
    inline_graphic_tags = raw_parser.inline_graphic(soup)
    
    position = 1
    
    for tag in inline_graphic_tags:
        item = {}
        
        copy_attribute(tag.attrs, 'xlink:href', item, 'xlink_href')

        # Get the tag type
        nodenames = ["sub-article"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', item)

        # Increment the position
        item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        item['ordinal'] = tag_ordinal(tag)
        
        inline_graphics.append(item)

    return inline_graphics

def self_uri(soup):
    """
    self-uri tags
    """
    
    self_uri = []
    self_uri_tags = raw_parser.self_uri(soup)
    position = 1
    for tag in self_uri_tags:
        item = {}
        
        copy_attribute(tag.attrs, 'xlink:href', item, 'xlink_href')
        copy_attribute(tag.attrs, 'content-type', item)
        
        # Get the tag type
        nodenames = ["sub-article"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', item)
        
        # Increment the position
        item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        item['ordinal'] = tag_ordinal(tag)
        
        self_uri.append(item)
        
    return self_uri

def supplementary_material(soup):
    """
    supplementary-material tags
    """
    supplementary_material = []
    
    supplementary_material_tags = raw_parser.supplementary_material(soup)
    
    position = 1
    
    for tag in supplementary_material_tags:
        item = {}
        
        copy_attribute(tag.attrs, 'id', item)

        # Get the tag type
        nodenames = ["supplementary-material"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', item)
        copy_attribute(details, 'asset', item)
        copy_attribute(details, 'component_doi', item)
        copy_attribute(details, 'sibling_ordinal', item)
        
        if raw_parser.label(tag):
            item['label'] = node_text(raw_parser.label(tag))
            item['full_label'] = node_contents_str(raw_parser.label(tag))

        # Increment the position
        item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        item['ordinal'] = tag_ordinal(tag)
        
        supplementary_material.append(item)

    return supplementary_material


def add_to_list_dictionary(list_dict, list_key, val):
    if val is not None:
        if list_key not in list_dict:
            list_dict[list_key] = []
        list_dict[list_key].append(val)

def contrib_email(contrib_tag):
    """
    Given a contrib tag, look for an email tag, and
    only return the value if it is not inside an aff tag
    """
    email = None
    for email_tag in extract_nodes(contrib_tag, "email"):
        if email_tag.parent.name != "aff":
            email = email_tag.text
    return email

def contrib_phone(contrib_tag):
    """
    Given a contrib tag, look for an phone tag
    """
    phone = None
    if raw_parser.phone(contrib_tag):
        phone = first(raw_parser.phone(contrib_tag)).text
    return phone


def format_contributor(contrib_tag, soup, detail="brief"):
    contributor = {}
    copy_attribute(contrib_tag.attrs, 'contrib-type', contributor, 'type')
    copy_attribute(contrib_tag.attrs, 'equal-contrib', contributor)
    copy_attribute(contrib_tag.attrs, 'corresp', contributor)
    copy_attribute(contrib_tag.attrs, 'deceased', contributor)
    copy_attribute(contrib_tag.attrs, 'id', contributor)
    contrib_id_tag = first(raw_parser.contrib_id(contrib_tag))
    if contrib_id_tag and 'contrib-id-type' in contrib_id_tag.attrs:
        if contrib_id_tag['contrib-id-type'] == 'group-author-key':
            contributor['group-author-key'] = node_contents_str(contrib_id_tag)
        elif contrib_id_tag['contrib-id-type'] == 'orcid':
            contributor['orcid'] = node_contents_str(contrib_id_tag)
    set_if_value(contributor, "collab", first_node_str_contents(contrib_tag, "collab"))
    set_if_value(contributor, "role", first_node_str_contents(contrib_tag, "role"))
    set_if_value(contributor, "email", contrib_email(contrib_tag))
    set_if_value(contributor, "phone", contrib_phone(contrib_tag))
    name_tag = first(extract_nodes(contrib_tag, "name"))
    if name_tag is not None:
        set_if_value(contributor, "surname", first_node_str_contents(name_tag, "surname"))
        set_if_value(contributor, "given-names", first_node_str_contents(name_tag, "given-names"))
        set_if_value(contributor, "suffix", first_node_str_contents(name_tag, "suffix"))

    # on-behalf-of
    if contrib_tag.name == 'on-behalf-of':
        contributor['type'] = 'on-behalf-of'
        contributor['on-behalf-of'] = node_contents_str(contrib_tag)

    contrib_refs = {}
    ref_tags = extract_nodes(contrib_tag, "xref")
    ref_type_aff_count = 0
    for ref_tag in ref_tags:
        if "ref-type" in ref_tag.attrs and "rid" in ref_tag.attrs:
            ref_type = ref_tag['ref-type']
            rid = ref_tag['rid']

            if ref_type == "aff":
                ref_type_aff_count += 1
                add_to_list_dictionary(contrib_refs, 'affiliation', rid)
            if ref_type == "corresp":
                # Check for email or phone type
                corresp_tag = firstnn(soup.find_all(id=rid))
                if contrib_phone(corresp_tag):
                    add_to_list_dictionary(contrib_refs, 'phone', rid)
                elif contrib_email(corresp_tag):
                    add_to_list_dictionary(contrib_refs, 'email', rid)
            if ref_type == "fn":
                if rid.startswith('equal-contrib'):
                    add_to_list_dictionary(contrib_refs, 'equal-contrib', rid)
                elif rid.startswith('conf'):
                    add_to_list_dictionary(contrib_refs, 'competing-interest', rid)
                elif rid.startswith('con'):  # not conf though, see above!
                    add_to_list_dictionary(contrib_refs, 'contribution', rid)
                elif rid.startswith('pa'):
                    add_to_list_dictionary(contrib_refs, 'present-address', rid)
                elif rid.startswith('fn'):
                    add_to_list_dictionary(contrib_refs, 'foot-note', rid)
            elif ref_type == "other":
                if rid.startswith('par-'):
                    add_to_list_dictionary(contrib_refs, 'funding', rid)
                elif rid.startswith('dataro'):
                    add_to_list_dictionary(contrib_refs, 'related-object', rid)

    if len(contrib_refs) > 0:
        contributor['references'] = contrib_refs

    if detail == "brief" or ref_type_aff_count == 0:
        # Brief format only allows one aff and it must be within the contrib tag
        aff_tag = first(extract_nodes(contrib_tag, "aff"))
        if aff_tag:
            contributor['affiliations'] = []
            contrib_affs = {}
            (none_return, aff_detail) = format_aff(aff_tag)
            if len(aff_detail) > 0:
                aff_attributes = ['dept', 'institution', 'country', 'city', 'email']
                for aff_attribute in aff_attributes:
                    if aff_attribute in aff_detail and aff_detail[aff_attribute] is not None:
                        copy_attribute(aff_detail, aff_attribute, contrib_affs)
                if len(contrib_affs) > 0:
                    contributor['affiliations'].append(contrib_affs)

    if detail == "full":
        # person_id
        if 'id' in contributor:
            if contributor['id'].startswith("author"):
                person_id = contributor['id'].replace("author-", "")
                contributor['person_id'] = int(person_id)
        # Author - given names + surname
        author_name = ""
        if 'given-names' in contributor:
            author_name += contributor['given-names'] + " "
        if 'surname' in contributor:
            author_name += contributor['surname']
        if author_name != "":
            contributor['author'] = author_name
    
        aff_tags = extract_nodes(contrib_tag, "xref", attr = "ref-type", value = "aff")
        if len(aff_tags) <= 0:
            # No aff found? Look for an aff tag inside the contrib tag
            aff_tags = extract_nodes(contrib_tag, "aff")
        if aff_tags:
            contributor['affiliations'] = []
        for aff_tag in aff_tags:
            contrib_affs = {}
            rid = aff_tag.get('rid')
            if rid:
                # Look for the matching aff tag by rid
                aff_node = first(extract_nodes(soup, "aff", attr = "id", value = rid)) 
            else:
                # Aff tag inside contrib tag
                aff_node = aff_tag
            
            (none_return, aff_detail) = format_aff(aff_node)
            
            if len(aff_detail) > 0:
                aff_attributes = ['dept', 'institution', 'country', 'city', 'email']
                for aff_attribute in aff_attributes:
                    if aff_attribute in aff_detail and aff_detail[aff_attribute] is not None:
                        copy_attribute(aff_detail, aff_attribute, contrib_affs)
                contributor['affiliations'].append(contrib_affs)
    
        # Add xref linked correspondence author notes if applicable
        corresp_tags = extract_nodes(contrib_tag, "xref", attr = "ref-type", value = "corresp")
        if(len(corresp_tags) > 0):
            if 'notes-corresp' not in contributor:
                contributor['notes-corresp'] = []
            target_tags = raw_parser.corresp(soup)
            for cor in corresp_tags:
                # Find the matching tag
                rid = cor['rid']
                corresp_node = first(filter(lambda tag: tag.get("id") == rid, target_tags))
                author_notes = node_text(corresp_node)
                if author_notes:
                    contributor['notes-corresp'].append(author_notes)
        
        # Add xref linked footnotes if applicable
        fn_tags = extract_nodes(contrib_tag, "xref", attr = "ref-type", value = "fn")
        if(len(fn_tags) > 0):
            if 'notes-fn' not in contributor:
                contributor['notes-fn'] = []
            target_tags = raw_parser.fn(soup)
            for fn in fn_tags:
               # Find the matching tag
               rid = fn['rid']
               fn_node = first(filter(lambda tag: tag.get("id") == rid, target_tags))
               fn_text = node_text(fn_node)
               if fn_text:
                   contributor['notes-fn'].append(fn_text)
    
    return contributor

def contributors(soup, detail="brief"):
    contrib_tags = raw_parser.article_contributors(soup)
    contributors = []
    for tag in contrib_tags:
        contributors.append(format_contributor(tag, soup, detail))
    return contributors

#
# HERE BE DRAGONS
#

def authors_non_byline(soup):
    """Non-byline authors for group author members"""
    authors_list = authors(soup, contrib_type = "author non-byline")
    return authors_list

def authors(soup, contrib_type = "author", detail = "full"):

    tags = raw_parser.authors(soup, contrib_type)
    authors = []
    position = 1
    
    article_doi = doi(soup)
    
    for tag in tags:
        author = format_contributor(tag, soup, detail)

        # If not empty, add position value, append, then increment the position counter
        if(len(author) > 0):
            author['article_doi'] = article_doi
            
            author['position'] = position
                        
            authors.append(author)
            position += 1
        
    return authors


def format_aff(aff_tag):
    values = {
        'dept': node_contents_str(first(extract_nodes(aff_tag, "institution", "content-type", "dept"))),
        'institution': node_contents_str(first(
            filter(lambda n: "content-type" not in n.attrs, extract_nodes(aff_tag, "institution")))),
        'city': node_contents_str(first(extract_nodes(aff_tag, "named-content", "content-type", "city"))),
        'country': node_contents_str(first(extract_nodes(aff_tag, "country"))),
        'email': node_contents_str(first(extract_nodes(aff_tag, "email")))
        }
    # Remove keys with None value
    prune_dict_of_none_values(values)

    if 'id' in aff_tag.attrs:
        return aff_tag['id'], values
    else:
        return None, values


def full_affiliation(soup):
    aff_tags = raw_parser.affiliation(soup)
    aff_tags = filter(lambda aff: 'id' in aff.attrs, aff_tags)
    affs = []
    for tag in aff_tags:
        aff = {}
        (id, aff_details) = format_aff(tag)
        aff[id] = aff_details
        affs.append(aff)
    return affs


def references(soup):
    """Renamed to refs"""
    return refs(soup)
    
def refs(soup):
    """Find and return all the references"""
    tags = raw_parser.ref_list(soup)
    refs = []
    position = 1

    article_doi = doi(soup)

    for tag in tags:
        ref = {}

        ref['ref'] = ref_text(tag)

        # ref_id
        copy_attribute(tag.attrs, "id", ref)

        # article_title
        if raw_parser.article_title(tag):
            ref['article_title'] = node_text(raw_parser.article_title(tag))
            ref['full_article_title'] = node_contents_str(raw_parser.article_title(tag))

        if raw_parser.pub_id(tag, "pmid"):
            ref['pmid'] = node_contents_str(first(raw_parser.pub_id(tag, "pmid")))

        if raw_parser.pub_id(tag, "isbn"):
            ref['isbn'] = node_contents_str(first(raw_parser.pub_id(tag, "isbn")))

        if raw_parser.pub_id(tag, "doi"):
            ref['reference_id'] = node_contents_str(first(raw_parser.pub_id(tag, "doi")))
            ref['doi'] = node_contents_str(first(raw_parser.pub_id(tag, "doi")))

        if raw_parser.ext_link(tag, "uri"):
            uri_tag = first(raw_parser.ext_link(tag, "uri"))
            set_if_value(ref, "uri", uri_tag.get('xlink:href'))
            set_if_value(ref, "uri_text", node_contents_str(uri_tag))

        set_if_value(ref, "year", node_text(raw_parser.year(tag)))
        set_if_value(ref, "source", node_text(first(raw_parser.source(tag))))
        set_if_value(ref, "elocation-id", node_text(first(raw_parser.elocation_id(tag))))
        copy_attribute(first(raw_parser.element_citation(tag)).attrs, "publication-type", ref)

        # authors
        person_group = raw_parser.person_group(tag)
        authors = []

        for group in person_group:

            author_type = None
            if "person-group-type" in group.attrs:
                author_type = group["person-group-type"]

            # Read name or collab tag in the order they are listed
            for name_or_collab_tag in extract_nodes(group, ["name","collab"]):
                author = {}

                # Shared tag attribute
                set_if_value(author, "group-type", author_type)

                # name tag attributes
                if name_or_collab_tag.name == "name":
                    set_if_value(author, "surname", node_text(first(raw_parser.surname(name_or_collab_tag))))
                    set_if_value(author, "given-names", node_text(first(raw_parser.given_names(name_or_collab_tag))))
                    set_if_value(author, "suffix", node_text(first(raw_parser.suffix(name_or_collab_tag))))

                # collab tag attribute
                if name_or_collab_tag.name == "collab":
                    set_if_value(author, "collab", node_contents_str(name_or_collab_tag))

                if len(author) > 0:
                    authors.append(author)

            # etal for the person group
            if first(raw_parser.etal(group)):
                author = {}
                author['etal'] = True
                set_if_value(author, "group-type", author_type)
                authors.append(author)

        # Check for collab tag not wrapped in a person-group for backwards compatibility
        if len(person_group) == 0:
            collab_tags = raw_parser.collab(tag)
            for collab_tag in collab_tags:
                author = {}
                set_if_value(author, "group-type", "author")
                set_if_value(author, "collab", node_contents_str(collab_tag))

                if len(author) > 0:
                    authors.append(author)

        if len(authors) > 0:
            ref['authors'] = authors

        set_if_value(ref, "volume", node_text(first(raw_parser.volume(tag))))
        set_if_value(ref, "fpage", node_text(first(raw_parser.fpage(tag))))
        set_if_value(ref, "lpage", node_text(first(raw_parser.lpage(tag))))
        set_if_value(ref, "collab", node_text(first(raw_parser.collab(tag))))
        set_if_value(ref, "publisher_loc", node_text(first(raw_parser.publisher_loc(tag))))
        set_if_value(ref, "publisher_name", node_text(first(raw_parser.publisher_name(tag))))
        set_if_value(ref, "edition", node_contents_str(first(raw_parser.edition(tag))))
        set_if_value(ref, "chapter-title", node_contents_str(first(raw_parser.chapter_title(tag))))
        set_if_value(ref, "comment", node_text(first(raw_parser.comment(tag))))

        # If not empty, add position value, append, then increment the position counter
        if(len(ref) > 0):
            ref['article_doi'] = article_doi

            ref['position'] = position

            refs.append(ref)
            position += 1

    return refs

def extract_component_doi(tag, nodenames):
    """
    Used to get component DOI from a tag and confirm it is actually for that tag
    and it is not for one of its children in the list of nodenames
    """
    component_doi = None

    if(tag.name == "sub-article"):
        component_doi = node_text(first(raw_parser.article_id(tag, pub_id_type= "doi")))
    else:
        object_id_tag = first(raw_parser.object_id(tag, pub_id_type= "doi"))
        # Tweak: if it is media and has no object_id_tag then it is not a "component"
        if tag.name == "media" and not object_id_tag:
            component_doi = None
        else:
            # Check the object id is for this tag and not one of its children
            #   This happens for example when boxed text has a child figure,
            #   the boxed text does not have a DOI, the figure does have one
            if object_id_tag and first_parent(object_id_tag, nodenames).name == tag.name:
                component_doi = node_text(object_id_tag)

    return component_doi

def components(soup):
    """
    Find the components, i.e. those parts that would be assigned
    a unique component DOI, such as figures, tables, etc.
    - position is in what order the tag appears in the entire set of nodes
    - ordinal is in what order it is for all the tags of its own type
    """
    components = []
    
    nodenames = ["abstract", "fig", "table-wrap", "media",
                 "chem-struct-wrap", "sub-article", "supplementary-material",
                 "boxed-text", "app"]
    
    # Count node order overall
    position = 1
    
    position_by_type = {}
    for nodename in nodenames:
        position_by_type[nodename] = 1
     
    article_doi = doi(soup)
    
    # Find all tags for all component_types, allows the order
    #  in which they are found to be preserved
    component_tags = extract_nodes(soup, nodenames)
    
    for tag in component_tags:
        
        component = {}
        
        # Component type is the tag's name
        ctype = tag.name
        
        # First find the doi if present
        component_doi = extract_component_doi(tag, nodenames)
        if component_doi is None:
            continue
        else:
            component['doi'] = component_doi
            component['doi_url'] = 'http://dx.doi.org/' + component_doi
            
        
        if(ctype == "sub-article"):
            title_tag = raw_parser.article_title(tag)
        else:
            title_tag = raw_parser.title(tag)

        if title_tag:
            component['title'] = node_text(title_tag)
            component['full_title'] = node_contents_str(title_tag)

        if raw_parser.label(tag):
            component['label'] = node_text(raw_parser.label(tag))
            component['full_label'] = node_contents_str(raw_parser.label(tag))

        if raw_parser.caption(tag):
            first_paragraph = first(paragraphs(raw_parser.caption(tag)))
            if first_paragraph and not starts_with_doi(first_paragraph):
                component['caption'] = node_text(first_paragraph)
                component['full_caption'] = node_contents_str(first_paragraph)

        if raw_parser.permissions(tag):
            
            component['permissions'] = []
            for permissions_tag in raw_parser.permissions(tag):
                permissions_item = {}
                if raw_parser.copyright_statement(permissions_tag):
                    permissions_item['copyright_statement'] = \
                        node_text(raw_parser.copyright_statement(permissions_tag))
                    
                if raw_parser.copyright_year(permissions_tag):
                    permissions_item['copyright_year'] = \
                        node_text(raw_parser.copyright_year(permissions_tag))
                    
                if raw_parser.copyright_holder(permissions_tag):
                    permissions_item['copyright_holder'] = \
                        node_text(raw_parser.copyright_holder(permissions_tag))

                if raw_parser.licence_p(permissions_tag):
                    permissions_item['license'] = \
                        node_text(raw_parser.licence_p(permissions_tag))
                    permissions_item['full_license'] = \
                        node_contents_str(raw_parser.licence_p(permissions_tag))

                component['permissions'].append(permissions_item)

        if raw_parser.contributors(tag):
            component['contributors'] = []
            for contributor_tag in raw_parser.contributors(tag):
                component['contributors'].append(format_contributor(contributor_tag, soup))

        # There are only some parent tags we care about for components
        #  and only check two levels of parentage
        parent_nodenames = ["sub-article", "fig-group", "fig", "boxed-text", "table-wrap", "app", "media"]
        parent_tag = first_parent(tag, parent_nodenames)
        
        if parent_tag:

            # For fig-group we actually want the first fig of the fig-group as the parent
            acting_parent_tag = component_acting_parent_tag(parent_tag, tag)
            
            # Only counts if the acting parent tag has a DOI
            if (acting_parent_tag and \
               extract_component_doi(acting_parent_tag, parent_nodenames) is not None):
                
                component['parent_type'] = acting_parent_tag.name
                component['parent_ordinal'] = tag_ordinal(acting_parent_tag)
                component['parent_sibling_ordinal'] = tag_details_sibling_ordinal(acting_parent_tag)
                component['parent_asset'] = tag_details_asset(acting_parent_tag)

            # Look for parent parent, if available
            parent_parent_tag = first_parent(parent_tag, parent_nodenames)
            
            if parent_parent_tag:
                
                acting_parent_tag = component_acting_parent_tag(parent_parent_tag, parent_tag)
                
                if (acting_parent_tag and \
                   extract_component_doi(acting_parent_tag, parent_nodenames) is not None):
                    component['parent_parent_type'] = acting_parent_tag.name
                    component['parent_parent_ordinal'] = tag_ordinal(acting_parent_tag)
                    component['parent_parent_sibling_ordinal'] = tag_details_sibling_ordinal(acting_parent_tag)
                    component['parent_parent_asset'] = tag_details_asset(acting_parent_tag)

        content = ""
        for p_tag in extract_nodes(tag, "p"):
            if content != "":
                # Add a space before each new paragraph for now
                content = content + " "
            content = content + node_text(p_tag)
            
        if(content != ""):
            component['content'] = content
    
        # mime type
        media_tag = None
        if(ctype == "media"):
            media_tag = tag
        elif(ctype == "supplementary-material"):
            media_tag = first(raw_parser.media(tag))
        if media_tag:
            component['mimetype'] = media_tag.get("mimetype")
            component['mime-subtype'] = media_tag.get("mime-subtype")
    
        if(len(component) > 0):
            component['article_doi'] = article_doi
            component['type'] = ctype
            component['position'] = position
            
            # Ordinal is based on all tags of the same type even if they have no DOI
            component['ordinal'] = tag_ordinal(tag)
            component['sibling_ordinal'] = tag_details_sibling_ordinal(tag)
            component['asset'] = tag_details_asset(tag)
            #component['ordinal'] = position_by_type[ctype]
                        
            components.append(component)
            
            position += 1
            position_by_type[ctype] += 1

    
    return components



def correspondence(soup):
    """
    Find the corresp tags included in author-notes
    for primary correspondence
    """
    correspondence = []
    
    author_notes_nodes = raw_parser.author_notes(soup)
    
    if author_notes_nodes:
        corresp_nodes = raw_parser.corresp(author_notes_nodes)
        for tag in corresp_nodes:
            correspondence.append(tag.text)

    return correspondence


def full_correspondence(soup):
    cor = {}

    author_notes_nodes = raw_parser.author_notes(soup)
    if author_notes_nodes:
        corresp_nodes = raw_parser.corresp(author_notes_nodes)
        for tag in corresp_nodes:
            if raw_parser.email(tag):
                cor[tag['id']] = node_contents_str(first(raw_parser.email(tag)))
            elif raw_parser.phone(tag):
                # Look for a phone number
                cor[tag['id']] = node_contents_str(first(raw_parser.phone(tag)))

    return cor


@nullify
def author_notes(soup):
    """
    Find the fn tags included in author-notes
    """
    author_notes = []

    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = raw_parser.fn(author_notes_section)
        for tag in fn_nodes:
            if 'fn-type' in tag.attrs:
                if(tag['fn-type'] != 'present-address'):
                    author_notes.append(node_text(tag))

    return author_notes

@nullify
def full_author_notes(soup, fntype_filter=None):
    """
    Find the fn tags included in author-notes
    """
    notes = []
    
    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = raw_parser.fn(author_notes_section)
        notes = footnotes(fn_nodes, fntype_filter)

    return notes

@nullify
def competing_interests(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    competing_interests_section = extract_nodes(soup, "fn-group", attr="content-type", value="competing-interest")
    if not competing_interests_section:
        return None
    fn = extract_nodes(first(competing_interests_section), "fn")
    interests = footnotes(fn, fntype_filter)

    return interests

@nullify
def author_contributions(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    author_contributions_section = extract_nodes(soup, "fn-group", attr="content-type", value="author-contribution")
    if not author_contributions_section:
        return None
    fn = extract_nodes(first(author_contributions_section), "fn")
    cons = footnotes(fn, fntype_filter)

    return cons

def footnotes(fn, fntype_filter):
    notes = []
    for f in fn:
        try:
            if fntype_filter is None or f['fn-type'] in fntype_filter:
                notes.append({
                    'id': f['id'],
                    'text': node_contents_str(f),
                    'fn-type': f['fn-type'],
                })
        except KeyError:
            # TODO log
            pass
    return notes


@nullify
def full_award_groups(soup):
    """
    Find the award-group items and return a list of details
    """
    award_groups = []

    funding_group_section = extract_nodes(soup, "funding-group")
    for fg in funding_group_section:

        award_group_tags = extract_nodes(fg, "award-group")

        for ag in award_group_tags:

            ref = ag['id']

            award_group = {}
            award_group_id = award_group_award_id(ag)
            if award_group_id is not None:
                award_group['award-id'] = first(award_group_id)
            funding_sources = full_award_group_funding_source(ag)
            source = first(funding_sources)
            if source is not None:
                copy_attribute(source, 'institution', award_group)
                copy_attribute(source, 'institution-id', award_group, 'id')
                copy_attribute(source, 'institution-id-type', award_group, destination_key='id-type')
            award_group_by_ref = {}
            award_group_by_ref[ref] = award_group
            award_groups.append(award_group_by_ref)

    return award_groups


@nullify
def award_groups(soup):
    """
    Find the award-group items and return a list of details
    """
    award_groups = []
    
    funding_group_section = extract_nodes(soup, "funding-group")
    for fg in funding_group_section:
        
        award_group_tags = extract_nodes(fg, "award-group")
        
        for ag in award_group_tags:
        
            award_group = {}

            award_group['funding_source'] = award_group_funding_source(ag)
            award_group['recipient'] = award_group_principal_award_recipient(ag)
            award_group['award_id'] = award_group_award_id(ag)

            award_groups.append(award_group)
    
    return award_groups


@nullify
def award_group_funding_source(tag):
    """
    Given a funding group element
    Find the award group funding sources, one for each
    item found in the get_funding_group section
    """
    award_group_funding_source = []
    funding_source_tags = extract_nodes(tag, "funding-source")
    for t in funding_source_tags:
        award_group_funding_source.append(t.text)
    return award_group_funding_source

@nullify
def full_award_group_funding_source(tag):
    """
    Given a funding group element
    Find the award group funding sources, one for each
    item found in the get_funding_group section
    """
    award_group_funding_sources = []
    funding_source_nodes = extract_nodes(tag, "funding-source")
    for funding_source_node in funding_source_nodes:

        award_group_funding_source = {}

        institution_nodes = extract_nodes(funding_source_node, 'institution')

        institution_node = first(institution_nodes)
        if institution_node:
            award_group_funding_source['institution'] = node_text(institution_node)
            if 'content-type' in institution_node.attrs:
                award_group_funding_source['institution-type'] = institution_node['content-type']

        institution_id_nodes = extract_nodes(funding_source_node, 'institution-id')
        institution_id_node = first(institution_id_nodes)
        if institution_id_node:
            award_group_funding_source['institution-id'] = node_text(institution_id_node)
            if 'institution-id-type' in institution_id_node.attrs:
                award_group_funding_source['institution-id-type'] = institution_id_node['institution-id-type']

        award_group_funding_sources.append(award_group_funding_source)

    return award_group_funding_sources


@nullify
def award_group_award_id(tag):
    """
    Find the award group award id, one for each
    item found in the get_funding_group section
    """
    award_group_award_id = []
    award_id_tags = extract_nodes(tag, "award-id")
    for t in award_id_tags:
        award_group_award_id.append(t.text)
    return award_group_award_id

@nullify
def award_group_principal_award_recipient(tag):
    """
    Find the award group principal award recipient, one for each
    item found in the get_funding_group section
    """
    award_group_principal_award_recipient = []
    principal_award_recipients = extract_nodes(tag, "principal-award-recipient")
    
    for t in principal_award_recipients:
        principal_award_recipient_text = ""
        
        try:
            institution = node_text(first(extract_nodes(t, "institution")))
            surname = node_text(first(extract_nodes(t, "surname")))
            given_names = node_text(first(extract_nodes(t, "given-names")))
            # Concatenate name and institution values if found
            #  while filtering out excess whitespace
            if(given_names):
                principal_award_recipient_text += given_names
            if(principal_award_recipient_text != ""):
                principal_award_recipient_text += " "
            if(surname):
                principal_award_recipient_text += surname
            if(institution):
                principal_award_recipient_text += institution
        except IndexError:
            continue
        award_group_principal_award_recipient.append(principal_award_recipient_text)
    return award_group_principal_award_recipient

def object_id_doi(tag, parent_tag_name=None):
    """DOI in an object-id tag found inside the tag"""
    doi = None
    object_id = None
    object_ids = raw_parser.object_id(tag, "doi")
    if object_ids:
        object_id = first(object_ids)
    if parent_tag_name and object_id and object_id.parent.name != parent_tag_name:
        object_id = None
    if object_id:
        doi = node_contents_str(object_id)
    return doi

def title_text(tag, parent_tag_name=None):
    """Extract the text of a title tag"""
    title = None
    title_tag = raw_parser.title(tag)
    if parent_tag_name and title_tag and title_tag.parent.name != parent_tag_name:
        title_tag = None
    if title_tag:
        title = node_contents_str(title_tag)
    return title

def caption_title(tag):
    """Extract the text of a title or p tag inside the first caption tag"""
    title = None
    caption = raw_parser.caption(tag)
    if caption:
        title_tag = raw_parser.title(caption)
        if title_tag:
            title = node_contents_str(title_tag)
        if not title:
            p_tags = raw_parser.paragraph(caption)
            if p_tags:
                title = node_contents_str(first(p_tags))
    return title

def label(tag, parent_tag_name=None):
    label = None
    label_tag = raw_parser.label(tag)
    if parent_tag_name and label_tag and label_tag.parent.name != parent_tag_name:
        label_tag = None
    if label_tag:
        label = node_contents_str(label_tag)
    return label

def body(soup):

    body_content = []

    raw_body = raw_parser.article_body(soup)

    if raw_body:
        body_content = render_raw_body(raw_body)

    return body_content


def render_raw_body(tag):
    body_content = []
    body_tags = body_blocks(tag)
    for tag in body_tags:
        if tag.name == "boxed-text" and not raw_parser.title(tag) and not raw_parser.label(tag):
            # Collapse boxed-text here if it has no title or label
            for boxed_tag in tag:
                tag_blocks = body_block_content_render(boxed_tag)
                for tag_block in tag_blocks:
                    if tag_block != {}:
                        body_content.append(tag_block)
        else:

            tag_blocks = body_block_content_render(tag)
            #tag_content = body_block_content_render(tag)
            for tag_block in tag_blocks:
                if tag_block != {}:
                    body_content.append(tag_block)

    return body_content

def body_block_nodenames():
    return ["sec", "p", "table-wrap", "boxed-text",
            "disp-formula", "fig", "fig-group", "list", "media"]

def body_block_content_render(tag):
    """
    Render the tag as body content and call recursively if
    the tag has child tags
    """
    block_content_list = []
    tag_content = OrderedDict()

    if tag.name == "p":
        for block_content in body_block_paragraph_render(tag):
            if block_content != {}:
                block_content_list.append(block_content)
    else:
        tag_content = body_block_content(tag)

    nodenames = body_block_nodenames()

    tag_content_content = []

    # Collect the content of the tag but only for some tags
    if tag.name not in ["p", "fig", "table-wrap"]:
        for child_tag in tag:
            if not(hasattr(child_tag, 'name')):
                continue

            if child_tag.name == "p":
                if (child_tag.parent.name == "caption"
                    and child_tag.parent.parent.name == "boxed-text"):
                    continue
                for block_content in body_block_paragraph_render(child_tag):
                    if block_content != {}:
                        tag_content_content.append(block_content)

            elif child_tag.name == "fig" and tag.name == "fig-group":
                # Do not fig inside fig-group a second time
                pass
            else:
                for block_content in body_block_content_render(child_tag):
                    if block_content != {}:
                        tag_content_content.append(block_content)

    if len(tag_content_content) > 0:
        tag_content["content"] = []
        for block_content in tag_content_content:
            tag_content["content"].append(block_content)

    block_content_list.append(tag_content)
    return block_content_list

def body_block_paragraph_render(p_tag):
    """
    paragraphs may wrap some other body block content
    this is separated out so it can be called from more than one place
    """
    block_content_list = []

    tag_content_content = []
    nodenames = body_block_nodenames()

    paragraph_content = u''
    for child_tag in p_tag:

        if child_tag.name is None or body_block_content(child_tag) == {}:
            paragraph_content = paragraph_content + unicode(child_tag)

        else:
            # Add previous paragraph content first
            if paragraph_content.strip() != '':
                tag_content_content.append(body_block_paragraph_content(paragraph_content))
                paragraph_content = u''

        if child_tag.name is not None and body_block_content(child_tag) != {}:
            for block_content in body_block_content_render(child_tag):
                if block_content != {}:
                    tag_content_content.append(block_content)
    # finish up
    if paragraph_content.strip() != '':
        tag_content_content.append(body_block_paragraph_content(paragraph_content))

    if len(tag_content_content) > 0:
        for block_content in tag_content_content:
            block_content_list.append(block_content)

    return block_content_list

def body_block_caption_render(caption_tags):
    """fig and media tag captions are similar so use this common function"""
    caption_content = []
    supplementary_material_tags = []

    for block_tag in caption_tags:
        # Note then skip p tags with supplementary-material inside
        if raw_parser.supplementary_material(block_tag):
            for supp_tag in raw_parser.supplementary_material(block_tag):
                supplementary_material_tags.append(supp_tag)
            continue

        for block_content in body_block_content_render(block_tag):

            if block_content != {}:
                caption_content.append(block_content)

    return caption_content, supplementary_material_tags

def body_block_supplementary_material_render(supp_tags):
    """fig and media tag caption may have supplementary material"""
    source_data = []
    for supp_tag in supp_tags:
        for block_content in body_block_content_render(supp_tag):
            if block_content != {}:
                if "content" in block_content:
                    del block_content["content"]
                source_data.append(block_content)
    return source_data

def body_block_paragraph_content(text):
    "for formatting of simple paragraphs of text only, and check if it is all whitespace"
    tag_content = OrderedDict()
    if text and text != '':
        tag_content["type"] = "paragraph"
        tag_content["text"] = unicode(text)
    return tag_content

def body_block_content(tag):

    tag_content = OrderedDict()

    if not(hasattr(tag, 'name')):
        return OrderedDict()

    if tag.name == "sec":
        tag_content["type"] = "section"
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "title", title_text(tag, tag.name))

    elif tag.name == "boxed-text":
        tag_content["type"] = "box"
        set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))
        set_if_value(tag_content, "title", title_text(tag))

    elif tag.name == "p":
        tag_content["type"] = "paragraph"

        # Remove unwanted nested tags
        unwanted_tag_names = body_block_nodenames()
        tag_copy = duplicate_tag(tag)
        tag_copy = remove_tag_from_tag(tag_copy, unwanted_tag_names)

        if node_contents_str(tag_copy):
            tag_content["text"] = node_contents_str(tag_copy)

    elif tag.name == "table-wrap":
        tag_content["type"] = "table"
        set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))
        set_if_value(tag_content, "title", caption_title(tag))

        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags)
            if len(caption_content) > 0:
                tag_content["caption"] = caption_content

        tables = raw_parser.table(tag)
        tag_content["tables"] = []
        for table in tables:
            # Add the table tag back for now
            table_content = '<table>' + node_contents_str(table) + '</table>'
            tag_content["tables"].append(table_content)

        table_wrap_foot = raw_parser.table_wrap_foot(tag)
        for foot_tag in table_wrap_foot:
            # TODO ? We are ignoring label tags
            for fn_tag in raw_parser.fn(foot_tag):
                for p_tag in raw_parser.paragraph(fn_tag):
                    if "footer" not in tag_content:
                        tag_content["footer"] = []
                    tag_content["footer"].append(body_block_content(p_tag))

    elif tag.name == "disp-formula":
        tag_content["type"] = "mathml"

        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))

        math_tag = first(raw_parser.math(tag))
        tag_content["mathml"] = node_contents_str(math_tag)

    elif tag.name == "fig":
        tag_content["type"] = "image"
        set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))
        set_if_value(tag_content, "title", caption_title(tag))
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags)
            if len(caption_content) > 0:
                tag_content["caption"] = caption_content

        # todo!! alt
        set_if_value(tag_content, "alt", "")
        # todo!! set base URL for images
        graphic_tags = raw_parser.graphic(tag)
        if graphic_tags:
            copy_attribute(first(graphic_tags).attrs, 'xlink:href', tag_content, 'uri')
        # todo!! support for custom permissions of use or license
        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(supplementary_material_tags)
            if len(source_data) > 0:
                tag_content["sourceData"] = source_data

    elif tag.name == "media":
        # For video media only
        if tag.get("mimetype") != "video":
            return OrderedDict()

        tag_content["type"] = "video"
        set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))
        set_if_value(tag_content, "title", caption_title(tag))
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags)
            if len(caption_content) > 0:
                tag_content["caption"] = caption_content

        set_if_value(tag_content, "uri", tag.get('xlink:href'))

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(supplementary_material_tags)
            if len(source_data) > 0:
                tag_content["sourceData"] = source_data

    elif tag.name == "fig-group":
        for i, fig_tag in enumerate(raw_parser.fig(tag)):
            if i == 0:
                tag_content = body_block_content(fig_tag)
            elif i > 0:
                if "supplements" not in tag_content:
                    tag_content["supplements"] = []
                tag_content["supplements"].append(body_block_content(fig_tag))

    elif tag.name == "supplementary-material":
        set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))
        set_if_value(tag_content, "title", caption_title(tag))
        if raw_parser.media(tag):
            media_tag = first(raw_parser.media(tag))
            if media_tag.get("mimetype") and media_tag.get("mime-subtype"):
                # Quick concatenation for now
                tag_content["mediaType"] = media_tag.get("mimetype") + "/" + media_tag.get("mime-subtype")
            copy_attribute(media_tag.attrs, 'xlink:href', tag_content, 'uri')

    elif tag.name == "list":
        tag_content["type"] = "list"
        if tag.get("list-type"):
            if tag.get("list-type") == "simple":
                tag_content["prefix"] = "bullet"
            elif tag.get("list-type") == "order":
                tag_content["prefix"] = "number"
            else:
                tag_content["prefix"] = tag.get("list-type")
        else:
            tag_content["prefix"] = "none"

        for list_item_tag in raw_parser.list_item(tag):
            if "items" not in tag_content:
                tag_content["items"] = []

            if len(body_block_content_render(list_item_tag)) > 0:
                for list_item in body_block_content_render(list_item_tag):
                    # Note: wrapped inside another list to pass the current article json schema
                    if list_item != {}:
                        list_item_content = list_item["content"]
                        tag_content["items"].append(list_item_content)
                    else:
                        tag_content["items"].append(node_contents_str(list_item_tag))

    return tag_content

def body_blocks(soup):
    """
    Note: for some reason this works and few other attempted methods work
    Search for certain node types, find the first nodes siblings of the same type
    Add the first sibling and the other siblings to a list and return them
    """
    nodenames = body_block_nodenames()

    body_block_tags = []

    first_sibling_node = firstnn(soup.find_all())

    if first_sibling_node is None:
        return body_block_tags

    sibling_tags = first_sibling_node.find_next_siblings(nodenames)

    # Add the first component tag and the ResultSet tags together
    body_block_tags.append(first_sibling_node)

    for tag in sibling_tags:
        body_block_tags.append(tag)

    return body_block_tags

def sub_article_doi(tag):
    doi = None
    article_id_tag = first(raw_parser.article_id(tag, "doi"))
    if article_id_tag:
        doi = article_id_tag.text
    return doi

def decision_letter(soup):

    sub_article_content = OrderedDict()
    sub_article = raw_parser.decision_letter(soup)

    if sub_article:
        if sub_article_doi(sub_article):
            sub_article_content["doi"] = sub_article_doi(sub_article)
        raw_body = raw_parser.article_body(sub_article)
    else:
        raw_body = None

    # description
    if raw_body:
        # Description will be the first boxed-text tag
        if raw_parser.boxed_text(raw_body):
            sub_article_content["description"] = []
            boxed_text_description = first(raw_parser.boxed_text(raw_body))
            tags = body_blocks(boxed_text_description)
            for tag in tags:
                block_content = body_block_content_render(tag)
                for tag_content in block_content:
                    if tag_content != {}:
                        sub_article_content["description"].append(tag_content)

            # Remove the tag before content is compiled
            boxed_text_description.decompose()

    # content
    if raw_body:
        body_content = render_raw_body(raw_body)
        if len(body_content) > 0:
            sub_article_content["content"] = body_content

    return sub_article_content


def author_response(soup):

    sub_article_content = OrderedDict()
    sub_article = raw_parser.author_response(soup)

    if sub_article:
        if sub_article_doi(sub_article):
            sub_article_content["doi"] = sub_article_doi(sub_article)
        raw_body = raw_parser.article_body(sub_article)
    else:
        raw_body = None

    # content
    if raw_body:
        body_content = render_raw_body(raw_body)
        if len(body_content) > 0:
            sub_article_content["content"] = body_content

    return sub_article_content


def render_abstract_json(abstract_tag):
    abstract_json = OrderedDict()
    set_if_value(abstract_json, "doi", object_id_doi(abstract_tag))
    for child_tag in body_blocks(abstract_tag):
        if body_block_content(child_tag) != {}:
            if "content" not in abstract_json:
                 abstract_json["content"] = []
            abstract_json["content"].append(body_block_content(child_tag))
    return abstract_json


def abstract_json(soup):
    """abstract in article json format"""
    abstract_tags = raw_parser.abstract(soup)
    abstract_json = None
    for tag in abstract_tags:
        if tag.get("abstract-type") is None:
            abstract_json = render_abstract_json(tag)
    return abstract_json


def digest_json(soup):
    """digest in article json format"""
    abstract_tags = raw_parser.abstract(soup, abstract_type="executive-summary")
    abstract_json = None
    for tag in abstract_tags:
        abstract_json = render_abstract_json(tag)
    return abstract_json


def author_preferred_name(surname, given_names, suffix):
    preferred_name = None
    preferred_name = " ".join(filter(lambda element: element is not None,
                                     [given_names, surname, suffix]))
    return preferred_name


def author_index_name(surname, given_names, suffix):
    index_name = None
    index_name = ", ".join(filter(lambda element: element is not None,
                                  [surname, given_names, suffix]))
    return index_name


def author_affiliations(author):
    """compile author affiliations for json output"""
    affilations = []

    if author.get("affiliations"):
        for affiliation in author.get("affiliations"):
            affiliation_json = OrderedDict()
            affiliation_json["name"] = []
            if affiliation.get("dept"):
                affiliation_json["name"].append(affiliation.get("dept"))
            if affiliation.get("institution"):
                affiliation_json["name"].append(affiliation.get("institution"))
            # Remove if empty
            if affiliation_json["name"] == []:
                del affiliation_json["name"]

            if affiliation.get("city") or affiliation.get("country"):
                affiliation_address = OrderedDict()
                affiliation_address["formatted"] = []
                affiliation_address["components"] = OrderedDict()
                if affiliation.get("city"):
                    affiliation_address["formatted"].append(affiliation.get("city"))
                    affiliation_address["components"]["locality"] = []
                    affiliation_address["components"]["locality"].append(affiliation.get("city"))
                if affiliation.get("country"):
                    affiliation_address["formatted"].append(affiliation.get("country"))
                    affiliation_address["components"]["country"] = affiliation.get("country")
                # Add if not empty
                if affiliation_address != {}:
                    affiliation_json["address"] = affiliation_address

            # Add if not empty
            if affiliation_json != {}:
                affilations.append(affiliation_json)

    if affilations != []:
        return affilations
    else:
        return None

def author_phone_numbers(author, correspondence):
    phone_numbers = []
    if "phone" in author.get("references"):
        for ref_id in author["references"]["phone"]:
            if correspondence and ref_id in correspondence:
                phone_numbers.append(correspondence[ref_id])
    if phone_numbers != []:
        return phone_numbers
    else:
        return None


def author_email_addresses(author, correspondence):
    email_addresses = []

    if "email" in author.get("references"):
        for ref_id in author["references"]["email"]:
            if correspondence and ref_id in correspondence:
                email_addresses.append(correspondence[ref_id])

    # Also look in affiliations for inline email tags
    if author.get("affiliations"):
        for affiliation in author.get("affiliations"):
            if "email" in affiliation and affiliation["email"] not in email_addresses:
                email_addresses.append(affiliation["email"])

    if email_addresses != []:
        return email_addresses
    else:
        return None

def author_contribution(author, contributions):
    contribution_text = None

    if "contribution" in author.get("references"):
        for ref_id in author["references"]["contribution"]:
            if contributions:
                for contribution in contributions:
                    if contribution.get("text") and contribution.get("id") == ref_id:
                        contribution_text = (
                            contribution.get("text").replace('<p>', '').replace('</p>', ''))

    return contribution_text

def author_competing_interests(author, competing_interests):
    competing_interests_text = None

    if "competing-interest" in author.get("references"):
        for ref_id in author["references"]["competing-interest"]:
            if competing_interests:
                for competing_interest in competing_interests:
                    if competing_interest.get("text") and competing_interest.get("id") == ref_id:
                        competing_interests_text = (
                            competing_interest.get("text").replace('<p>', '').replace('</p>', ''))

    return competing_interests_text

def author_equal_contribution(author, equal_contributions_map):
    equal_contributions = []

    if "contribution" in author.get("references"):
        if "equal-contrib" in author["references"]:
            for ref_id in author["references"]["equal-contrib"]:
                if ref_id in equal_contributions_map:
                    equal_contributions.append(equal_contributions_map[ref_id])
    if equal_contributions != []:
        return equal_contributions
    else:
        return None



def author_json_details(author, author_json, contributions, correspondence, competing_interests, equal_contributions_map):
    """add more author json"""
    if author_affiliations(author):
        author_json["affiliations"] = author_affiliations(author)

    if author.get("references"):
        # email
        if author_email_addresses(author, correspondence):
            author_json["emailAddresses"] = author_email_addresses(author, correspondence)

        # phone
        if author_phone_numbers(author, correspondence):
            author_json["phoneNumbers"] = author_phone_numbers(author, correspondence)

        # contributions
        if author_contribution(author, contributions):
            author_json["contribution"] = author_contribution(author, contributions)

        # competing interests
        if author_competing_interests(author, competing_interests):
            author_json["competingInterests"] = author_competing_interests(author, competing_interests)

        # equal-contributions
        if author_equal_contribution(author, equal_contributions_map):
            author_json["equalContributionGroups"] = author_equal_contribution(author, equal_contributions_map)

    return author_json

def author_person(author, contributions, correspondence, competing_interests, equal_contributions_map):
    author_json = OrderedDict()
    author_json["type"] = "person"
    author_name = OrderedDict()
    author_name["preferred"] = author_preferred_name(
        author.get("surname"), author.get("given-names"), author.get("suffix"))
    author_name["index"] = author_index_name(
        author.get("surname"), author.get("given-names"), author.get("suffix"))
    author_json["name"] = author_name
    if author.get("orcid"):
        author_json["orcid"] = author.get("orcid").replace("http://orcid.org/", "")
    author_json = author_json_details(author, author_json, contributions, correspondence,
                                      competing_interests, equal_contributions_map)

    return author_json


def author_group(author, contributions, correspondence, competing_interests, equal_contributions_map):
    author_json = OrderedDict()
    author_json["type"] = "group"
    author_json["name"] = author.get("collab")

    author_json = author_json_details(author, author_json, contributions, correspondence,
                                      competing_interests, equal_contributions_map)

    return author_json


def author_on_behalf_of(author):
    author_json = OrderedDict()
    author_json["type"] = "on-behalf-of"
    author_json["onBehalfOf"] = author.get("on-behalf-of")
    return author_json


def collab_to_group_author_key_map(authors):
    """compile a map of author collab to group-author-key"""
    collab_map = {}
    for author in authors:
        if author.get("collab"):
            collab_map[author.get("collab")] = author.get("group-author-key")
    return collab_map

def map_equal_contributions(contributors):
    """assign numeric values to each unique equal-contrib id"""
    equal_contribution_map = {}
    equal_contribution_keys = []
    for contributor in contributors:
        if contributor.get("references") and "equal-contrib" in contributor.get("references"):
            for key in contributor["references"]["equal-contrib"]:
                if key not in equal_contribution_keys:
                    equal_contribution_keys.append(key)
    # Do a basic sort
    equal_contribution_keys = sorted(equal_contribution_keys)
    # Assign keys based on sorted values
    for i, equal_contribution_key in enumerate(equal_contribution_keys):
        equal_contribution_map[equal_contribution_key] = i+1
    return equal_contribution_map

def authors_json(soup):
    """authors list in article json format"""
    authors_json_data = []
    contributors_data = contributors(soup, "full")
    author_contributions_data = author_contributions(soup, None)
    author_competing_interests_data = competing_interests(soup, None)
    author_correspondence_data = full_correspondence(soup)
    authors_non_byline_data = authors_non_byline(soup)
    equal_contributions_map = map_equal_contributions(contributors_data)

    # First line authors builds basic structure
    for contributor in contributors_data:
        author_json = None
        if contributor["type"] == "author" and contributor.get("collab"):
            author_json = author_group(contributor, author_contributions_data, author_correspondence_data,
                                       author_competing_interests_data, equal_contributions_map)
            author_json["people"] = []
        elif contributor.get("on-behalf-of"):
            author_json = author_on_behalf_of(contributor)
        elif contributor["type"] == "author":
            author_json = author_person(contributor, author_contributions_data, author_correspondence_data,
                                        author_competing_interests_data, equal_contributions_map)

        if author_json:
            authors_json_data.append(author_json)

    # Second, add byline author data
    collab_map = collab_to_group_author_key_map(contributors_data)
    for contributor in filter(lambda json_element: json_element["type"] == "author non-byline", contributors_data):
        for group_author in filter(
            lambda json_element: json_element["type"] == "group", authors_json_data):
            group_author_key = None
            if group_author["name"] in collab_map:
                group_author_key = collab_map[group_author["name"]]
            if contributor.get("group-author-key") == group_author_key:
                author_json = author_person(contributor, author_contributions_data, author_correspondence_data,
                                            author_competing_interests_data, equal_contributions_map)
                group_author["people"].append(author_json)


    return authors_json_data

def author_line(soup):
    """take preferred names from authors json and format them into an author line"""
    author_line = None
    authors_json_data = authors_json(soup)
    author_names = extract_author_line_names(authors_json_data)
    if len(author_names) > 0:
        author_line = format_author_line(author_names)
    return author_line

def extract_author_line_names(authors_json_data):
    author_names = []
    if not authors_json_data:
        return author_names
    for author in authors_json_data:
        if "name" in author and type(author["name"]) == str:
            # collab
            author_names.append(author["name"])
        elif "name" in author and "preferred" in author["name"]:
            # person
            author_names.append(author["name"]["preferred"])
    return author_names

def format_author_line(author_names):
    """authorLine format depends on if there is 1, 2 or more than 2 authors"""
    author_line = None
    if not author_names:
        return author_line
    if len(author_names) <= 2:
        author_line = ", ".join(author_names)
    elif len(author_names) > 2:
        author_line = author_names[0] + " et al"
    return author_line

def references_json(soup):
    references_json = []
    for ref in refs(soup):
        ref_content = OrderedDict()
        set_if_value(ref_content, "type", ref.get("publication-type"))
        set_if_value(ref_content, "id", ref.get("id"))
        set_if_value(ref_content, "date", ref.get("year"))

        # authors and etal - TODO!!

        # titles
        if ref.get("publication-type") in ["journal"]:
            set_if_value(ref_content, "articleTitle", ref.get("full_article_title"))
        elif ref.get("publication-type") in ["book"]:
            set_if_value(ref_content, "bookTitle", ref.get("source"))
        elif ref.get("publication-type") in ["web"]:
            set_if_value(ref_content, "title", ref.get("full_article_title"))
            if "title" not in ref_content:
                set_if_value(ref_content, "title", ref.get("comment"))

        # source
        if ref.get("publication-type") in ["journal"]:
            if ref.get("source"):
                journal = OrderedDict()
                journal["name"] = []
                journal["name"].append(ref.get("source"))
                ref_content["journal"] = journal
        elif ref.get("publication-type") in ["web"]:
            set_if_value(ref_content, "website", ref.get("source"))
        else:
            set_if_value(ref_content, "source", ref.get("source"))

        # volume
        set_if_value(ref_content, "volume", ref.get("volume"))

        # edition - TODO!!

        # todo - publisher - TODO!!

        # pages
        if ref.get("elocation-id"):
            ref_content["pages"] = ref.get("elocation-id")
        elif ref.get("fpage"):
            ref_content["pages"] = OrderedDict()
            ref_content["pages"]["first"] = ref.get("fpage").strip()

            if ref.get("lpage"):
                ref_content["pages"]["last"] = ref.get("lpage").strip()
                # use unichr(8211) for the hyphen because the schema is requiring it
                ref_content["pages"]["range"] = ref.get("fpage").strip() + unichr(8211) + ref.get("lpage").strip()
            else:
                ref_content["pages"]["last"] = ref.get("fpage").strip()
                ref_content["pages"]["range"] = ref.get("fpage").strip()

        elif ref.get("comment"):
            if ref.get("comment").lower().strip() == "in press":
                ref_content["pages"] = "in-press"

        # doi
        set_if_value(ref_content, "doi", ref.get("doi"))

        # uri
        set_if_value(ref_content, "uri", ref.get("uri"))


        # publisher
        if ref.get("publisher_name"):
            publisher = OrderedDict()
            publisher["name"] = []
            publisher["name"].append(ref.get("publisher_name"))
            if ref.get("publisher_loc"):
                address = OrderedDict()
                address["formatted"] = []
                address["formatted"].append(ref.get("publisher_loc"))
                address["components"] = OrderedDict()
                address["components"]["locality"] = []
                address["components"]["locality"].append(ref.get("publisher_loc"))
                publisher["address"] = address
            ref_content["publisher"] = publisher

        references_json.append(ref_content)

    return references_json
