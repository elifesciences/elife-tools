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

def article_meta_aff(soup):
    return node_text(raw_parser.article_meta_add(soup))
    
def research_organism(soup):
    "Find the research-organism from the set of kwd-group tags"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return map(node_text, raw_parser.research_organism_keywords(soup))

def keywords(soup):
    """
    Find the keywords from the set of kwd-group tags
    which are typically labelled as the author keywords
    """
    if not raw_parser.author_keywords(soup):
        return []
    return map(node_text, raw_parser.author_keywords(soup))

def full_keyword_groups(soup):
    groups = {}
    for group_tag in raw_parser.keyword_group(soup):
        group = map(node_contents_str, extract_nodes(group_tag, "kwd"))
        group = map(lambda s: s.strip(), group)
        groups[group_tag['kwd-group-type'].strip()] = group
    return groups

def full_custom_meta(soup, meta_name=None):
    return raw_parser.custom_meta(soup, meta_name)

def impact_statement(soup):
    tag = first(full_custom_meta(soup, "Author impact statement"))
    return node_contents_str(first(extract_nodes(tag, "meta-value")))


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


def ref_text(ref):
    # ref - human readable full reference text
    ref_text = tag.get_text()
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
    
    year = raw_parser.year(pub_date)
    
    if year:
        return int(node_text(year))
    else:
        return None

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
        
        if len(paragraphs(tag)) > 0:
            abstract["content"] = ""
            abstract["full_content"] = ""
            
            good_paragraphs = remove_doi_paragraph(paragraphs(tag))
            
            glue = ""
            for p_tag in good_paragraphs:
                abstract["content"] += glue + node_text(p_tag)
                abstract["full_content"] += glue + node_contents_str(p_tag)
                glue = " "
        else:
            abstract["content"] = None
    
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


def add_to_list_dictionary(list_dict, list_key, val):
    if val is not None:
        if list_key not in list_dict:
            list_dict[list_key] = []
        list_dict[list_key].append(val)


