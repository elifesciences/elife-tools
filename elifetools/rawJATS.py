from elifetools.utils import first, firstnn, extract_nodes, node_contents_str

"""
rawParser.py extracts and returns the nodes from the article xml using BeautifulSoup so that functionality at higher levels may use and combine them as neccessary.

"""


def article_meta(soup):
    return first(extract_nodes(soup, "article-meta"))


def article_title(soup):
    return first(extract_nodes(soup, "article-title"))


def title(soup):
    return first(extract_nodes(soup, "title"))


def abstract(soup, abstract_type=None):
    if abstract_type:
        return extract_nodes(
            soup, "abstract", attr="abstract-type", value=abstract_type
        )
    else:
        return extract_nodes(soup, "abstract")


def article_id(soup, pub_id_type=None):
    if pub_id_type:
        return extract_nodes(soup, "article-id", attr="pub-id-type", value=pub_id_type)
    else:
        return extract_nodes(soup, "article-id")


def meta_article_id(soup, pub_id_type):
    tags = article_id(soup, pub_id_type)
    # the first article-id tag whose parent is article-meta
    return first([tag for tag in tags if tag.parent.name == "article-meta"])


def doi(soup):
    return meta_article_id(soup, pub_id_type="doi")


def publisher_id(soup):
    return meta_article_id(soup, pub_id_type="publisher-id")


def journal_id(soup):
    # the first non-nil tag
    return firstnn(
        extract_nodes(soup, "journal-id", attr="journal-id-type", value="publisher-id")
    )


def journal_title(soup):
    return first(extract_nodes(soup, "journal-title"))


def journal_issn(soup, pub_format, pub_type):
    if pub_format is None and pub_type is None:
        # return the first issn tag found regardless of which type
        return first(extract_nodes(soup, "issn"))
    elif pub_format is not None:
        return first(
            extract_nodes(soup, "issn", attr="publication-format", value=pub_format)
        )
    elif pub_type is not None:
        return first(extract_nodes(soup, "issn", attr="pub-type", value=pub_type))


def publisher(soup):
    return first(extract_nodes(soup, "publisher-name"))


def article_type(soup):
    # returns raw data, just that the data doesn't contain any BS nodes
    return first(extract_nodes(soup, "article")).get("article-type")


def pub_date(soup, date_type=None, pub_type=None):
    if date_type is not None:
        return extract_nodes(soup, "pub-date", attr="date-type", value=date_type)
    elif pub_type is not None:
        return extract_nodes(soup, "pub-date", attr="pub-type", value=pub_type)
    else:
        return extract_nodes(soup, "pub-date")


def date(soup, date_type=None):
    if date_type is not None:
        return extract_nodes(soup, "date", attr="date-type", value=date_type)
    else:
        return extract_nodes(soup, "date")


def history_date(soup, date_type):
    date_tags = date(soup, date_type)
    return first([tag for tag in date_tags if tag.parent.name == "history"])


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
    conflict_tags = extract_nodes(soup, "fn", attr="fn-type", value="conflict")
    conflict_tags += extract_nodes(soup, "fn", attr="fn-type", value="COI-statement")
    return conflict_tags


def permissions(soup):
    # a better selector might be "article-meta.permissions"
    return extract_nodes(soup, "permissions")


def article_permissions(soup):
    # a better selector might be "article-meta.permissions"
    permissions_tags = permissions(soup)
    return first([tag for tag in permissions_tags if tag.parent.name == "article-meta"])


def licence(soup):
    return extract_nodes(soup, "license")


def licence_p(soup):
    return extract_nodes(soup, "license-p")


def licence_url(soup):
    "License url attribute of the license tag"
    if licence(soup):
        return first(licence(soup)).get("xlink:href")


