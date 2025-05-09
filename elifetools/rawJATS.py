from elifetools.utils import (
    first,
    firstnn,
    lazy_extract_nodes,
    extract_first_node,
    extract_nodes,
    node_contents_str,
)

"""
rawParser.py extracts and returns the nodes from the article xml using BeautifulSoup so that functionality at higher levels may use and combine them as neccessary.

"""


def article_meta(soup):
    return extract_first_node(soup, "article-meta")


def article_title(soup):
    return extract_first_node(soup, "article-title")


def title(soup):
    return extract_first_node(soup, "title")


def lazy_abstract(soup, abstract_type=None):
    if abstract_type:
        return lazy_extract_nodes(
            soup, "abstract", attr="abstract-type", value=abstract_type
        )
    else:
        return lazy_extract_nodes(soup, "abstract")


def abstract(soup, abstract_type=None):
    return list(lazy_abstract(soup, abstract_type))


def lazy_article_id(soup, pub_id_type=None):
    if pub_id_type:
        return lazy_extract_nodes(soup, "article-id", attr="pub-id-type", value=pub_id_type)
    else:
        return lazy_extract_nodes(soup, "article-id")


def article_id(soup, pub_id_type=None):
    return list(lazy_article_id(soup, pub_id_type))


def meta_article_id(soup, pub_id_type, specific_use=None):
    for tag in lazy_article_id(soup, pub_id_type):
        # filter by specific-use attribute
        if tag.get("specific-use") == specific_use:
            # the first article-id tag whose parent is article-meta
            if tag.parent.name == "article-meta":
                return tag
    return None


def doi(soup):
    return meta_article_id(soup, pub_id_type="doi")


def version_doi(soup):
    return meta_article_id(soup, pub_id_type="doi", specific_use="version")


def publisher_id(soup):
    return meta_article_id(soup, pub_id_type="publisher-id")


def journal_id(soup):
    # the first non-nil tag
    return firstnn(
        lazy_extract_nodes(soup, "journal-id", attr="journal-id-type", value="publisher-id")
    )


def journal_title(soup):
    return extract_first_node(soup, "journal-title")


def journal_issn(soup, pub_format, pub_type):
    if pub_format is None and pub_type is None:
        # return the first issn tag found regardless of which type
        return extract_first_node(soup, "issn")
    elif pub_format is not None:
        return extract_first_node(
            soup, "issn", attr="publication-format", value=pub_format
        )

    elif pub_type is not None:
        return extract_first_node(soup, "issn", attr="pub-type", value=pub_type)


def publisher(soup):
    return extract_first_node(soup, "publisher-name")


def article_type(soup):
    # returns raw data, just that the data doesn't contain any BS nodes
    return extract_first_node(soup, "article").get("article-type")


def article_version(soup):
    return lazy_extract_nodes(soup, "article-version")


def lazy_pub_date(soup, date_type=None, pub_type=None):
    if date_type is not None:
        return lazy_extract_nodes(soup, "pub-date", attr="date-type", value=date_type)
    elif pub_type is not None:
        return lazy_extract_nodes(soup, "pub-date", attr="pub-type", value=pub_type)
    else:
        return lazy_extract_nodes(soup, "pub-date")


def pub_date(soup, date_type=None, pub_type=None):
    return list(lazy_pub_date(soup, date_type, pub_type))


def lazy_date(soup, date_type=None):
    if date_type is not None:
        return lazy_extract_nodes(soup, "date", attr="date-type", value=date_type)
    else:
        return lazy_extract_nodes(soup, "date")


def date(soup, date_type=None):
    return list(lazy_date(soup, date_type))


def history_date(soup, date_type):
    for date_tag in lazy_date(soup, date_type):
        if date_tag.parent.name == "history":
            return date_tag


def day(soup):
    return extract_first_node(soup, "day")


def month(soup):
    return extract_first_node(soup, "month")


def year(soup):
    return extract_first_node(soup, "year")


def lazy_keyword_group(soup):
    return lazy_extract_nodes(soup, "kwd-group")


def keyword_group(soup):
    return list(lazy_keyword_group(soup))


def acknowledgements(soup):
    return extract_first_node(soup, "ack")


