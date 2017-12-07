from collections import OrderedDict

from bs4 import BeautifulSoup
from slugify import slugify

import elifetools.rawJATS as raw_parser
import elifetools.json_rewrite
from elifetools.utils import *
from elifetools.utils import unicode_value
from elifetools.utils_html import xml_to_html, references_author_collab


def parse_xml(xml):
    return BeautifulSoup(xml, "lxml-xml")

def parse_document(filelocation):
    with open(filelocation, 'rb') as fp:
        return parse_xml(fp)

def duplicate_tag(tag):
    # Make a completely new copy of a tag by parsing its contents again
    tag_xml = u'<article xmlns:ali="http://www.niso.org/schemas/ali/1.0/" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">' + unicode_value(tag) + u'</article>'
    soup_copy = parse_xml(tag_xml)
    tag_copy = first(extract_nodes(soup_copy, tag.name))
    return tag_copy

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

def title_prefix(soup):
    "titlePrefix for article JSON is only articles with certain display_channel values"
    prefix = None
    display_channel_match_list = ['feature article', 'insight', 'editorial']
    for d_channel in display_channel(soup):
        if d_channel.lower() in display_channel_match_list:
            if raw_parser.sub_display_channel(soup):
                prefix = node_text(first(raw_parser.sub_display_channel(soup)))
    return prefix

def title_prefix_json(soup):
    "titlePrefix with capitalisation changed"
    prefix = title_prefix(soup)
    prefix_rewritten = elifetools.json_rewrite.rewrite_json("title_prefix_json", soup, prefix)
    return prefix_rewritten

def doi(soup):
    # the first non-nil value returned by the raw parser
    return doi_uri_to_doi(node_text(raw_parser.doi(soup)))

def publisher_id(soup):
    # aka the article_id, specified by the publisher
    return node_text(raw_parser.publisher_id(soup))

def journal_id(soup):
    return node_text(raw_parser.journal_id(soup))

def journal_title(soup):
    return node_text(raw_parser.journal_title(soup))

def journal_issn(soup, pub_format=None, pub_type=None):
    return node_text(raw_parser.journal_issn(soup, pub_format, pub_type))

def publisher(soup):
    return node_text(raw_parser.publisher(soup))

def article_type(soup):
    # no node text extraction required
    return raw_parser.article_type(soup)

def volume(soup):
    return node_text(first(raw_parser.volume(soup)))

def issue(soup):
    return node_text(first(raw_parser.issue(raw_parser.article_meta(soup))))

def elocation_id(soup):
    return node_text(first(raw_parser.elocation_id(soup)))

def research_organism(soup):
    "Find the research-organism from the set of kwd-group tags"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return list(map(node_text, raw_parser.research_organism_keywords(soup)))

def full_research_organism(soup):
    "research-organism list including inline tags, such as italic"
    if not raw_parser.research_organism_keywords(soup):
        return []
    return list(map(node_contents_str, raw_parser.research_organism_keywords(soup)))

def keywords(soup):
    """
    Find the keywords from the set of kwd-group tags
    which are typically labelled as the author keywords
    """
    if not raw_parser.author_keywords(soup):
        return []
    return list(map(node_text, raw_parser.author_keywords(soup)))

def full_keywords(soup):
    "author keywords list including inline tags, such as italic"
    if not raw_parser.author_keywords(soup):
        return []
    return list(map(node_contents_str, raw_parser.author_keywords(soup)))

def full_keyword_groups(soup):
    groups = {}
    for group_tag in raw_parser.keyword_group(soup):
        group = list(map(node_contents_str, extract_nodes(group_tag, "kwd")))
        group = list(map(lambda s: s.strip(), group))
        if 'kwd-group-type' in group_tag.attrs:
            groups[group_tag['kwd-group-type'].strip()] = group
    return groups

def full_custom_meta(soup, meta_name=None):
    return raw_parser.custom_meta(soup, meta_name)

def impact_statement(soup):
    tag = first(full_custom_meta(soup, "Author impact statement"))
    if tag is not None:
        return node_contents_str(first(extract_nodes(tag, "meta-value")))
    return ""

def version_history(soup, html_flag=True):
    "extract the article version history details"
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)
    version_history = []
    related_object_tags = raw_parser.related_object(raw_parser.article_meta(soup))
    for tag in related_object_tags:
        article_version = OrderedDict()
        date_tag = first(raw_parser.date(tag))
        if date_tag:
            copy_attribute(date_tag.attrs, 'date-type', article_version, 'version')
            (day, month, year) = ymd(date_tag)
            article_version['day'] = day
            article_version['month'] = month
            article_version['year'] = year
            article_version['date'] = date_struct_nn(year, month, day)
        copy_attribute(tag.attrs, 'xlink:href', article_version, 'xlink_href')
        set_if_value(article_version, "comment",
                     convert(node_contents_str(first(raw_parser.comment(tag)))))
        version_history.append(article_version)
    return version_history

def format_related_object(related_object):
    return related_object["id"], {}


def related_object_ids(soup):
    tags = []
    if raw_parser.related_object(soup):
        tags = list(filter(lambda tag: tag.get("id") is not None, raw_parser.related_object(soup)))
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
    result = [node_text(tag) for tag in raw_parser.conflict(soup)]
    return result

