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