def lazy_conflict(soup):
    for tag in lazy_extract_nodes(soup, "fn", attr="fn-type", value="conflict"):
        yield tag
    for tag in lazy_extract_nodes(soup, "fn", attr="fn-type", value="COI-statement"):
        yield tag


def conflict(soup):
    return list(lazy_conflict(soup))


def lazy_permissions(soup):
    # a better selector might be "article-meta.permissions"
    return lazy_extract_nodes(soup, "permissions")


def permissions(soup):
    return list(lazy_permissions(soup))


def article_permissions(soup):
    # a better selector might be "article-meta.permissions"
    for tag in lazy_permissions(soup):
        if tag.parent.name == "article-meta":
            return tag


def lazy_licence(soup):
    return lazy_extract_nodes(soup, "license")


def licence(soup):
    return list(lazy_licence(soup))


def lazy_licence_p(soup):
    return lazy_extract_nodes(soup, "license-p")


def licence_p(soup):
    return list(lazy_licence_p(soup))


def licence_url(soup):
    "License url attribute of the license tag"
    first_licence = first(lazy_licence(soup))
    if first_licence:
        return first_licence.get("xlink:href")


def attrib(soup):
    return extract_nodes(soup, "attrib")


def copyright_statement(soup):
    return extract_first_node(soup, "copyright-statement")


def copyright_year(soup):
    return extract_first_node(soup, "copyright-year")


def copyright_holder(soup):
    return extract_first_node(soup, "copyright-holder")


def funding_statement(soup):
    return extract_first_node(soup, "funding-statement")


def affiliation(soup):
    return extract_nodes(soup, "aff")


def research_organism_keywords(soup):
    tags = extract_first_node(
        soup, "kwd-group", attr="kwd-group-type", value="research-organism"
    )

    if not tags:
        return None
    return [tag for tag in tags if tag.name == "kwd"] or None


def author_keywords(soup):
    # A few articles have kwd-group with no kwd-group-type, so account for those
    tags = extract_nodes(soup, "kwd-group")
    keyword_tags = []
    for tag in tags:
        if (
            tag.get("kwd-group-type") == "author-keywords"
            or tag.get("kwd-group-type") is None
        ):
            keyword_tags += [tag for tag in tag if tag.name == "kwd"]
    return keyword_tags


def lazy_subject_area(soup, subject_group_type=None):
    # Supports all subject areas or just particular ones filtered by
    tags = lazy_extract_nodes(soup, "subject")

    if subject_group_type:
        for tag in tags:
            if tag.parent.get("subj-group-type") == subject_group_type:
                yield tag
    else:
        for tag in tags:
            if (
                tag.parent.name == "subj-group" and
                tag.parent.parent.name == "article-categories" and
                tag.parent.parent.parent.name == "article-meta"
            ):
                yield tag


def subject_area(soup, subject_group_type=None):
    return list(lazy_subject_area(soup, subject_group_type))


def full_subject_area(soup, subject_group_type=None):

    subject_group_tags = extract_nodes(soup, "subj-group")
    subject_group_tags = [
        tag
        for tag in subject_group_tags
        if tag.parent.name == "article-categories"
        and tag.parent.parent.name == "article-meta"
    ]

    if subject_group_type:
        subject_group_tags = list(
            filter(lambda tag: tag.get("subj-group-type" == subject_group_type))
        )

    return subject_group_tags


def lazy_custom_meta(soup, meta_name=None):
    custom_meta_tags = lazy_extract_nodes(soup, "custom-meta")
    if meta_name is not None:
        for tag in custom_meta_tags:
            if node_contents_str(extract_first_node(tag, "meta-name")) == meta_name:
                yield tag
    else:
        for tag in custom_meta_tags:
            yield tag


def custom_meta(soup, meta_name=None):
    return list(lazy_custom_meta(soup, meta_name))


def display_channel(soup):
    return subject_area(soup, subject_group_type="display-channel")


def lazy_sub_display_channel(soup):
    return lazy_subject_area(soup, subject_group_type="sub-display-channel")


def sub_display_channel(soup):
    return list(lazy_sub_display_channel(soup))


def category(soup):
    return subject_area(soup, subject_group_type="heading")


def related_article(soup):
    related_article_tags = extract_nodes(soup, "related-article")
    return [tag for tag in related_article_tags if tag.parent.name == "article-meta"]


def lazy_mixed_citations(soup):
    return lazy_extract_nodes(soup, "mixed-citation")