def format_contributor(contrib_tag, soup, detail="brief"):
    contributor = {}
    copy_attribute(contrib_tag.attrs, 'contrib-type', contributor, 'type')
    copy_attribute(contrib_tag.attrs, 'equal-contrib', contributor)
    copy_attribute(contrib_tag.attrs, 'corresp', contributor)
    copy_attribute(contrib_tag.attrs, 'deceased', contributor)
    copy_attribute(contrib_tag.attrs, 'id', contributor)
    contrib_id_tag = first(extract_nodes(contrib_tag, "contrib-id"))
    if contrib_id_tag and 'contrib-id-type' in contrib_id_tag.attrs:
        if contrib_id_tag['contrib-id-type'] == 'group-author-key':
            contributor['group-author-key'] = node_contents_str(contrib_id_tag)
        elif contrib_id_tag['contrib-id-type'] == 'orcid':
            contributor['orcid'] = node_contents_str(contrib_id_tag)
    set_if_value(contributor, "collab", first_node_str_contents(contrib_tag, "collab"))
    set_if_value(contributor, "role", first_node_str_contents(contrib_tag, "role"))
    name_tag = first(extract_nodes(contrib_tag, "name"))
    if name_tag is not None:
        set_if_value(contributor, "surname", first_node_str_contents(name_tag, "surname"))
        set_if_value(contributor, "given-names", first_node_str_contents(name_tag, "given-names"))
        set_if_value(contributor, "suffix", first_node_str_contents(name_tag, "suffix"))

    contrib_refs = {}
    ref_tags = extract_nodes(contrib_tag, "xref")
    for ref_tag in ref_tags:
        if "ref-type" in ref_tag.attrs and "rid" in ref_tag.attrs:
            ref_type = ref_tag['ref-type']
            rid = ref_tag['rid']

            if ref_type == "aff":
                add_to_list_dictionary(contrib_refs, 'affiliation', rid)
            if ref_type == "corresp":
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
            elif ref_type == "other":
                if rid.startswith('par-'):
                    add_to_list_dictionary(contrib_refs, 'funding', rid)
                elif rid.startswith('dataro'):
                    add_to_list_dictionary(contrib_refs, 'related-object', rid)

    if len(contrib_refs) > 0:
        contributor['references'] = contrib_refs

    if detail == "brief":
        # Brief format only allows one aff and it must be within the contrib tag
        aff_tag = first(extract_nodes(contrib_tag, "aff"))
        if aff_tag:
            contributor['affiliation'] = []
            contrib_affs = {}
            (none_return, aff_detail) = format_aff(aff_tag)
            if len(aff_detail) > 0:
                aff_attributes = ['dept', 'institution', 'country', 'city']
                for aff_attribute in aff_attributes:
                    if aff_attribute in aff_detail and aff_detail[aff_attribute] is not None:
                        copy_attribute(aff_detail, aff_attribute, contrib_affs)
                if len(contrib_affs) > 0:
                    contributor['affiliation'].append(contrib_affs)

    elif detail == "full":
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
            contributor['affiliation'] = []
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
                aff_attributes = ['dept', 'institution', 'country', 'city']
                for aff_attribute in aff_attributes:
                    if aff_attribute in aff_detail and aff_detail[aff_attribute] is not None:
                        copy_attribute(aff_detail, aff_attribute, contrib_affs)
                contributor['affiliation'].append(contrib_affs)
    
        # Add xref linked correspondence author notes if applicable
        corresp_tags = extract_nodes(contrib_tag, "xref", attr = "ref-type", value = "corresp")
        if(len(corresp_tags) > 0):
            if 'notes-corresp' not in contributor:
                contributor['notes-corresp'] = []
    
            for cor in corresp_tags:
                # Find the matching tag
                rid = cor['rid']
                corresp_node = first(soup.select("#" + rid))
                author_notes = node_text(corresp_node)
                if author_notes:
                    contributor['notes-corresp'].append(author_notes)
        
        # Add xref linked footnotes if applicable
        fn_tags = extract_nodes(contrib_tag, "xref", attr = "ref-type", value = "fn")
        if(len(fn_tags) > 0):
            if 'notes-fn' not in contributor:
                contributor['notes-fn'] = []
            for fn in fn_tags:
               # Find the matching tag
               rid = fn['rid']
               fn_node = first(soup.select("#" + rid))
               fn_text = node_text(fn_node)
               if fn_text:
                   contributor['notes-fn'].append(fn_text)
    
    return contributor

def contributors(soup):
    contrib_tags = raw_parser.article_contributors(soup)
    contributors = []
    for tag in contrib_tags:
        contributors.append(format_contributor(tag, soup))
    return contributors

#
# HERE BE DRAGONS
#

def authors_non_byline(soup):
    """Non-byline authors for group author members"""
    authors_list = authors(soup, contrib_type = "author non-byline")
    return authors_list

def authors(soup, contrib_type = "author"):

    tags = raw_parser.authors(soup, contrib_type)
    authors = []
    position = 1
    
    article_doi = doi(soup)
    
    for tag in tags:
        author = format_contributor(tag, soup, detail="full")

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
        'country': node_contents_str(first(extract_nodes(aff_tag, "country")))
        }
    if 'id' in aff_tag.attrs:
        return aff_tag['id'], values
    else:
        return None, values


def full_affiliation(soup):
    aff_tags = raw_parser.affiliation(soup)
    aff_tags = filter(lambda aff: 'id' in aff.attrs, aff_tags)
    return {key: value for (key, value) in map(format_aff, aff_tags)}


def references(soup):
    """Renamed to refs"""
    return refs(soup)
    
