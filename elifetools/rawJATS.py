from bs4 import BeautifulSoup
from utils import first, firstnn, extract_nodes

"""
rawParser.py extracts and returns the nodes from the article xml using BeautifulSoup so that functionality at higher levels may use and combine them as neccessary.

"""

def article_title(soup):
    return first(extract_nodes(soup, "article-title"))

def title(soup):
    return first(extract_nodes(soup, "title"))

def abstract(soup):
    return extract_nodes(soup, "abstract")

def doi(soup):
    doi_tags = extract_nodes(soup, "article-id", attr = "pub-id-type", value = "doi")
    # the first article-id tag whose parent is article-meta
    return first(filter(lambda tag: tag.parent.name == "article-meta", doi_tags))

def publisher_id(soup):
    article_id_tags = extract_nodes(soup, "article-id", attr = "pub-id-type", value = "publisher-id")
    # the first article-id tag whose parent is article-meta
    return first(filter(lambda tag: tag.parent.name == "article-meta", article_id_tags))

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

def pub_date(soup, date_type):
    return first(extract_nodes(soup, "pub-date", attr = "date-type", value = date_type))

def pub_date_collection(soup, pub_type):
    return first(extract_nodes(soup, "pub-date", attr = "pub-type", value = pub_type))

def history_date(soup, date_type):
    date_tags = extract_nodes(soup, "date", attr = "date-type", value = date_type)
    return first(filter(lambda tag: tag.parent.name == "history", date_tags))

def day(soup):
    return first(extract_nodes(soup, "day"))

def month(soup):
    return first(extract_nodes(soup, "month"))

def year(soup):
    return first(extract_nodes(soup, "year"))

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

def research_organism_keywords(soup):
    tags = first(extract_nodes(soup, "kwd-group", attr = "kwd-group-type", value = "research-organism"))
    if not tags:
        return None
    return filter(lambda tag: tag.name == "kwd", tags) or None   

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
    
    subject_area_tags = filter(lambda tag: tag.parent.name == "subj-group" \
                                           and tag.parent.parent.name == "article-categories"
                                           and tag.parent.parent.parent.name == "article-meta", tags)
    if subject_group_type:
        subject_area_tags = filter(lambda tag:
                                    tag.parent.get("subj-group-type") == subject_group_type, tags)
    return subject_area_tags

def full_subject_area(soup, subject_group_type=None):

    subject_group_tags = extract_nodes(soup, "subj-group")
    subject_group_tags = filter(lambda tag: tag.parent.name == "article-categories"
                                              and tag.parent.parent.name == "article-meta", subject_group_tags)

    if subject_group_type:
        subject_group_tags = filter(lambda tag:
                                    tag.get("subj-group-type" == subject_group_type))

    return subject_group_tags


def display_channel(soup):
    return (subject_area(soup, subject_group_type = "display-channel"))

def category(soup):
    return (subject_area(soup, subject_group_type = "heading"))

def related_article(soup):
    related_article_tags = extract_nodes(soup, "related-article")
    return filter(lambda tag: tag.parent.name == "article-meta", related_article_tags)

def institution_wrap(soup):
    institution_wrap_tags = extract_nodes(soup, "institution-wrap")
    return institution_wrap_tags

def institution_id(soup):
    institution_id_tags = extract_nodes(soup, "institution-id")
    return institution_id_tags

def institution_id_type(soup):
    institution_id_tags = extract_nodes(soup, "institution-id-type")
    return institution_id_tags

def institution_id(soup):
    institution_id_tags = extract_nodes(soup, "institution")
    return institution_id_tags

def award_id(soup):
    award_id_tags = extract_nodes(soup, "award_id")
    return award_id_tags


#
# authors
#

def contrib_id(soup, contrib_id_type):
    return extract_nodes(soup, "contrib-id", attr = "contrib-id-type", value = contrib_id_type)

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
