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
    return node_text(raw_parser.copyright_statement(soup))

@inten
def copyright_year(soup):
    return node_text(raw_parser.copyright_year(soup))

def copyright_holder(soup):
    return node_text(raw_parser.copyright_holder(soup))

def license(soup):
    return node_text(raw_parser.licence_p(soup))

def license_url(soup):
    return raw_parser.licence_url(soup)

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

    for tag in object_id_tags:
        component_object = {}
        component_object["doi"] = tag.text
        component_doi.append(component_object)        
    
    return component_doi
    

#
# HERE BE DRAGONS
#

def authors_non_byline(soup):
    """Non-byline authors for group author members"""
    authors_list = authors(soup, contrib_type = "author non-byline")
    return authors_list


def authors(soup, contrib_type = "author"):
    """Find and return all the authors"""
    tags = extract_nodes(soup, "contrib", attr = "contrib-type", value = contrib_type)
    authors = []
    position = 1
    
    article_doi = doi(soup)
    
    for tag in tags:
        author = {}
        
        # Person id
        try:
            person_id = tag["id"]
            if person_id.startswith("author"):
                person_id = person_id.replace("author-", "")
                author['person_id'] = int(person_id)
        except(KeyError):
            pass

        # Equal contrib
        try:
            equal_contrib = tag["equal-contrib"]
            if(equal_contrib == 'yes'):
                author['equal_contrib'] = True
        except(KeyError):
            pass
        
        # Correspondence
        try:
            corresponding = tag["corresp"]
            if(corresponding == 'yes'):
                author['corresponding'] = True
        except(KeyError):
            pass
        
        # Surname
        surname = node_text(first(extract_nodes(tag, "surname")))
        if(surname != None):
            author['surname'] = surname

        # Given names
        given_names = node_text(first(extract_nodes(tag, "given-names")))
        if(given_names != None):
            author['given_names'] = given_names
        
        # Collab for group authors
        collab = node_text(first(extract_nodes(tag, "collab")))
        if(collab != None):
            author['collab'] = collab
        
        # Group author key
        author['group_author_key'] = node_text(first(raw_parser.contrib_id(tag, "group-author-key")))
 
        # ORCID
        author['orcid'] = node_text(first(raw_parser.contrib_id(tag, "orcid")))
        
        # Find and parse affiliations
        affs = extract_nodes(tag, "xref", attr = "ref-type", value = "aff")
        if len(affs) <= 0:
            # No aff found? Look for an aff tag inside the contrib tag
            affs = extract_nodes(tag, "aff")
            
        if(len(affs) > 0):
            # One or more affiliations
            if(len(affs) > 1):
                # Prepare for multiple affiliations if multiples found
                author['country'] = []
                author['institution'] = []
                author['department'] = []
                author['city'] = []
                
            for aff in affs:
                # Find the matching affiliation detail
                rid = aff.get('rid')
                if rid:
                    # Look for the matching aff tag by rid
                    aff_node = first(extract_nodes(soup, "aff", attr = "id", value = rid)) 
                else:
                    # Aff tag inside contrib tag
                    aff_node = aff
                    
                country = node_text(first(extract_nodes(aff_node, "country")))
                
                # Institution is the tag with no attribute
                institutions = extract_nodes(aff_node, "institution")
                institution = None
                for inst in institutions:
                    try:
                        if(inst["content-type"] != None):
                            # A tag attribute found, skip it
                            pass
                    except KeyError:
                        institution = node_text(inst)
                       
                # Department tag does have an attribute
                department = node_text(first(extract_nodes(aff_node, "institution", attr = "content-type", value = "dept")))
                city = node_text(first(extract_nodes(aff_node, "named-content", attr = "content-type", value = "city")))
                
                # Convert None to empty string if there is more than one affiliation
                if((country == None) and (len(affs) > 1)):
                    country = ''
                if((institution == None) and (len(affs) > 1)):
                    institution = ''
                if((department == None) and (len(affs) > 1)):
                    department = ''
                if((city == None) and (len(affs) > 1)):
                    city = ''
                    
                # Append values
                try:
                    # Multiple values
                    author['country'].append(country)
                except(KeyError):
                    author['country'] = country
                try:
                    # Multiple values
                    author['institution'].append(institution)
                except(KeyError):
                    author['institution'] = institution
                try:
                    # Multiple values
                    author['department'].append(department)
                except(KeyError):
                    author['department'] = department
                try:
                    # Multiple values
                    author['city'].append(city)
                except(KeyError):
                    author['city'] = city

        # Author - given names + surname
        author_name = ""
        if(given_names != None):
            author_name += given_names + " "
        if(surname != None):
            author_name += surname
        author['author'] = author_name
        
        # Add xref linked correspondence author notes if applicable
        cors = extract_nodes(tag, "xref", attr = "ref-type", value = "corresp")
        if(len(cors) > 0):
            # One or more 
            if(len(cors) > 1):
                # Prepare for multiple values if multiples found
                author['notes_correspondence'] = []
                
            for cor in cors:
                # Find the matching affiliation detail
                rid = cor['rid']

                # Find elements by id
                try:
                    corresp_node = soup.select("#" + rid)
                    author_notes = corresp_node[0].get_text()
                    author_notes = strip_strings(author_notes)
                except:
                    continue
                try:
                    # Multiple values
                    author['notes_correspondence'].append(author_notes)
                except(KeyError):
                    author['notes_correspondence'] = author_notes
                    
        # Add xref linked footnotes if applicable
        fns = extract_nodes(tag, "xref", attr = "ref-type", value = "fn")
        if(len(fns) > 0):
            # One or more 
            if(len(fns) > 1):
                # Prepare for multiple values if multiples found
                author['notes_footnotes'] = []
                
            for fn in fns:
                # Find the matching affiliation detail
                rid = fn['rid']

                # Find elements by id
                try:
                    fn_node = soup.select("#" + rid)
                    fn_text = fn_node[0].get_text()
                    fn_text = strip_strings(fn_text)
                except:
                    continue
                try:
                    # Multiple values
                    author['notes_footnotes'].append(fn_text)
                except(KeyError):
                    author['notes_footnotes'] = fn_text
                    
        # Add xref linked other notes if applicable, such as funding detail
        others = extract_nodes(tag, "xref", attr = "ref-type", value = "other")
        if(len(others) > 0):
            # One or more 
            if(len(others) > 1):
                # Prepare for multiple values if multiples found
                author['notes_other'] = []
                
            for other in others:
                # Find the matching affiliation detail
                rid = other['rid']

                # Find elements by id
                try:
                    other_node = soup.select("#" + rid)
                    other_text = other_node[0].get_text()
                    other_text = strip_strings(other_text)
                except:
                    continue
                try:
                    # Multiple values
                    author['notes_other'].append(other_text)
                except(KeyError):
                    author['notes_other'] = other_text    

        # If not empty, add position value, append, then increment the position counter
        if(len(author) > 0):
            author['article_doi'] = article_doi
            
            author['position'] = position
                        
            authors.append(author)
            position += 1
        
    return authors

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

def components(soup):
    """
    Find the components, i.e. those parts that would be assigned
    a unique component DOI, such as figures, tables, etc.
    """
    components = []
    
    component_types = ["abstract", "fig", "table-wrap", "media",
                       "chem-struct-wrap", "sub-article", "supplementary-material",
                       "boxed-text"]
    
    position = 1
    
    article_doi = doi(soup)
    
    # Find all tags for all component_types, allows the order
    #  in which they are found to be preserved
    tags = soup.find_all(component_types) 
    
    for tag in tags:
        
        component = {}
        
        # Component type is the tag's name
        ctype = tag.name
        
        # First find the doi if present
        if(ctype == "sub-article"):
            object_id = node_text(first(extract_nodes(tag, "article-id", attr = "pub-id-type", value = "doi")))
        else:
            object_id = node_text(first(extract_nodes(tag, "object-id", attr = "pub-id-type", value = "doi")))
        if(object_id is not None):
            component['doi'] = object_id
            component['doi_url'] = 'http://dx.doi.org/' + object_id
        else:
            # If no object-id is found, then skip this component
            continue

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
                        
            components.append(component)
            position += 1
    
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