def refs(soup):
    """Find and return all the references"""
    tags = extract_nodes(soup, "ref")
    refs = []
    position = 1
    
    article_doi = doi(soup)
    
    for tag in tags:
        ref = {}
        
        # etal
        etal = extract_nodes(tag, "etal")
        try:
            if(etal[0]):
                ref['etal'] = True
        except(IndexError):
            pass
        
        # ref - human readable full reference text
        ref_text = tag.get_text()
        ref_text = strip_strings(ref_text)
        # Remove excess space
        ref_text = ' '.join(ref_text.split())
        # Fix punctuation spaces and extra space
        ref['ref'] = strip_punctuation_space(strip_strings(ref_text))
        
        # article_title
        article_title = node_text(first(extract_nodes(tag, "article-title")))
        if(article_title != None):
            ref['article_title'] = article_title
            
        # year
        year = node_text(first(extract_nodes(tag, "year")))
        if(year != None):
            ref['year'] = year
            
        # source
        source = node_text(first(extract_nodes(tag, "source")))
        if(source != None):
            ref['source'] = source
            
        # publication_type
        mixed_citation = extract_nodes(tag, "mixed-citation")
        try:
            publication_type = mixed_citation[0]["publication-type"]
            ref['publication_type'] = publication_type
        except(KeyError, IndexError):
            pass

        # authors
        person_group = extract_nodes(tag, "person-group")
        authors = []
        try:
            name = extract_nodes(person_group[0], "name")
            for n in name:
                surname = node_text(first(extract_nodes(n, "surname")))
                given_names = node_text(first(extract_nodes(n, "given-names")))
                # Convert all to strings in case a name component is missing
                if(surname is None):
                    surname = ""
                if(given_names is None):
                    given_names = ""
                full_name = strip_strings(surname + ' ' + given_names)
                authors.append(full_name)
            if(len(authors) > 0):
                ref['authors'] = authors
        except(KeyError, IndexError):
            pass
            
        # volume
        volume = node_text(first(extract_nodes(tag, "volume")))
        if(volume != None):
            ref['volume'] = volume
            
        # fpage
        fpage = node_text(first(extract_nodes(tag, "fpage")))
        if(fpage != None):
            ref['fpage'] = fpage
            
        # lpage
        lpage = node_text(first(extract_nodes(tag, "lpage")))
        if(lpage != None):
            ref['lpage'] = lpage
            
        # collab
        collab = node_text(first(extract_nodes(tag, "collab")))
        if(collab != None):
            ref['collab'] = collab
            
        # publisher_loc
        publisher_loc = node_text(first(extract_nodes(tag, "publisher-loc")))
        if(publisher_loc != None):
            ref['publisher_loc'] = publisher_loc
        
        # publisher_name
        publisher_name = node_text(first(extract_nodes(tag, "publisher-name")))
        if(publisher_name != None):
            ref['publisher_name'] = publisher_name
            
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
                 "boxed-text"]
    
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
            if not starts_with_doi(first_paragraph):
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

                if raw_parser.licence_url(permissions_tag):
                    permissions_item['license_url'] = \
                        node_text(raw_parser.licence_url(permissions_tag))

                component['permissions'].append(permissions_item)

        if raw_parser.contributors(tag):
            component['contributors'] = []
            for contributor_tag in raw_parser.contributors(tag):
                component['contributors'].append(format_contributor(contributor_tag, soup))

        # There are only some parent tags we care about for components
        #  and only check two levels of parentage
        parent_nodenames = ["sub-article", "fig-group", "fig", "boxed-text", "table-wrap"]
        parent_tag = first_parent(tag, parent_nodenames)
        
        if parent_tag:

            # For fig-group we actually want the first fig of the fig-group as the parent
            acting_parent_tag = component_acting_parent_tag(parent_tag, tag)
            
            # Only counts if the acting parent tag has a DOI
            if (acting_parent_tag and \
               extract_component_doi(acting_parent_tag, parent_nodenames) is not None):
                
                component['parent_type'] = acting_parent_tag.name
                component['parent_ordinal'] = tag_ordinal(acting_parent_tag)

            # Look for parent parent, if available
            parent_parent_tag = first_parent(parent_tag, parent_nodenames)
            
            if parent_parent_tag:
                
                acting_parent_tag = component_acting_parent_tag(parent_parent_tag, parent_tag)
                
                if (acting_parent_tag and \
                   extract_component_doi(acting_parent_tag, parent_nodenames) is not None):
                    component['parent_parent_type'] = acting_parent_tag.name
                    component['parent_parent_ordinal'] = tag_ordinal(acting_parent_tag)

        content = ""
        for p_tag in extract_nodes(tag, "p"):
            if content != "":
                # Add a space before each new paragraph for now
                content = content + " "
            content = content + node_text(p_tag)
            
        if(content != ""):
            component['content'] = content
    
        if(len(component) > 0):
            component['article_doi'] = article_doi
            component['type'] = ctype
            component['position'] = position
            component['ordinal'] = position_by_type[ctype]
                        
            components.append(component)
            
            position += 1
            position_by_type[ctype] += 1

    
    return components

