from collections import OrderedDict
import copy
import re

from bs4 import BeautifulSoup
from slugify import slugify

import elifetools.rawJATS as raw_parser
import elifetools.json_rewrite
from elifetools import utils
from elifetools.utils_html import xml_to_html, references_author_collab


XML_NAMESPACES = [
    OrderedDict(
        [
            ("prefix", "mml:"),
            ("attribute", "xmlns:mml"),
            ("uri", "http://www.w3.org/1998/Math/MathML"),
        ]
    ),
    OrderedDict(
        [
            ("prefix", "xlink:"),
            ("attribute", "xmlns:xlink"),
            ("uri", "http://www.w3.org/1999/xlink"),
        ]
    ),
]

SCIETY_URI_DOMAIN = "sciety.org"


def parse_xml(xml):
    return BeautifulSoup(xml, "lxml-xml")


def parse_document(filelocation):
    with open(filelocation, "rb") as open_file:
        return parse_xml(open_file)


def title(soup):
    return utils.node_text(raw_parser.article_title(soup))


def full_title(soup):
    # The title including italic tags, etc.
    return utils.node_contents_str(raw_parser.article_title(soup))


def title_short(soup):
    "'title' truncated to 20 chars"
    # TODO: 20 is arbitrary,
    return str(title(soup))[:20]


def title_slug(soup):
    "'title' slugified"
    return slugify(title(soup))


def title_prefix(soup):
    "titlePrefix for article JSON is only articles with certain display_channel values"
    prefix = None
    display_channel_match_list = ["feature article", "insight", "editorial"]
    for d_channel in display_channel(soup):
        if d_channel.lower() in display_channel_match_list:
            if raw_parser.sub_display_channel(soup):
                prefix = utils.node_text(
                    utils.first(raw_parser.sub_display_channel(soup))
                )
    return prefix


def title_prefix_json(soup):
    "titlePrefix with capitalisation changed"
    prefix = title_prefix(soup)
    prefix_rewritten = elifetools.json_rewrite.rewrite_json(
        "title_prefix_json", soup, prefix
    )
    return prefix_rewritten


def doi(soup):
    # the first non-nil value returned by the raw parser
    return utils.doi_uri_to_doi(utils.node_text(raw_parser.doi(soup)))


def publisher_id(soup):
    # aka the article_id, specified by the publisher
    return utils.node_text(raw_parser.publisher_id(soup))


def journal_id(soup):
    return utils.node_text(raw_parser.journal_id(soup))


def journal_title(soup):
    return utils.node_text(raw_parser.journal_title(soup))


def journal_issn(soup, pub_format=None, pub_type=None):
    return utils.node_text(raw_parser.journal_issn(soup, pub_format, pub_type))


def publisher(soup):
    return utils.node_text(raw_parser.publisher(soup))


def article_type(soup):
    # no node text extraction required
    return raw_parser.article_type(soup)


def volume(soup):
    return utils.node_text(utils.first(raw_parser.volume(soup)))


def issue(soup):
    return utils.node_text(utils.first(raw_parser.issue(raw_parser.article_meta(soup))))


def fpage(soup):
    return utils.node_text(utils.first(raw_parser.fpage(raw_parser.article_meta(soup))))


def lpage(soup):
    return utils.node_text(utils.first(raw_parser.lpage(raw_parser.article_meta(soup))))


def elocation_id(soup):
    return utils.node_text(
        utils.first(raw_parser.elocation_id(raw_parser.article_meta(soup)))
    )


def research_organism(soup):
    "Find the research-organism from the set of kwd-group tags"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return list(map(utils.node_text, raw_parser.research_organism_keywords(soup)))


def full_research_organism(soup):
    "research-organism list including inline tags, such as italic"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return list(
        map(utils.node_contents_str, raw_parser.research_organism_keywords(soup))
    )


def keywords(soup):
    """
    Find the keywords from the set of kwd-group tags
    which are typically labelled as the author keywords
    """
    if not raw_parser.author_keywords(soup):
        return []
    return list(map(utils.node_text, raw_parser.author_keywords(soup)))


def full_keywords(soup):
    "author keywords list including inline tags, such as italic"
    if not raw_parser.author_keywords(soup):
        return []
    return list(map(utils.node_contents_str, raw_parser.author_keywords(soup)))


def full_keyword_groups(soup):
    groups = {}
    for group_tag in raw_parser.keyword_group(soup):
        group = list(
            map(utils.node_contents_str, utils.extract_nodes(group_tag, "kwd"))
        )
        group = list(map(lambda s: s.strip(), group))
        if "kwd-group-type" in group_tag.attrs:
            groups[group_tag["kwd-group-type"].strip()] = group
    return groups


def full_custom_meta(soup, meta_name=None):
    return raw_parser.custom_meta(soup, meta_name)


def impact_statement(soup):
    tag = utils.first(full_custom_meta(soup, "Author impact statement"))
    if tag is not None:
        return utils.node_contents_str(
            utils.first(utils.extract_nodes(tag, "meta-value"))
        )
    return ""


def version_history(soup, html_flag=True):
    "extract the article version history details"

    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    version_history = []
    related_object_tags = raw_parser.related_object(raw_parser.article_meta(soup))
    for tag in related_object_tags:
        article_version = OrderedDict()
        date_tag = utils.first(raw_parser.date(tag))

        if not date_tag:
            continue

        utils.copy_attribute(date_tag.attrs, "date-type", article_version, "version")
        (day, month, year) = ymd(date_tag)
        article_version["day"] = day
        article_version["month"] = month
        article_version["year"] = year
        article_version["date"] = utils.date_struct_nn(year, month, day)

        utils.copy_attribute(tag.attrs, "xlink:href", article_version, "xlink_href")
        utils.set_if_value(
            article_version,
            "comment",
            convert(utils.node_contents_str(utils.first(raw_parser.comment(tag)))),
        )
        version_history.append(article_version)
    return version_history


def clinical_trials(soup):
    clinical_trials = []
    related_object_tags = raw_parser.related_object(raw_parser.article_meta(soup))
    # only consider related-object tags that have a source-id-type attribute
    for tag in [tag for tag in related_object_tags if "source-id-type" in tag.attrs]:
        clinical_trial = OrderedDict()
        for attribute in [
            "id",
            "content-type",
            "document-id",
            "document-id-type",
            "source-id",
            "source-id-type",
            "source-type",
        ]:
            utils.copy_attribute(tag.attrs, attribute, clinical_trial)
        clinical_trial["text"] = tag.text
        utils.copy_attribute(tag.attrs, "xlink:href", clinical_trial, "xlink_href")
        clinical_trials.append(clinical_trial)
    return clinical_trials


def format_related_object(related_object):
    return related_object["id"], {}


def related_object_ids(soup):
    tags = []
    if raw_parser.related_object(soup):
        tags = list(
            filter(
                lambda tag: tag.get("id") is not None, raw_parser.related_object(soup)
            )
        )
    return dict(map(format_related_object, tags))


def article_id_list(soup):
    """return a list of article-id data"""
    id_list = []
    for article_id_tag in raw_parser.article_id(soup):
        id_details = OrderedDict()
        utils.set_if_value(id_details, "type", article_id_tag.get("pub-id-type"))
        utils.set_if_value(id_details, "value", article_id_tag.text)
        utils.set_if_value(
            id_details, "assigning-authority", article_id_tag.get("assigning-authority")
        )
        id_list.append(id_details)
    return id_list


def pub_history(soup):
    events = []
    pub_history = utils.first(raw_parser.pub_history(soup))
    if pub_history:
        event_tags = raw_parser.event(pub_history)
        for event_tag in event_tags:
            event = OrderedDict()

            date_tag = utils.first(raw_parser.date(event_tag))

            # set event_type from the event tag, otherwise from the date tag
            utils.set_if_value(event, "event_type", event_tag.get("event-type"))
            if not event.get("event_type") and date_tag:
                utils.set_if_value(event, "event_type", date_tag.get("date-type"))

            event_desc_tag = utils.first(raw_parser.event_desc(event_tag))
            if event_desc_tag:
                event_desc = utils.node_contents_str(event_desc_tag).rstrip()
                utils.set_if_value(event, "event_desc", event_desc)
                utils.set_if_value(
                    event, "event_desc_html", xml_to_html(True, event_desc)
                )
            # look for uri in a self-uri tag, otherwise look for an ext-link tag
            self_uri_tag = utils.first(raw_parser.self_uri(event_tag))
            if self_uri_tag:
                utils.set_if_value(event, "uri", self_uri_tag.get("xlink:href"))
            else:
                uri_tag = utils.first(raw_parser.ext_link(event_tag, "uri"))
                if uri_tag:
                    utils.set_if_value(event, "uri", uri_tag.get("xlink:href"))
                    utils.set_if_value(
                        event, "uri_text", utils.node_contents_str(uri_tag)
                    )
            if article_id_list(event_tag):
                event["id_list"] = article_id_list(event_tag)

            if date_tag:
                (day, month, year) = ymd(date_tag)
                event["day"] = day
                event["month"] = month
                event["year"] = year
                event["date"] = utils.date_struct_nn(year, month, day)
                utils.set_if_value(
                    event, "iso-8601-date", date_tag.get("iso-8601-date")
                )
                (day, month, year) = ymd(date_tag)
            events.append(event)
    return events


@utils.strippen
def acknowledgements(soup):
    return utils.node_text(raw_parser.acknowledgements(soup))


# DEPRECATED: use `acknowledgements`. avoid unnecessary abbreviations
def ack(soup):
    return acknowledgements(soup)


@utils.nullify
@utils.strippen
def conflict(soup):
    result = [utils.node_text(tag) for tag in raw_parser.conflict(soup)]
    return result