def mixed_citations(soup):
    return list(lazy_mixed_citations(soup))


def related_object(soup):
    return extract_nodes(soup, "related-object")


def lazy_object_id(soup, pub_id_type):
    return lazy_extract_nodes(soup, "object-id", attr="pub-id-type", value=pub_id_type)


def object_id(soup, pub_id_type):
    return list(lazy_object_id(soup, pub_id_type))


def lazy_pub_history(soup):
    return lazy_extract_nodes(soup, "pub-history")


def pub_history(soup):
    return list(lazy_pub_history(soup))


def event(soup):
    return extract_nodes(soup, "event")


def lazy_event_desc(soup):
    return lazy_extract_nodes(soup, "event-desc")


def event_desc(soup):
    return list(lazy_event_desc(soup))


def label(soup):
    return extract_first_node(soup, "label")


def contributors(soup):
    return extract_nodes(soup, "contrib")


def article_contributors(soup):
    article_meta_tag = article_meta(soup)
    if article_meta_tag:
        contributor_tags = extract_nodes(article_meta_tag, ["contrib", "on-behalf-of"])
        return [tag for tag in contributor_tags if tag.parent.name == "contrib-group"]


def authors(soup, contrib_type="author"):
    if contrib_type:
        return extract_nodes(soup, "contrib", attr="contrib-type", value=contrib_type)
    else:
        return extract_nodes(soup, "contrib")


def caption(soup):
    return extract_first_node(soup, "caption")


def author_notes(soup):
    return extract_first_node(soup, "author-notes")


def corresp(soup):
    return extract_nodes(soup, "corresp")


def lazy_fn_group(soup, content_type=None):
    if content_type:
        return lazy_extract_nodes(soup, "fn-group", attr="content-type", value=content_type)
    else:
        return lazy_extract_nodes(soup, "fn-group")


def fn_group(soup, content_type=None):
    return list(lazy_fn_group(soup, content_type))


def fn(soup):
    return extract_nodes(soup, "fn")


def lazy_media(soup):
    return lazy_extract_nodes(soup, "media")


def media(soup):
    return list(lazy_media(soup))


def lazy_inline_graphic(soup):
    return lazy_extract_nodes(soup, "inline-graphic")


def inline_graphic(soup):
    return list(lazy_inline_graphic(soup))


def lazy_graphic(soup):
    return lazy_extract_nodes(soup, "graphic")


def graphic(soup):
    return list(lazy_graphic(soup))


def lazy_self_uri(soup):
    return lazy_extract_nodes(soup, "self-uri")


def self_uri(soup):
    return list(lazy_self_uri(soup))


def lazy_supplementary_material(soup):
    return lazy_extract_nodes(soup, "supplementary-material")


def supplementary_material(soup):
    return list(lazy_supplementary_material(soup))


#
# authors
#

def lazy_contrib_id(soup):
    return lazy_extract_nodes(soup, "contrib-id")


def contrib_id(soup):
    return list(lazy_contrib_id(soup))


def email(soup):
    return extract_nodes(soup, "email")


def lazy_phone(soup):
    return lazy_extract_nodes(soup, "phone")


def phone(soup):
    return list(lazy_phone(soup))


def lazy_bio(soup):
    return lazy_extract_nodes(soup, "bio")


def bio(soup):
    return list(lazy_bio(soup))


#
# references
#


def ref_list(soup):
    return extract_nodes(soup, "ref")


def lazy_volume(soup):
    return lazy_extract_nodes(soup, "volume")


def volume(soup):
    return list(lazy_volume(soup))


def lazy_issue(soup):
    return lazy_extract_nodes(soup, "issue")


def issue(soup):
    return list(lazy_issue(soup))


def lazy_elocation_id(soup):
    return lazy_extract_nodes(soup, "elocation-id")


def elocation_id(soup):
    return list(lazy_elocation_id(soup))


def lazy_fpage(soup):
    return lazy_extract_nodes(soup, "fpage")    


def fpage(soup):
    return list(lazy_fpage(soup))


def lazy_lpage(soup):
    return lazy_extract_nodes(soup, "lpage")


def lpage(soup):
    return list(lazy_lpage(soup))


def lazy_collab(soup):
    return lazy_extract_nodes(soup, "collab")