@nullify
@strippen
def correspondence(soup):
    """
    Find the corresp tags included in author-notes
    for primary correspondence
    """
    correspondence = []
    try:
        author_notes = extract_nodes(soup, "author-notes")
        tags = extract_nodes(author_notes[0], "corresp")
        for tag in tags:
            correspondence.append(tag.text)
    except(IndexError):
        # Tag not found
        return None
    return correspondence


def get_email(text):
    if text:
        match = re.search('<email>(.*?)</email>', text, re.DOTALL)
        if match is not None:
            return match.group(1)

    return ""


@nullify
def full_correspondence(soup):
    cor = {}
    try:
        author_notes_nodes = extract_nodes(soup,"author-notes")
        tags = extract_nodes(author_notes_nodes[0], "corresp")
        for tag in tags:
            cor[tag['id']] = get_email(node_contents_str(tag))
    except IndexError:
        return None
    return cor


@nullify
@strippen
def author_notes(soup):
    """
    Find the fn tags included in author-notes
    """
    author_notes = []
    try:
        author_notes_section = extract_nodes(soup, "author-notes")
        fn = extract_nodes(author_notes_section[0], "fn")
        for f in fn:
            try:
                if(f['fn-type'] != 'present-address'):
                    author_notes.append(f.text)
                else:
                    # Throw it away if it is a present-address footnote
                    continue
            except(KeyError):
                # Append if the fn-type attribute does not exist
                author_notes.append(f.text)
    except(IndexError):
        # Tag not found
        return None
    return author_notes

@nullify
def full_author_notes(soup, fntype_filter=None):
    """
    Find the fn tags included in author-notes
    """
    author_notes = []
    try:
        author_notes_section = extract_nodes(soup, "author-notes")
        fn = extract_nodes(author_notes_section[0], "fn")
        for f in fn:
            try:
                if fntype_filter is None or f['fn-type'] in fntype_filter:
                    author_notes.append({
                        'id': f['id'],
                        'text': node_contents_str(f),
                        'fn-type': f['fn-type'],
                    })
                else:
                    # Throw it away if it is a present-address footnote
                    continue
            except(KeyError):
                # Append if the fn-type attribute does not exist
                # author_notes.append(f.text) TODO : is this required here?
                pass
    except(IndexError):
        # Tag not found
        return None
    return author_notes

@nullify
def full_author_notes(soup, fntype_filter=None):
    """
    Find the fn tags included in author-notes
    """

    try:
        author_notes_section = extract_nodes(soup, "author-notes")
        fn = extract_nodes(author_notes_section[0], "fn")
        notes = footnotes(fn, fntype_filter)
    except IndexError:
        # TODO log - Tag not found
        return None
    return notes

@nullify
def competing_interests(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    try:
        competing_interests_section = extract_nodes(soup, "fn-group", attr="content-type", value="competing-interest")
        fn = extract_nodes(competing_interests_section[0], "fn")
        interests = footnotes(fn, fntype_filter)
    except IndexError:
        return None
    return interests

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
    award_groups = {}

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
            award_groups[ref] = award_group

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
            if(institution and len(institution) > 1):
                if(principal_award_recipient_text != ""):
                    principal_award_recipient_text += ", "
                principal_award_recipient_text += institution
        except IndexError:
            continue
        award_group_principal_award_recipient.append(principal_award_recipient_text)
    return award_group_principal_award_recipient
