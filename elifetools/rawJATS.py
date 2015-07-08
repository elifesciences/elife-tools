from bs4 import BeautifulSoup
from utils import first, firstnn, extract_nodes, node_contents_str

"""
rawParser.py extracts and returns the nodes from the article xml using BeautifulSoup so that functionality at higher levels may use and combine them as neccessary.

"""

def article_title(soup):
    return first(extract_nodes(soup, "article-title"))

def title(soup):
    return first(extract_nodes(soup, "title"))

def abstract(soup):
    return extract_nodes(soup, "abstract")

def article_id(soup, pub_id_type):
    return extract_nodes(soup, "article-id", attr = "pub-id-type", value = pub_id_type)
    
def doi(soup):
    doi_tags = article_id(soup, pub_id_type = "doi")
    # the first article-id tag whose parent is article-meta
    return first(filter(lambda tag: tag.parent.name == "article-meta", doi_tags))

def publisher_id(soup):
    article_id_tags = article_id(soup, pub_id_type = "publisher-id")
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
    return extract_nodes(soup, "permissions")

def article_permissions(soup):
    # a better selector might be "article-meta.permissions"
    permissions_tags = permissions(soup)
    return first(filter(lambda tag: tag.parent.name == "article-meta", permissions_tags))

def licence(soup):
    return first(extract_nodes(soup, "license"))

def licence_p(soup):
    return first(extract_nodes(licence(soup), "license-p"))

def licence_url(soup):
    "License url attribute of the license tag"
    return licence(soup).get("xlink:href")

def copyright_statement(soup):
    return first(extract_nodes(soup, "copyright-statement"))

def copyright_year(soup):
    return first(extract_nodes(soup, "copyright-year"))

def copyright_holder(soup):
    return first(extract_nodes(soup, "copyright-holder"))

def funding_statement(soup):
    return first(extract_nodes(soup, "funding-statement"))

def affiliation(soup):
    return extract_nodes(soup, "aff")

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

def custom_meta(soup, meta_name=None):
    custom_meta_tags = extract_nodes(soup, "custom-meta")
    if meta_name is not None:
        custom_meta_tags = filter(lambda tag: node_contents_str(first(extract_nodes(tag, "meta-name"))) == meta_name, custom_meta_tags)
    return custom_meta_tags

def display_channel(soup):
    return (subject_area(soup, subject_group_type = "display-channel"))

def category(soup):
    return (subject_area(soup, subject_group_type = "heading"))

def related_article(soup):
    related_article_tags = extract_nodes(soup, "related-article")
    return filter(lambda tag: tag.parent.name == "article-meta", related_article_tags)

def related_object(soup):
    return extract_nodes(soup, "related-object")

def object_id(soup, pub_id_type):
    return extract_nodes(soup, "object-id", attr = "pub-id-type", value = pub_id_type)

def label(soup):
    return first(extract_nodes(soup, "label"))

def contributors(soup):
    return extract_nodes(soup, "contrib")

def article_contributors(soup):
    contributor_tags = contributors(soup)
    return filter(lambda tag: tag.parent.name == "contrib-group"
                        and tag.parent.parent.name == "article-meta", contributor_tags)

def authors(soup, contrib_type = "author"):
    return extract_nodes(soup, "contrib", attr = "contrib-type", value = contrib_type)

def caption(soup):
    return first(extract_nodes(soup, "caption"))

def author_notes(soup):
    return first(extract_nodes(soup, "author-notes"))

def corresp(soup):
    return extract_nodes(soup, "corresp")

def fn(soup):
    return extract_nodes(soup, "fn")

def media(soup):
    return extract_nodes(soup, "media")

def inline_graphic(soup):
    return extract_nodes(soup, "inline-graphic")

def graphic(soup):
    return extract_nodes(soup, "graphic")

#
# authors
#

def contrib_id(soup):
    return extract_nodes(soup, "contrib-id")

#
# references
#

def ref_list(soup):
    return extract_nodes(soup, "ref")

def volume(soup):
    return extract_nodes(soup, "volume")

def fpage(soup):
    return extract_nodes(soup, "fpage")
            
def lpage(soup):
    return extract_nodes(soup, "lpage")

def collab(soup):
    return extract_nodes(soup, "collab")

def publisher_loc(soup):
    return extract_nodes(soup, "publisher-loc")

def publisher_name(soup):
    return extract_nodes(soup, "publisher-name")

def comment(soup):
    return extract_nodes(soup, "comment")