def collab(soup):
    return list(lazy_collab(soup))


def lazy_publisher_loc(soup):
    return lazy_extract_nodes(soup, "publisher-loc")


def publisher_loc(soup):
    return list(lazy_publisher_loc(soup))


def lazy_publisher_name(soup):
    return lazy_extract_nodes(soup, "publisher-name")


def publisher_name(soup):
    return list(lazy_publisher_name(soup))


def lazy_comment(soup):
    return lazy_extract_nodes(soup, "comment")


def comment(soup):
    return list(lazy_comment(soup))


def lazy_element_citation(soup):
    return lazy_extract_nodes(soup, "element-citation")


def element_citation(soup):
    return list(lazy_element_citation(soup))


def lazy_etal(soup):
    return lazy_extract_nodes(soup, "etal")


def etal(soup):
    return list(lazy_etal(soup))


def lazy_pub_id(soup, pub_id_type=None):
    if pub_id_type:
        return lazy_extract_nodes(soup, "pub-id", attr="pub-id-type", value=pub_id_type)
    else:
        return lazy_extract_nodes(soup, "pub-id")


def pub_id(soup, pub_id_type=None):
    return list(lazy_pub_id(soup, pub_id_type))


def lazy_source(soup):
    return lazy_extract_nodes(soup, "source")


def source(soup):
    return list(lazy_source(soup))


def person_group(soup):
    return extract_nodes(soup, "person-group")


def lazy_surname(soup):
    return lazy_extract_nodes(soup, "surname")


def surname(soup):
    return list(lazy_surname(soup))


def lazy_given_names(soup):
    return lazy_extract_nodes(soup, "given-names")


def given_names(soup):
    return list(lazy_given_names(soup))


def lazy_suffix(soup):
    return lazy_extract_nodes(soup, "suffix")


def suffix(soup):
    return list(lazy_suffix(soup))


def lazy_ext_link(soup, ext_link_type=None):
    if ext_link_type:
        return lazy_extract_nodes(
            soup, "ext-link", attr="ext-link-type", value=ext_link_type
        )
    else:
        return lazy_extract_nodes(soup, "ext-link")


def ext_link(soup, ext_link_type=None):
    return list(lazy_ext_link(soup, ext_link_type))


def lazy_uri(soup):
    return lazy_extract_nodes(soup, "uri")


def uri(soup):
    return list(lazy_uri(soup))


def lazy_edition(soup):
    return lazy_extract_nodes(soup, "edition")


def edition(soup):
    return list(lazy_edition(soup))


def lazy_version(soup):
    return lazy_extract_nodes(soup, "version")


def version(soup):
    return list(lazy_version(soup))

def lazy_chapter_title(soup):
    return lazy_extract_nodes(soup, "chapter-title")


def chapter_title(soup):
    return list(lazy_chapter_title(soup))


def lazy_data_title(soup):
    return lazy_extract_nodes(soup, "data-title")


def data_title(soup):
    return list(lazy_data_title(soup))


def lazy_conf_name(soup):
    return lazy_extract_nodes(soup, "conf-name")


def conf_name(soup):
    return list(lazy_conf_name(soup))


def lazy_date_in_citation(soup):
    return lazy_extract_nodes(soup, "date-in-citation")


def date_in_citation(soup):
    return list(lazy_date_in_citation(soup))


def lazy_patent(soup):
    return lazy_extract_nodes(soup, "patent")


def patent(soup):
    return list(lazy_patent(soup))


#
# back
#


def back(soup):
    return extract_first_node(soup, "back")


def lazy_app_group(soup):
    return lazy_extract_nodes(soup, "app-group")


def app_group(soup):
    return list(lazy_app_group(soup))


def app(soup):
    return extract_nodes(soup, "app")


#
# body
#


def body(soup):
    return extract_nodes(soup, "body")


def article_body(soup):
    return extract_first_node(soup, "body")


#
# sub-article
#


def sub_article(soup, article_type=None):
    return extract_nodes(soup, "sub-article", attr="article-type", value=article_type)