def copyright_statement(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return node_text(raw_parser.copyright_statement(permissions_tag))
    return None

@inten
def copyright_year(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return node_text(raw_parser.copyright_year(permissions_tag))
    return None

def copyright_holder(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return node_text(raw_parser.copyright_holder(permissions_tag))
    return None

def copyright_holder_json(soup):
    "for json output add a full stop if ends in et al"
    holder = None
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        holder = node_text(raw_parser.copyright_holder(permissions_tag))
    if holder is not None and holder.endswith('et al'):
        holder = holder + '.'
    return holder

def license(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return node_text(first(raw_parser.licence_p(permissions_tag)))
    return None

def full_license(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return node_contents_str(first(raw_parser.licence_p(permissions_tag)))
    return None

def license_url(soup):
    permissions_tag = raw_parser.article_permissions(soup)
    if permissions_tag:
        return raw_parser.licence_url(permissions_tag)
    return None

def license_json(soup):
    return xml_to_html(True, full_license(soup))

def funding_statement(soup):
    return node_text(raw_parser.funding_statement(soup))

def full_funding_statement(soup):
    return node_contents_str(raw_parser.funding_statement(soup))

#
# authors
#

#
# refs
#


def ref_text(tag):
    # ref - human readable full reference text
    ref_text = node_text(tag)
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
    pub_date = first(raw_parser.pub_date(soup, date_type="pub"))
    if pub_date is None:
        pub_date = first(raw_parser.pub_date(soup, date_type="publication"))
    if pub_date is None:
        return None
    (day, month, year) = ymd(pub_date)
    return date_struct(year, month, day)

def pub_dates(soup):
    """
    return a list of all the pub dates
    """
    pub_dates = []
    tags = raw_parser.pub_date(soup)
    for tag in tags:
        pub_date = OrderedDict()
        copy_attribute(tag.attrs, 'publication-format', pub_date)
        copy_attribute(tag.attrs, 'date-type', pub_date)
        copy_attribute(tag.attrs, 'pub-type', pub_date)
        for tag_attr in ["date-type", "pub-type"]:
            if tag_attr in tag.attrs:
                (day, month, year) = ymd(tag)
                pub_date['day'] = day
                pub_date['month'] = month
                pub_date['year'] = year
                pub_date['date'] = date_struct_nn(year, month, day)
        pub_dates.append(pub_date)
    return pub_dates

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
    pub_date = first(raw_parser.pub_date(soup, pub_type="collection"))
    if pub_date is None:
        return None

    year = None
    year_tag = raw_parser.year(pub_date)
    if year_tag:
        year = int(node_text(year_tag))

    return year

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

        abstract["content"] = None
        if raw_parser.paragraph(tag):
            abstract["content"] = ""
            abstract["full_content"] = ""

            good_paragraphs = remove_doi_paragraph(raw_parser.paragraph(tag))

            # Plain text content
            glue = ""
            for p_tag in good_paragraphs:
                abstract["content"] += glue + node_text(p_tag)
                glue = " "

            # Content including markup tags
            # When more than one paragraph, wrap each in a <p> tag
            for p_tag in good_paragraphs:
                abstract["full_content"] += '<p>' + node_contents_str(p_tag) + '</p>'

        abstracts.append(abstract)

    return abstracts


def abstract(soup):
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = first(list(filter(lambda tag: tag.get("abstract_type") is None, abstract_list)))
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
        abstract = first(list(filter(lambda tag: tag.get("abstract_type") is None, abstract_list)))
    if abstract:
        return abstract.get("full_content")
    else:
        return None

def digest(soup):
    abstract = None
    abstract_list = abstracts(soup)
    if abstract_list:
        abstract = first(list(filter(lambda tag: tag.get("abstract_type") == "executive-summary", abstract_list)))
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
        abstract = first(list(filter(lambda tag: tag.get("abstract_type") == "executive-summary", abstract_list)))
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

def mixed_citations(soup):
    mc_tags = raw_parser.mixed_citations(soup)
    def name(nom):
        return {
            'surname': nom.surname.text,
            'given': nom.find('given-names').text,
        }
    def preferred_name(nom):
        suffix = None
        return author_preferred_name(nom.surname.text, nom.find('given-names').text, suffix)
    def do(mc):
        return {
            'journal': {
                'name': mc.source.text,
                'volume': mc.volume.text,
                'fpage':  mc.fpage.text,
                'lpage': node_text(mc.lpage),
            },
            'article': {
                'title': mc.find('article-title').text,
                'doi': mc.find('pub-id', attrs={'pub-id-type': 'doi'}).text,
                'pub-date': list(map(int, ymd(soup)[::-1])),
                'authors': list(map(name, mc.find('person-group', attrs={'person-group-type': 'author'}).contents)),
                'authorLine': format_author_line(list(map(preferred_name, mc.find('person-group', attrs={'person-group-type': 'author'}).contents))),
            },
        }
    return list(map(do, mc_tags))

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
        component_object["doi"] = doi_uri_to_doi(tag.text)
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

    if ((tag.name == "fig" and 'specific-use' not in tag.attrs)
         or tag.name == "media"):
        # Fig that is not a child figure / figure supplement
        if first_parent(tag, 'sub-article'):
            # Sub-article sibling ordinal numbers work differently
            sibling_ordinal = tag_subarticle_sibling_ordinal(tag)
        elif first_parent(tag, 'app'):
            sibling_ordinal = tag_appendix_sibling_ordinal(tag)
        elif tag.name == "media":
            # Media video or non-video are different numbering
            sibling_ordinal = tag_media_sibling_ordinal(tag)
        else:
            sibling_ordinal = tag_fig_ordinal(tag)
    elif tag.name == "supplementary-material":
        sibling_ordinal = tag_supplementary_material_sibling_ordinal(tag)
    else:
        # Default
        sibling_ordinal = tag_sibling_ordinal(tag)

    return sibling_ordinal

def tag_details_asset(tag):
    asset = None

    if tag.name == "fig" and 'specific-use' in tag.attrs:
        # Child figure / figure supplement
        asset = 'figsupp'
    elif tag.name == "media":
        # Set media tag asset value, it is useful
        asset = 'media'
    elif tag.name == "app":
        asset = 'app'
    elif tag.name == "supplementary-material":
        # Default is supp
        asset = supp_asset(tag)
    elif tag.name == "sub-article":
        if (node_text(raw_parser.article_title(tag)) and
            node_text(raw_parser.article_title(tag)).lower() == 'decision letter'):
            asset = 'dec'
        elif (node_text(raw_parser.article_title(tag)) and
              node_text(raw_parser.article_title(tag)).lower() == 'author response'):
            asset = 'resp'

    return asset


def tag_details(tag, nodenames):
    """
    Used in media and graphics to extract data from their parent tags
    """
    details = {}

    details['type'] = tag.name
    details['ordinal'] = tag_ordinal(tag)

    # Ordinal value
    if tag_details_sibling_ordinal(tag):
        details['sibling_ordinal'] = tag_details_sibling_ordinal(tag)

    # Asset name
    if tag_details_asset(tag):
        details['asset'] = tag_details_asset(tag)

    object_id_tag = first(raw_parser.object_id(tag, pub_id_type= "doi"))
    if object_id_tag:
        details['component_doi'] = extract_component_doi(tag, nodenames)

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

        copy_attribute(tag.attrs, 'mime-subtype', media_item)
        copy_attribute(tag.attrs, 'mimetype', media_item)
        copy_attribute(tag.attrs, 'xlink:href', media_item, 'xlink_href')
        copy_attribute(tag.attrs, 'content-type', media_item)

        nodenames = ["sub-article", "media", "fig-group", "fig", "supplementary-material"]

        details = tag_details(tag, nodenames)
        copy_attribute(details, 'component_doi', media_item)
        copy_attribute(details, 'type', media_item)
        copy_attribute(details, 'sibling_ordinal', media_item)

        # Try to get the component DOI of the parent tag
        parent_tag = first_parent(tag, nodenames)
        if parent_tag:
            acting_parent_tag = component_acting_parent_tag(parent_tag, tag)
            if acting_parent_tag:
                details = tag_details(acting_parent_tag, nodenames)
                copy_attribute(details, 'type', media_item, 'parent_type')
                copy_attribute(details, 'ordinal', media_item, 'parent_ordinal')
                copy_attribute(details, 'asset', media_item, 'parent_asset')
                copy_attribute(details, 'sibling_ordinal', media_item, 'parent_sibling_ordinal')
                copy_attribute(details, 'component_doi', media_item, 'parent_component_doi')

            # Try to get the parent parent
            p_parent_tag = first_parent(parent_tag, nodenames)
            if p_parent_tag:
                acting_p_parent_tag = component_acting_parent_tag(p_parent_tag, parent_tag)
                if acting_p_parent_tag:
                    details = tag_details(acting_p_parent_tag, nodenames)
                    copy_attribute(details, 'type', media_item, 'p_parent_type')
                    copy_attribute(details, 'ordinal', media_item, 'p_parent_ordinal')
                    copy_attribute(details, 'asset', media_item, 'p_parent_asset')
                    copy_attribute(details, 'sibling_ordinal', media_item, 'p_parent_sibling_ordinal')
                    copy_attribute(details, 'component_doi', media_item, 'p_parent_component_doi')

                # Try to get the parent parent parent
                p_p_parent_tag = first_parent(p_parent_tag, nodenames)
                if p_p_parent_tag:
                    acting_p_p_parent_tag = component_acting_parent_tag(p_p_parent_tag, p_parent_tag)
                    if acting_p_p_parent_tag:
                        details = tag_details(acting_p_p_parent_tag, nodenames)
                        copy_attribute(details, 'type', media_item, 'p_p_parent_type')
                        copy_attribute(details, 'ordinal', media_item, 'p_p_parent_ordinal')
                        copy_attribute(details, 'asset', media_item, 'p_p_parent_asset')
                        copy_attribute(details, 'sibling_ordinal', media_item, 'p_p_parent_sibling_ordinal')
                        copy_attribute(details, 'component_doi', media_item, 'p_p_parent_component_doi')

        # Increment the position
        media_item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        media_item['ordinal'] = tag_ordinal(tag)

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

        copy_attribute(tag.attrs, 'xlink:href', graphic_item, 'xlink_href')

        # Get the tag type
        nodenames = ["sub-article", "fig-group", "fig", "app"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', graphic_item)

        parent_tag = first_parent(tag, nodenames)
        if parent_tag:
            details = tag_details(parent_tag, nodenames)
            copy_attribute(details, 'type', graphic_item, 'parent_type')
            copy_attribute(details, 'ordinal', graphic_item, 'parent_ordinal')
            copy_attribute(details, 'asset', graphic_item, 'parent_asset')
            copy_attribute(details, 'sibling_ordinal', graphic_item, 'parent_sibling_ordinal')
            copy_attribute(details, 'component_doi', graphic_item, 'parent_component_doi')

            # Try to get the parent parent - special for looking at fig tags
            #  use component_acting_parent_tag
            p_parent_tag = first_parent(parent_tag, nodenames)
            if p_parent_tag:
                acting_p_parent_tag = component_acting_parent_tag(p_parent_tag, parent_tag)
                if acting_p_parent_tag:
                    details = tag_details(acting_p_parent_tag, nodenames)
                    copy_attribute(details, 'type', graphic_item, 'p_parent_type')
                    copy_attribute(details, 'ordinal', graphic_item, 'p_parent_ordinal')
                    copy_attribute(details, 'asset', graphic_item, 'p_parent_asset')
                    copy_attribute(details, 'sibling_ordinal', graphic_item, 'p_parent_sibling_ordinal')
                    copy_attribute(details, 'component_doi', graphic_item, 'p_parent_component_doi')

        # Increment the position
        graphic_item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        graphic_item['ordinal'] = tag_ordinal(tag)

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

        copy_attribute(tag.attrs, 'xlink:href', item, 'xlink_href')

        # Get the tag type
        nodenames = ["sub-article"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', item)

        # Increment the position
        item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        item['ordinal'] = tag_ordinal(tag)

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

        copy_attribute(tag.attrs, 'xlink:href', item, 'xlink_href')
        copy_attribute(tag.attrs, 'content-type', item)

        # Get the tag type
        nodenames = ["sub-article"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', item)

        # Increment the position
        item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        item['ordinal'] = tag_ordinal(tag)

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

        copy_attribute(tag.attrs, 'id', item)

        # Get the tag type
        nodenames = ["supplementary-material"]
        details = tag_details(tag, nodenames)
        copy_attribute(details, 'type', item)
        copy_attribute(details, 'asset', item)
        copy_attribute(details, 'component_doi', item)
        copy_attribute(details, 'sibling_ordinal', item)

        if raw_parser.label(tag):
            item['label'] = node_text(raw_parser.label(tag))
            item['full_label'] = node_contents_str(raw_parser.label(tag))

        # Increment the position
        item['position'] = position
        # Ordinal should be the same as position in this case but set it anyway
        item['ordinal'] = tag_ordinal(tag)

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
    for email_tag in extract_nodes(contrib_tag, "email"):
        if email_tag.parent.name != "aff":
            email.append(email_tag.text)
    return email if len(email) > 0 else None

def contrib_phone(contrib_tag):
    """
    Given a contrib tag, look for an phone tag
    """
    phone = None
    if raw_parser.phone(contrib_tag):
        phone = first(raw_parser.phone(contrib_tag)).text
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
        if (child_tag and child_tag.name and child_tag.name == "xref"
            and child_tag.get('ref-type') and child_tag.get('ref-type') == ref_type):
            aff_tags.append(child_tag)
    return aff_tags

def format_contrib_refs(contrib_tag, soup):
    contrib_refs = {}
    ref_tags = extract_nodes(contrib_tag, "xref")
    ref_type_aff_count = 0
    for ref_tag in ref_tags:
        if "ref-type" in ref_tag.attrs and "rid" in ref_tag.attrs:
            ref_type = ref_tag['ref-type']
            rid = ref_tag['rid']

            if ref_type == "aff":
                ref_type_aff_count += 1
                add_to_list_dictionary(contrib_refs, 'affiliation', rid)
            if ref_type == "corresp":
                # Check for email or phone type
                corresp_tag = firstnn(soup.find_all(id=rid))
                if contrib_phone(corresp_tag):
                    add_to_list_dictionary(contrib_refs, 'phone', rid)
                elif contrib_email(corresp_tag):
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
                elif rid.startswith('fn'):
                    add_to_list_dictionary(contrib_refs, 'foot-note', rid)
            elif ref_type == "other":
                if rid.startswith('par-') or rid.startswith('fund'):
                    add_to_list_dictionary(contrib_refs, 'funding', rid)
                elif rid.startswith('dataro') or rid.startswith('dataset'):
                    add_to_list_dictionary(contrib_refs, 'related-object', rid)
    return contrib_refs, ref_type_aff_count

def format_contributor(contrib_tag, soup, detail="brief", contrib_type=None,
                       group_author_key=None, target_tags_corresp=None, target_tags_fn=None):
    contributor = {}
    copy_attribute(contrib_tag.attrs, 'contrib-type', contributor, 'type')
    # Set contrib type if passed via params
    if not contributor.get('type') and contrib_type:
        contributor['type'] = contrib_type
    copy_attribute(contrib_tag.attrs, 'equal-contrib', contributor)
    copy_attribute(contrib_tag.attrs, 'corresp', contributor)
    copy_attribute(contrib_tag.attrs, 'deceased', contributor)
    copy_attribute(contrib_tag.attrs, 'id', contributor)
    contrib_id_tag = first(raw_parser.contrib_id(contrib_tag))
    if contrib_id_tag and 'contrib-id-type' in contrib_id_tag.attrs:
        if contrib_id_tag['contrib-id-type'] == 'group-author-key':
            contributor['group-author-key'] = node_contents_str(contrib_id_tag)
    # Set group-author-key if passed via params
    if not contributor.get('group-author-key') and group_author_key:
        contributor['group-author-key'] = group_author_key
    if raw_parser.collab(contrib_tag):
        collab_tag = first(raw_parser.collab(contrib_tag))
        if collab_tag:
            # Clean up if there are tags inside the collab tag
            tag_copy = duplicate_tag(collab_tag)
            tag_copy = remove_tag_from_tag(tag_copy, 'contrib-group')
            contributor['collab'] = node_contents_str(tag_copy).rstrip()

    # Check if it is not a group author
    if not is_author_group_author(contrib_tag):
        if contrib_id_tag and 'contrib-id-type' in contrib_id_tag.attrs:
            if contrib_id_tag['contrib-id-type'] == 'orcid':
                contributor['orcid'] = node_contents_str(contrib_id_tag)
        set_if_value(contributor, "role", first_node_str_contents(contrib_tag, "role"))
        if raw_parser.bio(contrib_tag):
            biography_content = body_block_content_render(firstnn(raw_parser.bio(contrib_tag)))
            if len(biography_content) > 0:
                contributor["bio"] = biography_content[0].get("content")
        set_if_value(contributor, "email", contrib_email(contrib_tag))
        set_if_value(contributor, "phone", contrib_phone(contrib_tag))
        set_if_value(contributor, "surname", first_node_str_contents(contrib_tag, "surname"))
        set_if_value(contributor, "given-names", first_node_str_contents(contrib_tag, "given-names"))
        set_if_value(contributor, "suffix", first_node_str_contents(contrib_tag, "suffix"))
        # Get the sub-group value from the parent role tag if it is inside a group
        if (contrib_tag.parent and contrib_tag.parent.parent and contrib_tag.parent.parent.parent
            and is_author_group_author(contrib_tag.parent.parent.parent)):
            set_if_value(contributor, "sub-group", first_node_str_contents(contrib_tag.parent, "role"))
    elif contributor.get('corresp') and not contributor.get('email'):
        # For corresponding group authors, look for an email address anywhere in the group
        set_if_value(contributor, "email", contrib_email(contrib_tag))

    # on-behalf-of
    if contrib_tag.name == 'on-behalf-of':
        contributor['type'] = 'on-behalf-of'
        contributor['on-behalf-of'] = node_contents_str(contrib_tag)

    contrib_refs, ref_type_aff_count = format_contrib_refs(contrib_tag, soup)
    if len(contrib_refs) > 0:
        contributor['references'] = contrib_refs

    if detail == "brief" or ref_type_aff_count == 0:
        # Brief format only allows one aff and it must be within the contrib tag
        aff_tag = firstnn(contrib_inline_aff(contrib_tag))
        if aff_tag:
            contributor['affiliations'] = []
            contrib_affs = {}
            (none_return, aff_detail) = format_aff(aff_tag)
            if len(aff_detail) > 0:
                aff_attributes = ['dept', 'institution', 'country', 'city', 'email']
                for aff_attribute in aff_attributes:
                    if aff_attribute in aff_detail and aff_detail[aff_attribute] is not None:
                        copy_attribute(aff_detail, aff_attribute, contrib_affs)
                if len(contrib_affs) > 0:
                    contributor['affiliations'].append(contrib_affs)

    if detail == "full":
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

        aff_tags = contrib_xref(contrib_tag, "aff")
        if len(aff_tags) <= 0:
            aff_tags = contrib_inline_aff(contrib_tag)
        if aff_tags:
            contributor['affiliations'] = []
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
                aff_attributes = ['dept', 'institution', 'country', 'city', 'email']
                for aff_attribute in aff_attributes:
                    if aff_attribute in aff_detail and aff_detail[aff_attribute] is not None:
                        copy_attribute(aff_detail, aff_attribute, contrib_affs)
                contributor['affiliations'].append(contrib_affs)

        # Add xref linked correspondence author notes if applicable
        corresp_tags = contrib_xref(contrib_tag, "corresp")
        if(len(corresp_tags) > 0):
            if 'notes-corresp' not in contributor:
                contributor['notes-corresp'] = []
            if not target_tags_corresp:
                target_tags_corresp = raw_parser.corresp(soup)
            for cor in corresp_tags:
                # Find the matching tag
                rid = cor['rid']
                corresp_node = first(list(filter(lambda tag: tag.get("id") == rid, target_tags_corresp)))
                author_notes = node_text(corresp_node)
                if author_notes:
                    contributor['notes-corresp'].append(author_notes)
        # Add xref linked footnotes if applicable
        fn_tags = contrib_xref(contrib_tag, "fn")
        if(len(fn_tags) > 0):
            if 'notes-fn' not in contributor:
                contributor['notes-fn'] = []
            if not target_tags_fn:
                target_tags_fn = raw_parser.fn(soup)
            for fn in fn_tags:
               # Find the matching tag
               rid = fn['rid']
               fn_node = first(list(filter(lambda tag: tag.get("id") == rid, target_tags_fn)))
               fn_text = node_text(fn_node)
               if fn_text:
                   contributor['notes-fn'].append(fn_text)

    return contributor

def contributors(soup, detail="brief"):
    contrib_tags = raw_parser.article_contributors(soup)
    contributors = format_authors(soup, contrib_tags, detail)
    return contributors

#
# HERE BE DRAGONS
#

def is_author_non_byline(tag, contrib_type="author non-byline"):
    if tag and tag.get("contrib-type") and tag.get("contrib-type") == contrib_type:
        return True
    elif tag and tag.parent and tag.parent.parent and tag.parent.parent.name == "collab":
        return True
    return False

def authors_non_byline(soup, detail="full"):
    """Non-byline authors for group author members"""
    # Get a filtered list of contributors, in order to get their group-author-id
    contrib_type = "author non-byline"
    contributors_ = contributors(soup, detail)
    non_byline_authors = [author for author in contributors_ if author.get('type', None) == contrib_type]

    # Then renumber their position attribute
    position = 1
    for author in non_byline_authors:
        author["position"] = position
        position = position + 1
    return non_byline_authors

def authors(soup, contrib_type = "author", detail = "full"):
    contrib_tags = raw_parser.authors(raw_parser.article_meta(soup), contrib_type)
    tags = list(filter(lambda tag: is_author_non_byline(tag) is False, contrib_tags))
    return format_authors(soup, tags, detail)

def is_author_group_author(tag):
    if tag:
        for child_tag in tag:
            # look at the child tags for a collab tag
            if child_tag.name == "collab":
                return True
    return False

def format_authors(soup, contrib_tags, detail = "full", contrib_type=None):
    authors = []
    position = 1

    article_doi = doi(soup)

    group_author_id = 0
    prev_group_author_id = 0

    # Pre-parse some values to pass to optimise this procedure
    target_tags_corresp = raw_parser.corresp(soup)
    target_tags_fn = raw_parser.fn(soup)

    for tag in contrib_tags:

        # Set the group author key if missing
        if is_author_group_author(tag):
            group_author_id = group_author_id + 1
            group_author_key = 'group-author-id' + str(group_author_id)
        else:
            group_author_key = None

        # Set the contrib_type and group author key for non-byline authors
        if is_author_non_byline(tag) is True and contrib_type is None:
            author_contrib_type = 'author non-byline'
            group_author_key = 'group-author-id' + str(prev_group_author_id)
        elif is_author_non_byline(tag) is False and is_author_group_author(tag) is not True:
            author_contrib_type = contrib_type
            group_author_key = None
        else:
            author_contrib_type = contrib_type

        author = format_contributor(tag, soup, detail, author_contrib_type, group_author_key, target_tags_corresp, target_tags_fn)

        # If not empty, add position value, append, then increment the position counter
        if(len(author) > 0):
            if detail == "full":
                author['article_doi'] = article_doi
                author['position'] = position

            authors.append(author)
            position += 1

        prev_group_author_id = group_author_id


    return authors


def format_aff(aff_tag):
    if not aff_tag:
        return None, {}
    values = {
        'dept': node_contents_str(first(extract_nodes(aff_tag, "institution", "content-type", "dept"))),
        'institution': node_contents_str(first(list(filter(lambda n: "content-type" not in n.attrs, extract_nodes(aff_tag, "institution"))))),
        'city': node_contents_str(first(extract_nodes(aff_tag, "named-content", "content-type", "city"))),
        'country': node_contents_str(first(extract_nodes(aff_tag, "country"))),
        'email': node_contents_str(first(extract_nodes(aff_tag, "email")))
        }
    # Remove keys with None value
    values = prune_dict_of_none_values(values)

    if 'id' in aff_tag.attrs:
        return aff_tag['id'], values
    else:
        return None, values


def full_affiliation(soup):
    aff_tags = raw_parser.affiliation(soup)
    aff_tags = list(filter(lambda aff: 'id' in aff.attrs, aff_tags))
    affs = []
    for tag in aff_tags:
        aff = {}
        (id, aff_details) = format_aff(tag)
        aff[id] = aff_details
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

        ref['ref'] = ref_text(tag)

        # ref_id
        copy_attribute(tag.attrs, "id", ref)

        # article_title
        if raw_parser.article_title(tag):
            ref['article_title'] = node_text(raw_parser.article_title(tag))
            ref['full_article_title'] = node_contents_str(raw_parser.article_title(tag))

        if raw_parser.pub_id(tag, "pmid"):
            ref['pmid'] = node_contents_str(first(raw_parser.pub_id(tag, "pmid")))

        if raw_parser.pub_id(tag, "isbn"):
            ref['isbn'] = node_contents_str(first(raw_parser.pub_id(tag, "isbn")))

        if raw_parser.pub_id(tag, "doi"):
            ref['reference_id'] = node_contents_str(first(raw_parser.pub_id(tag, "doi")))
            ref['doi'] = doi_uri_to_doi(node_contents_str(first(raw_parser.pub_id(tag, "doi"))))

        uri_tag = None
        if raw_parser.ext_link(tag, "uri"):
            uri_tag = first(raw_parser.ext_link(tag, "uri"))
        elif raw_parser.uri(tag):
            uri_tag = first(raw_parser.uri(tag))
        if uri_tag:
            set_if_value(ref, "uri", uri_tag.get('xlink:href'))
            set_if_value(ref, "uri_text", node_contents_str(uri_tag))

        # accession, could be in either of two tags
        set_if_value(ref, "accession", node_contents_str(first(raw_parser.object_id(tag, "art-access-id"))))
        if not ref.get('accession'):
            set_if_value(ref, "accession", node_contents_str(first(raw_parser.pub_id(tag, pub_id_type="accession"))))

        if(raw_parser.year(tag)):
            set_if_value(ref, "year", node_text(raw_parser.year(tag)))
            set_if_value(ref, "year-iso-8601-date", raw_parser.year(tag).get('iso-8601-date'))

        if(raw_parser.date_in_citation(tag)):
            set_if_value(ref, "date-in-citation", node_text(first(raw_parser.date_in_citation(tag))))
            set_if_value(ref, "iso-8601-date", first(raw_parser.date_in_citation(tag)).get('iso-8601-date'))

        if(raw_parser.patent(tag)):
            set_if_value(ref, "patent", node_text(first(raw_parser.patent(tag))))
            set_if_value(ref, "country", first(raw_parser.patent(tag)).get('country'))

        set_if_value(ref, "source", node_text(first(raw_parser.source(tag))))
        set_if_value(ref, "elocation-id", node_text(first(raw_parser.elocation_id(tag))))
        if raw_parser.element_citation(tag):
            copy_attribute(first(raw_parser.element_citation(tag)).attrs, "publication-type", ref)

        # authors
        person_group = raw_parser.person_group(tag)
        authors = []

        for group in person_group:

            author_type = None
            if "person-group-type" in group.attrs:
                author_type = group["person-group-type"]

            # Read name or collab tag in the order they are listed
            for name_or_collab_tag in extract_nodes(group, ["name","collab"]):
                author = {}

                # Shared tag attribute
                set_if_value(author, "group-type", author_type)

                # name tag attributes
                if name_or_collab_tag.name == "name":
                    set_if_value(author, "surname", node_text(first(raw_parser.surname(name_or_collab_tag))))
                    set_if_value(author, "given-names", node_text(first(raw_parser.given_names(name_or_collab_tag))))
                    set_if_value(author, "suffix", node_text(first(raw_parser.suffix(name_or_collab_tag))))

                # collab tag attribute
                if name_or_collab_tag.name == "collab":
                    set_if_value(author, "collab", node_contents_str(name_or_collab_tag))

                if len(author) > 0:
                    authors.append(author)

            # etal for the person group
            if first(raw_parser.etal(group)):
                author = {}
                author['etal'] = True
                set_if_value(author, "group-type", author_type)
                authors.append(author)

        # Check for collab tag not wrapped in a person-group for backwards compatibility
        if len(person_group) == 0:
            collab_tags = raw_parser.collab(tag)
            for collab_tag in collab_tags:
                author = {}
                set_if_value(author, "group-type", "author")
                set_if_value(author, "collab", node_contents_str(collab_tag))

                if len(author) > 0:
                    authors.append(author)

        if len(authors) > 0:
            ref['authors'] = authors

        set_if_value(ref, "volume", node_text(first(raw_parser.volume(tag))))
        set_if_value(ref, "issue", node_text(first(raw_parser.issue(tag))))
        set_if_value(ref, "fpage", node_text(first(raw_parser.fpage(tag))))
        set_if_value(ref, "lpage", node_text(first(raw_parser.lpage(tag))))
        set_if_value(ref, "collab", node_text(first(raw_parser.collab(tag))))
        set_if_value(ref, "publisher_loc", node_text(first(raw_parser.publisher_loc(tag))))
        set_if_value(ref, "publisher_name", node_text(first(raw_parser.publisher_name(tag))))
        set_if_value(ref, "edition", node_contents_str(first(raw_parser.edition(tag))))
        set_if_value(ref, "version", node_contents_str(first(raw_parser.version(tag))))
        set_if_value(ref, "chapter-title", node_contents_str(first(raw_parser.chapter_title(tag))))
        set_if_value(ref, "comment", node_text(first(raw_parser.comment(tag))))
        set_if_value(ref, "data-title", node_contents_str(first(raw_parser.data_title(tag))))
        set_if_value(ref, "conf-name", node_text(first(raw_parser.conf_name(tag))))

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
        component_doi = doi_uri_to_doi(node_text(first(raw_parser.article_id(tag, pub_id_type= "doi"))))
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
                component_doi = doi_uri_to_doi(node_text(object_id_tag))

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
                 "boxed-text", "app"]

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

        component = OrderedDict()

        # Component type is the tag's name
        ctype = tag.name

        # First find the doi if present
        component_doi = extract_component_doi(tag, nodenames)
        if component_doi is None:
            continue
        else:
            component['doi'] = doi_uri_to_doi(component_doi)
            component['doi_url'] = doi_to_doi_uri(component['doi'])

        copy_attribute(tag.attrs, 'id', component)

        if(ctype == "sub-article"):
            title_tag = raw_parser.article_title(tag)
        elif(ctype == "boxed-text"):
            title_tag = title_tag_inspected(tag, tag.name, direct_sibling_only=True)
            if not title_tag:
                title_tag = title_tag_inspected(tag, "caption", "boxed-text")
            # New kitchen sink has boxed-text inside app tags, tag the sec tag title if so
            #  but do not take it if there is a caption
            if (not title_tag and tag.parent and tag.parent.name in ["sec", "app"]
                and not caption_tag_inspected(tag, tag.name)):
                title_tag = title_tag_inspected(tag.parent, tag.parent.name, direct_sibling_only=True)
        else:
            title_tag = raw_parser.title(tag)

        if title_tag:
            component['title'] = node_text(title_tag)
            component['full_title'] = node_contents_str(title_tag)

        if ctype == "boxed-text":
            label_tag = label_tag_inspected(tag, "boxed-text")
        else:
            label_tag = raw_parser.label(tag)

        if label_tag:
            component['label'] = node_text(label_tag)
            component['full_label'] = node_contents_str(label_tag)

        if raw_parser.caption(tag):
            first_paragraph = first(paragraphs(raw_parser.caption(tag)))
            if first_paragraph and not starts_with_doi(first_paragraph):
                # Remove the supplementary tag from the paragraph if present
                #  fixes a problem with the new kitchen sink of caption within caption tag
                paragraph_tag_copy = duplicate_tag(first_paragraph)
                if raw_parser.supplementary_material(paragraph_tag_copy):
                    paragraph_tag_copy = remove_tag_from_tag(paragraph_tag_copy, 'supplementary-material')
                if node_text(paragraph_tag_copy).strip() != '':
                    component['caption'] = node_text(paragraph_tag_copy)
                    component['full_caption'] = node_contents_str(paragraph_tag_copy)


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
                        node_text(first(raw_parser.licence_p(permissions_tag)))
                    permissions_item['full_license'] = \
                        node_contents_str(first(raw_parser.licence_p(permissions_tag)))

                component['permissions'].append(permissions_item)

        if raw_parser.contributors(tag):
            component['contributors'] = []
            for contributor_tag in raw_parser.contributors(tag):
                component['contributors'].append(format_contributor(contributor_tag, soup))

        # There are only some parent tags we care about for components
        #  and only check two levels of parentage
        parent_nodenames = ["sub-article", "fig-group", "fig", "boxed-text", "table-wrap", "app", "media"]
        parent_tag = first_parent(tag, parent_nodenames)

        if parent_tag:

            # For fig-group we actually want the first fig of the fig-group as the parent
            acting_parent_tag = component_acting_parent_tag(parent_tag, tag)

            # Only counts if the acting parent tag has a DOI
            if (acting_parent_tag and \
               extract_component_doi(acting_parent_tag, parent_nodenames) is not None):

                component['parent_type'] = acting_parent_tag.name
                component['parent_ordinal'] = tag_ordinal(acting_parent_tag)
                component['parent_sibling_ordinal'] = tag_details_sibling_ordinal(acting_parent_tag)
                component['parent_asset'] = tag_details_asset(acting_parent_tag)

            # Look for parent parent, if available
            parent_parent_tag = first_parent(parent_tag, parent_nodenames)

            if parent_parent_tag:

                acting_parent_tag = component_acting_parent_tag(parent_parent_tag, parent_tag)

                if (acting_parent_tag and \
                   extract_component_doi(acting_parent_tag, parent_nodenames) is not None):
                    component['parent_parent_type'] = acting_parent_tag.name
                    component['parent_parent_ordinal'] = tag_ordinal(acting_parent_tag)
                    component['parent_parent_sibling_ordinal'] = tag_details_sibling_ordinal(acting_parent_tag)
                    component['parent_parent_asset'] = tag_details_asset(acting_parent_tag)

        content = ""
        for p_tag in extract_nodes(tag, "p"):
            if content != "":
                # Add a space before each new paragraph for now
                content = content + " "
            content = content + node_text(p_tag)

        if(content != ""):
            component['content'] = content

        # mime type
        media_tag = None
        if(ctype == "media"):
            media_tag = tag
        elif(ctype == "supplementary-material"):
            media_tag = first(raw_parser.media(tag))
        if media_tag:
            component['mimetype'] = media_tag.get("mimetype")
            component['mime-subtype'] = media_tag.get("mime-subtype")

        if(len(component) > 0):
            component['article_doi'] = article_doi
            component['type'] = ctype
            component['position'] = position

            # Ordinal is based on all tags of the same type even if they have no DOI
            component['ordinal'] = tag_ordinal(tag)
            component['sibling_ordinal'] = tag_details_sibling_ordinal(tag)
            component['asset'] = tag_details_asset(tag)
            #component['ordinal'] = position_by_type[ctype]

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
            if 'id' not in tag.attrs:
                continue
            if tag['id'] not in cor:
                cor[tag['id']] = []
            if raw_parser.email(tag):
                # Multiple email addresses possible
                for email_tag in raw_parser.email(tag):
                    cor[tag['id']].append(node_contents_str(email_tag))
            elif raw_parser.phone(tag):
                # Look for a phone number
                cor[tag['id']].append(node_contents_str(first(raw_parser.phone(tag))))

    return cor


@nullify
def author_notes(soup):
    """
    Find the fn tags included in author-notes
    """
    author_notes = []

    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = raw_parser.fn(author_notes_section)
        for tag in fn_nodes:
            if 'fn-type' in tag.attrs:
                if(tag['fn-type'] != 'present-address'):
                    author_notes.append(node_text(tag))

    return author_notes

@nullify
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

@nullify
def competing_interests(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    competing_interests_section = extract_nodes(soup, "fn-group", attr="content-type", value="competing-interest")
    if not competing_interests_section:
        return None
    fn = extract_nodes(first(competing_interests_section), "fn")
    interests = footnotes(fn, fntype_filter)

    return interests

@nullify
def present_addresses(soup):
    notes = []
    fntype_filter = 'present-address'
    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = extract_nodes(author_notes_section, "fn")
        notes = footnotes(fn_nodes, fntype_filter)
    return notes

@nullify
def other_foot_notes(soup):
    notes = []
    fntype_filter = ['fn', 'other']
    author_notes_section = raw_parser.author_notes(soup)
    if author_notes_section:
        fn_nodes = extract_nodes(author_notes_section, "fn")
        notes = footnotes(fn_nodes, fntype_filter)
    return notes


@nullify
def author_contributions(soup, fntype_filter):
    """
    Find the fn tags included in the competing interest
    """

    author_contributions_section = extract_nodes(soup, "fn-group", attr="content-type", value="author-contribution")
    if not author_contributions_section:
        return None
    fn = extract_nodes(first(author_contributions_section), "fn")
    cons = footnotes(fn, fntype_filter)

    return cons

def footnotes(fn, fntype_filter):
    notes = []
    for f in fn:
        try:
            if fntype_filter is None or f['fn-type'] in fntype_filter:
                notes.append({
                    'id': f['id'],
                    'text': clean_whitespace(node_contents_str(f)),
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
    award_groups = []

    funding_group_section = extract_nodes(soup, "funding-group")
    # counter for auto generated id values, if required
    generated_id_counter = 1
    for fg in funding_group_section:

        award_group_tags = extract_nodes(fg, "award-group")

        for ag in award_group_tags:
            if 'id' in ag.attrs:
                ref = ag['id']
            else:
                # hack: generate and increment an id value none is available
                ref = "award-group-{id}".format(id=generated_id_counter)
                generated_id_counter += 1

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
            award_group_by_ref = {}
            award_group_by_ref[ref] = award_group
            award_groups.append(award_group_by_ref)

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

        institution = node_text(first(extract_nodes(t, "institution")))
        surname = node_text(first(extract_nodes(t, "surname")))
        given_names = node_text(first(extract_nodes(t, "given-names")))
        string_name = node_text(first(raw_parser.string_name(t)))
        # Concatenate name and institution values if found
        #  while filtering out excess whitespace
        if(given_names):
            principal_award_recipient_text += given_names
        if(principal_award_recipient_text != ""):
            principal_award_recipient_text += " "
        if(surname):
            principal_award_recipient_text += surname
        if(institution):
            principal_award_recipient_text += institution
        if(string_name):
            principal_award_recipient_text += string_name

        award_group_principal_award_recipient.append(principal_award_recipient_text)
    return award_group_principal_award_recipient

def object_id_doi(tag, parent_tag_name=None):
    """DOI in an object-id tag found inside the tag"""
    doi = None
    object_id = None
    object_ids = raw_parser.object_id(tag, "doi")
    if object_ids:
        object_id = first([id_ for id_ in object_ids])
    if parent_tag_name and object_id and object_id.parent.name != parent_tag_name:
        object_id = None
    if object_id:
        doi = node_contents_str(object_id)
    return doi

def title_tag_inspected(tag, parent_tag_name=None, p_parent_tag_name=None, direct_sibling_only=False):
    """Extract the title tag and sometimes inspect its parents"""

    title_tag = None
    if direct_sibling_only is True:
        for sibling_tag in tag:
            if sibling_tag.name and sibling_tag.name == "title":
                title_tag = sibling_tag
    else:
        title_tag = raw_parser.title(tag)

    if parent_tag_name and p_parent_tag_name:
        if (title_tag and title_tag.parent.name and title_tag.parent.parent.name
            and title_tag.parent.name == parent_tag_name
            and title_tag.parent.parent.name == p_parent_tag_name):
            pass
        else:
            title_tag = None

    return title_tag

def title_text(tag, parent_tag_name=None, p_parent_tag_name=None, direct_sibling_only=False):
    """Extract the text of a title tag and sometimes inspect its parents"""
    title = None

    title_tag = title_tag_inspected(tag, parent_tag_name, p_parent_tag_name, direct_sibling_only)

    if title_tag:
        title = node_contents_str(title_tag)
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
        label = node_contents_str(label_tag)
    return label

def full_title_json(soup):
    return xml_to_html(True, full_title(soup))

def impact_statement_json(soup):
    return xml_to_html(True, impact_statement(soup))

def acknowledgements_json(soup):
    if raw_parser.acknowledgements(soup):
        return body_block_content_render(raw_parser.acknowledgements(soup))[0].get("content")
    else:
        return None

def keywords_json(soup, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)
    return list(map(convert, full_keywords(soup)))

def research_organism_json(soup, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)

    do_not_include = ['none', 'other']
    research_organisms = list(filter(lambda term: term and term.lower() not in do_not_include, full_research_organism(soup)))
    return list(map(convert, research_organisms))

def body(soup, remove_key_info_box=False, base_url=None):

    body_content = []

    raw_body = raw_parser.article_body(soup)

    if raw_body:

        body_content = render_raw_body(raw_body,
                                       remove_key_info_box=remove_key_info_box,
                                       base_url=base_url)
    return body_content

def body_json(soup, base_url=None):
    """ Get body json and then alter it with section wrapping and removing boxed-text """
    body_content = body(soup, remove_key_info_box=True, base_url=base_url)
    # Wrap in a section if the first block is not a section
    if (body_content and len(body_content) > 0 and "type" in body_content[0]
        and body_content[0]["type"] != "section"):
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
    body_content_rewritten = elifetools.json_rewrite.rewrite_json("body_json", soup, body_content)
    return body_content_rewritten

def render_raw_body(tag, remove_key_info_box=False, base_url=None):
    body_content = []
    body_tags = body_blocks(tag)
    for tag in body_tags:
        if tag.name == "boxed-text":
            # Extract the text of the first child tag for comparison, if present
            first_node_text = None
            if tag.children:
                first_node_text = node_text(first(list(tag.children)))

            if (remove_key_info_box is True and first_node_text
                and "related" in first_node_text.lower()):
                # Skip this tag
                continue

            elif not raw_parser.title(tag) and not raw_parser.label(tag):
                # Collapse boxed-text here if it has no title or label
                for boxed_tag in tag:
                    tag_blocks = body_block_content_render(boxed_tag, base_url=base_url)
                    for tag_block in tag_blocks:
                        if tag_block != {}:
                            body_content.append(tag_block)
            else:
                # Add it
                tag_blocks = body_block_content_render(tag, base_url=base_url)
                for tag_block in tag_blocks:
                    if tag_block != {}:
                        body_content.append(tag_block)
        else:

            tag_blocks = body_block_content_render(tag, base_url=base_url)
            #tag_content = body_block_content_render(tag)
            for tag_block in tag_blocks:
                if tag_block != {}:
                    body_content.append(tag_block)

    return body_content

def body_block_nodenames():
    return ["sec", "p", "table-wrap", "boxed-text",
            "disp-formula", "disp-quote", "fig", "fig-group", "list", "media", "code"]

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
    if tag.name not in ["p", "fig", "table-wrap", "list", "media", "disp-quote", "code"]:
        for child_tag in tag:
            if not(hasattr(child_tag, 'name')):
                continue

            if child_tag.name == "p":
                # Ignore paragraphs that start with DOI:
                if node_text(child_tag) and len(remove_doi_paragraph([child_tag])) <= 0:
                    continue
                for block_content in body_block_paragraph_render(child_tag, base_url=base_url):
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
                for block_content in body_block_content_render(child_tag, recursive=True, base_url=base_url):
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
    convert = lambda xml_string: xml_to_html(html_flag, xml_string, base_url)

    block_content_list = []

    tag_content_content = []
    nodenames = body_block_nodenames()

    paragraph_content = u''
    for child_tag in p_tag:

        if child_tag.name is None or body_block_content(child_tag) == {}:
            paragraph_content = paragraph_content + unicode_value(child_tag)

        else:
            # Add previous paragraph content first
            if paragraph_content.strip() != '':
                tag_content_content.append(body_block_paragraph_content(convert(paragraph_content)))
                paragraph_content = u''

        if child_tag.name is not None and body_block_content(child_tag) != {}:
            for block_content in body_block_content_render(child_tag, base_url=base_url):
                if block_content != {}:
                    tag_content_content.append(block_content)
    # finish up
    if paragraph_content.strip() != '':
        tag_content_content.append(body_block_paragraph_content(convert(paragraph_content)))

    if len(tag_content_content) > 0:
        for block_content in tag_content_content:
            block_content_list.append(block_content)

    return block_content_list

def body_block_caption_render(caption_tags, base_url=None):
    """fig and media tag captions are similar so use this common function"""
    caption_content = []
    supplementary_material_tags = []

    for block_tag in remove_doi_paragraph(caption_tags):
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
    if text and text != '':
        tag_content["type"] = "paragraph"
        tag_content["text"] = clean_whitespace(text)
    return tag_content

def body_block_title_label_caption(tag_content, title_value, label_value,
                                   caption_content, set_caption=True, prefer_title=False, prefer_label=False):
    """set the title, label and caption values in a consistent way

    set_caption: insert a "caption" field
    prefer_title: when only one value is available, set title rather than label. If False, set label rather than title"""
    set_if_value(tag_content, "label", rstrip_punctuation(label_value))
    set_if_value(tag_content, "title", title_value)
    if set_caption is True and caption_content and len(caption_content) > 0:
        tag_content["caption"] = caption_content
    if prefer_title:
        if "title" not in tag_content and label_value:
            set_if_value(tag_content, "title", label_value)
            del(tag_content["label"])
    if prefer_label:
        if "label" not in tag_content and title_value:
            set_if_value(tag_content, "label", rstrip_punctuation(title_value))
            del(tag_content["title"])

def body_block_content(tag, html_flag=True, base_url=None):
    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string, base_url)

    tag_content = OrderedDict()

    if not(hasattr(tag, 'name')):
        return OrderedDict()

    if tag.name == "sec":
        tag_content["type"] = "section"
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "title", convert(title_text(tag, direct_sibling_only=True)))

    elif tag.name == "boxed-text":
        tag_content["type"] = "box"
        set_if_value(tag_content, "doi", doi_uri_to_doi(object_id_doi(tag, tag.name)))
        set_if_value(tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags, base_url=base_url)
        body_block_title_label_caption(tag_content, title_value, label_value, caption_content, set_caption=False, prefer_title=True)

    elif tag.name == "p":
        tag_content["type"] = "paragraph"

        # Remove unwanted nested tags
        unwanted_tag_names = body_block_nodenames()
        tag_copy = duplicate_tag(tag)
        tag_copy = remove_tag_from_tag(tag_copy, unwanted_tag_names)

        if node_contents_str(tag_copy):
            tag_content["text"] = convert(clean_whitespace(node_contents_str(tag_copy)))

    elif tag.name == "disp-quote":
        if tag.get("content-type") and tag.get("content-type") == "editor-comment":
            tag_content["type"] = "excerpt"
            block_array_name = "content"
        else:
            tag_content["type"] = "quote"
            block_array_name = "text"
        for child_tag in tag:
            if body_block_content(child_tag) != {}:
                if block_array_name not in tag_content:
                    tag_content[block_array_name] = []
                tag_content[block_array_name].append(body_block_content(child_tag, base_url=base_url))

    elif tag.name == "table-wrap":
        # figure wrap
        tag_content["type"] = "figure"
        tag_content["assets"] = []
        asset_tag_content = OrderedDict()

        asset_tag_content["type"] = "table"
        set_if_value(asset_tag_content, "doi", doi_uri_to_doi(object_id_doi(tag, tag.name)))
        set_if_value(asset_tag_content, "id", tag.get("id"))
        title_value = convert(title_text(tag, "caption", tag.name))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if caption_tag_inspected(tag, tag.name):
            caption_tags = body_blocks(caption_tag_inspected(tag, tag.name))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags, base_url=base_url)

        body_block_title_label_caption(asset_tag_content, title_value, label_value, caption_content, set_caption=True)

        tables = raw_parser.table(tag)
        asset_tag_content["tables"] = []
        for table in tables:
            # Add the table tag back for now
            table_content = '<table>' + node_contents_str(table) + '</table>'
            asset_tag_content["tables"].append(convert(table_content))

        table_wrap_foot = raw_parser.table_wrap_foot(tag)
        for foot_tag in table_wrap_foot:
            footnotes = []
            for fn_tag in raw_parser.fn(foot_tag):
                footnote_content = OrderedDict()
                # Only set id if a label is present
                if label(fn_tag, fn_tag.name):
                    set_if_value(footnote_content, "id", fn_tag.get("id"))
                    set_if_value(footnote_content, "label", rstrip_punctuation(label(fn_tag, fn_tag.name)))
                for p_tag in raw_parser.paragraph(fn_tag):
                    if "text" not in footnote_content:
                        footnote_content["text"] = []
                    footnote_blocks = body_block_content_render(p_tag, base_url=base_url)
                    for footnote_block in footnote_blocks:
                        if footnote_block != {}:
                            footnote_content["text"].append(footnote_block)

                if "footnotes" not in asset_tag_content:
                    asset_tag_content["footnotes"] = []
                asset_tag_content["footnotes"].append(footnote_content)

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(supplementary_material_tags, base_url=base_url)
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

        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "label", label(tag, tag.name))

        math_tag = first(raw_parser.math(tag))
        # Add the math tag back for now
        math_content = '<math>' + node_contents_str(math_tag) + '</math>'
        tag_content["mathml"] = convert(math_content)

    elif tag.name == "fig":
        # figure wrap
        tag_content["type"] = "figure"
        tag_content["assets"] = []
        asset_tag_content = OrderedDict()

        asset_tag_content["type"] = "image"
        set_if_value(asset_tag_content, "doi", doi_uri_to_doi(object_id_doi(tag, tag.name)))
        set_if_value(asset_tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag, u"caption", u"fig"))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags, base_url=base_url)
        body_block_title_label_caption(asset_tag_content, title_value, label_value, caption_content, set_caption=True)

        if raw_parser.graphic(tag):
            image_content = {}
            graphic_tags = raw_parser.graphic(tag)
            if graphic_tags:
                copy_attribute(first(graphic_tags).attrs, 'xlink:href', image_content, 'uri')
                if "uri" in image_content:
                    # todo!! alt
                    set_if_value(image_content, "alt", "")
            if len(image_content) > 0:
                asset_tag_content["image"] = image_content

        # license or attribution
        attributions = []
        if raw_parser.attrib(tag):
            for attrib_tag in raw_parser.attrib(tag):
                attributions.append(node_contents_str(attrib_tag))
        if raw_parser.licence(tag) and raw_parser.licence_p(tag):
            for attrib_tag in raw_parser.licence_p(tag):
                attributions.append(node_contents_str(attrib_tag))
        if len(attributions) > 0:
            asset_tag_content["image"]["attribution"] = []
            for attrib_string in attributions:
                asset_tag_content["image"]["attribution"].append(convert(attrib_string))

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(supplementary_material_tags, base_url=base_url)
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
        set_if_value(asset_tag_content, "doi", doi_uri_to_doi(object_id_doi(tag, tag.name)))
        set_if_value(asset_tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag, "caption", tag.name))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags, base_url=base_url)
        body_block_title_label_caption(asset_tag_content, title_value, label_value, caption_content, set_caption=True)

        set_if_value(asset_tag_content, "uri", tag.get('xlink:href'))
        if "uri" in asset_tag_content and asset_tag_content["uri"].endswith('.gif'):
            asset_tag_content["autoplay"] = True
            asset_tag_content["loop"] = True

        # sourceData
        if supplementary_material_tags and len(supplementary_material_tags) > 0:
            source_data = body_block_supplementary_material_render(supplementary_material_tags, base_url=base_url)
            if len(source_data) > 0:
                asset_tag_content["sourceData"] = source_data

        # add the asset
        tag_content["assets"].append(asset_tag_content)

    elif tag.name == "fig-group":
        for fig_tag in extract_nodes(tag, ["fig", "media"]):
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
        set_if_value(tag_content, "doi", doi_uri_to_doi(object_id_doi(tag, tag.name)))
        set_if_value(tag_content, "id", tag.get("id"))

        title_value = convert(title_text(tag, "caption", tag.name))
        label_value = label(tag, tag.name)

        caption_content = None
        supplementary_material_tags = None
        if raw_parser.caption(tag):
            caption_tags = body_blocks(raw_parser.caption(tag))
            caption_content, supplementary_material_tags = body_block_caption_render(caption_tags, base_url=base_url)
        body_block_title_label_caption(tag_content, title_value, label_value, caption_content, set_caption=True, prefer_label=True)

        if raw_parser.media(tag):
            media_tag = first(raw_parser.media(tag))
            # If a mimetype contains a slash just use it, otherwise concatenate a value
            if media_tag.get("mimetype") and "/" in media_tag.get("mimetype"):
                tag_content["mediaType"] = media_tag.get("mimetype")
            elif media_tag.get("mimetype") and media_tag.get("mime-subtype"):
                tag_content["mediaType"] = media_tag.get("mimetype") + "/" + media_tag.get("mime-subtype")

            copy_attribute(media_tag.attrs, 'xlink:href', tag_content, 'uri')
            copy_attribute(media_tag.attrs, 'xlink:href', tag_content, 'filename')

    elif tag.name == "list":
        tag_content["type"] = "list"
        if tag.get("list-type"):
            if tag.get("list-type") == "simple":
                tag_content["prefix"] = "none"
            elif tag.get("list-type") == "order":
                tag_content["prefix"] = "number"
            else:
                tag_content["prefix"] = tag.get("list-type")
        else:
            tag_content["prefix"] = "none"

        for list_item_tag in raw_parser.list_item(tag):
            # Do not add list items of child lists to the main list by skipping them here first
            if list_item_tag.parent != tag:
                continue

            if "items" not in tag_content:
                tag_content["items"] = []

            if len(body_block_content_render(list_item_tag)) > 0:
                for list_item in body_block_content_render(list_item_tag, base_url=base_url):
                    # Note: wrapped inside another list to pass the current article json schema
                    if list_item != {}:
                        list_item_content = list_item["content"]
                        tag_content["items"].append(list_item_content)
                    else:
                        tag_content["items"].append(node_contents_str(list_item_tag))

    elif tag.name == "app":
        set_if_value(tag_content, "id", tag.get("id"))
        set_if_value(tag_content, "doi", doi_uri_to_doi(object_id_doi(tag, tag.name)))
        set_if_value(tag_content, "title", convert(title_text(tag, direct_sibling_only=True)))

    elif tag.name == "code":
        tag_content["type"] = "code"
        set_if_value(tag_content, "code", node_contents_str(tag))

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

    first_sibling_node = firstnn(soup.find_all())

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
    article_id_tag = first(raw_parser.article_id(tag, "doi"))
    if article_id_tag:
        doi = article_id_tag.text
    return doi

def decision_letter(soup):

    sub_article_content = OrderedDict()
    sub_article = raw_parser.decision_letter(soup)

    if sub_article:
        if sub_article_doi(sub_article):
            sub_article_content["doi"] = doi_uri_to_doi(sub_article_doi(sub_article))
        raw_body = raw_parser.article_body(sub_article)
    else:
        raw_body = None

    # description
    if raw_body:
        # Description will be the first boxed-text tag
        if raw_parser.boxed_text(raw_body):
            sub_article_content["description"] = []
            boxed_text_description = first(raw_parser.boxed_text(raw_body))
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
        body_content_rewritten = elifetools.json_rewrite.rewrite_json("body_json", soup, body_content)
        if len(body_content) > 0:
            sub_article_content["content"] = body_content

    return elifetools.json_rewrite.rewrite_json("decision_letter_json", soup, sub_article_content)


def author_response(soup):

    sub_article_content = OrderedDict()
    sub_article = raw_parser.author_response(soup)

    if sub_article:
        if sub_article_doi(sub_article):
            sub_article_content["doi"] = doi_uri_to_doi(sub_article_doi(sub_article))
        raw_body = raw_parser.article_body(sub_article)
    else:
        raw_body = None

    # content
    if raw_body:
        body_content = render_raw_body(raw_body)
        body_content_rewritten = elifetools.json_rewrite.rewrite_json("body_json", soup, body_content)
        if len(body_content) > 0:
            sub_article_content["content"] = body_content

    return sub_article_content


def render_abstract_json(abstract_tag):
    abstract_json = OrderedDict()
    set_if_value(abstract_json, "doi", doi_uri_to_doi(object_id_doi(abstract_tag)))
    for child_tag in remove_doi_paragraph(body_blocks(abstract_tag)):
        if body_block_content(child_tag) != {}:
            if "content" not in abstract_json:
                 abstract_json["content"] = []
            abstract_json["content"].append(body_block_content(child_tag))
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
    abstract_json = None
    for tag in abstract_tags:
        abstract_json = render_abstract_json(tag)
    return abstract_json


def author_affiliations(author, html_flag=True):
    """compile author affiliations for json output"""

    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)

    affilations = []

    if author.get("affiliations"):
        for affiliation in author.get("affiliations"):
            affiliation_json = OrderedDict()
            affiliation_json["name"] = []
            if affiliation.get("dept"):
                affiliation_json["name"].append(convert(affiliation.get("dept")))
            if affiliation.get("institution") and affiliation.get("institution").strip() != '':
                affiliation_json["name"].append(convert(affiliation.get("institution")))
            # Remove if empty
            if affiliation_json["name"] == []:
                del affiliation_json["name"]

            if ((affiliation.get("city") and affiliation.get("city").strip() != '')
                or affiliation.get("country") and affiliation.get("country").strip() != ''):
                affiliation_address = OrderedDict()
                affiliation_address["formatted"] = []
                affiliation_address["components"] = OrderedDict()
                if affiliation.get("city") and affiliation.get("city").strip() != '':
                    affiliation_address["formatted"].append(affiliation.get("city"))
                    affiliation_address["components"]["locality"] = []
                    affiliation_address["components"]["locality"].append(affiliation.get("city"))
                if affiliation.get("country") and affiliation.get("country").strip() != '':
                    affiliation_address["formatted"].append(affiliation.get("country"))
                    affiliation_address["components"]["country"] = affiliation.get("country")
                # Add if not empty
                if affiliation_address != {}:
                    affiliation_json["address"] = affiliation_address

            # Add if not empty
            if affiliation_json != {}:
                affilations.append(affiliation_json)

    if affilations != []:
        return affilations
    else:
        return None

def author_phone_numbers(author, correspondence):
    phone_numbers = []
    if correspondence and "phone" in author.get("references"):
        for ref_id in author["references"]["phone"]:
            for corr_ref_id, data in iteritems(correspondence):
                if ref_id == corr_ref_id:
                    for phone_number in data:
                        phone_numbers.append(phone_number)
    if phone_numbers != []:
        return phone_numbers
    else:
        return None

def phone_number_json(phone):
    if phone:
        phone = re.sub(r'[\(\) -]', '', phone)
    return phone

def author_phone_numbers_json(author, correspondence):
    phone_numbers = author_phone_numbers(author, correspondence)
    if phone_numbers:
        phone_numbers = list(map(phone_number_json, phone_numbers))
    return phone_numbers


def author_email_addresses(author, correspondence):
    email_addresses = []

    if correspondence and "email" in author.get("references"):
        for ref_id in author["references"]["email"]:
            for corr_ref_id, data in iteritems(correspondence):
                if ref_id == corr_ref_id:
                    for email_address in data:
                        email_addresses.append(email_address)

    # Also look in affiliations for inline email tags
    if author.get("affiliations"):
        for affiliation in author.get("affiliations"):
            if "email" in affiliation and affiliation["email"] not in email_addresses:
                email_addresses.append(affiliation["email"])

    # Also look at the author attributes
    if author.get("corresp") and author.get("email"):
        email_addresses = author["email"]

    if email_addresses != []:
        return email_addresses
    else:
        return None

def author_contribution(author, contributions):
    contribution_text = None

    if "contribution" in author.get("references"):
        for ref_id in author["references"]["contribution"]:
            if contributions:
                for contribution in contributions:
                    if contribution.get("text") and contribution.get("id") == ref_id:
                        contribution_text = (
                            contribution.get("text").replace('<p>', '').replace('</p>', ''))

    return contribution_text

def author_competing_interests(author, competing_interests):
    competing_interests_text = None

    if "competing-interest" in author.get("references"):
        for ref_id in author["references"]["competing-interest"]:
            if competing_interests:
                for competing_interest in competing_interests:
                    if competing_interest.get("text") and competing_interest.get("id") == ref_id:
                        competing_interests_text = (
                            competing_interest.get("text").replace('<p>', '').replace('</p>', ''))
                        # Strip labels
                        p = re.compile('<label>.*</label>')
                        competing_interests_text = p.sub('', competing_interests_text)

    return competing_interests_text

def author_equal_contribution(author, equal_contributions_map):
    equal_contributions = []

    if "equal-contrib" in author.get("references"):
        if "equal-contrib" in author["references"]:
            for ref_id in author["references"]["equal-contrib"]:
                if ref_id in equal_contributions_map:
                    equal_contributions.append(equal_contributions_map[ref_id])
    if equal_contributions != []:
        return equal_contributions
    else:
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
                    text = re.sub(u'<label>.*</label>', '', present_address.get("text"))
                    text = (
                        text.replace('<p>', '').replace('</p>', ''))
                    # Format as a JSON address
                    address = OrderedDict()
                    address['formatted'] = []
                    address['formatted'].append(text)
                    address['components'] = OrderedDict()
                    address['components']['streetAddress'] = []
                    address['components']['streetAddress'].append(text)
                    postal_addresses.append(address)
    if postal_addresses != []:
        return postal_addresses
    else:
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
                    text = re.sub(u'<label>.*</label>', '', foot_note.get("text"))
                    text = (
                        text.replace('<p>', '').replace('</p>', ''))
                    # For authors json do not include footnotes regarding deceased
                    if 'deceased' not in text.lower():
                        foot_notes.append(text)
    if foot_notes != []:
        return foot_notes
    else:
        return None

def author_json_details(author, author_json, contributions, correspondence,
                        competing_interests, equal_contributions_map, present_address_data,
                        foot_notes_data, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)

    """add more author json"""
    if author_affiliations(author):
        author_json["affiliations"] = author_affiliations(author)

    if author.get("references"):
        # foot notes or additionalInformation
        if author_foot_notes(author, foot_notes_data):
            author_json["additionalInformation"] = author_foot_notes(author, foot_notes_data)

        # email
        if author_email_addresses(author, correspondence):
            author_json["emailAddresses"] = author_email_addresses(author, correspondence)

        # phone
        if author_phone_numbers(author, correspondence):
            author_json["phoneNumbers"] = author_phone_numbers_json(author, correspondence)

        # contributions
        if author_contribution(author, contributions):
            author_json["contribution"] = convert(author_contribution(author, contributions))

        # competing interests
        if author_competing_interests(author, competing_interests):
            author_json["competingInterests"] = convert(
                author_competing_interests(author, competing_interests))

        # equal-contributions
        if author_equal_contribution(author, equal_contributions_map):
            author_json["equalContributionGroups"] = author_equal_contribution(author, equal_contributions_map)

        # postalAddress
        if author_present_address(author, present_address_data):
            author_json["postalAddresses"] = author_present_address(author, present_address_data)

    return author_json

def author_person(author, contributions, correspondence, competing_interests,
                  equal_contributions_map, present_address_data, foot_notes_data):
    author_json = OrderedDict()
    author_json["type"] = "person"
    author_name = OrderedDict()
    author_name["preferred"] = author_preferred_name(
        author.get("surname"), author.get("given-names"), author.get("suffix"))
    author_name["index"] = author_index_name(
        author.get("surname"), author.get("given-names"), author.get("suffix"))
    author_json["name"] = author_name
    if author.get("orcid"):
        author_json["orcid"] = orcid_uri_to_orcid(author.get("orcid"))
    if author.get("deceased"):
        author_json["deceased"] = True
    if author.get("role"):
        author_json["role"] = xml_to_html(True, author.get("role"))
    if author.get("bio"):
        author_json["biography"] = author.get("bio")
    author_json = author_json_details(author, author_json, contributions, correspondence,
                                      competing_interests, equal_contributions_map,
                                      present_address_data, foot_notes_data)

    return author_json


def author_group(author, contributions, correspondence, competing_interests,
                 equal_contributions_map, present_address_data, foot_notes_data):
    author_json = OrderedDict()
    author_json["type"] = "group"
    author_json["name"] = author.get("collab")

    author_json = author_json_details(author, author_json, contributions, correspondence,
                                      competing_interests, equal_contributions_map,
                                      present_address_data, foot_notes_data)

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
        if author.get("collab"):
            collab_map[author.get("collab")] = author.get("group-author-key")
    return collab_map

def map_equal_contributions(contributors):
    """assign numeric values to each unique equal-contrib id"""
    equal_contribution_map = {}
    equal_contribution_keys = []
    for contributor in contributors:
        if contributor.get("references") and "equal-contrib" in contributor.get("references"):
            for key in contributor["references"]["equal-contrib"]:
                if key not in equal_contribution_keys:
                    equal_contribution_keys.append(key)
    # Do a basic sort
    equal_contribution_keys = sorted(equal_contribution_keys)
    # Assign keys based on sorted values
    for i, equal_contribution_key in enumerate(equal_contribution_keys):
        equal_contribution_map[equal_contribution_key] = i+1
    return equal_contribution_map

def editors_json(soup):
    editors_json_data = []
    contributors_data = contributors(soup, "full")
    for contributor in contributors_data:
        editor_json = None
        if contributor["type"] == "editor":
            editor_json = author_person(contributor, None, None, None, None, None, None)
        if editor_json:
            editors_json_data.append(editor_json)
    editors_json_data_rewritten = elifetools.json_rewrite.rewrite_json("editors_json", soup, editors_json_data)
    return editors_json_data_rewritten

def authors_json(soup):
    """authors list in article json format"""
    authors_json_data = []
    contributors_data = contributors(soup, "full")
    author_contributions_data = author_contributions(soup, None)
    author_competing_interests_data = competing_interests(soup, None)
    author_correspondence_data = full_correspondence(soup)
    authors_non_byline_data = authors_non_byline(soup)
    equal_contributions_map = map_equal_contributions(contributors_data)
    present_address_data = present_addresses(soup)
    foot_notes_data = other_foot_notes(soup)

    # First line authors builds basic structure
    for contributor in contributors_data:
        author_json = None
        if contributor["type"] == "author" and contributor.get("collab"):
            author_json = author_group(contributor, author_contributions_data,
                                       author_correspondence_data, author_competing_interests_data,
                                       equal_contributions_map, present_address_data,
                                       foot_notes_data)
        elif contributor.get("on-behalf-of"):
            author_json = author_on_behalf_of(contributor)
        elif contributor["type"] == "author" and not contributor.get("group-author-key"):
            author_json = author_person(contributor, author_contributions_data,
                                        author_correspondence_data, author_competing_interests_data,
                                        equal_contributions_map, present_address_data, foot_notes_data)

        if author_json:
            authors_json_data.append(author_json)

    # Second, add byline author data
    collab_map = collab_to_group_author_key_map(contributors_data)
    for contributor in [elem for elem in contributors_data if elem.get("group-author-key") and not elem.get("collab")]:
        for group_author in [elem for elem in authors_json_data if elem.get('type') == 'group']:
            group_author_key = None
            if group_author["name"] in collab_map:
                group_author_key = collab_map[group_author["name"]]
            if contributor.get("group-author-key") == group_author_key:
                author_json = author_person(contributor, author_contributions_data,
                                            author_correspondence_data, author_competing_interests_data,
                                            equal_contributions_map, present_address_data, foot_notes_data)
                if contributor.get("sub-group"):
                    if "groups" not in group_author:
                        group_author["groups"] = OrderedDict()
                    if contributor.get("sub-group") not in group_author["groups"]:
                        group_author["groups"][contributor.get("sub-group")] = []
                    group_author["groups"][contributor.get("sub-group")].append(author_json)
                else:
                    if "people" not in group_author:
                        group_author["people"] = []
                    group_author["people"].append(author_json)

    authors_json_data_rewritten = elifetools.json_rewrite.rewrite_json("authors_json", soup, authors_json_data)
    return authors_json_data_rewritten

def author_line(soup):
    """take preferred names from authors json and format them into an author line"""
    author_line = None
    authors_json_data = authors_json(soup)
    author_names = extract_author_line_names(authors_json_data)
    if len(author_names) > 0:
        author_line = format_author_line(author_names)
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
            author_names.append(unicode_value(author["name"]))
    return author_names

def format_author_line(author_names):
    """authorLine format depends on if there is 1, 2 or more than 2 authors"""
    author_line = None
    if not author_names:
        return author_line
    if len(author_names) <= 2:
        author_line = ", ".join(author_names)
    elif len(author_names) > 2:
        author_line = author_names[0] + " et al."
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
    else:
        return None

def references_pages_range(fpage=None, lpage=None):
    range = None
    if fpage and lpage:
        # use unichr(8211) for the hyphen because the schema is requiring it
        try:
            # Python 2
            range = fpage.strip() + unichr(8211) + lpage.strip()
        except NameError:
            # Python 3
            range = fpage.strip() + chr(8211) + lpage.strip()
    elif fpage:
        range = fpage.strip()
    elif lpage:
        range = lpage.strip()
    return range

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
                author_group_type = ref_author.get("group-type") + 's' + 'EtAl'
                etal_json = True
            elif "collab" in ref_author:
                author_group_type = ref_author.get("group-type") + 's'
                author_json = references_author_collab(ref_author)
            else:
                author_group_type = ref_author.get("group-type") + 's'
                author_json = references_author_person(ref_author)

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
        if ref_content.get("type") in ["conference-proceeding", "journal", "other",
                                           "periodical", "preprint", "report", "web"]:
            for author_type in ["authors", "authorsEtAl"]:
                set_if_value(ref_content, author_type, all_authors.get(author_type))
        elif ref_content.get("type") in ["book", "book-chapter"]:
            for author_type in ["authors", "authorsEtAl", "editors", "editorsEtAl"]:
                set_if_value(ref_content, author_type, all_authors.get(author_type))
        elif ref_content.get("type") in ["clinical-trial"]:
            # Always set as authors, once,  then add the authorsType
            for author_type in ["authors", "collaborators", "sponsors"]:
                if "authorsType" not in ref_content and all_authors.get(author_type):
                    set_if_value(ref_content, "authors", all_authors.get(author_type))
                    set_if_value(ref_content, "authorsEtAl", all_authors.get(author_type + "EtAl"))
                    ref_content["authorsType"] = author_type
        elif ref_content.get("type") in ["data", "software"]:
            for author_type in ["authors", "authorsEtAl",
                                "compilers", "compilersEtAl", "curators", "curatorsEtAl"]:
                set_if_value(ref_content, author_type, all_authors.get(author_type))
        elif ref_content.get("type") in ["patent"]:
            for author_type in ["inventors", "inventorsEtAl", "assignees", "assigneesEtAl"]:
                set_if_value(ref_content, author_type, all_authors.get(author_type))
        elif ref_content.get("type") in ["thesis"]:
            # Convert list to a non-list
            if all_authors.get("authors") and len(all_authors.get("authors")) > 0:
                ref_content["author"] = all_authors.get("authors")[0]
    return ref_content

def references_json(soup, html_flag=True):

    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)

    references_json = []
    for ref in refs(soup):
        ref_content = OrderedDict()

        # type
        if ref.get("publication-type") == "book" and (
            "chapter-title" in ref or "full_article_title" in ref):
            set_if_value(ref_content, "type", "book-chapter")
        elif ref.get("publication-type") == "confproc":
            set_if_value(ref_content, "type", "conference-proceeding")
        elif ref.get("publication-type") == "clinicaltrial":
            set_if_value(ref_content, "type", "clinical-trial")
        else:
            set_if_value(ref_content, "type", ref.get("publication-type"))

        set_if_value(ref_content, "id", ref.get("id"))

        (year_date, discriminator, year_in_press) = references_date(ref.get("year"))
        if not discriminator:
            set_if_value(ref_content, "date", ref.get("year-iso-8601-date"))
        if "date" not in ref_content:
            set_if_value(ref_content, "date", year_date)
            set_if_value(ref_content, "discriminator", discriminator)

        # accessed
        if ref.get("publication-type") in ["web"] and ref.get("iso-8601-date"):
            set_if_value(ref_content, "accessed", ref.get("iso-8601-date"))
            # Set the date to the year tag value if accessed is set and there is a year
            set_if_value(ref_content, "date", year_date)
            set_if_value(ref_content, "discriminator", discriminator)

        # authors and etal
        if ref.get("authors"):
            ref_content = references_json_authors(ref.get("authors"), ref_content)

        # titles
        if ref.get("publication-type") in ["journal", "confproc", "preprint", "periodical"]:
            set_if_value(ref_content, "articleTitle", ref.get("full_article_title"))
        elif ref.get("publication-type") in ["thesis", "clinicaltrial", "other"]:
            set_if_value(ref_content, "title", ref.get("full_article_title"))
        elif ref.get("publication-type") in ["book"]:
            set_if_value(ref_content, "bookTitle", ref.get("source"))
            if "bookTitle" not in ref_content:
                set_if_value(ref_content, "bookTitle", ref.get("full_article_title"))
        elif ref.get("publication-type") in ["software","data"]:
            set_if_value(ref_content, "title", ref.get("data-title"))
            if "title" not in ref_content:
                set_if_value(ref_content, "title", ref.get("source"))
        elif ref.get("publication-type") in ["patent", "web"]:
            set_if_value(ref_content, "title", ref.get("full_article_title"))
            if "title" not in ref_content:
                set_if_value(ref_content, "title", ref.get("comment"))
            if "title" not in ref_content:
                set_if_value(ref_content, "title", ref.get("uri"))
        # Finally try to extract from source if a title is not found
        if ("title" not in ref_content
            and "articleTitle" not in ref_content
            and "bookTitle" not in ref_content):
            set_if_value(ref_content, "title", ref.get("source"))

        # conference
        if ref.get("conf-name"):
            set_if_value(ref_content, "conference", references_publisher(
                ref.get("conf-name"), None))

        # source
        if ref.get("publication-type") == "journal":
            set_if_value(ref_content, "journal", ref.get("source"))
        elif ref.get("publication-type") == "periodical":
            set_if_value(ref_content, "periodical", ref.get("source"))
        elif ref.get("publication-type") in ["web"]:
            set_if_value(ref_content, "website", ref.get("source"))
        elif ref.get("publication-type") in ["patent"]:
            set_if_value(ref_content, "patentType", ref.get("source"))
        elif ref.get("publication-type") not in ["book"]:
            set_if_value(ref_content, "source", ref.get("source"))

        # patent details
        set_if_value(ref_content, "number", ref.get("patent"))
        set_if_value(ref_content, "country", ref.get("country"))

        # publisher
        if ref.get("publisher_name"):
            set_if_value(ref_content, "publisher", references_publisher(
                ref.get("publisher_name"), ref.get("publisher_loc")))
        elif ref.get("publication-type") in ["software"] and ref.get("source"):
            set_if_value(ref_content, "publisher", references_publisher(
                ref.get("source"), ref.get("publisher_loc")))

        # volume
        set_if_value(ref_content, "volume", ref.get("volume"))

        # edition
        if ref.get("publication-type") in ["software"]:
            set_if_value(ref_content, "version", ref.get("version"))
            if "version" not in ref_content:
                set_if_value(ref_content, "version", ref.get("edition"))
        else:
            set_if_value(ref_content, "edition", ref.get("edition"))

        # chapter-title
        set_if_value(ref_content, "chapterTitle", ref.get("chapter-title"))
        if ref_content["type"] == "book-chapter" and "chapterTitle" not in ref_content:
            set_if_value(ref_content, "chapterTitle", ref.get("full_article_title"))

        # pages
        if ref.get("elocation-id"):
            ref_content["pages"] = ref.get("elocation-id")
        elif ref.get("fpage") and not re.match("^[A-Za-z0-9\.]+$", ref.get("fpage")):
            # Use range as string value
            ref_content["pages"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage"))
        elif ref.get("lpage") and not re.match("^[A-Za-z0-9\.]+$", ref.get("lpage")):
            # Use range as string value
            ref_content["pages"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage"))
        elif ref.get("fpage") and not ref.get("lpage"):
            ref_content["pages"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage"))
        elif ref.get("fpage") and ref.get("lpage"):
            ref_content["pages"] = OrderedDict()
            ref_content["pages"]["first"] = ref.get("fpage").strip()
            if ref.get("lpage"):
                ref_content["pages"]["last"] = ref.get("lpage").strip()
            ref_content["pages"]["range"] = references_pages_range(
                ref.get("fpage"), ref.get("lpage"))

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
            set_if_value(ref_content, "dataId", ref.get("accession"))

        # doi
        if ref.get("publication-type") not in ["web"]:
            set_if_value(ref_content, "doi", ref.get("doi"))

        # pmid
        set_if_value(ref_content, "pmid", coerce_to_int(ref.get("pmid"), None))

        # isbn
        set_if_value(ref_content, "isbn", ref.get("isbn"))

        # uri
        set_if_value(ref_content, "uri", ref.get("uri"))
        if ("uri" not in ref_content
            and ref.get("publication-type") in ["confproc", "data", "web", "preprint"]):
            if ref.get("doi"):
                # Convert doi to uri
                ref_content["uri"] = "https://doi.org/" + ref.get("doi")

        # Convert to HTML
        for index in ["title", "articleTitle", "chapterTitle", "bookTitle", "edition"]:
            set_if_value(ref_content, index, convert(ref_content.get(index)))

        # Rewrite references data with support to delete a reference too
        ref_content_rewritten = elifetools.json_rewrite.rewrite_json("references_json", soup, [ref_content])
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
        or
        (ref_content.get("type") == "book-chapter" and "editors" not in ref_content)
        or
        (ref_content.get("type") == "journal" and "articleTitle" not in ref_content)
        or
        (ref_content.get("type") in ["journal", "book-chapter"]
         and not "pages" in ref_content)
        or
        (ref_content.get("type") == "journal" and "journal" not in ref_content)
        or
        (ref_content.get("type") in ["book", "book-chapter", "report", "thesis", "software"]
         and "publisher" not in ref_content)
        or
        (ref_content.get("type") == "book" and "bookTitle" not in ref_content)
        or
        (ref_content.get("type") == "data" and "source" not in ref_content)
        or
        (ref_content.get("type") == "conference-proceeding" and "conference" not in ref_content)
       ):
        ref_content = references_json_to_unknown(ref_content, soup)

    return ref_content

def references_json_to_unknown(ref_content, soup=None):
    unknown_ref_content = OrderedDict()
    unknown_ref_content["type"] = "unknown"
    set_if_value(unknown_ref_content, "id", ref_content.get("id"))
    set_if_value(unknown_ref_content, "date", ref_content.get("date"))
    set_if_value(unknown_ref_content, "authors", ref_content.get("authors"))
    if not unknown_ref_content.get("authors") and ref_content.get("author"):
        unknown_ref_content["authors"] = []
        unknown_ref_content["authors"].append(ref_content.get("author"))
    set_if_value(unknown_ref_content, "authorsEtAl", ref_content.get("authorsEtAl"))

    # compile details first for use later in title as a default
    details = references_json_unknown_details(ref_content, soup)

    # title
    set_if_value(unknown_ref_content, "title", ref_content.get("title"))
    if "title" not in unknown_ref_content:
        set_if_value(unknown_ref_content, "title", ref_content.get("bookTitle"))
    if "title" not in unknown_ref_content:
        set_if_value(unknown_ref_content, "title", ref_content.get("articleTitle"))
    if "title" not in unknown_ref_content:
        # Still not title, try to use the details as the title
        set_if_value(unknown_ref_content, "title", details)

    # add details
    set_if_value(unknown_ref_content, "details", details)

    set_if_value(unknown_ref_content, "uri", ref_content.get("uri"))

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
            ref_tag = first(soup.select("ref#" + ref_content["id"]))
            if ref_tag:
                # Now remove tags that would be already part of the unknown reference by now
                for remove_tag in ["person-group", "year", "article-title",
                                   "elocation-id", "fpage", "lpage"]:
                    ref_tag = remove_tag_from_tag(ref_tag, remove_tag)
                # Add the remaining tag content comma separated
                for tag in first(raw_parser.element_citation(ref_tag)):
                    if node_text(tag) is not None:
                        if details != "":
                            details += ", "
                        details += node_text(tag)
    if details == "":
        return None
    else:
        return details


def ethics_json(soup):
    ethics_json = []
    ethics_fn_group = first(raw_parser.fn_group(soup, "ethics-information"))

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
        if (first_block.get("type")
            and first_block.get("type") == "box"
            and first_block.get("content")):
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
        app_group = first(raw_parser.app_group(back))
    if app_group:
        app_tags = raw_parser.app(app_group)
    for app_tag in app_tags:
        app_content = body_block_content(app_tag, base_url=base_url)
        app_blocks = body_blocks(app_tag)
        if app_blocks:
            app_content["content"] = []
            for block_tag in app_blocks:
                if len(body_block_content_render(block_tag)) > 0:
                    if body_block_content_render(block_tag)[0] != {}:
                        app_content["content"].append(body_block_content_render(block_tag, base_url=base_url)[0])

        # If the first element is a box and it has no DOI, then ignore it
        #  by setting its child content to itself
        #  Also check one level deeper for box elements
        app_content = unwrap_appendix_box(app_content)
        if app_content.get("content") and len(app_content["content"]) > 0:
            app_content["content"][0] = unwrap_appendix_box(app_content["content"][0])

        # Then check all first level sections with no title, and fix them by
        #  building the content list again, unwrapping each non-title section
        clean_app_content = []
        for i, content_block in enumerate(app_content["content"]):
            if (content_block.get("type")
                and content_block.get("type") == "section"
                and content_block.get("content")
                and not content_block.get("title")):
                for block in content_block.get("content"):
                    clean_app_content.append(block)
            else:
                # Unwrap boxed-text if found here too
                content_block = unwrap_appendix_box(content_block)
                clean_app_content.append(content_block)
        app_content["content"] = clean_app_content

        appendices_json.append(app_content)
    return appendices_json


def dataset_related_object_json(tag, html_flag=True):
    # Configure the XML to HTML conversion preference for shorthand use below
    convert = lambda xml_string: xml_to_html(html_flag, xml_string)

    dataset_content = OrderedDict()

    #set_if_value(tag_content, "doi", object_id_doi(tag, tag.name))
    set_if_value(dataset_content, "id", tag.get("id"))
    set_if_value(dataset_content, "date", node_text(raw_parser.year(tag)))

    # authors
    dataset_authors = []
    for contrib_tag in extract_nodes(tag, ["name", "collab"]):
        dataset_author = OrderedDict()
        if contrib_tag.name == "collab":
            dataset_author["type"] = "group"
            set_if_value(dataset_author, "name", node_contents_str(contrib_tag))
        elif contrib_tag.name == "name":
            person_details = {}
            set_if_value(person_details, "surname", first_node_str_contents(contrib_tag, "surname"))
            set_if_value(person_details, "given-names", first_node_str_contents(contrib_tag, "given-names"))
            set_if_value(person_details, "suffix", first_node_str_contents(contrib_tag, "suffix"))
            dataset_author = references_author_person(person_details)
        if len(dataset_author) > 0:
            dataset_authors.append(dataset_author)
    if len(dataset_authors) > 0:
        dataset_content["authors"] = dataset_authors

    # et al
    if raw_parser.etal(tag):
        dataset_content["authorsEtAl"] = True

    # title
    set_if_value(dataset_content, "title", convert(node_contents_str(first(raw_parser.source(tag)))))

    # dataId
    set_if_value(dataset_content, "dataId",
                 convert(node_contents_str(first(raw_parser.object_id(tag, "art-access-id")))))

    # details
    set_if_value(dataset_content, "details", convert(node_contents_str(first(raw_parser.comment(tag)))))

    # doi
    if raw_parser.pub_id(tag, "doi"):
        doi_tag = first(raw_parser.pub_id(tag, "doi"))
        set_if_value(dataset_content, "doi", doi_uri_to_doi(doi_tag.get('xlink:href')))

    # uri
    if raw_parser.ext_link(tag, "uri"):
        uri_tag = first(raw_parser.ext_link(tag, "uri"))
        set_if_value(dataset_content, "uri", uri_tag.get('xlink:href'))

    return dataset_content


def datasets_json(soup, html_flag=True):
    datasets_json = OrderedDict()
    generated_datasets = []
    used_datasets = []
    generated_datasets_related_object_tags = []
    used_datasets_related_object_tags = []
    p_tags = []

    back_tag = raw_parser.back(soup)
    if back_tag:
        datasets_section_tag = first(raw_parser.section(back_tag, "datasets"))
        if datasets_section_tag:
            p_tags = raw_parser.paragraph(datasets_section_tag)

    if p_tags:
        dataset_type = None
        for p_tag in p_tags:
            # Look for paragraphs with related-object in them and the
            #  ones with out them are above the generated and used datasets
            if raw_parser.related_object(p_tag):
                if dataset_type == "generated":
                    generated_datasets_related_object_tags += raw_parser.related_object(p_tag)
                elif dataset_type == "used":
                    used_datasets_related_object_tags += raw_parser.related_object(p_tag)
            else:
                if node_text(p_tag) and "generated" in node_text(p_tag):
                    dataset_type = "generated"
                elif node_text(p_tag):
                    dataset_type = "used"

    for related_object in generated_datasets_related_object_tags:
        if "generated" not in datasets_json:
            datasets_json["generated"] = []
        if dataset_related_object_json(related_object) != {}:
            datasets_json["generated"].append(dataset_related_object_json(related_object, html_flag))

    for related_object in used_datasets_related_object_tags:
        if "used" not in datasets_json:
            datasets_json["used"] = []
        if dataset_related_object_json(related_object) != {}:
            datasets_json["used"].append(dataset_related_object_json(related_object, html_flag))

    return elifetools.json_rewrite.rewrite_json("datasets_json", soup, datasets_json)

def poa_supplementary_material_block_content(tag):
    tag_content = OrderedDict()

    # Check its characteristics first
    if (tag and tag.name == "supplementary-material"
        and raw_parser.ext_link(tag) and not raw_parser.media(tag)):
        ext_link_tag = first(raw_parser.ext_link(tag))
        filename = ext_link_tag.get('xlink:href')

        if filename and filename.endswith(".zip"):
            tag_content["mediaType"] = "application/zip"

        set_if_value(tag_content, "uri", filename)
        set_if_value(tag_content, "filename", filename)

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
    poa_supp_material_tags = list(filter(lambda tag: tag.parent.name == "article-meta", all_supp_material_tags))
    for tag in poa_supp_material_tags:
        tag_content = poa_supplementary_material_block_content(tag)
        if tag_content != {}:
            additional_files_json.append(tag_content)

    # Add id and title for PoA articles, i.e. if there are none with an id value
    if len(list(filter(lambda file: file.get('id') is not None, supplementary_material_tags))) == 0:
        i = 1
        for file in additional_files_json:
            file["id"] = "SD" + str(i) + "-data"
            file["label"] = "Supplementary file " + str(i) + "."
            i = i + 1

    # if there is a single supplementary zip file for PoA,
    # rename it and describe it
    if len(additional_files_json) == 1:
        single_additional_file = additional_files_json[0]['filename']
        if re.match("^.+-supp-.+\.zip$", single_additional_file):
            file = additional_files_json[0]
            file["label"] = "All additional files"
            file['caption'] = [{
                "text": "Any figure supplements, source code, source data, videos or supplementary files associated with this article are contained within this zip.",
                "type": "paragraph",
            }]

    return additional_files_json

def funding_statement_json(soup, html_flag=True):
    return xml_to_html(html_flag, full_funding_statement(soup))

def funding_awards_json(soup):
    awards = []

    # Some details can take from existing award groups function
    award_groups = full_award_groups(soup)
    if award_groups:
        for award_group_dict in award_groups:
            for id, award_group in iteritems(award_group_dict):
                award_content = OrderedDict()
                set_if_value(award_content, "id", id)

                if award_group.get("institution") or award_group.get("id"):
                    # Set the source
                    source_content = OrderedDict()
                    set_if_value(source_content, "funderId", doi_uri_to_doi(award_group.get("id")))
                    if award_group.get("institution"):
                        source_name_content = OrderedDict()
                        set_if_value(source_content, "name", [award_group.get("institution")])
                    award_content["source"] = source_content

                # awardId
                if award_group.get("award-id") and award_group.get("award-id") != "":
                    set_if_value(award_content, "awardId", award_group.get("award-id"))

                if len(award_content) > 0:
                    awards.append(award_content)

    # recipients to parse fresh
    award_group_tags = []
    award_recipients = {}
    funding_group = first(raw_parser.funding_group(soup))
    if funding_group:
        award_group_tags = raw_parser.award_group(funding_group)
    for a_tag in award_group_tags:
        id = a_tag.get("id")
        recipient_tags = raw_parser.principal_award_recipient(a_tag)
        if recipient_tags:
            recipients = []
            for recipient_tag in recipient_tags:
                if len(extract_nodes(recipient_tag, ["name", "institution"])) <= 0:
                    # A loose institution name not surrounded by institution tag
                    recipient_content = OrderedDict()
                    recipient_content["type"] = "group"
                    set_if_value(recipient_content, "name", node_contents_str(recipient_tag))
                    if len(recipient_content) > 0:
                        # add it
                        recipients.append(recipient_content)
                else:
                    for contrib_tag in extract_nodes(recipient_tag, ["name", "institution"]):
                        recipient_content = OrderedDict()
                        if contrib_tag.name == "institution":
                            recipient_content["type"] = "group"
                            set_if_value(recipient_content, "name", node_contents_str(contrib_tag))
                        elif contrib_tag.name == "name":
                            person_details = {}
                            set_if_value(person_details, "surname",
                                         first_node_str_contents(contrib_tag, "surname"))
                            set_if_value(person_details, "given-names",
                                         first_node_str_contents(contrib_tag, "given-names"))
                            set_if_value(person_details, "suffix",
                                         first_node_str_contents(contrib_tag, "suffix"))
                            recipient_content = references_author_person(person_details)
                        if len(recipient_content) > 0:
                            # add it
                            recipients.append(recipient_content)

            # Add to the dict for adding to the award data later
            if len(recipients) > 0:
                if id not in award_recipients:
                    award_recipients[id] = []
                award_recipients[id] = recipients

    # Add recipient data to the award data
    for award in awards:
        if award.get("id") and award.get("id") in award_recipients:
            award["recipients"] = award_recipients.get(award.get("id"))

    awards = elifetools.json_rewrite.rewrite_json("funding_awards", soup, awards)

    return awards
