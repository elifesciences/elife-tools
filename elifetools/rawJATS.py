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

def acknowledgements(soup):
    return first(extract_nodes(soup, "ack"))

def conflict(soup):
    return extract_nodes(soup, "fn", attr = "fn-type", value = "conflict")

def permissions(soup):
    # a better selector might be "article-meta.permissions"
    return first(extract_nodes(soup, "permissions"))

def licence(soup):
    return first(extract_nodes(permissions(soup), "license"))

def licence_p(soup):
    return first(extract_nodes(licence(soup), "license-p"))

def licence_url(soup):
    "License url attribute of the license tag"
    return licence(soup).get("xlink:href")

def copyright_statement(soup):
    return first(extract_nodes(permissions(soup), "copyright-statement"))

def copyright_year(soup):
    return first(extract_nodes(permissions(soup), "copyright-year"))

def copyright_holder(soup):
    return first(extract_nodes(permissions(soup), "copyright-holder"))

def funding_statement(soup):
    return first(extract_nodes(soup, "funding-statement"))

#
# authors
#


#
# references
#

def ref_list(soup):
    return extract_nodes(soup, "ref")

def volume(ref):
    return extract_nodes(ref, "volume")

def fpage(ref):
    return extract_node(ref, "fpage")
            
def lpage(ref):
    return extract_node(ref, "lpage")

def collab(ref):
    return extract_node(ref, "collab")

def publisher_loc(ref):
    return extract_node(ref, "publisher-loc")

def publisher_name(ref):
    return extract_node(ref, "publisher-name")