def copyright_statement(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return utils.node_text(raw_parser.copyright_statement(permissions_tag))
    return None


@utils.inten
def copyright_year(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return utils.node_text(raw_parser.copyright_year(permissions_tag))
    return None


def copyright_holder(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return utils.node_text(raw_parser.copyright_holder(permissions_tag))
    return None


def copyright_holder_json(soup):
    "for json output add a full stop if ends in et al"
    holder = None
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        holder = utils.node_text(raw_parser.copyright_holder(permissions_tag))
    if holder is not None and holder.endswith("et al"):
        holder = holder + "."
    return holder


def license(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return utils.node_text(utils.first(raw_parser.licence_p(permissions_tag)))
    return None


def full_license(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return utils.node_contents_str(
            utils.first(raw_parser.licence_p(permissions_tag))
        )
    return None


def license_url(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return raw_parser.licence_url(permissions_tag)
    return None


def license_json(soup):
    return xml_to_html(True, full_license(soup))


def funding_statement(soup):
    return utils.node_text(raw_parser.funding_statement(soup))


def full_funding_statement(soup):
    return utils.node_contents_str(raw_parser.funding_statement(soup))


#
# authors
#

#
# refs
#


def ref_text(tag):
    # ref - human readable full reference text
    ref_text = utils.node_text(tag)
    ref_text = utils.strip_strings(ref_text)
    # Remove excess space
    ref_text = " ".join(ref_text.split())
    # Fix punctuation spaces and extra space
    ref_text = utils.strip_punctuation_space(utils.strip_strings(ref_text))
    return ref_text


def subject_area(soup):
    """
    Find the subject areas from article-categories subject tags
    """
    subject_area = []

    tags = raw_parser.subject_area(soup)
    for tag in tags:
        subject_area.append(utils.node_text(tag))

    return subject_area


def full_subject_area(soup):
    subject_areas = raw_parser.full_subject_area(soup)
    areas = {}
    for tag in subject_areas:
        subj_type = tag["subj-group-type"]
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
        display_channel.append(utils.node_text(tag))

    return display_channel


def category(soup):
    """
    Find the category from subject areas
    """
    category = []

    tags = raw_parser.category(soup)
    for tag in tags:
        category.append(utils.node_text(tag))

    return category


def ymd(soup):
    """
    Get the year, month and day from child tags
    """
    day = utils.node_text(raw_parser.day(soup))
    month = utils.node_text(raw_parser.month(soup))
    year = utils.node_text(raw_parser.year(soup))
    return (day, month, year)


def pub_date(soup):
    """
    Return the publishing date in struct format
    pub_date_date, pub_date_day, pub_date_month, pub_date_year, pub_date_timestamp
    Default date_type is pub
    """
    pub_date = utils.first(raw_parser.pub_date(soup, date_type="pub"))
    if pub_date is None:
        pub_date = utils.first(raw_parser.pub_date(soup, date_type="publication"))
    if pub_date is None:
        return None
    (day, month, year) = ymd(pub_date)
    return utils.date_struct(year, month, day)


def pub_dates(soup):
    """
    return a list of all the pub dates
    """
    pub_dates = []
    tags = raw_parser.pub_date(soup)
    for tag in tags:
        pub_date = OrderedDict()
        utils.copy_attribute(tag.attrs, "publication-format", pub_date)
        utils.copy_attribute(tag.attrs, "date-type", pub_date)
        utils.copy_attribute(tag.attrs, "pub-type", pub_date)
        for tag_attr in ["date-type", "pub-type"]:
            if tag_attr in tag.attrs:
                (day, month, year) = ymd(tag)
                pub_date["day"] = day
                pub_date["month"] = month
                pub_date["year"] = year
                pub_date["date"] = utils.date_struct_nn(year, month, day)
        pub_dates.append(pub_date)
    return pub_dates


def history_date(soup, date_type=None):
    """
    Find a date in the history tag for the specific date_type
    typical date_type values: received, accepted
    """
    if date_type is None:
        return None

    history_date = raw_parser.history_date(soup, date_type)
    if history_date is None:
        return None
    (day, month, year) = ymd(history_date)
    return utils.date_struct(year, month, day)


def pub_date_date(soup):
    """
    Find the published date in human readable form
    """
    return utils.date_text(pub_date(soup))


def pub_date_day(soup):
    """
    Find the published date day
    """
    return utils.day_text(pub_date(soup))


def pub_date_month(soup):
    """
    Find the published date month
    """
    return utils.month_text(pub_date(soup))


def pub_date_year(soup):
    """
    Find the published date year
    """
    return utils.year_text(pub_date(soup))


def pub_date_timestamp(soup):
    """
    Find the published date timestamp, in UTC time
    """
    return utils.date_timestamp(pub_date(soup))


def received_date_date(soup):
    """
    Find the received date in human readable form
    """
    return utils.date_text(history_date(soup, date_type="received"))


def received_date_day(soup):
    """
    Find the received date day
    """
    return utils.day_text(history_date(soup, date_type="received"))


def received_date_month(soup):
    """
    Find the received date month
    """
    return utils.month_text(history_date(soup, date_type="received"))


def received_date_year(soup):
    """
    Find the received date year
    """
    return utils.year_text(history_date(soup, date_type="received"))


def received_date_timestamp(soup):
    """
    Find the received date timestamp, in UTC time
    """
    return utils.date_timestamp(history_date(soup, date_type="received"))


def accepted_date_date(soup):
    """
    Find the accepted date in human readable form
    """
    return utils.date_text(history_date(soup, date_type="accepted"))


def accepted_date_day(soup):
    """
    Find the accepted date day
    """
    return utils.day_text(history_date(soup, date_type="accepted"))


def accepted_date_month(soup):
    """
    Find the accepted date month
    """
    return utils.month_text(history_date(soup, date_type="accepted"))


def accepted_date_year(soup):
    """
    Find the accepted date year
    """
    return utils.year_text(history_date(soup, date_type="accepted"))


def accepted_date_timestamp(soup):
    """
    Find the accepted date timestamp, in UTC time
    """
    return utils.date_timestamp(history_date(soup, date_type="accepted"))


def collection_year(soup):
    """
    Pub date of type collection will hold a year element for VOR articles
    """
    pub_date = utils.first(raw_parser.pub_date(soup, pub_type="collection"))
    if not pub_date:
        pub_date = utils.first(raw_parser.pub_date(soup, date_type="collection"))
    if not pub_date:
        return None

    year = None
    year_tag = raw_parser.year(pub_date)
    if year_tag:
        year = int(utils.node_text(year_tag))

    return year


def is_poa(soup):
    """
    Test for whether is POA XML or not
    """
    if not raw_parser.body(soup):
        return True

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
            abstract["title"] = utils.node_text(title_tag)

        abstract["content"] = None
        if raw_parser.paragraph(tag):
            abstract["content"] = ""
            abstract["full_content"] = ""

            good_paragraphs = utils.remove_doi_paragraph(raw_parser.paragraph(tag))

            # Plain text content
            glue = ""
            for p_tag in good_paragraphs:
                abstract["content"] += glue + utils.node_text(p_tag)
                glue = " "

            # Content including markup tags
            # When more than one paragraph, wrap each in a <p> tag
            for p_tag in good_paragraphs:
                if utils.node_contents_str(p_tag):
                    abstract["full_content"] += (
                        "<p>" + utils.node_contents_str(p_tag) + "</p>"
                    )

        abstracts.append(abstract)

    return abstracts


def abstract(soup):
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = utils.first(
            list(filter(lambda tag: tag.get("abstract_type") is None, abstract_list))
        )
    if abstract:
        return abstract.get("content")

    return None


def abstract_xml(soup, strip_doi_paragraphs=True, abstract_type=None):
    original_abstract_tag = utils.first(raw_parser.abstract(soup, abstract_type))
    if not original_abstract_tag:
        return None
    abstract_tag = copy.copy(original_abstract_tag)
    if strip_doi_paragraphs and raw_parser.paragraph(abstract_tag):
        for p_tag in raw_parser.paragraph(abstract_tag):
            if utils.paragraph_is_only_doi(p_tag) or utils.starts_with_doi(p_tag):
                p_tag.decompose()
    # add in common JATS XML namespaces which are getting lost
    for namespace in XML_NAMESPACES:
        prefix_match = "<%s" % namespace.get("prefix")
        if namespace.get("attribute") not in abstract_tag.attrs and prefix_match in str(
            abstract_tag
        ):
            abstract_tag[namespace.get("attribute")] = namespace.get("uri")

    return str(abstract_tag)


def full_abstract(soup):
    """
    Return the abstract including inline tags
    """
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = utils.first(
            list(filter(lambda tag: tag.get("abstract_type") is None, abstract_list))
        )
    if abstract:
        return abstract.get("full_content")

    return None


def digest(soup):
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = utils.first(
            list(
                filter(
                    lambda tag: tag.get("abstract_type")
                    in ["executive-summary", "plain-language-summary"],
                    abstract_list,
                )
            )
        )
    if abstract:
        return abstract.get("content")

    return None


def full_digest(soup):
    """
    Return the digest including inline tags
    """
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = utils.first(
            list(
                filter(
                    lambda tag: tag.get("abstract_type")
                    in ["executive-summary", "plain-language-summary"],
                    abstract_list,
                )
            )
        )
    if abstract:
        return abstract["full_content"]

    return None


def related_article(soup):
    related_articles = []

    related_article_tags = raw_parser.related_article(soup)

    for tag in related_article_tags:
        related_article = {}
        related_article["ext_link_type"] = tag.get("ext-link-type")
        related_article["related_article_type"] = tag.get("related-article-type")
        related_article["xlink_href"] = tag.get("xlink:href")
        related_articles.append(related_article)

    return related_articles


def sub_articles(soup):
    article_list = []
    sub_article_tags = raw_parser.sub_article(soup)
    for tag in sub_article_tags:
        sub_article = OrderedDict()
        utils.set_if_value(sub_article, "doi", sub_article_doi(tag))
        utils.set_if_value(sub_article, "article_type", tag.get("article-type"))
        utils.set_if_value(sub_article, "id", tag.get("id"))
        utils.set_if_value(sub_article, "article_title", title(tag))
        if all_contributors(tag):
            sub_article["contributors"] = all_contributors(tag)
        if raw_parser.related_object(tag):
            sub_article["related_objects"] = []
            for related_object_tag in raw_parser.related_object(tag):
                related_object = OrderedDict()
                utils.set_if_value(related_object, "id", related_object_tag.get("id"))
                utils.set_if_value(
                    related_object, "link_type", related_object_tag.get("link-type")
                )
                utils.set_if_value(
                    related_object, "xlink_href", related_object_tag.get("xlink:href")
                )
                sub_article["related_objects"].append(related_object)
        # find parent article tag and set attributes
        for parent in tag.parents:
            if parent.name == "article":
                utils.set_if_value(sub_article, "parent_doi", doi(parent))
                utils.set_if_value(
                    sub_article, "parent_article_type", parent.get("article-type")
                )
                utils.set_if_value(sub_article, "parent_article_title", title(parent))
                utils.set_if_value(
                    sub_article, "parent_license_url", license_url(parent)
                )
                break
        # append
        article_list.append(sub_article)
    return article_list


def mixed_citations(soup):
    mc_tags = raw_parser.mixed_citations(soup)

    def name(nom):
        return {
            "surname": nom.surname.text,
            "given": nom.find("given-names").text,
        }

    def preferred_name(nom):
        suffix = None
        return utils.author_preferred_name(
            nom.surname.text, nom.find("given-names").text, suffix
        )

    def do_format(mc_tag):
        return {
            "journal": {
                "name": mc_tag.source.text,
                "volume": mc_tag.volume.text,
                "fpage": mc_tag.fpage.text,
                "lpage": utils.node_text(mc_tag.lpage),
            },
            "article": {
                "title": mc_tag.find("article-title").text,
                "doi": mc_tag.find("pub-id", attrs={"pub-id-type": "doi"}).text,
                "pub-date": list(map(int, ymd(soup)[::-1])),
                "authors": list(
                    map(
                        name,
                        mc_tag.find(
                            "person-group", attrs={"person-group-type": "author"}
                        ).contents,
                    )
                ),
                "authorLine": format_author_line(
                    list(
                        map(
                            preferred_name,
                            mc_tag.find(
                                "person-group", attrs={"person-group-type": "author"}
                            ).contents,
                        )
                    ),
                    style="ellipsis",
                ),
            },
        }

    return list(map(do_format, mc_tags))


def component_doi(soup):
    """
    Look for all object-id of pub-type-id = doi, these are the component DOI tags
    """
    component_doi = []

    object_id_tags = raw_parser.object_id(soup, pub_id_type="doi")

    # Get components too for later
    component_list = components(soup)

    position = 1

    for tag in object_id_tags:
        component_object = {}
        component_object["doi"] = utils.doi_uri_to_doi(tag.text)
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

    if (tag.name == "fig" and "specific-use" not in tag.attrs) or tag.name == "media":
        # Fig that is not a child figure / figure supplement
        if utils.first_parent(tag, "sub-article"):
            # Sub-article sibling ordinal numbers work differently
            sibling_ordinal = utils.tag_subarticle_sibling_ordinal(tag)
        elif utils.first_parent(tag, "app"):
            sibling_ordinal = utils.tag_appendix_sibling_ordinal(tag)
        elif tag.name == "media":
            # Media video or non-video are different numbering
            sibling_ordinal = utils.tag_media_sibling_ordinal(tag)
        else:
            sibling_ordinal = utils.tag_fig_ordinal(tag)
    elif tag.name == "supplementary-material":
        sibling_ordinal = utils.tag_supplementary_material_sibling_ordinal(tag)
    else:
        # Default
        sibling_ordinal = utils.tag_sibling_ordinal(tag)

    return sibling_ordinal


def tag_details_asset(tag):
    asset = None

    if tag.name == "fig" and "specific-use" in tag.attrs:
        # Child figure / figure supplement
        asset = "figsupp"
    elif tag.name == "media":
        # Set media tag asset value, it is useful
        asset = "media"
    elif tag.name == "app":
        asset = "app"
    elif tag.name == "supplementary-material":
        # Default is supp
        asset = utils.supp_asset(tag)
    elif tag.name == "sub-article":
        if (
            utils.node_text(raw_parser.article_title(tag))
            and utils.node_text(raw_parser.article_title(tag)).lower()
            == "decision letter"
        ):
            asset = "dec"
        elif (
            utils.node_text(raw_parser.article_title(tag))
            and utils.node_text(raw_parser.article_title(tag)).lower()
            == "author response"
        ):
            asset = "resp"

    return asset


def tag_details(tag, nodenames):
    """
    Used in media and graphics to extract data from their parent tags
    """
    details = {}

    details["type"] = tag.name
    details["ordinal"] = utils.tag_ordinal(tag)

    # Ordinal value
    if tag_details_sibling_ordinal(tag):
        details["sibling_ordinal"] = tag_details_sibling_ordinal(tag)

    # Asset name
    if tag_details_asset(tag):
        details["asset"] = tag_details_asset(tag)

    object_id_tag = utils.first(raw_parser.object_id(tag, pub_id_type="doi"))
    if object_id_tag:
        details["component_doi"] = extract_component_doi(tag, nodenames)

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

        utils.copy_attribute(tag.attrs, "mime-subtype", media_item)
        utils.copy_attribute(tag.attrs, "mimetype", media_item)
        utils.copy_attribute(tag.attrs, "xlink:href", media_item, "xlink_href")
        utils.copy_attribute(tag.attrs, "content-type", media_item)

        nodenames = [
            "sub-article",
            "media",
            "fig-group",
            "fig",
            "supplementary-material",
        ]

        details = tag_details(tag, nodenames)
        utils.copy_attribute(details, "component_doi", media_item)
        utils.copy_attribute(details, "type", media_item)
        utils.copy_attribute(details, "sibling_ordinal", media_item)

        # Try to get the component DOI of the parent tag
        parent_tag = utils.first_parent(tag, nodenames)
        if parent_tag:
            acting_parent_tag = utils.component_acting_parent_tag(parent_tag, tag)
            if acting_parent_tag:
                details = tag_details(acting_parent_tag, nodenames)
                utils.copy_attribute(details, "type", media_item, "parent_type")
                utils.copy_attribute(details, "ordinal", media_item, "parent_ordinal")
                utils.copy_attribute(details, "asset", media_item, "parent_asset")
                utils.copy_attribute(
                    details, "sibling_ordinal", media_item, "parent_sibling_ordinal"
                )
                utils.copy_attribute(
                    details, "component_doi", media_item, "parent_component_doi"
                )

            # Try to get the parent parent
            p_parent_tag = utils.first_parent(parent_tag, nodenames)
            if p_parent_tag:
                acting_p_parent_tag = utils.component_acting_parent_tag(
                    p_parent_tag, parent_tag
                )
                if acting_p_parent_tag:
                    details = tag_details(acting_p_parent_tag, nodenames)
                    utils.copy_attribute(details, "type", media_item, "p_parent_type")
                    utils.copy_attribute(
                        details, "ordinal", media_item, "p_parent_ordinal"
                    )
                    utils.copy_attribute(details, "asset", media_item, "p_parent_asset")
                    utils.copy_attribute(
                        details,
                        "sibling_ordinal",
                        media_item,
                        "p_parent_sibling_ordinal",
                    )
                    utils.copy_attribute(
                        details, "component_doi", media_item, "p_parent_component_doi"
                    )

                # Try to get the parent parent parent
                p_p_parent_tag = utils.first_parent(p_parent_tag, nodenames)
                if p_p_parent_tag:
                    acting_p_p_parent_tag = utils.component_acting_parent_tag(
                        p_p_parent_tag, p_parent_tag
                    )
                    if acting_p_p_parent_tag:
                        details = tag_details(acting_p_p_parent_tag, nodenames)
                        utils.copy_attribute(
                            details, "type", media_item, "p_p_parent_type"
                        )
                        utils.copy_attribute(
                            details, "ordinal", media_item, "p_p_parent_ordinal"
                        )
                        utils.copy_attribute(
                            details, "asset", media_item, "p_p_parent_asset"
                        )
                        utils.copy_attribute(
                            details,
                            "sibling_ordinal",
                            media_item,
                            "p_p_parent_sibling_ordinal",
                        )
                        utils.copy_attribute(
                            details,
                            "component_doi",
                            media_item,
                            "p_p_parent_component_doi",
                        )

        # Increment the position
        media_item["position"] = position
        # Ordinal should be the same as position in this case but set it anyway
        media_item["ordinal"] = utils.tag_ordinal(tag)

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

        utils.copy_attribute(tag.attrs, "xlink:href", graphic_item, "xlink_href")

        # Get the tag type
        nodenames = ["sub-article", "fig-group", "fig", "app"]
        details = tag_details(tag, nodenames)
        utils.copy_attribute(details, "type", graphic_item)

        parent_tag = utils.first_parent(tag, nodenames)
        if parent_tag:
            details = tag_details(parent_tag, nodenames)
            utils.copy_attribute(details, "type", graphic_item, "parent_type")
            utils.copy_attribute(details, "ordinal", graphic_item, "parent_ordinal")
            utils.copy_attribute(details, "asset", graphic_item, "parent_asset")
            utils.copy_attribute(
                details, "sibling_ordinal", graphic_item, "parent_sibling_ordinal"
            )
            utils.copy_attribute(
                details, "component_doi", graphic_item, "parent_component_doi"
            )

            # Try to get the parent parent - special for looking at fig tags
            #  use component_acting_parent_tag
            p_parent_tag = utils.first_parent(parent_tag, nodenames)
            if p_parent_tag:
                acting_p_parent_tag = utils.component_acting_parent_tag(
                    p_parent_tag, parent_tag
                )
                if acting_p_parent_tag:
                    details = tag_details(acting_p_parent_tag, nodenames)
                    utils.copy_attribute(details, "type", graphic_item, "p_parent_type")
                    utils.copy_attribute(
                        details, "ordinal", graphic_item, "p_parent_ordinal"
                    )
                    utils.copy_attribute(
                        details, "asset", graphic_item, "p_parent_asset"
                    )
                    utils.copy_attribute(
                        details,
                        "sibling_ordinal",
                        graphic_item,
                        "p_parent_sibling_ordinal",
                    )
                    utils.copy_attribute(
                        details, "component_doi", graphic_item, "p_parent_component_doi"
                    )

        # Increment the position
        graphic_item["position"] = position
        # Ordinal should be the same as position in this case but set it anyway
        graphic_item["ordinal"] = utils.tag_ordinal(tag)

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

        utils.copy_attribute(tag.attrs, "xlink:href", item, "xlink_href")

        # Get the tag type
        nodenames = ["sub-article"]
        details = tag_details(tag, nodenames)
        utils.copy_attribute(details, "type", item)

        # Increment the position
        item["position"] = position
        # Ordinal should be the same as position in this case but set it anyway
        item["ordinal"] = utils.tag_ordinal(tag)

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

        utils.copy_attribute(tag.attrs, "xlink:href", item, "xlink_href")
        utils.copy_attribute(tag.attrs, "content-type", item)

        # Get the tag type
        nodenames = ["sub-article"]
        details = tag_details(tag, nodenames)
        utils.copy_attribute(details, "type", item)

        # Increment the position
        item["position"] = position
        # Ordinal should be the same as position in this case but set it anyway
        item["ordinal"] = utils.tag_ordinal(tag)

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

        utils.copy_attribute(tag.attrs, "id", item)

        # Get the tag type
        nodenames = ["supplementary-material"]
        details = tag_details(tag, nodenames)
        utils.copy_attribute(details, "type", item)
        utils.copy_attribute(details, "asset", item)
        utils.copy_attribute(details, "component_doi", item)
        utils.copy_attribute(details, "sibling_ordinal", item)

        if raw_parser.label(tag):
            item["label"] = utils.node_text(raw_parser.label(tag))
            item["full_label"] = utils.node_contents_str(raw_parser.label(tag))

        # Increment the position
        item["position"] = position
        # Ordinal should be the same as position in this case but set it anyway
        item["ordinal"] = utils.tag_ordinal(tag)

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
    email = []
    for email_tag in utils.extract_nodes(contrib_tag, "email"):
        if email_tag.parent.name != "aff":
            email.append(email_tag.text)
    return email if len(email) > 0 else None


def contrib_phone(contrib_tag):
    """
    Given a contrib tag, look for an phone tag
    """
    phone = None
    if raw_parser.phone(contrib_tag):
        phone = utils.first(raw_parser.phone(contrib_tag)).text
    return phone


def contrib_inline_aff(contrib_tag):
    """
    Given a contrib tag, look for an aff tag directly inside it
    """
    aff_tags = []
    for child_tag in contrib_tag:
        if child_tag and child_tag.name and child_tag.name == "aff":
            aff_tags.append(child_tag)
    return aff_tags


def contrib_xref(contrib_tag, ref_type):
    """
    Given a contrib tag, look for an xref tag of type ref_type directly inside the contrib tag
    """
    aff_tags = []
    for child_tag in contrib_tag:
        if (
            child_tag
            and child_tag.name
            and child_tag.name == "xref"
            and child_tag.get("ref-type")
            and child_tag.get("ref-type") == ref_type
        ):
            aff_tags.append(child_tag)
    return aff_tags


def format_contrib_refs(contrib_tag, soup):
    contrib_refs = {}
    ref_tags = utils.extract_nodes(contrib_tag, "xref")
    ref_type_aff_count = 0
    for ref_tag in ref_tags:
        if "ref-type" in ref_tag.attrs and "rid" in ref_tag.attrs:
            ref_type = ref_tag["ref-type"]
            rid = ref_tag["rid"]

            if ref_type == "aff":
                ref_type_aff_count += 1
                add_to_list_dictionary(contrib_refs, "affiliation", rid)
            if ref_type == "corresp":
                # Check for email or phone type
                corresp_tag = utils.firstnn(soup.find_all(id=rid))
                if contrib_phone(corresp_tag):
                    add_to_list_dictionary(contrib_refs, "phone", rid)
                elif contrib_email(corresp_tag):
                    add_to_list_dictionary(contrib_refs, "email", rid)
            if ref_type == "fn":
                if rid.startswith("equal-contrib"):
                    add_to_list_dictionary(contrib_refs, "equal-contrib", rid)
                elif rid.startswith("conf"):
                    add_to_list_dictionary(contrib_refs, "competing-interest", rid)
                elif rid.startswith("con"):  # not conf though, see above!
                    add_to_list_dictionary(contrib_refs, "contribution", rid)
                elif rid.startswith("pa"):
                    add_to_list_dictionary(contrib_refs, "present-address", rid)
                elif rid.startswith("fn"):
                    add_to_list_dictionary(contrib_refs, "foot-note", rid)
            elif ref_type == "other":
                if rid.startswith("par-") or rid.startswith("fund"):
                    add_to_list_dictionary(contrib_refs, "funding", rid)
                elif rid.startswith("dataro") or rid.startswith("dataset"):
                    add_to_list_dictionary(contrib_refs, "related-object", rid)
    return contrib_refs, ref_type_aff_count


def format_contributor(
    contrib_tag,
    soup,
    detail="brief",
    contrib_type=None,
    group_author_key=None,
    target_tags_corresp=None,
    target_tags_fn=None,
    target_tags_aff=None,
):
    contributor = {}
    utils.copy_attribute(contrib_tag.attrs, "contrib-type", contributor, "type")
    # Set contrib type if passed via params
    if not contributor.get("type") and contrib_type:
        contributor["type"] = contrib_type
    utils.copy_attribute(contrib_tag.attrs, "equal-contrib", contributor)
    utils.copy_attribute(contrib_tag.attrs, "corresp", contributor)
    utils.copy_attribute(contrib_tag.attrs, "deceased", contributor)
    utils.copy_attribute(contrib_tag.attrs, "id", contributor)
    contrib_id_tag = utils.first(raw_parser.contrib_id(contrib_tag))
    if contrib_id_tag and "contrib-id-type" in contrib_id_tag.attrs:
        if contrib_id_tag["contrib-id-type"] == "group-author-key":
            contributor["group-author-key"] = utils.node_contents_str(contrib_id_tag)
    # Set group-author-key if passed via params
    if not contributor.get("group-author-key") and group_author_key:
        contributor["group-author-key"] = group_author_key
    if raw_parser.collab(contrib_tag):
        collab_tag = utils.first(raw_parser.collab(contrib_tag))
        if collab_tag:
            # Clean up if there are tags inside the collab tag
            tag_copy = copy.copy(collab_tag)
            tag_copy = utils.remove_tag_from_tag(tag_copy, "contrib-group")
            contributor["collab"] = utils.node_contents_str(tag_copy).rstrip()

    # Check if it is not a group author
    if not is_author_group_author(contrib_tag):
        if contrib_id_tag and "contrib-id-type" in contrib_id_tag.attrs:
            if contrib_id_tag["contrib-id-type"] == "orcid":
                contributor["orcid"] = utils.node_contents_str(contrib_id_tag)
        utils.set_if_value(
            contributor, "role", utils.first_node_str_contents(contrib_tag, "role")
        )
        if raw_parser.bio(contrib_tag):
            biography_content = body_block_content_render(
                utils.firstnn(raw_parser.bio(contrib_tag))
            )
            if len(biography_content) > 0:
                contributor["bio"] = biography_content[0].get("content")
        utils.set_if_value(contributor, "email", contrib_email(contrib_tag))
        utils.set_if_value(contributor, "phone", contrib_phone(contrib_tag))
        utils.set_if_value(
            contributor,
            "surname",
            utils.first_node_str_contents(contrib_tag, "surname"),
        )
        utils.set_if_value(
            contributor,
            "given-names",
            utils.first_node_str_contents(contrib_tag, "given-names"),
        )
        utils.set_if_value(
            contributor, "suffix", utils.first_node_str_contents(contrib_tag, "suffix")
        )
        utils.set_if_value(
            contributor,
            "collab",
            utils.first_node_str_contents(contrib_tag, "collab"),
        )
        # Get the sub-group value from the parent role tag if it is inside a group
        if (
            contrib_tag.parent
            and contrib_tag.parent.parent
            and contrib_tag.parent.parent.parent
            and is_author_group_author(contrib_tag.parent.parent.parent)
        ):
            utils.set_if_value(
                contributor,
                "sub-group",
                utils.first_node_str_contents(contrib_tag.parent, "role"),
            )
    elif contributor.get("corresp") and not contributor.get("email"):
        # For corresponding group authors, look for an email address anywhere in the group
        utils.set_if_value(contributor, "email", contrib_email(contrib_tag))

    # on-behalf-of
    if contrib_tag.name == "on-behalf-of":
        contributor["type"] = "on-behalf-of"
        contributor["on-behalf-of"] = utils.node_contents_str(contrib_tag)

    contrib_refs, ref_type_aff_count = format_contrib_refs(contrib_tag, soup)
    if len(contrib_refs) > 0:
        contributor["references"] = contrib_refs

    if detail == "brief" or ref_type_aff_count == 0:
        # Brief format only allows one aff and it must be within the contrib tag
        aff_tag = utils.firstnn(contrib_inline_aff(contrib_tag))
        if aff_tag:
            contributor["affiliations"] = []
            contrib_affs = {}
            (none_return, aff_detail) = format_aff(aff_tag)
            if aff_detail:
                aff_attributes = [
                    "dept",
                    "institution",
                    "country",
                    "city",
                    "email",
                    "ror",
                    "text",
                ]
                for aff_attribute in aff_attributes:
                    if (
                        aff_attribute in aff_detail
                        and aff_detail[aff_attribute] is not None
                    ):
                        utils.copy_attribute(aff_detail, aff_attribute, contrib_affs)
                if len(contrib_affs) > 0:
                    contributor["affiliations"].append(contrib_affs)

    if detail == "full":
        # person_id
        if "id" in contributor:
            if contributor["id"].startswith("author"):
                person_id = contributor["id"].replace("author-", "")
                contributor["person_id"] = int(person_id) if person_id else None
        # Author - given names + surname
        author_name = ""
        if "given-names" in contributor:
            author_name += contributor["given-names"] + " "
        if "surname" in contributor:
            author_name += contributor["surname"]
        if author_name != "":
            contributor["author"] = author_name

        aff_tags = contrib_xref(contrib_tag, "aff")
        if len(aff_tags) <= 0:
            aff_tags = contrib_inline_aff(contrib_tag)
        if aff_tags:
            contributor["affiliations"] = []
        for aff_tag in aff_tags:
            contrib_affs = {}
            rid = aff_tag.get("rid")
            if rid:
                # Look for the matching aff tag by rid
                if target_tags_aff:
                    # look in the list of aff_nodes supplied as an argument
                    aff_node = utils.first(
                        [
                            aff_tag
                            for aff_tag in target_tags_aff
                            if aff_tag.get("id") == rid
                        ]
                    )
                else:
                    # search for aff nodes
                    aff_node = utils.first(
                        utils.extract_nodes(soup, "aff", attr="id", value=rid)
                    )
            else:
                # Aff tag inside contrib tag
                aff_node = aff_tag

            (none_return, aff_detail) = format_aff(aff_node)

            if aff_detail:
                aff_attributes = [
                    "dept",
                    "institution",
                    "country",
                    "city",
                    "email",
                    "ror",
                    "text",
                ]
                for aff_attribute in aff_attributes:
                    if (
                        aff_attribute in aff_detail
                        and aff_detail[aff_attribute] is not None
                    ):
                        utils.copy_attribute(aff_detail, aff_attribute, contrib_affs)
                contributor["affiliations"].append(contrib_affs)

        # Add xref linked correspondence author notes if applicable
        corresp_tags = contrib_xref(contrib_tag, "corresp")
        if len(corresp_tags) > 0:
            if "notes-corresp" not in contributor:
                contributor["notes-corresp"] = []
            if not target_tags_corresp:
                target_tags_corresp = raw_parser.corresp(soup)
            for cor in corresp_tags:
                # Find the matching tag
                rid = cor["rid"]
                corresp_node = utils.first(
                    list(filter(lambda tag: tag.get("id") == rid, target_tags_corresp))
                )
                author_notes = utils.node_text(corresp_node)
                if author_notes:
                    contributor["notes-corresp"].append(author_notes)
        # Add xref linked footnotes if applicable
        fn_tags = contrib_xref(contrib_tag, "fn")
        if len(fn_tags) > 0:
            if "notes-fn" not in contributor:
                contributor["notes-fn"] = []
            if not target_tags_fn:
                target_tags_fn = raw_parser.fn(soup)
            for fn_tag in fn_tags:
                # Find the matching tag
                rid = fn_tag["rid"]
                fn_node = utils.first(
                    list(filter(lambda tag: tag.get("id") == rid, target_tags_fn))
                )
                fn_text = utils.node_text(fn_node)
                if fn_text:
                    contributor["notes-fn"].append(fn_text)

    return contributor


def contributors(soup, detail="brief"):
    contrib_tags = raw_parser.article_contributors(soup)
    contributors = format_authors(soup, contrib_tags, detail)
    return contributors


def all_contributors(soup, detail="brief"):
    "find all contributors not contrained to only the ones in article meta"
    contrib_tags = raw_parser.contributors(soup)
    contributors = format_authors(soup, contrib_tags, detail)
    return contributors


#
# HERE BE DRAGONS
#


def is_author_non_byline(tag, contrib_type="author non-byline"):
    if tag and tag.get("contrib-type") and tag.get("contrib-type") == contrib_type:
        return True
    if tag and tag.parent and tag.parent.parent and tag.parent.parent.name == "collab":
        return True
    return False


def authors_non_byline(soup, detail="full"):
    """Non-byline authors for group author members"""
    # Get a filtered list of contributors, in order to get their group-author-id
    contrib_type = "author non-byline"
    contributors_ = contributors(soup, detail)
    non_byline_authors = [
        author for author in contributors_ if author.get("type", None) == contrib_type
    ]

    # Then renumber their position attribute
    position = 1
    for author in non_byline_authors:
        author["position"] = position
        position = position + 1
    return non_byline_authors


def authors(soup, contrib_type="author", detail="full"):
    contrib_tags = raw_parser.authors(raw_parser.article_meta(soup), contrib_type)
    tags = list(filter(lambda tag: is_author_non_byline(tag) is False, contrib_tags))
    return format_authors(soup, tags, detail)


def is_author_group_author(tag):
    if tag:
        for child_tag in tag:
            # look at the child tags for a collab tag
            # and that its parent tag is not a collab tag
            if (
                child_tag.name == "collab"
                and utils.first_parent(tag, ["collab", "article-meta", "front-stub"])
                and utils.first_parent(
                    tag, ["collab", "article-meta", "front-stub"]
                ).name != "collab"
            ):
                return True
    return False


def format_authors(soup, contrib_tags, detail="full", contrib_type=None):
    authors = []
    position = 1

    article_doi = doi(soup)

    group_author_id = 0
    prev_group_author_id = 0

    # Pre-parse some values to pass to optimise this procedure
    target_tags_corresp = raw_parser.corresp(soup)
    target_tags_fn = raw_parser.fn(soup)
    target_tags_aff = raw_parser.affiliation(soup)
    for tag in contrib_tags:

        # Set the group author key if missing
        if is_author_group_author(tag):
            group_author_id = group_author_id + 1
            group_author_key = "group-author-id" + str(group_author_id)
        else:
            group_author_key = None

        # Set the contrib_type and group author key for non-byline authors
        if is_author_non_byline(tag) is True and contrib_type is None:
            author_contrib_type = "author non-byline"
            group_author_key = "group-author-id" + str(prev_group_author_id)
        elif (
            is_author_non_byline(tag) is False
            and is_author_group_author(tag) is not True
        ):
            author_contrib_type = contrib_type
            group_author_key = None
        else:
            author_contrib_type = contrib_type

        author = format_contributor(
            tag,
            soup,
            detail,
            author_contrib_type,
            group_author_key,
            target_tags_corresp,
            target_tags_fn,
            target_tags_aff,
        )

        # If not empty, add position value, append, then increment the position counter
        if len(author) > 0:
            if detail == "full":
                author["article_doi"] = article_doi
                author["position"] = position

            authors.append(author)
            position += 1

        prev_group_author_id = group_author_id

    return authors


def format_aff(aff_tag):
    if not aff_tag:
        return None, {}
    values = {
        "dept": utils.node_contents_str(
            utils.first(
                utils.extract_nodes(aff_tag, "institution", "content-type", "dept")
            )
        ),
        "institution": utils.node_contents_str(
            utils.first(
                list(
                    filter(
                        lambda n: "content-type" not in n.attrs,
                        utils.extract_nodes(aff_tag, "institution"),
                    )
                )
            )
        ),
        "city": utils.node_contents_str(
            utils.first(
                utils.extract_nodes(aff_tag, "named-content", "content-type", "city")
            )
        ),
        "country": utils.node_contents_str(
            utils.first(utils.extract_nodes(aff_tag, "country"))
        ),
        "email": utils.node_contents_str(
            utils.first(utils.extract_nodes(aff_tag, "email"))
        ),
        "ror": utils.node_contents_str(
            utils.first(
                utils.extract_nodes(
                    aff_tag, "institution-id", "institution-id-type", "ror"
                )
            )
        ),
    }
    # Remove keys with None value
    values = utils.prune_dict_of_none_values(values)
    # If all values are none then extract as text
    if not values:
        # extract the text ignoring the label tag
        aff_tag = utils.remove_tag_from_tag(aff_tag, "label")
        values = {"text": utils.node_text(aff_tag).strip()}

    if "id" in aff_tag.attrs:
        return aff_tag["id"], values

    return None, values


def full_affiliation(soup):
    aff_tags = raw_parser.affiliation(soup)
    aff_tags = list(filter(lambda aff: "id" in aff.attrs, aff_tags))
    affs = []
    for tag in aff_tags:
        aff = {}
        (aff_id, aff_details) = format_aff(tag)
        aff[aff_id] = aff_details
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

        ref["ref"] = ref_text(tag)

        # ref_id
        utils.copy_attribute(tag.attrs, "id", ref)

        # article_title
        if raw_parser.article_title(tag):
            ref["article_title"] = utils.node_text(raw_parser.article_title(tag))
            ref["full_article_title"] = utils.node_contents_str(
                raw_parser.article_title(tag)
            )

        if raw_parser.pub_id(tag, "pmid"):
            ref["pmid"] = utils.node_contents_str(
                utils.first(raw_parser.pub_id(tag, "pmid"))
            )

        if raw_parser.pub_id(tag, "isbn"):
            ref["isbn"] = utils.node_contents_str(
                utils.first(raw_parser.pub_id(tag, "isbn"))
            )

        if raw_parser.pub_id(tag, "doi"):
            ref["reference_id"] = utils.node_contents_str(
                utils.first(raw_parser.pub_id(tag, "doi"))
            )
            ref["doi"] = utils.doi_uri_to_doi(
                utils.node_contents_str(utils.first(raw_parser.pub_id(tag, "doi")))
            )

        uri_tag = None
        if raw_parser.ext_link(tag, "uri"):
            uri_tag = utils.first(raw_parser.ext_link(tag, "uri"))
        elif raw_parser.uri(tag):
            uri_tag = utils.first(raw_parser.uri(tag))
        if uri_tag:
            utils.set_if_value(ref, "uri", uri_tag.get("xlink:href"))
            utils.set_if_value(ref, "uri_text", utils.node_contents_str(uri_tag))
        # look for a pub-id tag if no uri yet
        if not ref.get("uri"):
            for pub_id_type in ["archive", "accession"]:
                if raw_parser.pub_id(tag, pub_id_type):
                    pub_id_tag = utils.first(
                        raw_parser.pub_id(tag, pub_id_type=pub_id_type)
                    )
                    utils.set_if_value(ref, "uri", pub_id_tag.get("xlink:href"))
                if ref.get("uri"):
                    break

        # accession, could be in either of two tags
        utils.set_if_value(
            ref,
            "accession",
            utils.node_contents_str(
                utils.first(raw_parser.object_id(tag, "art-access-id"))
            ),
        )
        if not ref.get("accession"):
            utils.set_if_value(
                ref,
                "accession",
                utils.node_contents_str(
                    utils.first(raw_parser.pub_id(tag, pub_id_type="accession"))
                ),
            )
        if not ref.get("accession"):
            utils.set_if_value(
                ref,
                "accession",
                utils.node_contents_str(
                    utils.first(raw_parser.pub_id(tag, pub_id_type="archive"))
                ),
            )

        if raw_parser.year(tag):
            utils.set_if_value(ref, "year", utils.node_text(raw_parser.year(tag)))
            utils.set_if_value(
                ref, "year-iso-8601-date", raw_parser.year(tag).get("iso-8601-date")
            )

        if raw_parser.date_in_citation(tag):
            utils.set_if_value(
                ref,
                "date-in-citation",
                utils.node_text(utils.first(raw_parser.date_in_citation(tag))),
            )
            utils.set_if_value(
                ref,
                "iso-8601-date",
                utils.first(raw_parser.date_in_citation(tag)).get("iso-8601-date"),
            )

        if raw_parser.patent(tag):
            utils.set_if_value(
                ref, "patent", utils.node_text(utils.first(raw_parser.patent(tag)))
            )
            utils.set_if_value(
                ref, "country", utils.first(raw_parser.patent(tag)).get("country")
            )

        utils.set_if_value(
            ref, "source", utils.node_text(utils.first(raw_parser.source(tag)))
        )
        utils.set_if_value(
            ref,
            "elocation-id",
            utils.node_text(utils.first(raw_parser.elocation_id(tag))),
        )
        if raw_parser.element_citation(tag):
            utils.copy_attribute(
                utils.first(raw_parser.element_citation(tag)).attrs,
                "publication-type",
                ref,
            )
        if "publication-type" not in ref and raw_parser.mixed_citations(tag):
            utils.copy_attribute(
                utils.first(raw_parser.mixed_citations(tag)).attrs,
                "publication-type",
                ref,
            )

        # authors
        person_group = raw_parser.person_group(tag)
        authors = []

        for group in person_group:

            author_type = None
            if "person-group-type" in group.attrs:
                author_type = group["person-group-type"]

            # Read name or collab tag in the order they are listed
            for name_or_collab_tag in utils.extract_nodes(
                group, ["name", "string-name", "collab"]
            ):
                author = {}

                # Shared tag attribute
                utils.set_if_value(author, "group-type", author_type)

                # name tag attributes
                if name_or_collab_tag.name in ["name", "string-name"]:
                    utils.set_if_value(
                        author,
                        "surname",
                        utils.node_text(
                            utils.first(raw_parser.surname(name_or_collab_tag))
                        ),
                    )
                    utils.set_if_value(
                        author,
                        "given-names",
                        utils.node_text(
                            utils.first(raw_parser.given_names(name_or_collab_tag))
                        ),
                    )
                    utils.set_if_value(
                        author,
                        "suffix",
                        utils.node_text(
                            utils.first(raw_parser.suffix(name_or_collab_tag))
                        ),
                    )

                # collab tag attribute
                if name_or_collab_tag.name == "collab":
                    utils.set_if_value(
                        author, "collab", utils.node_contents_str(name_or_collab_tag)
                    )

                if len(author) > 0:
                    authors.append(author)

            # etal for the person group
            if utils.first(raw_parser.etal(group)):
                author = {}
                author["etal"] = True
                utils.set_if_value(author, "group-type", author_type)
                authors.append(author)

        # Check for collab tag not wrapped in a person-group for backwards compatibility
        if len(person_group) == 0:
            collab_tags = raw_parser.collab(tag)
            for collab_tag in collab_tags:
                author = {}
                utils.set_if_value(author, "group-type", "author")
                utils.set_if_value(
                    author, "collab", utils.node_contents_str(collab_tag)
                )

                if len(author) > 0:
                    authors.append(author)

        if len(authors) > 0:
            ref["authors"] = authors

        utils.set_if_value(
            ref, "volume", utils.node_text(utils.first(raw_parser.volume(tag)))
        )
        utils.set_if_value(
            ref, "issue", utils.node_text(utils.first(raw_parser.issue(tag)))
        )
        utils.set_if_value(
            ref, "fpage", utils.node_text(utils.first(raw_parser.fpage(tag)))
        )
        utils.set_if_value(
            ref, "lpage", utils.node_text(utils.first(raw_parser.lpage(tag)))
        )
        utils.set_if_value(
            ref, "collab", utils.node_text(utils.first(raw_parser.collab(tag)))
        )
        utils.set_if_value(
            ref,
            "publisher_loc",
            utils.node_text(utils.first(raw_parser.publisher_loc(tag))),
        )
        utils.set_if_value(
            ref,
            "publisher_name",
            utils.node_text(utils.first(raw_parser.publisher_name(tag))),
        )
        utils.set_if_value(
            ref,
            "edition",
            utils.node_contents_str(utils.first(raw_parser.edition(tag))),
        )
        utils.set_if_value(
            ref,
            "version",
            utils.node_contents_str(utils.first(raw_parser.version(tag))),
        )
        utils.set_if_value(
            ref,
            "chapter-title",
            utils.node_contents_str(utils.first(raw_parser.chapter_title(tag))),
        )
        utils.set_if_value(
            ref, "comment", utils.node_text(utils.first(raw_parser.comment(tag)))
        )
        utils.set_if_value(
            ref,
            "data-title",
            utils.node_contents_str(utils.first(raw_parser.data_title(tag))),
        )
        utils.set_if_value(
            ref, "conf-name", utils.node_text(utils.first(raw_parser.conf_name(tag)))
        )

        # If not empty, add position value, append, then increment the position counter
        if len(ref) > 0:
            ref["article_doi"] = article_doi

            ref["position"] = position

            refs.append(ref)
            position += 1

    return refs


def extract_component_doi(tag, nodenames):
    """
    Used to get component DOI from a tag and confirm it is actually for that tag
    and it is not for one of its children in the list of nodenames
    """
    component_doi = None

    if tag.name == "sub-article":
        component_doi = utils.doi_uri_to_doi(
            utils.node_text(utils.first(raw_parser.article_id(tag, pub_id_type="doi")))
        )
    else:
        object_id_tag = utils.first(raw_parser.object_id(tag, pub_id_type="doi"))
        # Tweak: if it is media and has no object_id_tag then it is not a "component"
        if tag.name == "media" and not object_id_tag:
            component_doi = None
        else:
            # Check the object id is for this tag and not one of its children
            #   This happens for example when boxed text has a child figure,
            #   the boxed text does not have a DOI, the figure does have one
            if (
                object_id_tag
                and utils.first_parent(object_id_tag, nodenames).name == tag.name
            ):
                component_doi = utils.doi_uri_to_doi(utils.node_text(object_id_tag))

    return component_doi


def components(soup):
    """
    Find the components, i.e. those parts that would be assigned
    a unique component DOI, such as figures, tables, etc.
    - position is in what order the tag appears in the entire set of nodes
    - ordinal is in what order it is for all the tags of its own type
    """
    components = []

    nodenames = [
        "abstract",
        "fig",
        "table-wrap",
        "media",
        "chem-struct-wrap",
        "sub-article",
        "supplementary-material",
        "boxed-text",
        "app",
    ]

    # Count node order overall
    position = 1

    position_by_type = {}
    for nodename in nodenames:
        position_by_type[nodename] = 1

    article_doi = doi(soup)

    # Find all tags for all component_types, allows the order
    #  in which they are found to be preserved
    component_tags = utils.extract_nodes(soup, nodenames)

    for tag in component_tags:

        component = OrderedDict()

        # Component type is the tag's name
        ctype = tag.name

        # First find the doi if present
        component_doi = extract_component_doi(tag, nodenames)
        if component_doi is None:
            continue

        component["doi"] = utils.doi_uri_to_doi(component_doi)
        component["doi_url"] = utils.doi_to_doi_uri(component["doi"])

        utils.copy_attribute(tag.attrs, "id", component)

        if ctype == "sub-article":
            title_tag = raw_parser.article_title(tag)
        elif ctype == "boxed-text":
            title_tag = title_tag_inspected(tag, tag.name, direct_sibling_only=True)
            if not title_tag:
                title_tag = title_tag_inspected(tag, "caption", "boxed-text")
            # New kitchen sink has boxed-text inside app tags, tag the sec tag title if so
            #  but do not take it if there is a caption
            if (
                not title_tag
                and tag.parent
                and tag.parent.name in ["sec", "app"]
                and not caption_tag_inspected(tag, tag.name)
            ):
                title_tag = title_tag_inspected(
                    tag.parent, tag.parent.name, direct_sibling_only=True
                )
        else:
            title_tag = raw_parser.title(tag)

        if title_tag:
            component["title"] = utils.node_text(title_tag)
            component["full_title"] = utils.node_contents_str(title_tag)

        if ctype == "boxed-text":
            label_tag = label_tag_inspected(tag, "boxed-text")
        else:
            label_tag = raw_parser.label(tag)

        if label_tag:
            component["label"] = utils.node_text(label_tag)
            component["full_label"] = utils.node_contents_str(label_tag)

        if raw_parser.caption(tag):
            first_paragraph = utils.first(utils.paragraphs(raw_parser.caption(tag)))
            # fix a problem with the new kitchen sink of caption within caption tag
            if first_paragraph:
                nested_caption = raw_parser.caption(first_paragraph)
                if nested_caption:
                    nested_paragraphs = utils.paragraphs(nested_caption)
                    first_paragraph = utils.first(nested_paragraphs) or first_paragraph
            if first_paragraph and not utils.starts_with_doi(first_paragraph):
                # Remove the supplementary tag from the paragraph if present
                if raw_parser.supplementary_material(first_paragraph):
                    first_paragraph = utils.remove_tag_from_tag(
                        first_paragraph, "supplementary-material"
                    )
                if utils.node_text(first_paragraph).strip():
                    component["caption"] = utils.node_text(first_paragraph)
                    component["full_caption"] = utils.node_contents_str(first_paragraph)

        if raw_parser.permissions(tag):

            component["permissions"] = []
            for permissions_tag in raw_parser.permissions(tag):
                permissions_item = {}
                if raw_parser.copyright_statement(permissions_tag):
                    permissions_item["copyright_statement"] = utils.node_text(
                        raw_parser.copyright_statement(permissions_tag)
                    )

                if raw_parser.copyright_year(permissions_tag):
                    permissions_item["copyright_year"] = utils.node_text(
                        raw_parser.copyright_year(permissions_tag)
                    )

                if raw_parser.copyright_holder(permissions_tag):
                    permissions_item["copyright_holder"] = utils.node_text(
                        raw_parser.copyright_holder(permissions_tag)
                    )

                if raw_parser.licence_p(permissions_tag):
                    permissions_item["license"] = utils.node_text(
                        utils.first(raw_parser.licence_p(permissions_tag))
                    )
                    permissions_item["full_license"] = utils.node_contents_str(
                        utils.first(raw_parser.licence_p(permissions_tag))
                    )

                component["permissions"].append(permissions_item)

        if raw_parser.contributors(tag):
            component["contributors"] = []
            for contributor_tag in raw_parser.contributors(tag):
                component["contributors"].append(
                    format_contributor(contributor_tag, soup)
                )

        # There are only some parent tags we care about for components
        #  and only check two levels of parentage
        parent_nodenames = [
            "sub-article",
            "fig-group",
            "fig",
            "boxed-text",
            "table-wrap",
            "app",
            "media",
        ]
        parent_tag = utils.first_parent(tag, parent_nodenames)

        if parent_tag:

            # For fig-group we actually want the first fig of the fig-group as the parent
            acting_parent_tag = utils.component_acting_parent_tag(parent_tag, tag)

            # Only counts if the acting parent tag has a DOI
            if (
                acting_parent_tag
                and extract_component_doi(acting_parent_tag, parent_nodenames)
                is not None
            ):

                component["parent_type"] = acting_parent_tag.name
                component["parent_ordinal"] = utils.tag_ordinal(acting_parent_tag)
                component["parent_sibling_ordinal"] = tag_details_sibling_ordinal(
                    acting_parent_tag
                )
                component["parent_asset"] = tag_details_asset(acting_parent_tag)

            # Look for parent parent, if available
            parent_parent_tag = utils.first_parent(parent_tag, parent_nodenames)

            if parent_parent_tag:

                acting_parent_tag = utils.component_acting_parent_tag(
                    parent_parent_tag, parent_tag
                )

                if (
                    acting_parent_tag
                    and extract_component_doi(acting_parent_tag, parent_nodenames)
                    is not None
                ):
                    component["parent_parent_type"] = acting_parent_tag.name
                    component["parent_parent_ordinal"] = utils.tag_ordinal(
                        acting_parent_tag
                    )
                    component[
                        "parent_parent_sibling_ordinal"
                    ] = tag_details_sibling_ordinal(acting_parent_tag)
                    component["parent_parent_asset"] = tag_details_asset(
                        acting_parent_tag
                    )

        content = ""
        for p_tag in utils.extract_nodes(tag, "p"):
            if content != "":
                # Add a space before each new paragraph for now
                content = content + " "
            content = content + utils.node_text(p_tag)

        if content != "":
            component["content"] = content

        # mime type
        media_tag = None
        if ctype == "media":
            media_tag = tag
        elif ctype == "supplementary-material":
            media_tag = utils.first(raw_parser.media(tag))
        if media_tag:
            component["mimetype"] = media_tag.get("mimetype")
            component["mime-subtype"] = media_tag.get("mime-subtype")

        if len(component) > 0:
            component["article_doi"] = article_doi
            component["type"] = ctype
            component["position"] = position

            # Ordinal is based on all tags of the same type even if they have no DOI
            component["ordinal"] = utils.tag_ordinal(tag)
            component["sibling_ordinal"] = tag_details_sibling_ordinal(tag)
            component["asset"] = tag_details_asset(tag)
            # component['ordinal'] = position_by_type[ctype]

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
            # check for required id attribute
            if "id" not in tag.attrs:
                continue
            if tag["id"] not in cor:
                cor[tag["id"]] = []
            if raw_parser.email(tag):
                # Multiple email addresses possible
                for email_tag in raw_parser.email(tag):
                    cor[tag["id"]].append(utils.node_contents_str(email_tag))
            elif raw_parser.phone(tag):
                # Look for a phone number
                cor[tag["id"]].append(
                    utils.node_contents_str(utils.first(raw_parser.phone(tag)))
                )

    return cor


@utils.nullify
def author_notes(soup):
    """
    Find the fn tags included in author-notes
    """
    author_notes = []

    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = raw_parser.fn(author_notes_section)
        for tag in fn_nodes:
            if "fn-type" in tag.attrs:
                if tag["fn-type"] != "present-address":
                    author_notes.append(utils.node_text(tag))

    return author_notes


@utils.nullify
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


@utils.nullify
def competing_interests(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    competing_interests_section = utils.extract_nodes(
        soup, "fn-group", attr="content-type", value="competing-interest"
    )
    if not competing_interests_section:
        return None
    fn_nodes = utils.extract_nodes(utils.first(competing_interests_section), "fn")
    interests = footnotes(fn_nodes, fntype_filter)

    return interests


@utils.nullify
def present_addresses(soup):
    notes = []
    fntype_filter = "present-address"
    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = utils.extract_nodes(author_notes_section, "fn")
        notes = footnotes(fn_nodes, fntype_filter)
    return notes


@utils.nullify
def other_foot_notes(soup):
    notes = []
    fntype_filter = ["fn", "other"]
    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = utils.extract_nodes(author_notes_section, "fn")
        notes = footnotes(fn_nodes, fntype_filter)
    return notes


@utils.nullify
def author_contributions(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    author_contributions_section = utils.extract_nodes(
        soup, "fn-group", attr="content-type", value="author-contribution"
    )
    if not author_contributions_section:
        return None
    fn_nodes = utils.extract_nodes(utils.first(author_contributions_section), "fn")
    cons = footnotes(fn_nodes, fntype_filter)

    return cons


def footnotes(fn_nodes, fntype_filter):
    notes = []
    for fn_node in fn_nodes:
        try:
            if fntype_filter is None or fn_node["fn-type"] in fntype_filter:
                notes.append(
                    {
                        "id": fn_node["id"],
                        "text": utils.clean_whitespace(
                            utils.node_contents_str(fn_node)
                        ),
                        "fn-type": fn_node["fn-type"],
                    }
                )
        except KeyError:
            # TODO log
            pass
    return notes


@utils.nullify
def full_award_groups(soup):
    """
    Find the award-group items and return a list of details
    """
    award_groups = []

    funding_group_section = utils.extract_nodes(soup, "funding-group")
    # counter for auto generated id values, if required
    generated_id_counter = 1
    for funding_group in funding_group_section:

        award_group_tags = utils.extract_nodes(funding_group, "award-group")

        for award_group_tag in award_group_tags:
            if "id" in award_group_tag.attrs:
                ref = award_group_tag["id"]
            else:
                # hack: generate and increment an id value none is available
                ref = "award-group-{id}".format(id=generated_id_counter)
                generated_id_counter += 1

            award_group = {}
            award_group_id = award_group_award_id(award_group_tag)
            if award_group_id is not None:
                award_group["award-id"] = utils.first(award_group_id)
            funding_sources = full_award_group_funding_source(award_group_tag)
            source = utils.first(funding_sources)
            if source is not None:
                utils.copy_attribute(source, "institution", award_group)
                utils.copy_attribute(source, "institution-id", award_group, "id")
                utils.copy_attribute(
                    source,
                    "institution-id-type",
                    award_group,
                    destination_key="id-type",
                )
            award_group_by_ref = {}
            award_group_by_ref[ref] = award_group
            award_groups.append(award_group_by_ref)

    return award_groups


@utils.nullify
def award_groups(soup):
    """
    Find the award-group items and return a list of details
    """
    award_groups = []

    funding_group_section = utils.extract_nodes(soup, "funding-group")
    for funding_group in funding_group_section:

        award_group_tags = utils.extract_nodes(funding_group, "award-group")

        for award_group_tag in award_group_tags:

            award_group = {}

            award_group["funding_source"] = award_group_funding_source(award_group_tag)
            award_group["recipient"] = award_group_principal_award_recipient(
                award_group_tag
            )
            award_group["award_id"] = award_group_award_id(award_group_tag)

            award_groups.append(award_group)

    return award_groups


@utils.nullify
def award_group_funding_source(tag):
    """
    Given a funding group element
    Find the award group funding sources, one for each
    item found in the get_funding_group section
    """
    award_group_funding_source = []
    funding_source_tags = utils.extract_nodes(tag, "funding-source")
    for funding_source_tag in funding_source_tags:
        award_group_funding_source.append(funding_source_tag.text)
    return award_group_funding_source


@utils.nullify
def full_award_group_funding_source(tag):
    """
    Given a funding group element
    Find the award group funding sources, one for each
    item found in the get_funding_group section
    """
    award_group_funding_sources = []
    funding_source_nodes = utils.extract_nodes(tag, "funding-source")
    for funding_source_node in funding_source_nodes:

        award_group_funding_source = {}

        institution_nodes = utils.extract_nodes(funding_source_node, "institution")

        institution_node = utils.first(institution_nodes)
        if institution_node:
            award_group_funding_source["institution"] = utils.node_text(
                institution_node
            )
            if "content-type" in institution_node.attrs:
                award_group_funding_source["institution-type"] = institution_node[
                    "content-type"
                ]

        institution_id_nodes = utils.extract_nodes(
            funding_source_node, "institution-id"
        )
        institution_id_node = utils.first(institution_id_nodes)
        if institution_id_node:
            award_group_funding_source["institution-id"] = utils.node_text(
                institution_id_node
            )
            if "institution-id-type" in institution_id_node.attrs:
                award_group_funding_source["institution-id-type"] = institution_id_node[
                    "institution-id-type"
                ]

        award_group_funding_sources.append(award_group_funding_source)

    return award_group_funding_sources


@utils.nullify
def award_group_award_id(tag):
    """
    Find the award group award id, one for each
    item found in the get_funding_group section
    """
    award_group_award_id = []
    award_id_tags = utils.extract_nodes(tag, "award-id")
    for award_id_tag in award_id_tags:
        award_group_award_id.append(award_id_tag.text)
    return award_group_award_id


@utils.nullify
def award_group_principal_award_recipient(tag):
    """
    Find the award group principal award recipient, one for each
    item found in the get_funding_group section
    """
    award_group_principal_award_recipient = []
    principal_award_recipients = utils.extract_nodes(tag, "principal-award-recipient")

    for recipient_tag in principal_award_recipients:
        principal_award_recipient_text = ""

        institution = utils.node_text(
            utils.first(utils.extract_nodes(recipient_tag, "institution"))
        )
        surname = utils.node_text(
            utils.first(utils.extract_nodes(recipient_tag, "surname"))
        )
        given_names = utils.node_text(
            utils.first(utils.extract_nodes(recipient_tag, "given-names"))
        )
        string_name = utils.node_text(
            utils.first(raw_parser.string_name(recipient_tag))
        )
        # Concatenate name and institution values if found
        #  while filtering out excess whitespace
        if given_names:
            principal_award_recipient_text += given_names
        if principal_award_recipient_text != "":
            principal_award_recipient_text += " "
        if surname:
            principal_award_recipient_text += surname
        if institution:
            principal_award_recipient_text += institution
        if string_name:
            principal_award_recipient_text += string_name

        award_group_principal_award_recipient.append(principal_award_recipient_text)
    return award_group_principal_award_recipient


def object_id_doi(tag, parent_tag_name=None):
    """DOI in an object-id tag found inside the tag"""
    doi = None
    object_id = None
    object_ids = raw_parser.object_id(tag, "doi")
    if object_ids:
        object_id = utils.first(object_ids)
    if parent_tag_name and object_id and object_id.parent.name != parent_tag_name:
        object_id = None
    if object_id:
        doi = utils.node_contents_str(object_id)
    return doi


def title_tag_inspected(
    tag, parent_tag_name=None, p_parent_tag_name=None, direct_sibling_only=False
):
    """Extract the title tag and sometimes inspect its parents"""

    title_tag = None
    if direct_sibling_only is True:
        for sibling_tag in tag:
            if sibling_tag.name and sibling_tag.name == "title":
                title_tag = sibling_tag
    else:
        title_tag = raw_parser.title(tag)

    if parent_tag_name and p_parent_tag_name:
        if (
            title_tag
            and title_tag.parent.name
            and title_tag.parent.parent.name
            and title_tag.parent.name == parent_tag_name
            and title_tag.parent.parent.name == p_parent_tag_name
        ):
            pass
        else:
            title_tag = None

    return title_tag


def title_text(
    tag, parent_tag_name=None, p_parent_tag_name=None, direct_sibling_only=False
):
    """Extract the text of a title tag and sometimes inspect its parents"""
    title = None

    title_tag = title_tag_inspected(
        tag, parent_tag_name, p_parent_tag_name, direct_sibling_only
    )

    if title_tag:
        title = utils.node_contents_str(title_tag)
    return title


def caption_tag_inspected(tag, parent_tag_name=None):
    caption_tag = raw_parser.caption(tag)
    if parent_tag_name and caption_tag and caption_tag.parent.name != parent_tag_name:
        caption_tag = None
    return caption_tag


def label_tag_inspected(tag, parent_tag_name=None):
    label_tag = raw_parser.label(tag)
    if parent_tag_name and label_tag and label_tag.parent.name != parent_tag_name:
        label_tag = None
    return label_tag


def label(tag, parent_tag_name=None):
    label = None
    label_tag = label_tag_inspected(tag, parent_tag_name)
    if label_tag:
        label = utils.node_contents_str(label_tag)
    return label


def full_title_json(soup):
    return xml_to_html(True, full_title(soup))


def impact_statement_json(soup):
    return xml_to_html(True, impact_statement(soup))


def acknowledgements_json(soup):
    if raw_parser.acknowledgements(soup):
        return body_block_content_render(raw_parser.acknowledgements(soup))[0].get(
            "content"
        )

    return None


def keywords_json(soup, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    return list(map(convert, full_keywords(soup)))


def research_organism_json(soup, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    do_not_include = ["none", "other"]
    research_organisms = list(
        filter(
            lambda term: term and term.lower() not in do_not_include,
            full_research_organism(soup),
        )
    )
    return list(map(convert, research_organisms))


def boxed_text_to_image_block(tag):
    "covert boxed-text to an image block containing an inline-graphic"
    tag_block = OrderedDict()
    image_content = body_block_image_content(
        utils.first(raw_parser.inline_graphic(tag))
    )
    tag_block["type"] = "image"
    utils.set_if_value(
        tag_block, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
    )
    utils.set_if_value(tag_block, "id", tag.get("id"))
    utils.set_if_value(tag_block, "image", image_content)
    # render paragraphs into a caption
    p_tags = raw_parser.paragraph(tag)
    caption_content = []
    for p_tag in p_tags:
        if not raw_parser.inline_graphic(p_tag):
            caption_content.append(body_block_content(p_tag))
    utils.set_if_value(tag_block, "caption", caption_content)
    return tag_block


def body(soup, remove_key_info_box=False, base_url=None):

    body_content = []

    raw_body = raw_parser.article_body(soup)

    if raw_body:

        body_content = render_raw_body(
            raw_body, remove_key_info_box=remove_key_info_box, base_url=base_url
        )
    return body_content


def body_json(soup, base_url=None):
    """Get body json and then alter it with section wrapping and removing boxed-text"""
    body_content = body(soup, remove_key_info_box=True, base_url=base_url)
    # Wrap in a section if the first block is not a section
    if (
        body_content
        and len(body_content) > 0
        and "type" in body_content[0]
        and body_content[0]["type"] != "section"
    ):
        # Wrap this one
        new_body_section = OrderedDict()
        new_body_section["type"] = "section"
        new_body_section["id"] = "s0"
        new_body_section["title"] = "Main text"
        new_body_section["content"] = []
        for body_block in body_content:
            new_body_section["content"].append(body_block)
        new_body = []
        new_body.append(new_body_section)
        body_content = new_body
    body_content_rewritten = elifetools.json_rewrite.rewrite_json(
        "body_json", soup, body_content
    )
    return body_content_rewritten


def render_raw_body(tag, remove_key_info_box=False, base_url=None):
    body_content = []
    body_tags = body_blocks(tag)
    for body_tag in body_tags:
        if body_tag.name == "boxed-text":
            # Extract the text of the first child tag for comparison, if present
            first_node_text = None
            if body_tag.children:
                first_node_text = utils.node_text(utils.first(list(body_tag.children)))

            if (
                remove_key_info_box is True
                and first_node_text
                and "related" in first_node_text.lower()
            ):
                # Skip this tag
                continue

            if raw_parser.inline_graphic(body_tag):
                # edge case where inline-graphic is in the first boxed-text
                tag_block = boxed_text_to_image_block(body_tag)
                body_content.append(tag_block)

            elif not raw_parser.title(body_tag) and not raw_parser.label(body_tag):
                # Collapse boxed-text here if it has no title or label
                for boxed_tag in body_tag:
                    tag_blocks = body_block_content_render(boxed_tag, base_url=base_url)
                    for tag_block in tag_blocks:
                        if tag_block != {}:
                            body_content.append(tag_block)
            else:
                # Add it
                tag_blocks = body_block_content_render(body_tag, base_url=base_url)
                for tag_block in tag_blocks:
                    if tag_block != {}:
                        body_content.append(tag_block)
        else:

            tag_blocks = body_block_content_render(body_tag, base_url=base_url)
            # tag_content = body_block_content_render(tag)
            for tag_block in tag_blocks:
                if tag_block != {}:
                    body_content.append(tag_block)

    return body_content


def body_block_nodenames():
    return [
        "sec",
        "p",
        "table-wrap",
        "boxed-text",
        "disp-formula",
        "disp-quote",
        "fig",
        "fig-group",
        "list",
        "media",
        "code",
    ]


def body_block_content_render(tag, recursive=False, base_url=None):
    """
    Render the tag as body content and call recursively if
    the tag has child tags
    """
    block_content_list = []
    tag_content = OrderedDict()

    if tag.name == "p":
        for block_content in body_block_paragraph_render(tag, base_url=base_url):
            if block_content != {}:
                block_content_list.append(block_content)
    else:
        tag_content = body_block_content(tag, base_url=base_url)

    nodenames = body_block_nodenames()

    tag_content_content = []

    # Collect the content of the tag but only for some tags
    if tag.name not in [
        "p",
        "fig",
        "table-wrap",
        "list",
        "media",
        "disp-quote",
        "code",
    ]:
        for child_tag in tag:
            if not hasattr(child_tag, "name"):
                continue

            if child_tag.name == "p":
                # Ignore paragraphs that start with DOI:
                if (
                    utils.node_text(child_tag)
                    and len(utils.remove_doi_paragraph([child_tag])) <= 0
                ):
                    continue
                for block_content in body_block_paragraph_render(
                    child_tag, base_url=base_url
                ):
                    if block_content != {}:
                        tag_content_content.append(block_content)

            elif child_tag.name == "fig" and tag.name == "fig-group":
                # Do not fig inside fig-group a second time
                pass
            elif child_tag.name == "media" and tag.name == "fig-group":
                # Do not include a media video inside fig-group a second time
                if child_tag.get("mimetype") == "video":
                    pass
            else:
                for block_content in body_block_content_render(
                    child_tag, recursive=True, base_url=base_url
                ):
                    if block_content != {}:
                        tag_content_content.append(block_content)

    if len(tag_content_content) > 0:
        if tag.name in nodenames or recursive is False:
            tag_content["content"] = []
            for block_content in tag_content_content:
                tag_content["content"].append(block_content)
            block_content_list.append(tag_content)
        else:
            # Not a block tag, e.g. a caption tag, let the content pass through
            block_content_list = tag_content_content
    else:
        block_content_list.append(tag_content)

    return block_content_list


def body_block_paragraph_render(p_tag, html_flag=True, base_url=None):
    """
    paragraphs may wrap some other body block content
    this is separated out so it can be called from more than one place
    """
    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string, base_url)

    block_content_list = []

    tag_content_content = []

    paragraph_content = ""
    for child_tag in p_tag:

        if child_tag.name is None or body_block_content(child_tag) == {}:
            paragraph_content = paragraph_content + str(child_tag)

        else:
            # Add previous paragraph content first
            if paragraph_content.strip() != "":
                tag_content_content.append(
                    body_block_paragraph_content(convert(paragraph_content))
                )
                paragraph_content = ""

        if child_tag.name is not None and body_block_content(child_tag) != {}:
            for block_content in body_block_content_render(
                child_tag, base_url=base_url
            ):
                if block_content != {}:
                    tag_content_content.append(block_content)
    # finish up
    if paragraph_content.strip() != "":
        tag_content_content.append(
            body_block_paragraph_content(convert(paragraph_content))
        )

    if len(tag_content_content) > 0:
        for block_content in tag_content_content:
            block_content_list.append(block_content)

    return block_content_list


def body_block_caption_render(caption_tags, base_url=None):
    """fig and media tag captions are similar so use this common function"""
    caption_content = []
    supplementary_material_tags = []

    for block_tag in utils.remove_doi_paragraph(caption_tags):
        # Note then skip p tags with supplementary-material inside
        if raw_parser.supplementary_material(block_tag):
            for supp_tag in raw_parser.supplementary_material(block_tag):
                supplementary_material_tags.append(supp_tag)
            continue

        for block_content in body_block_content_render(block_tag, base_url=base_url):

            if block_content != {}:
                caption_content.append(block_content)

    return caption_content, supplementary_material_tags


def body_block_supplementary_material_render(supp_tags, base_url=None):
    """fig and media tag caption may have supplementary material"""
    source_data = []
    for supp_tag in supp_tags:
        for block_content in body_block_content_render(supp_tag, base_url=base_url):
            if block_content != {}:
                if "content" in block_content:
                    del block_content["content"]
                source_data.append(block_content)
    return source_data


def body_block_paragraph_content(text):
    "for formatting of simple paragraphs of text only, and check if it is all whitespace"
    tag_content = OrderedDict()
    if text and text != "":
        tag_content["type"] = "paragraph"
        tag_content["text"] = utils.clean_whitespace(text)
    return tag_content


def body_block_image_content(tag):
    "format a graphic or inline-graphic into a body block json format"
    image_content = OrderedDict()
    if tag:
        utils.copy_attribute(tag.attrs, "xlink:href", image_content, "uri")
        if "uri" in image_content:
            # todo!! alt
            utils.set_if_value(image_content, "alt", "")
    return image_content


def body_block_title_label_caption(
    tag_content,
    title_value,
    label_value,
    caption_content,
    set_caption=True,
    prefer_title=False,
    prefer_label=False,
):
    """set the title, label and caption values in a consistent way

    set_caption: insert a "caption" field
    prefer_title: when only one value is available,
       set title rather than label. If False, set label rather than title
    """
    utils.set_if_value(tag_content, "label", utils.rstrip_punctuation(label_value))
    utils.set_if_value(tag_content, "title", title_value)
    if set_caption is True and caption_content and len(caption_content) > 0:
        tag_content["caption"] = caption_content
    if prefer_title:
        if "title" not in tag_content and label_value:
            utils.set_if_value(tag_content, "title", label_value)
            del tag_content["label"]
    if prefer_label:
        if "label" not in tag_content and title_value:
            utils.set_if_value(
                tag_content, "label", utils.rstrip_punctuation(title_value)
            )
            del tag_content["title"]


def body_block_attribution(tag):
    "extract the attribution content for figures, tables, videos"
    attributions = []
    if raw_parser.attrib(tag):
        for attrib_tag in raw_parser.attrib(tag):
            attributions.append(utils.node_contents_str(attrib_tag))
    if raw_parser.permissions(tag):
        # concatenate content from from the permissions tag
        for permissions_tag in raw_parser.permissions(tag):
            attrib_string = ""
            # add the copyright statement if found
            attrib_string = utils.join_sentences(
                attrib_string,
                utils.node_contents_str(
                    raw_parser.copyright_statement(permissions_tag)
                ),
                ".",
            )
            # add the license paragraphs
            if raw_parser.licence_p(permissions_tag):
                for licence_p_tag in raw_parser.licence_p(permissions_tag):
                    attrib_string = utils.join_sentences(
                        attrib_string, utils.node_contents_str(licence_p_tag), "."
                    )
            if attrib_string != "":
                attributions.append(attrib_string)
    return attributions


def body_block_content(tag, html_flag=True, base_url=None):
    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string, base_url)

    tag_content = OrderedDict()

    if not hasattr(tag, "name"):
        return OrderedDict()

    if tag.name == "sec":
        tag_content["type"] = "section"
        utils.set_if_value(tag_content, "id", tag.get("id"))
        utils.set_if_value(
            tag_content, "title", convert(title_text(tag, direct_sibling_only=True))
        )

    elif tag.name == "boxed-text":
        tag_content["type"] = "box"
        utils.set_if_value(
            tag_content, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
        )
        utils.set_if_value(tag_content, "id", tag.get("id"))

        title_parent_tag = utils.first_parent(
            raw_parser.title(tag), ["boxed-text", "fig"]
        )
        if title_parent_tag and title_parent_tag.name == "boxed-text":
            title_value = convert(title_text(tag))
        else:
            title_value = None

        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(
                caption_tags, base_url=base_url
            )
        body_block_title_label_caption(
            tag_content,
            title_value,
            label_value,
            caption_content,
            set_caption=False,
            prefer_title=True,
        )

    elif tag.name == "p":
        tag_content["type"] = "paragraph"

        # Remove unwanted nested tags
        unwanted_tag_names = body_block_nodenames()
        tag = utils.remove_tag_from_tag(tag, unwanted_tag_names)

        if utils.node_contents_str(tag):
            tag_content["text"] = convert(
                utils.clean_whitespace(utils.node_contents_str(tag))
            )

    elif tag.name == "disp-quote":
        if tag.get("content-type") and tag.get("content-type") == "editor-comment":
            tag_content["type"] = "excerpt"
            block_array_name = "content"
            for child_tag in tag:
                if child_tag.name == "p":
                    for block_content in body_block_paragraph_render(
                        child_tag, base_url=base_url
                    ):
                        if block_content != {}:
                            if block_array_name not in tag_content:
                                tag_content[block_array_name] = []
                            tag_content[block_array_name].append(block_content)
                elif child_tag.name in ["code", "disp-formula", "list", "table-wrap"]:
                    block_content = body_block_content(child_tag, base_url=base_url)
                    if block_content != {}:
                        if block_array_name not in tag_content:
                            tag_content[block_array_name] = []
                        tag_content[block_array_name].append(block_content)
        else:
            tag_content["type"] = "quote"
            block_array_name = "text"
            for child_tag in tag:
                if child_tag.name == "p":
                    for block_content in body_block_paragraph_render(
                        child_tag, base_url=base_url
                    ):
                        if block_content != {}:
                            if block_array_name not in tag_content:
                                tag_content[block_array_name] = []
                            tag_content[block_array_name].append(block_content)

    elif tag.name == "table-wrap":
        # figure wrap
        tag_content["type"] = "figure"
        tag_content["assets"] = []
        asset_tag_content = OrderedDict()

        asset_tag_content["type"] = "table"
        utils.set_if_value(
            asset_tag_content, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
        )
        utils.set_if_value(asset_tag_content, "id", tag.get("id"))
        title_value = convert(title_text(tag, "caption", tag.name))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if caption_tag_inspected(tag, tag.name):
            caption_tags = body_blocks(caption_tag_inspected(tag, tag.name))
            caption_content, supplementary_material_tags = body_block_caption_render(
                caption_tags, base_url=base_url
            )

        body_block_title_label_caption(
            asset_tag_content,
            title_value,
            label_value,
            caption_content,
            set_caption=True,
        )

        tables = raw_parser.table(tag)
        asset_tag_content["tables"] = []
        for table in tables:
            # Add the table tag back for now
            table_content = "<table>" + utils.node_contents_str(table) + "</table>"
            asset_tag_content["tables"].append(convert(table_content))

        table_wrap_foot = raw_parser.table_wrap_foot(tag)
        for foot_tag in table_wrap_foot:
            for fn_tag in raw_parser.fn(foot_tag):
                footnote_content = OrderedDict()
                # Only set id if a label is present
                if label(fn_tag, fn_tag.name):
                    utils.set_if_value(footnote_content, "id", fn_tag.get("id"))
                    utils.set_if_value(
                        footnote_content,
                        "label",
                        utils.rstrip_punctuation(label(fn_tag, fn_tag.name)),
                    )
                for p_tag in raw_parser.paragraph(fn_tag):
                    if "text" not in footnote_content:
                        footnote_content["text"] = []
                    footnote_blocks = body_block_content_render(
                        p_tag, base_url=base_url
                    )
                    for footnote_block in footnote_blocks:
                        if footnote_block != {}:
                            footnote_content["text"].append(footnote_block)

                if "footnotes" not in asset_tag_content:
                    asset_tag_content["footnotes"] = []
                asset_tag_content["footnotes"].append(footnote_content)

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(
                supplementary_material_tags, base_url=base_url
            )
            if len(source_data) > 0:
                asset_tag_content["sourceData"] = source_data

        # add to figure assets if there is a label and it is not a keyresource table
        if asset_tag_content.get("label"):
            tag_content["assets"].append(asset_tag_content)
        else:
            # use the table asset alone
            tag_content = asset_tag_content

    elif tag.name == "disp-formula":
        tag_content["type"] = "mathml"

        utils.set_if_value(tag_content, "id", tag.get("id"))
        utils.set_if_value(tag_content, "label", label(tag, tag.name))

        math_tag = utils.first(raw_parser.math(tag))
        # Add the math tag back for now
        math_content = "<math>" + utils.node_contents_str(math_tag) + "</math>"
        tag_content["mathml"] = convert(math_content)

    elif tag.name == "fig":
        # figure wrap
        tag_content["type"] = "figure"
        tag_content["assets"] = []
        asset_tag_content = OrderedDict()

        asset_tag_content["type"] = "image"
        utils.set_if_value(
            asset_tag_content, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
        )
        utils.set_if_value(asset_tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag, "caption", "fig"))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(
                caption_tags, base_url=base_url
            )
        body_block_title_label_caption(
            asset_tag_content,
            title_value,
            label_value,
            caption_content,
            set_caption=True,
        )

        if raw_parser.graphic(tag):
            graphic_tags = raw_parser.graphic(tag)
            image_content = body_block_image_content(utils.first(graphic_tags))
            if len(image_content) > 0:
                asset_tag_content["image"] = image_content

        # license or attribution
        attributions = body_block_attribution(tag)
        if attributions:
            asset_tag_content["image"]["attribution"] = []
            for attrib_string in attributions:
                asset_tag_content["image"]["attribution"].append(convert(attrib_string))

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(
                supplementary_material_tags, base_url=base_url
            )
            if len(source_data) > 0:
                asset_tag_content["sourceData"] = source_data

        # add to figure assets if there is a label otherwise use the asset alone
        if asset_tag_content.get("label"):
            tag_content["assets"].append(asset_tag_content)
        else:
            tag_content = asset_tag_content

    elif tag.name == "media":
        # For video media only
        if tag.get("mimetype") != "video":
            return OrderedDict()

        # figure wrap
        tag_content["type"] = "figure"
        tag_content["assets"] = []
        asset_tag_content = OrderedDict()

        asset_tag_content["type"] = "video"
        utils.set_if_value(
            asset_tag_content, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
        )
        utils.set_if_value(asset_tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag, "caption", tag.name))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(
                caption_tags, base_url=base_url
            )
        body_block_title_label_caption(
            asset_tag_content,
            title_value,
            label_value,
            caption_content,
            set_caption=True,
        )

        # license or attribution
        attributions = body_block_attribution(tag)
        if attributions:
            asset_tag_content["attribution"] = []
            for attrib_string in attributions:
                asset_tag_content["attribution"].append(convert(attrib_string))

        utils.set_if_value(asset_tag_content, "uri", tag.get("xlink:href"))
        if "uri" in asset_tag_content and asset_tag_content["uri"].endswith(".gif"):
            asset_tag_content["autoplay"] = True
            asset_tag_content["loop"] = True

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(
                supplementary_material_tags, base_url=base_url
            )
            if len(source_data) > 0:
                asset_tag_content["sourceData"] = source_data

        # add the asset
        tag_content["assets"].append(asset_tag_content)

    elif tag.name == "fig-group":
        for fig_tag in utils.extract_nodes(tag, ["fig", "media"]):
            # Skip any media tags that are not videos
            if fig_tag.name == "media" and fig_tag.get("mimetype") != "video":
                continue
            fig_tag_content = body_block_content(fig_tag, base_url=base_url)
            if len(tag_content) <= 0:
                tag_content = fig_tag_content
            else:
                asset = fig_tag_content["assets"][0]
                # Only add if there is an id, should filter out unwanted supplementary file data
                if "id" in asset:
                    tag_content["assets"].append(asset)

    elif tag.name == "supplementary-material":
        utils.set_if_value(
            tag_content, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
        )
        utils.set_if_value(tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag, "caption", tag.name))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(
                caption_tags, base_url=base_url
            )
        body_block_title_label_caption(
            tag_content,
            title_value,
            label_value,
            caption_content,
            set_caption=True,
            prefer_label=True,
        )

        if raw_parser.media(tag):
            media_tag = utils.first(raw_parser.media(tag))
            # If a mimetype contains a slash just use it, otherwise concatenate a value
            if media_tag.get("mimetype") and "/" in media_tag.get("mimetype"):
                tag_content["mediaType"] = media_tag.get("mimetype")
            elif media_tag.get("mimetype") and media_tag.get("mime-subtype"):
                tag_content["mediaType"] = (
                    media_tag.get("mimetype") + "/" + media_tag.get("mime-subtype")
                )

            utils.copy_attribute(media_tag.attrs, "xlink:href", tag_content, "uri")
            utils.copy_attribute(media_tag.attrs, "xlink:href", tag_content, "filename")

    elif tag.name == "list":
        tag_content["type"] = "list"
        tag_content["prefix"] = utils.list_type_prefix(tag.get("list-type"))

        for list_item_tag in raw_parser.list_item(tag):
            # Do not add list items of child lists to the main list by skipping them here first
            if list_item_tag.parent != tag:
                continue

            if "items" not in tag_content:
                tag_content["items"] = []

            if len(body_block_content_render(list_item_tag)) > 0:
                for list_item in body_block_content_render(
                    list_item_tag, base_url=base_url
                ):
                    # Note: wrapped inside another list to pass the current article json schema
                    if list_item != {}:
                        list_item_content = list_item["content"]
                        tag_content["items"].append(list_item_content)
                    else:
                        tag_content["items"].append(
                            utils.node_contents_str(list_item_tag)
                        )

    elif tag.name == "app":
        utils.set_if_value(tag_content, "id", tag.get("id"))
        utils.set_if_value(
            tag_content, "doi", utils.doi_uri_to_doi(object_id_doi(tag, tag.name))
        )
        utils.set_if_value(
            tag_content, "title", convert(title_text(tag, direct_sibling_only=True))
        )

    elif tag.name == "code":
        tag_content["type"] = "code"
        utils.set_if_value(tag_content, "code", utils.node_contents_str(tag))

    return tag_content


def body_blocks(soup):
    """
    Note: for some reason this works and few other attempted methods work
    Search for certain node types, find the first nodes siblings of the same type
    Add the first sibling and the other siblings to a list and return them
    """
    nodenames = body_block_nodenames()

    body_block_tags = []

    if not soup:
        return body_block_tags

    first_sibling_node = utils.firstnn(soup.find_all())

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
    article_id_tag = utils.first(raw_parser.article_id(tag, "doi"))
    if article_id_tag:
        doi = article_id_tag.text
    return doi


def editor_evaluation(soup):
    "parse the Editor's evaluation sub-article into JSON format matching the API schema format"
    sub_article_content = OrderedDict()
    sub_article = raw_parser.editor_evaluation(soup)

    if not sub_article:
        return sub_article_content

    utils.copy_attribute(sub_article.attrs, "id", sub_article_content)
    if sub_article_doi(sub_article):
        sub_article_content["doi"] = utils.doi_uri_to_doi(sub_article_doi(sub_article))

    # content
    raw_body = raw_parser.article_body(sub_article)
    if raw_body:
        sub_article_content["content"] = render_raw_body(raw_body)

    # scietyUri
    if raw_parser.related_object(sub_article):
        for related_object in raw_parser.related_object(sub_article):
            uri = related_object.get("xlink:href")
            if SCIETY_URI_DOMAIN in uri:
                utils.set_if_value(sub_article_content, "scietyUri", uri)
                break

    return sub_article_content


def decision_letter(soup):

    sub_article_content = OrderedDict()
    sub_article = raw_parser.decision_letter(soup)

    if sub_article:
        utils.copy_attribute(sub_article.attrs, "id", sub_article_content)
        if sub_article_doi(sub_article):
            sub_article_content["doi"] = utils.doi_uri_to_doi(
                sub_article_doi(sub_article)
            )
        raw_body = raw_parser.article_body(sub_article)
    else:
        raw_body = None

    # description
    if raw_body:
        # Description will be the first boxed-text tag
        if raw_parser.boxed_text(raw_body):
            sub_article_content["description"] = []
            boxed_text_description = utils.first(raw_parser.boxed_text(raw_body))
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
        body_content_rewritten = elifetools.json_rewrite.rewrite_json(
            "body_json", soup, body_content
        )
        if len(body_content_rewritten) > 0:
            sub_article_content["content"] = body_content_rewritten

    return elifetools.json_rewrite.rewrite_json(
        "decision_letter_json", soup, sub_article_content
    )


def author_response(soup):

    sub_article_content = OrderedDict()
    sub_article = raw_parser.author_response(soup)

    if sub_article:
        utils.copy_attribute(sub_article.attrs, "id", sub_article_content)
        if sub_article_doi(sub_article):
            sub_article_content["doi"] = utils.doi_uri_to_doi(
                sub_article_doi(sub_article)
            )
        raw_body = raw_parser.article_body(sub_article)
    else:
        raw_body = None

    # content
    if raw_body:
        body_content = render_raw_body(raw_body)
        body_content_rewritten = elifetools.json_rewrite.rewrite_json(
            "body_json", soup, body_content
        )
        if len(body_content_rewritten) > 0:
            sub_article_content["content"] = body_content_rewritten

    return sub_article_content


def render_abstract_json(abstract_tag):
    abstract_json = OrderedDict()
    utils.set_if_value(
        abstract_json, "doi", utils.doi_uri_to_doi(object_id_doi(abstract_tag))
    )
    for child_tag in utils.remove_doi_paragraph(body_blocks(abstract_tag)):
        if body_block_content(child_tag) != {}:
            if "content" not in abstract_json:
                abstract_json["content"] = []
            # supports p or sec tags by recursive rendering the tag then keep the first element
            abstract_json["content"].append(body_block_content_render(child_tag)[0])
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
    if not abstract_tags:
        abstract_tags = raw_parser.abstract(
            soup, abstract_type="plain-language-summary"
        )
    abstract_json = None
    for tag in abstract_tags:
        abstract_json = render_abstract_json(tag)
    return abstract_json


def author_affiliations(author, html_flag=True):
    """compile author affiliations for json output"""

    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    affilations = []

    if author.get("affiliations"):
        for affiliation in author.get("affiliations"):
            affiliation_json = OrderedDict()
            affiliation_json["name"] = []
            if affiliation.get("dept"):
                affiliation_json["name"].append(convert(affiliation.get("dept")))
            if (
                affiliation.get("institution")
                and affiliation.get("institution").strip() != ""
            ):
                affiliation_json["name"].append(convert(affiliation.get("institution")))
            # Remove if empty
            if affiliation_json["name"] == []:
                del affiliation_json["name"]

            if (
                (affiliation.get("city") and affiliation.get("city").strip() != "")
                or affiliation.get("country")
                and affiliation.get("country").strip() != ""
            ):
                affiliation_address = OrderedDict()
                affiliation_address["formatted"] = []
                affiliation_address["components"] = OrderedDict()
                if affiliation.get("city") and affiliation.get("city").strip() != "":
                    affiliation_address["formatted"].append(affiliation.get("city"))
                    affiliation_address["components"]["locality"] = []
                    affiliation_address["components"]["locality"].append(
                        affiliation.get("city")
                    )
                if (
                    affiliation.get("country")
                    and affiliation.get("country").strip() != ""
                ):
                    affiliation_address["formatted"].append(affiliation.get("country"))
                    affiliation_address["components"]["country"] = affiliation.get(
                        "country"
                    )
                # Add if not empty
                if affiliation_address != {}:
                    affiliation_json["address"] = affiliation_address

            # Add if not empty
            if affiliation_json != {}:
                affilations.append(affiliation_json)

    if affilations != []:
        return affilations

    return None


def author_phone_numbers(author, correspondence):
    phone_numbers = []
    if correspondence and "phone" in author.get("references", {}):
        for ref_id in author["references"]["phone"]:
            for corr_ref_id, data in correspondence.items():
                if ref_id == corr_ref_id:
                    for phone_number in data:
                        phone_numbers.append(phone_number)
    if phone_numbers != []:
        return phone_numbers

    return None


def phone_number_json(phone):
    if phone:
        phone = re.sub(r"[\(\) -]", "", phone)
    return phone


def author_phone_numbers_json(author, correspondence):
    phone_numbers = author_phone_numbers(author, correspondence)
    if phone_numbers:
        phone_numbers = list(map(phone_number_json, phone_numbers))
    return phone_numbers


def author_email_addresses(author, correspondence):
    email_addresses = []

    if correspondence and "email" in author.get("references", {}):
        for ref_id in author["references"]["email"]:
            for corr_ref_id, data in correspondence.items():
                if ref_id == corr_ref_id:
                    for email_address in data:
                        email_addresses.append(email_address)

    # Also look in affiliations for inline email tags
    if author.get("affiliations"):
        for affiliation in author.get("affiliations"):
            if "email" in affiliation and affiliation["email"] not in email_addresses:
                email_addresses.append(affiliation["email"])

    # Also look at the author attributes
    if author.get("email"):
        email_addresses = author["email"]

    if email_addresses != []:
        return email_addresses

    return None


def author_contribution(author, contributions):
    contribution_text = None

    if "contribution" in author.get("references", {}):
        for ref_id in author["references"]["contribution"]:
            if contributions:
                for contribution in contributions:
                    if contribution.get("text") and contribution.get("id") == ref_id:
                        contribution_text = (
                            contribution.get("text")
                            .replace("<p>", "")
                            .replace("</p>", "")
                        )

    return contribution_text


def author_competing_interests(author, competing_interests):
    competing_interests_text = None

    label_pattern = re.compile(r"<label>.*</label>")

    if "competing-interest" in author.get("references", {}):
        for ref_id in author["references"]["competing-interest"]:
            if competing_interests:
                for competing_interest in competing_interests:
                    if (
                        competing_interest.get("text")
                        and competing_interest.get("id") == ref_id
                    ):
                        competing_interests_text = (
                            competing_interest.get("text")
                            .replace("<p>", "")
                            .replace("</p>", "")
                        )
                        # Strip labels
                        competing_interests_text = label_pattern.sub(
                            "", competing_interests_text
                        )

    return competing_interests_text


def author_equal_contribution(author, equal_contributions_map):
    equal_contributions = []

    if "equal-contrib" in author.get("references", {}):
        for ref_id in author["references"]["equal-contrib"]:
            if ref_id in equal_contributions_map:
                equal_contributions.append(equal_contributions_map[ref_id])
    if equal_contributions != []:
        return equal_contributions

    return None


def author_present_address(author, present_address_data):
    postal_addresses = []
    if not present_address_data or not author.get("references"):
        return postal_addresses
    if "present-address" in author["references"]:
        for ref_id in author["references"]["present-address"]:
            for present_address in present_address_data:
                if present_address.get("text") and present_address.get("id") == ref_id:
                    # Clean up the text
                    text = re.sub("<label>.*</label>", "", present_address.get("text"))
                    text = text.replace("<p>", "").replace("</p>", "")
                    # Format as a JSON address
                    address = OrderedDict()
                    address["formatted"] = []
                    address["formatted"].append(text)
                    address["components"] = OrderedDict()
                    address["components"]["streetAddress"] = []
                    address["components"]["streetAddress"].append(text)
                    postal_addresses.append(address)
    if postal_addresses != []:
        return postal_addresses

    return None


def author_foot_notes(author, foot_notes_data):
    foot_notes = []
    if not foot_notes_data or not author.get("references"):
        return foot_notes
    if "foot-note" in author["references"]:
        for ref_id in author["references"]["foot-note"]:
            for foot_note in foot_notes_data:
                if foot_note.get("text") and foot_note.get("id") == ref_id:
                    # Clean up the text
                    text = re.sub("<label>.*</label>", "", foot_note.get("text"))
                    text = text.replace("<p>", "").replace("</p>", "")
                    # For authors json do not include footnotes regarding deceased
                    if "deceased" not in text.lower():
                        foot_notes.append(text)
    if foot_notes != []:
        return foot_notes

    return None


def author_json_details(
    author,
    author_json,
    contributions,
    correspondence,
    competing_interests,
    equal_contributions_map,
    present_address_data,
    foot_notes_data,
    html_flag=True,
):
    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    """add more author json"""
    if author_affiliations(author):
        author_json["affiliations"] = author_affiliations(author)

    # foot notes or additionalInformation
    if author_foot_notes(author, foot_notes_data):
        author_json["additionalInformation"] = author_foot_notes(
            author, foot_notes_data
        )

    # email
    if author_email_addresses(author, correspondence):
        author_json["emailAddresses"] = author_email_addresses(author, correspondence)

    # phone
    if author_phone_numbers(author, correspondence):
        author_json["phoneNumbers"] = author_phone_numbers_json(author, correspondence)

    # contributions
    if author_contribution(author, contributions):
        author_json["contribution"] = convert(
            author_contribution(author, contributions)
        )

    # competing interests
    if author_competing_interests(author, competing_interests):
        author_json["competingInterests"] = convert(
            author_competing_interests(author, competing_interests)
        )

    # equal-contributions
    if author_equal_contribution(author, equal_contributions_map):
        author_json["equalContributionGroups"] = author_equal_contribution(
            author, equal_contributions_map
        )

    # postalAddress
    if author_present_address(author, present_address_data):
        author_json["postalAddresses"] = author_present_address(
            author, present_address_data
        )

    return author_json


def author_person(
    author,
    contributions,
    correspondence,
    competing_interests,
    equal_contributions_map,
    present_address_data,
    foot_notes_data,
):
    author_json = OrderedDict()
    author_json["type"] = "person"
    author_name = OrderedDict()
    author_name["preferred"] = utils.author_preferred_name(
        author.get("surname"), author.get("given-names"), author.get("suffix")
    )
    author_name["index"] = utils.author_index_name(
        author.get("surname"), author.get("given-names"), author.get("suffix")
    )
    author_json["name"] = author_name
    if author.get("orcid"):
        author_json["orcid"] = utils.orcid_uri_to_orcid(author.get("orcid"))
    if author.get("deceased"):
        author_json["deceased"] = True
    if author.get("role"):
        author_json["role"] = xml_to_html(True, author.get("role"))
    if author.get("bio"):
        author_json["biography"] = author.get("bio")
    author_json = author_json_details(
        author,
        author_json,
        contributions,
        correspondence,
        competing_interests,
        equal_contributions_map,
        present_address_data,
        foot_notes_data,
    )

    return author_json


def author_group(
    author,
    contributions,
    correspondence,
    competing_interests,
    equal_contributions_map,
    present_address_data,
    foot_notes_data,
):
    author_json = OrderedDict()
    author_json["type"] = "group"
    author_json["name"] = author.get("collab")

    author_json = author_json_details(
        author,
        author_json,
        contributions,
        correspondence,
        competing_interests,
        equal_contributions_map,
        present_address_data,
        foot_notes_data,
    )

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
        if author.get("collab") and not author.get("type") == "author non-byline":
            collab_map[author.get("collab")] = author.get("group-author-key")
    return collab_map


def map_equal_contributions(contributors):
    """assign numeric values to each unique equal-contrib id"""
    equal_contribution_map = {}
    equal_contribution_keys = []
    for contributor in contributors:
        if contributor.get("references") and "equal-contrib" in contributor.get(
            "references"
        ):
            for key in contributor["references"]["equal-contrib"]:
                if key not in equal_contribution_keys:
                    equal_contribution_keys.append(key)
    # Do a basic sort
    equal_contribution_keys = sorted(equal_contribution_keys)
    # Assign keys based on sorted values
    for i, equal_contribution_key in enumerate(equal_contribution_keys):
        equal_contribution_map[equal_contribution_key] = i + 1
    return equal_contribution_map


def editors_json(soup):
    editors_json_data = []
    contributors_data = all_contributors(soup, "full")
    for contributor in contributors_data:
        editor_json = None
        if contributor["type"] in ["editor", "senior_editor", "reviewer"]:
            editor_json = author_person(contributor, None, None, None, None, None, None)
        if editor_json:
            editors_json_data.append(editor_json)
    editors_json_data_rewritten = elifetools.json_rewrite.rewrite_json(
        "editors_json", soup, editors_json_data
    )
    return editors_json_data_rewritten


def authors_json(soup):
    """authors list in article json format"""
    authors_json_data = []
    contributors_data = contributors(soup, "full")
    author_contributions_data = author_contributions(soup, None)
    author_competing_interests_data = competing_interests(soup, None)
    author_correspondence_data = full_correspondence(soup)
    equal_contributions_map = map_equal_contributions(contributors_data)
    present_address_data = present_addresses(soup)
    foot_notes_data = other_foot_notes(soup)

    # First line authors builds basic structure
    for contributor in contributors_data:
        author_json = None
        if contributor["type"] == "author" and contributor.get("collab"):
            author_json = author_group(
                contributor,
                author_contributions_data,
                author_correspondence_data,
                author_competing_interests_data,
                equal_contributions_map,
                present_address_data,
                foot_notes_data,
            )
        elif contributor.get("on-behalf-of"):
            author_json = author_on_behalf_of(contributor)
        elif contributor["type"] == "author" and not contributor.get(
            "group-author-key"
        ):
            author_json = author_person(
                contributor,
                author_contributions_data,
                author_correspondence_data,
                author_competing_interests_data,
                equal_contributions_map,
                present_address_data,
                foot_notes_data,
            )

        if author_json:
            authors_json_data.append(author_json)

    # Second, add byline author data
    collab_map = collab_to_group_author_key_map(contributors_data)
    for contributor in [
        elem for elem in contributors_data if elem.get("group-author-key")
    ]:
        # skip the collab if its name is the same as the group author key
        if contributor.get("group-author-key") == collab_map.get(
            contributor.get("collab")
        ):
            continue
        for group_author in [
            elem for elem in authors_json_data if elem.get("type") == "group"
        ]:
            group_author_key = None
            if group_author["name"] in collab_map:
                group_author_key = collab_map[group_author["name"]]
            if contributor.get("group-author-key") == group_author_key:
                if contributor.get("collab"):
                    author_json = author_group(
                        contributor,
                        author_contributions_data,
                        author_correspondence_data,
                        author_competing_interests_data,
                        equal_contributions_map,
                        present_address_data,
                        foot_notes_data,
                    )
                else:
                    author_json = author_person(
                        contributor,
                        author_contributions_data,
                        author_correspondence_data,
                        author_competing_interests_data,
                        equal_contributions_map,
                        present_address_data,
                        foot_notes_data,
                    )
                if contributor.get("sub-group"):
                    if "groups" not in group_author:
                        group_author["groups"] = OrderedDict()
                    if contributor.get("sub-group") not in group_author["groups"]:
                        group_author["groups"][contributor.get("sub-group")] = []
                    group_author["groups"][contributor.get("sub-group")].append(
                        author_json
                    )
                else:
                    if "people" not in group_author:
                        group_author["people"] = []
                    group_author["people"].append(author_json)

    authors_json_data_rewritten = elifetools.json_rewrite.rewrite_json(
        "authors_json", soup, authors_json_data
    )
    return authors_json_data_rewritten


def author_line(soup):
    """take preferred names from authors json and format them into an author line"""
    author_line = None
    authors_json_data = authors_json(soup)
    author_names = extract_author_line_names(authors_json_data)
    if len(author_names) > 0:
        author_line = format_author_line(author_names, style="ellipsis")
    return author_line


def extract_author_line_names(authors_json_data):
    author_names = []
    if not authors_json_data:
        return author_names
    for author in authors_json_data:
        if "name" in author and "preferred" in author["name"]:
            # person
            author_names.append(author["name"]["preferred"])
        elif "name" in author:
            # collab
            author_names.append(str(author["name"]))
    return author_names


def format_author_line(author_names, style="etal"):
    """authorLine format depends on if there is 1, 2 or more than 2 authors"""
    if style == "ellipsis":
        return format_author_line_ellipsis(author_names)
    # default
    return format_author_line_etal(author_names)


def format_author_line_etal(author_names, max_names=2):
    """
    author line ending in etal if there are many authors
    example: Firstname M Lastname et al.
    """
    author_line = None
    if not author_names:
        return author_line
    # ensure max_names is a minimum of 2
    if not max_names or not (isinstance(max_names, int)) or max_names < 2:
        max_names = 2
    if len(author_names) <= max_names:
        author_line = ", ".join(author_names)
    elif len(author_names) > max_names:
        author_line = author_names[0] + " et al."
    return author_line


def format_author_line_ellipsis(author_names, max_names=3):
    """
    author line with an ellipsis before the final author if there are many authors
    example for three authors, max_names=3: First, Second, Third
    example for four authors, max_names=3: First, Second ... Fourth
    """
    author_line = None
    if not author_names:
        return author_line
    # ensure max_names is a minimum of 3
    if not max_names or not (isinstance(max_names, int)) or max_names < 3:
        max_names = 3
    if len(author_names) <= max_names:
        author_line = ", ".join(author_names)
    elif len(author_names) > max_names:
        author_line = "%s ... %s" % (
            ", ".join(author_names[0 : max_names - 1]),
            author_names[-1],
        )
    return author_line


def references_publisher(publisher_name=None, publisher_loc=None):
    publisher = OrderedDict()
    if publisher_name:
        publisher["name"] = []
        publisher["name"].append(publisher_name)
    if publisher_loc:
        address = OrderedDict()
        address["formatted"] = []
        address["formatted"].append(publisher_loc)
        address["components"] = OrderedDict()
        address["components"]["locality"] = []
        address["components"]["locality"].append(publisher_loc)
        publisher["address"] = address
    if len(publisher) > 0:
        return publisher

    return None


def references_pages_range(fpage=None, lpage=None):
    page_range = None
    if fpage and lpage:
        # use chr(8211) for the hyphen because the schema is requiring it
        page_range = fpage.strip() + chr(8211) + lpage.strip()
    elif fpage:
        page_range = fpage.strip()
    elif lpage:
        page_range = lpage.strip()
    return page_range


def references_date(year=None):
    "Handle year value parsing for some edge cases"
    date = None
    discriminator = None
    in_press = None
    if year and "in press" in year.lower().strip():
        in_press = True
    elif year and re.match("^[0-9]+$", year):
        date = year
    elif year:
        discriminator_match = re.match("^([0-9]+?)([a-z]+?)$", year)
        if discriminator_match:
            date = discriminator_match.group(1)
            discriminator = discriminator_match.group(2)
        else:
            date = year
    return (date, discriminator, in_press)


def references_authors(ref_authors):
    all_authors = OrderedDict()
    if ref_authors:
        for ref_author in ref_authors:
            author_json = OrderedDict()
            etal_json = None
            # Switch for type of record
            if "etal" in ref_author:
                author_group_type = ref_author.get("group-type") + "s" + "EtAl"
                etal_json = True
            elif "collab" in ref_author:
                author_group_type = ref_author.get("group-type") + "s"
                author_json = references_author_collab(ref_author)
            else:
                author_group_type = ref_author.get("group-type") + "s"
                author_json = utils.references_author_person(ref_author)

            if author_group_type:
                if author_group_type not in all_authors:
                    if not etal_json:
                        all_authors[author_group_type] = []
                if etal_json:
                    all_authors[author_group_type] = etal_json
                else:
                    all_authors[author_group_type].append(author_json)

    return all_authors


def references_json_authors(ref_authors, ref_content):
    "build the authors for references json here for testability"
    all_authors = references_authors(ref_authors)
    if all_authors != {}:
        if ref_content.get("type") in [
            "conference-proceeding",
            "journal",
            "other",
            "periodical",
            "preprint",
            "report",
            "web",
        ]:
            for author_type in ["authors", "authorsEtAl"]:
                utils.set_if_value(
                    ref_content, author_type, all_authors.get(author_type)
                )
        elif ref_content.get("type") in ["book", "book-chapter"]:
            for author_type in ["authors", "authorsEtAl", "editors", "editorsEtAl"]:
                utils.set_if_value(
                    ref_content, author_type, all_authors.get(author_type)
                )
        elif ref_content.get("type") in ["clinical-trial"]:
            # Always set as authors, once,  then add the authorsType
            for author_type in ["authors", "collaborators", "sponsors"]:
                if "authorsType" not in ref_content and all_authors.get(author_type):
                    utils.set_if_value(
                        ref_content, "authors", all_authors.get(author_type)
                    )
                    utils.set_if_value(
                        ref_content,
                        "authorsEtAl",
                        all_authors.get(author_type + "EtAl"),
                    )
                    ref_content["authorsType"] = author_type
        elif ref_content.get("type") in ["data", "software"]:
            for author_type in [
                "authors",
                "authorsEtAl",
                "compilers",
                "compilersEtAl",
                "curators",
                "curatorsEtAl",
            ]:
                utils.set_if_value(
                    ref_content, author_type, all_authors.get(author_type)
                )
        elif ref_content.get("type") in ["patent"]:
            for author_type in [
                "inventors",
                "inventorsEtAl",
                "assignees",
                "assigneesEtAl",
            ]:
                utils.set_if_value(
                    ref_content, author_type, all_authors.get(author_type)
                )
        elif ref_content.get("type") in ["thesis"]:
            # Convert list to a non-list
            if all_authors.get("authors") and len(all_authors.get("authors")) > 0:
                ref_content["author"] = all_authors.get("authors")[0]
    return ref_content


def references_json(soup, html_flag=True):

    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    references_json = []
    for ref in refs(soup):
        ref_content = OrderedDict()

        # type
        if ref.get("publication-type") == "book" and (
            "chapter-title" in ref or "full_article_title" in ref
        ):
            utils.set_if_value(ref_content, "type", "book-chapter")
        elif ref.get("publication-type") == "confproc":
            utils.set_if_value(ref_content, "type", "conference-proceeding")
        elif ref.get("publication-type") == "clinicaltrial":
            utils.set_if_value(ref_content, "type", "clinical-trial")
        elif ref.get("publication-type") == "webpage":
            utils.set_if_value(ref_content, "type", "web")
        else:
            utils.set_if_value(ref_content, "type", ref.get("publication-type"))

        utils.set_if_value(ref_content, "id", ref.get("id"))

        (year_date, discriminator, year_in_press) = references_date(ref.get("year"))
        if not discriminator:
            utils.set_if_value(ref_content, "date", ref.get("year-iso-8601-date"))
        if "date" not in ref_content:
            utils.set_if_value(ref_content, "date", year_date)
            utils.set_if_value(ref_content, "discriminator", discriminator)

        # accessed
        if ref.get("publication-type") in ["web", "webpage"] and ref.get(
            "iso-8601-date"
        ):
            utils.set_if_value(ref_content, "accessed", ref.get("iso-8601-date"))
            # Set the date to the year tag value if accessed is set and there is a year
            utils.set_if_value(ref_content, "date", year_date)
            utils.set_if_value(ref_content, "discriminator", discriminator)

        # authors and etal
        if ref.get("authors"):
            ref_content = references_json_authors(ref.get("authors"), ref_content)

        # titles
        if ref.get("publication-type") in [
            "journal",
            "confproc",
            "preprint",
            "periodical",
        ]:
            utils.set_if_value(
                ref_content, "articleTitle", ref.get("full_article_title")
            )
        elif ref.get("publication-type") in ["thesis", "clinicaltrial", "other"]:
            utils.set_if_value(ref_content, "title", ref.get("full_article_title"))
        elif ref.get("publication-type") in ["book"]:
            utils.set_if_value(ref_content, "bookTitle", ref.get("source"))
            if "bookTitle" not in ref_content:
                utils.set_if_value(
                    ref_content, "bookTitle", ref.get("full_article_title")
                )
        elif ref.get("publication-type") in ["software", "data"]:
            utils.set_if_value(ref_content, "title", ref.get("data-title"))
            if "title" not in ref_content:
                utils.set_if_value(ref_content, "title", ref.get("source"))
        elif ref.get("publication-type") in ["patent", "web", "webpage"]:
            utils.set_if_value(ref_content, "title", ref.get("full_article_title"))
            if "title" not in ref_content:
                utils.set_if_value(ref_content, "title", ref.get("comment"))
            if "title" not in ref_content:
                utils.set_if_value(ref_content, "title", ref.get("uri"))
        # Finally try to extract from source if a title is not found
        if (
            "title" not in ref_content
            and "articleTitle" not in ref_content
            and "bookTitle" not in ref_content
        ):
            utils.set_if_value(ref_content, "title", ref.get("source"))

        # conference
        if ref.get("conf-name"):
            utils.set_if_value(
                ref_content,
                "conference",
                references_publisher(ref.get("conf-name"), None),
            )

        # source
        if ref.get("publication-type") == "journal":
            utils.set_if_value(ref_content, "journal", ref.get("source"))
        elif ref.get("publication-type") == "periodical":
            utils.set_if_value(ref_content, "periodical", ref.get("source"))
        elif ref.get("publication-type") in ["web", "webpage"]:
            utils.set_if_value(ref_content, "website", ref.get("source"))
        elif ref.get("publication-type") in ["patent"]:
            utils.set_if_value(ref_content, "patentType", ref.get("source"))
        elif ref.get("publication-type") not in ["book"]:
            utils.set_if_value(ref_content, "source", ref.get("source"))

        # patent details
        utils.set_if_value(ref_content, "number", ref.get("patent"))
        utils.set_if_value(ref_content, "country", ref.get("country"))

        # publisher
        if ref.get("publisher_name"):
            utils.set_if_value(
                ref_content,
                "publisher",
                references_publisher(
                    ref.get("publisher_name"), ref.get("publisher_loc")
                ),
            )
        elif ref.get("publication-type") in ["software"] and ref.get("source"):
            utils.set_if_value(
                ref_content,
                "publisher",
                references_publisher(ref.get("source"), ref.get("publisher_loc")),
            )

        # volume
        utils.set_if_value(ref_content, "volume", ref.get("volume"))

        # edition
        if ref.get("publication-type") in ["software"]:
            utils.set_if_value(ref_content, "version", ref.get("version"))
            if "version" not in ref_content:
                utils.set_if_value(ref_content, "version", ref.get("edition"))
        else:
            utils.set_if_value(ref_content, "edition", ref.get("edition"))

        # chapter-title
        utils.set_if_value(ref_content, "chapterTitle", ref.get("chapter-title"))
        if ref_content["type"] == "book-chapter" and "chapterTitle" not in ref_content:
            utils.set_if_value(
                ref_content, "chapterTitle", ref.get("full_article_title")
            )

        # pages
        if ref.get("elocation-id"):
            ref_content["pages"] = ref.get("elocation-id")
        elif ref.get("fpage") and not re.match(r"^[A-Za-z0-9\.]+$", ref.get("fpage")):
            # Use range as string value
            ref_content["pages"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage")
            )
        elif ref.get("lpage") and not re.match(r"^[A-Za-z0-9\.]+$", ref.get("lpage")):
            # Use range as string value
            ref_content["pages"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage")
            )
        elif ref.get("fpage") and not ref.get("lpage"):
            ref_content["pages"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage")
            )
        elif ref.get("fpage") and ref.get("lpage"):
            ref_content["pages"] = OrderedDict()
            ref_content["pages"]["first"] = ref.get("fpage").strip()
            if ref.get("lpage"):
                ref_content["pages"]["last"] = ref.get("lpage").strip()
            ref_content["pages"]["range"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage")
            )

        elif ref.get("comment"):
            if "in press" in ref.get("comment").lower().strip():
                ref_content["pages"] = "In press"
        elif year_in_press:
            # in press may have been taken from the year field
            ref_content["pages"] = "In press"

        # Special, to retain some comment tag values, convert to type other
        if ref.get("comment"):
            if ref_content.get("pages") and ref_content.get("pages") == "In press":
                # Do not convert
                pass
            else:
                ref_content["type"] = "other"

        # dataId
        if ref.get("publication-type") in ["data"]:
            utils.set_if_value(ref_content, "dataId", ref.get("accession"))

        # doi
        if ref.get("publication-type") not in ["web", "webpage"]:
            utils.set_if_value(ref_content, "doi", ref.get("doi"))

        # pmid
        utils.set_if_value(
            ref_content, "pmid", utils.coerce_to_int(ref.get("pmid"), None)
        )

        # isbn
        utils.set_if_value(ref_content, "isbn", ref.get("isbn"))

        # uri
        utils.set_if_value(ref_content, "uri", ref.get("uri"))
        # take the uri_text value if no uri yet
        if "uri" not in ref_content:
            utils.set_if_value(ref_content, "uri", ref.get("uri_text"))
        # next option is to set the uri from the doi value
        if "uri" not in ref_content and ref.get("publication-type") in [
            "confproc",
            "data",
            "preprint",
            "report",
            "software",
            "thesis",
            "web",
            "webpage",
        ]:
            if ref.get("doi"):
                # Convert doi to uri
                ref_content["uri"] = "https://doi.org/" + ref.get("doi")

        # Convert to HTML
        for index in ["title", "articleTitle", "chapterTitle", "bookTitle", "edition"]:
            utils.set_if_value(ref_content, index, convert(ref_content.get(index)))

        # Rewrite references data with support to delete a reference too
        ref_content_rewritten = elifetools.json_rewrite.rewrite_json(
            "references_json", soup, [ref_content]
        )
        if ref_content_rewritten and len(ref_content_rewritten) > 0:
            ref_content = ref_content_rewritten[0]
        elif len(ref_content_rewritten) == 0:
            ref_content = None

        # Now can convert to type unknown if applicable
        if ref_content:
            ref_content = convert_references_json(ref_content, soup)
            references_json.append(ref_content)

    return references_json


def convert_references_json(ref_content, soup=None):
    "Check for references that will not pass schema validation, fix or convert them to unknown"

    # Convert reference to unkonwn if still missing important values
    if (
        (ref_content.get("type") == "other")
        or (ref_content.get("type") == "book-chapter" and "editors" not in ref_content)
        or (ref_content.get("type") == "journal" and "articleTitle" not in ref_content)
        or (ref_content.get("type") == "book-chapter" and "pages" not in ref_content)
        or (ref_content.get("type") == "journal" and "journal" not in ref_content)
        or (
            ref_content.get("type")
            in ["book", "book-chapter", "report", "thesis", "software"]
            and "publisher" not in ref_content
        )
        or (ref_content.get("type") == "book" and "bookTitle" not in ref_content)
        or (ref_content.get("type") == "data" and "source" not in ref_content)
        or (
            ref_content.get("type") == "conference-proceeding"
            and "conference" not in ref_content
        )
    ):
        ref_content = references_json_to_unknown(ref_content, soup)

    return ref_content


def references_json_to_unknown(ref_content, soup=None):
    unknown_ref_content = OrderedDict()
    unknown_ref_content["type"] = "unknown"
    utils.set_if_value(unknown_ref_content, "id", ref_content.get("id"))
    utils.set_if_value(unknown_ref_content, "date", ref_content.get("date"))
    utils.set_if_value(unknown_ref_content, "authors", ref_content.get("authors"))
    if not unknown_ref_content.get("authors") and ref_content.get("author"):
        unknown_ref_content["authors"] = []
        unknown_ref_content["authors"].append(ref_content.get("author"))
    utils.set_if_value(
        unknown_ref_content, "authorsEtAl", ref_content.get("authorsEtAl")
    )

    # compile details first for use later in title as a default
    details = references_json_unknown_details(ref_content, soup)

    # title
    utils.set_if_value(unknown_ref_content, "title", ref_content.get("title"))
    if "title" not in unknown_ref_content:
        utils.set_if_value(unknown_ref_content, "title", ref_content.get("bookTitle"))
    if "title" not in unknown_ref_content:
        utils.set_if_value(
            unknown_ref_content, "title", ref_content.get("articleTitle")
        )
    if "title" not in unknown_ref_content:
        # Still not title, try to use the details as the title
        utils.set_if_value(unknown_ref_content, "title", details)

    # add details
    utils.set_if_value(unknown_ref_content, "details", details)

    utils.set_if_value(unknown_ref_content, "uri", ref_content.get("uri"))

    return unknown_ref_content


def references_json_unknown_details(ref_content, soup=None):
    "Extract detail value for references of type unknown"
    details = ""

    # Try adding pages values first
    if "pages" in ref_content:
        if "range" in ref_content["pages"]:
            details += ref_content["pages"]["range"]
        else:
            details += ref_content["pages"]

    if soup:
        # Attempt to find the XML element by id, and convert it to details
        if "id" in ref_content:
            ref_tag = utils.first(soup.select("ref#" + ref_content["id"]))
            if ref_tag:
                # Now remove tags that would be already part of the unknown reference by now
                for remove_tag in [
                    "person-group",
                    "year",
                    "article-title",
                    "elocation-id",
                    "fpage",
                    "lpage",
                ]:
                    ref_tag = utils.remove_tag_from_tag(ref_tag, remove_tag)
                # Add the remaining tag content comma separated
                for tag in utils.first(raw_parser.element_citation(ref_tag)):
                    if utils.node_text(tag) is not None:
                        if details != "":
                            details += ", "
                        details += utils.node_text(tag)
    if details == "":
        return None

    return details


def ethics_json(soup):
    ethics_json = []
    ethics_fn_group = utils.first(raw_parser.fn_group(soup, "ethics-information"))

    # Part one, find the fn tags in the ethics section
    fn_body_blocks = []
    if ethics_fn_group:
        fn_tags = raw_parser.fn(ethics_fn_group)
        if fn_tags:
            for fn_tag in fn_tags:
                fn_body_blocks = fn_body_blocks + body_block_content_render(fn_tag)

    # Part two, if we have fn, then build out the json content
    for fn_content in fn_body_blocks:
        if fn_content.get("content"):
            for content_item in fn_content.get("content"):
                if "type" in content_item and content_item["type"] == "paragraph":
                    ethics_json.append(content_item)
    return ethics_json


def unwrap_appendix_box(json_content):
    """for use in removing unwanted boxed-content from appendices json"""
    if json_content.get("content") and len(json_content["content"]) > 0:
        first_block = json_content["content"][0]
        if (
            first_block.get("type")
            and first_block.get("type") == "box"
            and first_block.get("content")
        ):
            if first_block.get("doi") and not json_content.get("doi"):
                json_content["doi"] = first_block.get("doi")
            json_content["content"] = first_block["content"]
    return json_content


def appendices_json(soup, base_url=None):
    appendices_json = []
    app_group = None
    app_tags = []
    back = raw_parser.back(soup)
    if back:
        app_group = utils.first(raw_parser.app_group(back))
    if app_group:
        app_tags = raw_parser.app(app_group)
    for app_tag in app_tags:
        app_content = body_block_content(app_tag, base_url=base_url)
        app_blocks = body_blocks(app_tag)
        if app_blocks:
            app_content["content"] = []
            for block_tag in app_blocks:
                content_blocks = [
                    block
                    for block in body_block_content_render(block_tag, base_url=base_url)
                    if block
                ]
                # append the blocks to the content list
                app_content["content"] += content_blocks

        # If the first element is a box and it has no DOI, then ignore it
        #  by setting its child content to itself
        #  Also check one level deeper for box elements
        app_content = unwrap_appendix_box(app_content)
        if app_content.get("content") and len(app_content["content"]) > 0:
            app_content["content"][0] = unwrap_appendix_box(app_content["content"][0])

        # Then check all first level sections with no title, and fix them by
        #  building the content list again, unwrapping each non-title section
        clean_app_content = []
        for content_block in app_content["content"]:
            if (
                content_block.get("type")
                and content_block.get("type") == "section"
                and content_block.get("content")
                and not content_block.get("title")
            ):
                for block in content_block.get("content"):
                    clean_app_content.append(block)
            else:
                # Unwrap boxed-text if found here too
                content_block = unwrap_appendix_box(content_block)
                clean_app_content.append(content_block)
        app_content["content"] = clean_app_content

        appendices_json.append(app_content)
    return appendices_json


def dataset_tag_json(tag, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    def convert(xml_string):
        return xml_to_html(html_flag, xml_string)

    dataset_content = OrderedDict()

    # utils.set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
    utils.set_if_value(dataset_content, "id", tag.get("id"))
    utils.set_if_value(dataset_content, "date", utils.node_text(raw_parser.year(tag)))

    # authors
    dataset_authors = []
    for contrib_tag in utils.extract_nodes(tag, ["name", "collab"]):
        dataset_author = OrderedDict()
        if contrib_tag.name == "collab":
            dataset_author["type"] = "group"
            utils.set_if_value(
                dataset_author, "name", utils.node_contents_str(contrib_tag)
            )
        elif contrib_tag.name == "name":
            person_details = {}
            utils.set_if_value(
                person_details,
                "surname",
                utils.first_node_str_contents(contrib_tag, "surname"),
            )
            utils.set_if_value(
                person_details,
                "given-names",
                utils.first_node_str_contents(contrib_tag, "given-names"),
            )
            utils.set_if_value(
                person_details,
                "suffix",
                utils.first_node_str_contents(contrib_tag, "suffix"),
            )
            dataset_author = utils.references_author_person(person_details)
        if len(dataset_author) > 0:
            dataset_authors.append(dataset_author)
    if len(dataset_authors) > 0:
        dataset_content["authors"] = dataset_authors

    # et al
    if raw_parser.etal(tag):
        dataset_content["authorsEtAl"] = True

    # title
    utils.set_if_value(
        dataset_content,
        "title",
        convert(utils.node_contents_str(utils.first(raw_parser.source(tag)))),
    )

    # dataId
    utils.set_if_value(
        dataset_content,
        "dataId",
        convert(
            utils.node_contents_str(
                utils.first(raw_parser.object_id(tag, "art-access-id"))
            )
        ),
    )

    # details
    # prefer the data-title value first, then if not present use the comment tag value
    if raw_parser.data_title(tag):
        utils.set_if_value(
            dataset_content,
            "details",
            convert(utils.node_contents_str(utils.first(raw_parser.data_title(tag)))),
        )
    elif raw_parser.comment(tag):
        utils.set_if_value(
            dataset_content,
            "details",
            convert(utils.node_contents_str(utils.first(raw_parser.comment(tag)))),
        )

    # doi
    if raw_parser.pub_id(tag, "doi"):
        doi_tag = utils.first(raw_parser.pub_id(tag, "doi"))
        utils.set_if_value(
            dataset_content, "doi", utils.doi_uri_to_doi(doi_tag.get("xlink:href"))
        )
        if "doi" not in dataset_content:
            # use the tag value if xlink:href attribute is not present
            utils.set_if_value(
                dataset_content,
                "doi",
                utils.doi_uri_to_doi(utils.node_contents_str(doi_tag)),
            )
        utils.set_if_value(
            dataset_content, "assigningAuthority", doi_tag.get("assigning-authority")
        )

    # uri
    if raw_parser.ext_link(tag, "uri"):
        uri_tag = utils.first(raw_parser.ext_link(tag, "uri"))
        utils.set_if_value(dataset_content, "uri", uri_tag.get("xlink:href"))

    # uri from pub-id tag
    if "uri" not in dataset_content and raw_parser.pub_id(tag):
        pub_id_tag = utils.first(raw_parser.pub_id(tag))
        # set uri if it is not a doi tag
        if pub_id_tag.get("pub-id-type") != "doi":
            utils.set_if_value(dataset_content, "uri", pub_id_tag.get("xlink:href"))
        # set dataId if missing and the pub-id is an accession
        if (
            "dataId" not in dataset_content
            and pub_id_tag.get("pub-id-type") == "accession"
        ):
            utils.set_if_value(
                dataset_content, "dataId", convert(utils.node_contents_str(pub_id_tag))
            )
        utils.set_if_value(
            dataset_content, "assigningAuthority", pub_id_tag.get("assigning-authority")
        )

    return dataset_content


def datasets_json(soup, html_flag=True):
    datasets_json = OrderedDict()
    generated_datasets_tags = []
    used_datasets_tags = []
    availabilty_p_tags = []
    p_tags = []
    datasets_section_tag = None

    back_tag = raw_parser.back(soup)
    if back_tag:
        # find the section containing datasets by its sec-type value
        for sec_type in ["datasets", "data-availability"]:
            if raw_parser.section(back_tag, sec_type):
                datasets_section_tag = utils.first(
                    raw_parser.section(back_tag, sec_type)
                )
                break
        if datasets_section_tag:
            p_tags = raw_parser.paragraph(datasets_section_tag)

    if p_tags:
        dataset_type = None
        for p_tag in p_tags:
            # Look for paragraphs with related-object in them and the
            #  ones with out them are above the generated and used datasets
            if raw_parser.related_object(p_tag):
                if dataset_type == "generated":
                    generated_datasets_tags += raw_parser.related_object(p_tag)
                elif dataset_type == "used":
                    used_datasets_tags += raw_parser.related_object(p_tag)
            elif raw_parser.element_citation(p_tag):
                # also look for ones with element-citation tag
                if dataset_type == "generated":
                    generated_datasets_tags += raw_parser.element_citation(p_tag)
                elif dataset_type == "used":
                    used_datasets_tags += raw_parser.element_citation(p_tag)
            else:
                # Look for paragraphs ending in a certain term optionally with a colon at the end
                if utils.node_text(p_tag) and utils.node_text(p_tag).rstrip(
                    ":"
                ).endswith("generated"):
                    dataset_type = "generated"
                elif utils.node_text(p_tag) and utils.node_text(p_tag).rstrip(
                    ":"
                ).endswith("used"):
                    dataset_type = "used"
            # If no dataset type found yet, collect the first paragraphs for the data availability
            if not dataset_type:
                availabilty_p_tags.append(p_tag)

    # add data availability paragraphs
    for p_tag in availabilty_p_tags:
        block_content = body_block_content(p_tag)
        # check the text is not empty before adding
        if block_content and "text" in block_content:
            if "availability" not in datasets_json:
                datasets_json["availability"] = []
            datasets_json["availability"].append(block_content)

    for dataset_tag in generated_datasets_tags:
        if "generated" not in datasets_json:
            datasets_json["generated"] = []
        if dataset_tag_json(dataset_tag) != {}:
            datasets_json["generated"].append(dataset_tag_json(dataset_tag, html_flag))

    for dataset_tag in used_datasets_tags:
        if "used" not in datasets_json:
            datasets_json["used"] = []
        if dataset_tag_json(dataset_tag) != {}:
            datasets_json["used"].append(dataset_tag_json(dataset_tag, html_flag))

    return elifetools.json_rewrite.rewrite_json("datasets_json", soup, datasets_json)


def footnotes_json(soup, base_url=None):
    "format content from particular fn tags and ignore other fn tags"
    back = raw_parser.back(soup)
    if not back:
        return None
    fn_group_tags = raw_parser.fn_group(back)
    if not fn_group_tags:
        return None
    fn_group_tag = None
    # find the first tag with no content-type attribute and its direct parent is a back tag
    for tag in fn_group_tags:
        parent_tag = utils.first_parent(tag, ["back", "table-wrap"])
        if not tag.attrs.get("content-type") and parent_tag.name == "back":
            fn_group_tag = tag
            break
    if not fn_group_tag:
        return None
    footnotes_content = []
    for fn_tag in raw_parser.fn(fn_group_tag):
        # get title from label tag
        label_tag = raw_parser.label(fn_tag)
        section = {
            "id": fn_tag.attrs.get("id"),
            "title": label_tag.text,
            "type": "section",
        }
        section["content"] = render_raw_body(fn_tag, base_url=base_url)
        footnotes_content.append(section)
    return footnotes_content


def poa_supplementary_material_block_content(tag):
    tag_content = OrderedDict()

    # Check its characteristics first
    if (
        tag
        and tag.name == "supplementary-material"
        and raw_parser.ext_link(tag)
        and not raw_parser.media(tag)
    ):
        ext_link_tag = utils.first(raw_parser.ext_link(tag))
        filename = ext_link_tag.get("xlink:href")

        if filename and filename.endswith(".zip"):
            tag_content["mediaType"] = "application/zip"

        utils.set_if_value(tag_content, "uri", filename)
        utils.set_if_value(tag_content, "filename", filename)

    return tag_content


def supplementary_files_json(soup):
    additional_files_json = []

    supplementary_material_tags = []
    back = raw_parser.back(soup)
    if back:
        supplementary_material_tags = raw_parser.supplementary_material(back)

    for tag in supplementary_material_tags:
        tag_content = body_block_content(tag)
        if tag_content == {}:
            # Check if it is a simple PoA style supplementary-material
            tag_content = poa_supplementary_material_block_content(tag)

        if tag_content != {}:
            additional_files_json.append(tag_content)

    # Support for older PoA article supplementary material tags
    poa_supp_material_tags = []
    all_supp_material_tags = raw_parser.supplementary_material(soup)
    poa_supp_material_tags = list(
        filter(lambda tag: tag.parent.name == "article-meta", all_supp_material_tags)
    )
    for tag in poa_supp_material_tags:
        tag_content = poa_supplementary_material_block_content(tag)
        if tag_content != {}:
            additional_files_json.append(tag_content)

    # Add id and title for PoA articles, i.e. if there are none with an id value
    if (
        len(
            list(
                filter(
                    lambda file: file.get("id") is not None, supplementary_material_tags
                )
            )
        )
        == 0
    ):
        i = 1
        for file in additional_files_json:
            file["id"] = "SD" + str(i) + "-data"
            file["label"] = "Supplementary file " + str(i) + "."
            i = i + 1

    # if there is a single supplementary zip file for PoA,
    # rename it and describe it
    if len(additional_files_json) == 1:
        single_additional_file = additional_files_json[0]["filename"]
        if re.match(r"^.+-supp-.+\.zip$", single_additional_file):
            file = additional_files_json[0]
            file["label"] = "All additional files"
            file["caption"] = [
                {
                    "text": (
                        "Any figure supplements, source code, source data, videos or "
                        "supplementary files associated with this article are contained "
                        "within this zip."
                    ),
                    "type": "paragraph",
                }
            ]

    return additional_files_json


def funding_statement_json(soup, html_flag=True):
    return xml_to_html(html_flag, full_funding_statement(soup))


def funding_awards_json(soup):
    awards = []

    # Some details can take from existing award groups function
    award_groups = full_award_groups(soup)
    if award_groups:
        for award_group_dict in award_groups:
            for award_id, award_group in award_group_dict.items():
                award_content = OrderedDict()
                utils.set_if_value(award_content, "id", award_id)

                if award_group.get("institution") or award_group.get("id"):
                    # Set the source
                    source_content = OrderedDict()
                    utils.set_if_value(
                        source_content,
                        "funderId",
                        utils.doi_uri_to_doi(award_group.get("id")),
                    )
                    if award_group.get("institution"):
                        utils.set_if_value(
                            source_content, "name", [award_group.get("institution")]
                        )
                    award_content["source"] = source_content

                # awardId
                if award_group.get("award-id") and award_group.get("award-id") != "":
                    utils.set_if_value(
                        award_content, "awardId", award_group.get("award-id")
                    )

                if len(award_content) > 0:
                    awards.append(award_content)

    # recipients to parse fresh
    award_group_tags = []
    award_recipients = {}
    funding_group = utils.first(raw_parser.funding_group(soup))
    if funding_group:
        award_group_tags = raw_parser.award_group(funding_group)
    for a_tag in award_group_tags:
        award_id = a_tag.get("id")
        recipient_tags = raw_parser.principal_award_recipient(a_tag)
        if recipient_tags:
            recipients = []
            for recipient_tag in recipient_tags:
                if (
                    len(utils.extract_nodes(recipient_tag, ["name", "institution"]))
                    <= 0
                ):
                    # A loose institution name not surrounded by institution tag
                    recipient_content = OrderedDict()
                    recipient_content["type"] = "group"
                    utils.set_if_value(
                        recipient_content,
                        "name",
                        utils.node_contents_str(recipient_tag),
                    )
                    if len(recipient_content) > 0:
                        # add it
                        recipients.append(recipient_content)
                else:
                    for contrib_tag in utils.extract_nodes(
                        recipient_tag, ["name", "institution"]
                    ):
                        recipient_content = OrderedDict()
                        if contrib_tag.name == "institution":
                            recipient_content["type"] = "group"
                            utils.set_if_value(
                                recipient_content,
                                "name",
                                utils.node_contents_str(contrib_tag),
                            )
                        elif contrib_tag.name == "name":
                            person_details = {}
                            utils.set_if_value(
                                person_details,
                                "surname",
                                utils.first_node_str_contents(contrib_tag, "surname"),
                            )
                            utils.set_if_value(
                                person_details,
                                "given-names",
                                utils.first_node_str_contents(
                                    contrib_tag, "given-names"
                                ),
                            )
                            utils.set_if_value(
                                person_details,
                                "suffix",
                                utils.first_node_str_contents(contrib_tag, "suffix"),
                            )
                            recipient_content = utils.article_author_person(
                                person_details
                            )
                        if len(recipient_content) > 0:
                            # add it
                            recipients.append(recipient_content)

            # Add to the dict for adding to the award data later
            if len(recipients) > 0:
                if award_id not in award_recipients:
                    award_recipients[award_id] = []
                award_recipients[award_id] = recipients

    # Add recipient data to the award data
    for award in awards:
        if award.get("id") and award.get("id") in award_recipients:
            award["recipients"] = award_recipients.get(award.get("id"))

    awards = elifetools.json_rewrite.rewrite_json("funding_awards", soup, awards)

    return awards