def attrib(soup):
    return extract_nodes(soup, "attrib")


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
    tags = first(
        extract_nodes(
            soup, "kwd-group", attr="kwd-group-type", value="research-organism"
        )
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


def subject_area(soup, subject_group_type=None):
    # Supports all subject areas or just particular ones filtered by
    subject_area_tags = []
    tags = extract_nodes(soup, "subject")

    subject_area_tags = [
        tag
        for tag in tags
        if tag.parent.name == "subj-group"
        and tag.parent.parent.name == "article-categories"
        and tag.parent.parent.parent.name == "article-meta"
    ]
    if subject_group_type:
        subject_area_tags = [
            tag
            for tag in tags
            if tag.parent.get("subj-group-type") == subject_group_type
        ]
    return subject_area_tags


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


def custom_meta(soup, meta_name=None):
    custom_meta_tags = extract_nodes(soup, "custom-meta")
    if meta_name is not None:
        custom_meta_tags = [
            tag
            for tag in custom_meta_tags
            if node_contents_str(first(extract_nodes(tag, "meta-name"))) == meta_name
        ]
    return custom_meta_tags


def display_channel(soup):
    return subject_area(soup, subject_group_type="display-channel")


def sub_display_channel(soup):
    return subject_area(soup, subject_group_type="sub-display-channel")


def category(soup):
    return subject_area(soup, subject_group_type="heading")


def related_article(soup):
    related_article_tags = extract_nodes(soup, "related-article")
    return [tag for tag in related_article_tags if tag.parent.name == "article-meta"]


def mixed_citations(soup):
    return extract_nodes(soup, "mixed-citation")


def related_object(soup):
    return extract_nodes(soup, "related-object")


def object_id(soup, pub_id_type):
    return extract_nodes(soup, "object-id", attr="pub-id-type", value=pub_id_type)


def pub_history(soup):
    return extract_nodes(soup, "pub-history")


def event(soup):
    return extract_nodes(soup, "event")


def event_desc(soup):
    return extract_nodes(soup, "event-desc")


def label(soup):
    return first(extract_nodes(soup, "label"))


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
    return first(extract_nodes(soup, "caption"))


def author_notes(soup):
    return first(extract_nodes(soup, "author-notes"))


def corresp(soup):
    return extract_nodes(soup, "corresp")


def fn_group(soup, content_type=None):
    if content_type:
        return extract_nodes(soup, "fn-group", attr="content-type", value=content_type)
    else:
        return extract_nodes(soup, "fn-group")


def fn(soup):
    return extract_nodes(soup, "fn")


def media(soup):
    return extract_nodes(soup, "media")


def inline_graphic(soup):
    return extract_nodes(soup, "inline-graphic")


def graphic(soup):
    return extract_nodes(soup, "graphic")


def self_uri(soup):
    return extract_nodes(soup, "self-uri")


def supplementary_material(soup):
    return extract_nodes(soup, "supplementary-material")


#
# authors
#


def contrib_id(soup):
    return extract_nodes(soup, "contrib-id")


def email(soup):
    return extract_nodes(soup, "email")


def phone(soup):
    return extract_nodes(soup, "phone")


def bio(soup):
    return extract_nodes(soup, "bio")


#
# references
#


def ref_list(soup):
    return extract_nodes(soup, "ref")


def volume(soup):
    return extract_nodes(soup, "volume")


def issue(soup):
    return extract_nodes(soup, "issue")


def elocation_id(soup):
    return extract_nodes(soup, "elocation-id")


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


def element_citation(soup):
    return extract_nodes(soup, "element-citation")


def etal(soup):
    return extract_nodes(soup, "etal")


def pub_id(soup, pub_id_type=None):
    if pub_id_type:
        return extract_nodes(soup, "pub-id", attr="pub-id-type", value=pub_id_type)
    else:
        return extract_nodes(soup, "pub-id")


def source(soup):
    return extract_nodes(soup, "source")


def person_group(soup):
    return extract_nodes(soup, "person-group")


def surname(soup):
    return extract_nodes(soup, "surname")


def given_names(soup):
    return extract_nodes(soup, "given-names")


def suffix(soup):
    return extract_nodes(soup, "suffix")


def ext_link(soup, ext_link_type=None):
    if ext_link_type:
        return extract_nodes(
            soup, "ext-link", attr="ext-link-type", value=ext_link_type
        )
    else:
        return extract_nodes(soup, "ext-link")


def uri(soup):
    return extract_nodes(soup, "uri")


def edition(soup):
    return extract_nodes(soup, "edition")


def version(soup):
    return extract_nodes(soup, "version")


def chapter_title(soup):
    return extract_nodes(soup, "chapter-title")


def data_title(soup):
    return extract_nodes(soup, "data-title")


def conf_name(soup):
    return extract_nodes(soup, "conf-name")


def date_in_citation(soup):
    return extract_nodes(soup, "date-in-citation")


def patent(soup):
    return extract_nodes(soup, "patent")


#
# back
#


def back(soup):
    return first(extract_nodes(soup, "back"))


def app_group(soup):
    return extract_nodes(soup, "app-group")


def app(soup):
    return extract_nodes(soup, "app")


#
# body
#


def body(soup):
    return extract_nodes(soup, "body")


def article_body(soup):
    return first(extract_nodes(soup, "body"))


def sub_article(soup, article_type=None):
    return extract_nodes(soup, "sub-article", attr="article-type", value=article_type)


def editor_evaluation(soup):
    return first(sub_article(soup, "editor-report"))


def decision_letter(soup):
    tag = first(sub_article(soup, "article-commentary"))
    if not tag:
        tag = first(sub_article(soup, "decision-letter"))
    return tag


def author_response(soup):
    return first(sub_article(soup, "reply"))


def section(soup, sec_type=None):
    if sec_type:
        return extract_nodes(soup, "sec", attr="sec-type", value=sec_type)
    else:
        return extract_nodes(soup, "sec")


def paragraph(soup):
    return extract_nodes(soup, "p")


def table(soup):
    return extract_nodes(soup, "table")


def table_wrap_foot(soup):
    return extract_nodes(soup, "table-wrap-foot")


def disp_formula(soup):
    return extract_nodes(soup, "disp-formula")


def math(soup):
    return extract_nodes(soup, "math")


def boxed_text(soup):
    return extract_nodes(soup, "boxed-text")


def fig(soup):
    return extract_nodes(soup, "fig")


def fig_group(soup):
    return extract_nodes(soup, "fig-group")


def list(soup):  # Redefining `list` could be problematic
    return extract_nodes(soup, "list")


def list_item(soup):
    return extract_nodes(soup, "list-item")


#
# funding
#


def funding_group(soup):
    return extract_nodes(soup, "funding-group")


def award_group(soup):
    return extract_nodes(soup, "award-group")


def principal_award_recipient(soup):
    return extract_nodes(soup, "principal-award-recipient")


def string_name(soup):
    return extract_nodes(soup, "string-name")