def filter_sub_articles_by_title(
    sub_article_nodes, include_title=None, exclude_title=None
):
    "filter a list of sub-article nodes by case-insensitive article-title matching"
    node_list = []

    if not sub_article_nodes:
        return node_list

    for node in sub_article_nodes:

        # only filter by the title value if there is one
        if article_title(node):
            if include_title and exclude_title:
                # test if include_title matches and exclude_title does not match
                if (
                    include_title.lower()
                    in node_contents_str(article_title(node)).lower()
                ) and (
                    exclude_title.lower()
                    not in node_contents_str(article_title(node)).lower()
                ):
                    node_list.append(node)
            elif include_title:
                # if only include_title matches
                if (
                    include_title.lower()
                    in node_contents_str(article_title(node)).lower()
                ):
                    node_list.append(node)
            elif exclude_title:
                # if only exclude_title does not match
                if (
                    exclude_title.lower()
                    not in node_contents_str(article_title(node)).lower()
                ):
                    node_list.append(node)
            else:
                # by default keep the node
                node_list.append(node)
        else:
            # by default keep the node if it has no title regardless of filter term
            node_list.append(node)

    return node_list


def editor_report_by_title(soup, include_title=None):
    "list of editor-report sub-article filtered by article-title value"
    sub_article_nodes = sub_article(soup, "editor-report")
    return filter_sub_articles_by_title(sub_article_nodes, include_title=include_title)


def editor_evaluation(soup):
    "sub-article node of type editor-report with evaluation in the article-title"
    return first(editor_report_by_title(soup, include_title="evaluation"))


def elife_assessment(soup):
    "sub-article node of type editor-report with assessment in the article-title"
    return first(editor_report_by_title(soup, include_title="assessment"))


def decision_letter(soup):
    tag = first(sub_article(soup, "article-commentary"))
    if not tag:
        tag = first(sub_article(soup, "decision-letter"))
    return tag


def author_response(soup):
    "sub-article node of type reply or author-comment, return the first one found"
    return first(sub_article(soup, "reply") + sub_article(soup, "author-comment"))


def referee_report_by_title(soup, include_title=None, exclude_title=None):
    "list of referee-report sub-article filtered by article-title value"
    sub_article_nodes = sub_article(soup, "referee-report")
    return filter_sub_articles_by_title(
        sub_article_nodes, include_title=include_title, exclude_title=exclude_title
    )


def recommendations_for_authors(soup):
    "sub-article node of type referee-report with recommendations in the article-title"
    return first(referee_report_by_title(soup, include_title="recommendations"))


def public_reviews(soup):
    "list of sub-article node of type referee-report without recommendations in the article-title"
    return referee_report_by_title(soup, exclude_title="recommendations")


#
# block content
#

def lazy_section(soup, sec_type=None):
    if sec_type:
        return lazy_extract_nodes(soup, "sec", attr="sec-type", value=sec_type)
    else:
        return lazy_extract_nodes(soup, "sec")


def section(soup, sec_type=None):
    return list(lazy_section(soup, sec_type))


def lazy_paragraph(soup):
    return lazy_extract_nodes(soup, "p")


def paragraph(soup):
    return list(lazy_paragraph(soup))


def table(soup):
    return extract_nodes(soup, "table")


def table_wrap_foot(soup):
    return extract_nodes(soup, "table-wrap-foot")


def disp_formula(soup):
    return extract_nodes(soup, "disp-formula")


def lazy_math(soup):
    return lazy_extract_nodes(soup, "math")


def math(soup):
    return list(lazy_math(soup))


def lazy_boxed_text(soup):
    return lazy_extract_nodes(soup, "boxed-text")


def boxed_text(soup):
    return list(lazy_boxed_text(soup))


def fig(soup):
    return extract_nodes(soup, "fig")


def fig_group(soup):
    return extract_nodes(soup, "fig-group")


# Redefining `list` could be problematic
# lsh@2023-12-01: renamed `list` to `get_list`
def get_list(soup): 
    return extract_nodes(soup, "list")


def list_item(soup):
    return extract_nodes(soup, "list-item")


#
# funding
#

def lazy_funding_group(soup):
    return lazy_extract_nodes(soup, "funding-group")


def funding_group(soup):
    return list(lazy_funding_group(soup))


def award_group(soup):
    return extract_nodes(soup, "award-group")


def principal_award_recipient(soup):
    return extract_nodes(soup, "principal-award-recipient")


def lazy_string_name(soup):
    return lazy_extract_nodes(soup, "string-name")


def string_name(soup):
    return list(lazy_string_name(soup))


