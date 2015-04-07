from bs4 import BeautifulSoup
from utils import first, firstnn, extract_nodes

"""
rawParser.py extracts and returns the nodes from the article xml using BeautifulSoup so that functionality at higher levels may use and combine them as neccessary.

"""

def title(soup):
    return first(extract_nodes(soup, "article-title"))

def doi(soup):
    doi_tags = extract_nodes(soup, "article-id", attr = "pub-id-type", value = "doi")
    # the first article-id tag whose parent is article-meta
    return first(filter(lambda tag: tag.parent.name == "article-meta", doi_tags))

def journal_id(soup):
    # the first non-nil tag
    return firstnn(extract_nodes(soup, "journal-id", attr = "journal-id-type", value = "hwp"))

def journal_title(soup):
    return first(extract_nodes(soup, "journal-title"))

def journal_issn(soup, pub_format):
    return first(extract_nodes(soup, "issn", attr = "publication-format", value = pub_format))

def publisher(soup):
    return first(extract_nodes(soup, "publisher-name"))

def article_type(soup):
    # returns raw data, just that the data doesn't contain any BS nodes
    return first(extract_nodes(soup, "article")).get('article-type')

def keyword_group(soup):
    return extract_nodes(soup, "kwd-group")

def research_organism_keywords(soup):
    tags = first(extract_nodes(soup, "kwd-group", attr = "kwd-group-type", value = "research-organism"))
    return filter(lambda tag: tag.name == "kwd", tags)

def author_keywords(soup):
    # A few articles have kwd-group with no kwd-group-type, so account for those
    tags = extract_nodes(soup, "kwd-group")
    keyword_tags = []
    for tag in tags:
        if (tag.get("kwd-group-type") == "author-keywords" 
            or tag.get("kwd-group-type") is None):
            keyword_tags += filter(lambda tag: tag.name == "kwd", tag)
    return keyword_tags

def subject_area(soup, subject_group_type = None):
    # Supports all subject areas or just particular ones filtered by 
    subject_area_tags = []
    tags = extract_nodes(soup, "subject")
    
    subject_area_tags = filter(lambda tag: tag.parent.name == "subj-group"
                                            and tag.parent.parent.name == "article-categories"
                                            and tag.parent.parent.parent.name == "article-meta"
                                            , tags)
    if subject_group_type is not None:
        subject_area_tags = filter(lambda tag:
                                    tag.parent.get("subj-group-type") == subject_group_type, tags)
    return subject_area_tags

def display_channel(soup):
    return (subject_area(soup, subject_group_type = "display-channel"))
