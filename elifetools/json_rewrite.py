# coding=utf-8

from collections import OrderedDict
import elifetools.rawJATS
import elifetools.utils
import elifetools.utils_html


def rewrite_json(rewrite_type, soup, json_content):
    """
    Due to XML content that will not conform with the strict JSON schema validation rules,
    for elife articles only, rewrite the JSON to make it valid
    """
    if not soup:
        return json_content
    if not elifetools.rawJATS.doi(soup) or not elifetools.rawJATS.journal_id(soup):
        return json_content

    # Hook only onto elife articles for rewriting currently
    journal_id_tag = elifetools.rawJATS.journal_id(soup)
    doi_tag = elifetools.rawJATS.doi(soup)
    journal_id = elifetools.utils.node_text(journal_id_tag)
    doi = elifetools.utils.doi_uri_to_doi(elifetools.utils.node_text(doi_tag))
    if journal_id.lower() == "elife":
        function_name = rewrite_function_name(journal_id, rewrite_type)
        if function_name:
            try:
                json_content = globals()[function_name](json_content, doi)
            except KeyError:
                pass
    return json_content


def rewrite_function_name(journal_id, rewrite_type):
    """ concatenate the name of the rewriting function """
    if not journal_id or not rewrite_type:
        return None
    return "rewrite_" + journal_id.lower() + "_" + rewrite_type


def rewrite_elife_references_json(json_content, doi):
    """ this does the work of rewriting elife references json """
    references_rewrite_json = elife_references_rewrite_json()
    if doi in references_rewrite_json:
        json_content = rewrite_references_json(
            json_content, references_rewrite_json[doi]
        )

    # Edge case delete one reference
    if doi == "10.7554/eLife.12125":
        for i, ref in enumerate(json_content):
            if ref.get("id") and ref.get("id") == "bib11":
                del json_content[i]

    return json_content


def rewrite_references_json(json_content, rewrite_json):
    """ general purpose references json rewriting by matching the id value """
    for ref in json_content:
        if ref.get("id") and ref.get("id") in rewrite_json:
            for key, value in rewrite_json.get(ref.get("id")).items():
                ref[key] = value
    return json_content


def elife_references_rewrite_json():
    """ Here is the DOI and references json replacements data for elife """
    references_rewrite_json = {}

    references_rewrite_json["10.7554/eLife.00051"] = {"bib25": {"date": "2012"}}
    references_rewrite_json["10.7554/eLife.00278"] = {"bib11": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.00444"] = {"bib2": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.00569"] = {"bib74": {"date": "1996"}}
    references_rewrite_json["10.7554/eLife.00592"] = {"bib8": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.00633"] = {"bib38": {"date": "2004"}}
    references_rewrite_json["10.7554/eLife.00646"] = {"bib1": {"date": "2012"}}
    references_rewrite_json["10.7554/eLife.00813"] = {"bib33": {"date": "2007"}}
    references_rewrite_json["10.7554/eLife.01355"] = {"bib9": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.01530"] = {"bib12": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.01681"] = {"bib5": {"date": "2000"}}
    references_rewrite_json["10.7554/eLife.01917"] = {"bib35": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.02030"] = {
        "bib53": {"date": "2013"},
        "bib56": {"date": "2013"},
    }
    references_rewrite_json["10.7554/eLife.02076"] = {"bib93a": {"date": "1990"}}
    references_rewrite_json["10.7554/eLife.02217"] = {"bib27": {"date": "2009"}}
    references_rewrite_json["10.7554/eLife.02535"] = {"bib12": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.02862"] = {"bib8": {"date": "2010"}}
    references_rewrite_json["10.7554/eLife.03711"] = {"bib35": {"date": "2012"}}
    references_rewrite_json["10.7554/eLife.03819"] = {"bib37": {"date": "2008"}}
    references_rewrite_json["10.7554/eLife.04069"] = {"bib8": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.04247"] = {"bib19a": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.04333"] = {
        "bib3": {"date": "1859"},
        "bib37": {"date": "1959"},
    }
    references_rewrite_json["10.7554/eLife.04478"] = {"bib49": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.04580"] = {"bib139": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.05042"] = {"bib78": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.05323"] = {"bib102": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.05423"] = {"bib102": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.05503"] = {"bib94": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.05849"] = {"bib82": {"date": "2005"}}
    references_rewrite_json["10.7554/eLife.06072"] = {"bib17": {"date": "2003"}}
    references_rewrite_json["10.7554/eLife.06315"] = {"bib19": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.06426"] = {"bib39": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.07361"] = {"bib76": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.07460"] = {
        "bib1": {"date": "2013"},
        "bib2": {"date": "2014"},
    }
    references_rewrite_json["10.7554/eLife.08500"] = {"bib55": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.09066"] = {"bib46": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.09100"] = {"bib50": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.09148"] = {
        "bib47": {"articleTitle": "97–104"},
        "bib59": {"articleTitle": "1913–1918"},
    }
    references_rewrite_json["10.7554/eLife.09186"] = {
        "bib31": {"date": "2015"},
        "bib54": {"date": "2014"},
        "bib56": {"date": "2014"},
        "bib65": {"date": "2015"},
    }
    references_rewrite_json["10.7554/eLife.09215"] = {"bib5": {"date": "2012"}}

    references_rewrite_json["10.7554/eLife.09520"] = {
        "bib35": OrderedDict(
            [
                (
                    "conference",
                    OrderedDict([("name", ["WHO Expert Committee on Malaria"])]),
                ),
                (
                    "articleTitle",
                    (
                        "WHO Expert Committee on Malaria [meeting held in Geneva from 19 to 30 "
                        "October 1970]: fifteenth report"
                    ),
                ),
                (
                    "publisher",
                    OrderedDict(
                        [
                            ("name", ["World Health Organization"]),
                            (
                                "address",
                                OrderedDict(
                                    [
                                        ("formatted", ["Geneva"]),
                                        (
                                            "components",
                                            OrderedDict([("locality", ["Geneva"])]),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        )
    }

    references_rewrite_json["10.7554/eLife.09579"] = {
        "bib19": {"date": "2007"},
        "bib49": {"date": "2002"},
    }
    references_rewrite_json["10.7554/eLife.09600"] = {"bib13": {"date": "2009"}}
    references_rewrite_json["10.7554/eLife.09672"] = {
        "bib25": {
            "conference": {
                "name": [
                    (
                        "Seventeenth Meeting of the RBM Partnership Monitoring and Evaluation "
                        "Reference Group (MERG)"
                    )
                ]
            }
        }
    }
    references_rewrite_json["10.7554/eLife.09771"] = {"bib22": {"date": "2012"}}
    references_rewrite_json["10.7554/eLife.09972"] = {
        "bib61": {"date": "2007", "discriminator": "a"}
    }
    references_rewrite_json["10.7554/eLife.09977"] = {"bib41": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.10032"] = {"bib45": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.10042"] = {"bib14": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10070"] = {
        "bib15": {"date": "2015"},
        "bib38": {"date": "2014"},
    }
    references_rewrite_json["10.7554/eLife.10222"] = {"bib30": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10670"] = {
        "bib7": {"date": "2015"},
        "bib8": {"date": "2015"},
    }
    references_rewrite_json["10.7554/eLife.10781"] = {"bib32": {"date": "2003"}}
    references_rewrite_json["10.7554/eLife.11273"] = {"bib43": {"date": "2004"}}
    references_rewrite_json["10.7554/eLife.11305"] = {"bib68": {"date": "2000"}}
    references_rewrite_json["10.7554/eLife.11416"] = {"bib22": {"date": "1997"}}
    references_rewrite_json["10.7554/eLife.11860"] = {
        "bib48": {"title": "Light-switchable gene expression system"}
    }
    references_rewrite_json["10.7554/eLife.12401"] = {"bib25": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.12366"] = {"bib10": {"date": "2008"}}
    references_rewrite_json["10.7554/eLife.12703"] = {"bib27": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.12735"] = {"bib35": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.12830"] = {"bib118": {"date": "1982"}}
    references_rewrite_json["10.7554/eLife.13133"] = {"bib11": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.13152"] = {"bib25": {"date": "2000"}}
    references_rewrite_json["10.7554/eLife.13195"] = {
        "bib6": {"date": "2013"},
        "bib12": {"date": "2003"},
    }
    references_rewrite_json["10.7554/eLife.13479"] = {"bib5": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.13463"] = {"bib15": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.14119"] = {"bib40": {"date": "2007"}}
    references_rewrite_json["10.7554/eLife.14169"] = {"bib6": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.14523"] = {"bib7": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.15272"] = {"bib78": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.15504"] = {
        "bib67": {"isbn": "9780198524304"}
    }
    references_rewrite_json["10.7554/eLife.16105"] = {"bib2": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.16349"] = {"bib68": {"date": "2005"}}
    references_rewrite_json["10.7554/eLife.16394"] = {
        "bib6": {
            "type": "thesis",
            "author": {
                "type": "person",
                "name": {"preferred": "B Berret", "index": "Berret, B"},
            },
            "publisher": {"name": ["Université de Bourgogne"]},
        }
    }
    references_rewrite_json["10.7554/eLife.16443"] = {"bib58": {"date": "1987"}}
    references_rewrite_json["10.7554/eLife.16764"] = {"bib4": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.17092"] = {"bib102": {"date": "1980"}}
    references_rewrite_json["10.7554/eLife.18044"] = {"bib25": {"date": "2005"}}
    references_rewrite_json["10.7554/eLife.18370"] = {"bib1": {"date": "2006"}}
    references_rewrite_json["10.7554/eLife.18425"] = {"bib54": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.18683"] = {"bib47": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.19532"] = {"bib27": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.19545"] = {"bib51": {"date": "1996"}}
    references_rewrite_json["10.7554/eLife.19571"] = {"bib56": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.20352"] = {
        "bib53": {"country": "United States"}
    }
    references_rewrite_json["10.7554/eLife.21864"] = {"bib2": {"date": "2016-10-24"}}
    references_rewrite_json["10.7554/eLife.20522"] = {
        "bib42": {"date": "2016"},
        "bib110": {"date": "1996"},
    }
    references_rewrite_json["10.7554/eLife.22053"] = {"bib123": {"date": "2016"}}

    # Reference authors data to replace, processed further below into json
    references_authors = []
    references_authors.append(
        (
            "10.7554/eLife.00036",
            "bib8",
            "authors",
            [
                {"surname": "Butler", "given-names": "H"},
                {"surname": "Juurlink", "given-names": "BHJ"},
            ],
        )
    )
    references_authors.append(
        (
            "10.7554/eLife.00036",
            "bib30",
            "authors",
            [{"surname": "Joyner", "given-names": "AL"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.00048",
            "bib15",
            "authors",
            [
                {"surname": "Guthrie", "given-names": "C"},
                {"surname": "Fink", "given-names": "GR"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.00051",
            "bib21",
            "authors",
            [
                {"surname": "Jamison", "given-names": "DT"},
                {"surname": "Breman", "given-names": "JG"},
                {"surname": "Measham", "given-names": "AR"},
                {"surname": "Alleyne", "given-names": "G"},
                {"surname": "Claeson", "given-names": "M"},
                {"surname": "Evans", "given-names": "DB"},
                {"surname": "Jha", "given-names": "P"},
                {"surname": "Mills", "given-names": "A"},
                {"surname": "Musgrove", "given-names": "P"},
            ],
        )
    )
    references_authors.append(
        (
            "10.7554/eLife.00051",
            "bib36",
            "authors",
            [
                {"surname": "Rogers", "given-names": "RG"},
                {"surname": "Crimmins", "given-names": "EM"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.00668",
            "bib39",
            "authors",
            [{"surname": "Rice", "given-names": "SA"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.01730",
            "bib75",
            "authors",
            [{"collab": "Look AHEAD Research Group"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.03714",
            "bib64",
            "authors",
            [
                {"surname": "Otwinowski", "given-names": "Z"},
                {"surname": "Minor", "given-names": "W"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.04220",
            "bib31",
            "authors",
            [
                {"surname": "Tishby", "given-names": "N"},
                {"surname": "Polani", "given-names": "D"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.04395",
            "bib67",
            "authors",
            [
                {"surname": "King", "given-names": "AMQ"},
                {"surname": "Adams", "given-names": "MJ"},
                {"surname": "Carstens", "given-names": "EB"},
                {"surname": "Lefkowitz", "given-names": "E"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.04449",
            "bib62",
            "authors",
            [{"surname": "Shaham", "given-names": "S"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.04659",
            "bib57",
            "authors",
            [
                {"surname": "Sambrook", "given-names": "J"},
                {"surname": "Russell", "given-names": "TW"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.05423",
            "bib4",
            "authors",
            [
                {"surname": "Birkhead", "given-names": "TR"},
                {"surname": "Møller", "given-names": "AP"},
            ],
        )
    )
    references_authors.append(
        (
            "10.7554/eLife.05423",
            "bib5",
            "authors",
            [
                {"surname": "Birkhead", "given-names": "TR"},
                {"surname": "Møller", "given-names": "AP"},
            ],
        )
    )
    references_authors.append(
        (
            "10.7554/eLife.05423",
            "bib90",
            "authors",
            [{"surname": "Smith", "given-names": "RL"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.05564",
            "bib39",
            "authors",
            [{"surname": "Pattyn", "given-names": "S"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.05959",
            "bib76",
            "authors",
            [
                {"surname": "Macholán", "given-names": "M"},
                {"surname": "Baird", "given-names": "SJE"},
                {"surname": "Munclinger", "given-names": "P"},
                {"surname": "Piálek", "given-names": "J"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.06565",
            "bib1",
            "authors",
            [{"surname": "Ahringer", "given-names": "J"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.06576",
            "bib57",
            "authors",
            [{"surname": "Moller", "given-names": "AR"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.06813",
            "bib54",
            "authors",
            [{"surname": "King", "given-names": "JA"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.06813",
            "bib55",
            "authors",
            [
                {"surname": "Kirkland", "given-names": "Gl"},
                {"surname": "Layne", "given-names": "JN"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.07460",
            "bib1",
            "authors",
            [{"surname": "Rallapalli", "given-names": "Ghanasyam"}],
        )
    )
    references_authors.append(
        (
            "10.7554/eLife.07460",
            "bib2",
            "authors",
            [{"surname": "Bazyl", "given-names": "Steven"}],
        )
    )

    references_authors.append(
        ("10.7554/eLife.07847", "bib40", "authors", [{"collab": "Nature Immunology"}])
    )

    references_authors.append(
        (
            "10.7554/eLife.09666",
            "bib9",
            "authors",
            [{"surname": "Schüler", "given-names": "D"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.09868",
            "bib5",
            "authors",
            [{"surname": "Barlow", "given-names": "HB"}],
        )
    )

    references_authors.append(
        ("10.7554/eLife.10222", "bib30", "authors", [{"collab": "PharmaMar"}])
    )

    references_authors.append(
        (
            "10.7554/eLife.11860",
            "bib48",
            "authors",
            [
                {"surname": "Yang", "given-names": "Y"},
                {"surname": "Wang", "given-names": "X"},
                {"surname": "Chen", "given-names": "X"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.11945",
            "bib23",
            "authors",
            [
                {"surname": "Glimcher", "given-names": "P"},
                {"surname": "Fehr", "given-names": "E"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.13135",
            "bib26",
            "authors",
            [
                {"surname": "Ivanova", "given-names": "S"},
                {"surname": "Herbreteau", "given-names": "B"},
                {"surname": "Blasdell", "given-names": "K"},
                {"surname": "Chaval", "given-names": "Y"},
                {"surname": "Buchy", "given-names": "P"},
                {"surname": "Guillard", "given-names": "B"},
                {"surname": "Morand", "given-names": "S"},
            ],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.13135",
            "bib27",
            "authors",
            [
                {"surname": "King", "given-names": "AMQ"},
                {"surname": "Adams", "given-names": "J"},
                {"surname": "Carstens", "given-names": "EB"},
                {"surname": "Lefkowitz", "given-names": "EJ"},
            ],
        )
    )

    references_authors.append(
        ("10.7554/eLife.14188", "bib1", "authors", [{"collab": "Avisoft Bioacoustics"}])
    )

    references_authors.append(
        (
            "10.7554/eLife.17716",
            "bib7",
            "authors",
            [{"collab": "World Health Organization"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.17956",
            "bib4",
            "authors",
            [{"surname": "Barrett", "given-names": "SCH"}],
        )
    )

    references_authors.append(
        (
            "10.7554/eLife.18109",
            "bib39",
            "authors",
            [{"surname": "Weber", "given-names": "EH"}],
        )
    )

    # Now turn the authors data into the json
    for author_row in references_authors:
        ref_json = OrderedDict()
        doi, author_id, author_type, authors = author_row
        # if author_id not in ref_json:
        ref_json[author_id] = OrderedDict()
        ref_json[author_id][author_type] = []
        for ref_author in authors:
            if "collab" in ref_author:
                author_json = elifetools.utils_html.references_author_collab(ref_author)
            else:
                author_json = elifetools.utils.references_author_person(ref_author)
            if author_json:
                ref_json[author_id][author_type].append(author_json)
        # Add to json array, and do not rewrite existing rule of a
        # specific bib author_id (if present)
        if doi not in references_rewrite_json:
            references_rewrite_json[doi] = ref_json
        else:
            for key, value in ref_json.items():
                if key not in references_rewrite_json[doi]:
                    references_rewrite_json[doi][key] = value
                else:
                    # Append dict items
                    for child_key, child_value in value.items():
                        references_rewrite_json[doi][key][child_key] = child_value

    return references_rewrite_json


def rewrite_elife_body_json(json_content, doi):
    """ rewrite elife body json """

    # Edge case add an id to a section
    if doi == "10.7554/eLife.00013":
        if json_content and len(json_content) > 0:
            if (
                json_content[0].get("type")
                and json_content[0].get("type") == "section"
                and json_content[0].get("title")
                and json_content[0].get("title") == "Introduction"
                and not json_content[0].get("id")
            ):
                json_content[0]["id"] = "s1"

    # Edge case remove an extra section
    if doi == "10.7554/eLife.04232":
        if json_content and len(json_content) > 0:
            for outer_block in json_content:
                if outer_block.get("id") and outer_block.get("id") == "s4":
                    for mid_block in outer_block.get("content"):
                        if mid_block.get("id") and mid_block.get("id") == "s4-6":
                            for inner_block in mid_block.get("content"):
                                if inner_block.get("content") and not inner_block.get(
                                    "title"
                                ):
                                    mid_block["content"] = inner_block.get("content")

    # Edge case remove unwanted sections
    if doi == "10.7554/eLife.04871":
        if json_content and len(json_content) > 0:
            for i, outer_block in enumerate(json_content):
                if (
                    outer_block.get("id")
                    and outer_block.get("id") in ["s7", "s8"]
                    and not outer_block.get("title")
                ):
                    if outer_block.get("content"):
                        json_content[i] = outer_block.get("content")[0]

    # Edge case remove an extra section
    if doi == "10.7554/eLife.05519":
        if json_content and len(json_content) > 0:
            for outer_block in json_content:
                if outer_block.get("id") and outer_block.get("id") == "s4":
                    for mid_block in outer_block.get("content"):
                        if mid_block.get("content") and not mid_block.get("id"):
                            new_blocks = []
                            for inner_block in mid_block.get("content"):
                                new_blocks.append(inner_block)
                            outer_block["content"] = new_blocks

    # Edge case add a title to a section
    if doi == "10.7554/eLife.07157":
        if json_content and len(json_content) > 0:
            if (
                json_content[0].get("type")
                and json_content[0].get("type") == "section"
                and json_content[0].get("id")
                and json_content[0].get("id") == "s1"
            ):
                json_content[0]["title"] = "Main text"

    # Edge case remove a section with no content
    if doi == "10.7554/eLife.09977":
        if json_content and len(json_content) > 0:
            i_index = j_index = None
            for i, outer_block in enumerate(json_content):
                if (
                    outer_block.get("id")
                    and outer_block.get("id") == "s4"
                    and outer_block.get("content")
                ):
                    # We have i
                    i_index = i
                    break
            if i_index is not None:
                for j, inner_block in enumerate(json_content[i_index].get("content")):
                    if (
                        inner_block.get("id")
                        and inner_block.get("id") == "s4-11"
                        and inner_block.get("content") is None
                    ):
                        # Now we have i and j for deletion outside of the loop
                        j_index = j
                        break
            # Do the deletion on the original json
            if i_index is not None and j_index is not None:
                del json_content[i_index]["content"][j_index]

    # Edge case wrap sections differently
    if doi == "10.7554/eLife.12844":
        if (
            json_content
            and len(json_content) > 0
            and json_content[0].get("type")
            and json_content[0]["type"] == "section"
        ):
            new_body = OrderedDict()
            for i, tag_block in enumerate(json_content):
                if i == 0:
                    tag_block["title"] = "Main text"
                    new_body = tag_block
                elif i > 0:
                    new_body["content"].append(tag_block)
            json_content = [new_body]

    return json_content


def rewrite_elife_funding_awards(json_content, doi):
    """ rewrite elife funding awards """

    # remove a funding award
    if doi == "10.7554/eLife.00801":
        for i, award in enumerate(json_content):
            if "id" in award and award["id"] == "par-2":
                del json_content[i]

    # add funding award recipient
    if doi == "10.7554/eLife.04250":
        recipients_for_04250 = [
            {
                "type": "person",
                "name": {"preferred": "Eric Jonas", "index": "Jonas, Eric"},
            }
        ]
        for i, award in enumerate(json_content):
            if "id" in award and award["id"] in ["par-2", "par-3", "par-4"]:
                if "recipients" not in award:
                    json_content[i]["recipients"] = recipients_for_04250

    # add funding award recipient
    if doi == "10.7554/eLife.06412":
        recipients_for_06412 = [
            {
                "type": "person",
                "name": {"preferred": "Adam J Granger", "index": "Granger, Adam J"},
            }
        ]
        for i, award in enumerate(json_content):
            if "id" in award and award["id"] == "par-1":
                if "recipients" not in award:
                    json_content[i]["recipients"] = recipients_for_06412

    return json_content


def rewrite_elife_authors_json(json_content, doi):
    """ this does the work of rewriting elife authors json """

    # Convert doi from testing doi if applicable
    article_doi = elifetools.utils.convert_testing_doi(doi)

    # Edge case fix an affiliation name
    if article_doi == "10.7554/eLife.06956":
        for i, ref in enumerate(json_content):
            if ref.get("orcid") and ref.get("orcid") == "0000-0001-6798-0064":
                json_content[i]["affiliations"][0]["name"] = ["Cambridge"]

    # Edge case fix an ORCID
    if article_doi == "10.7554/eLife.09376":
        for i, ref in enumerate(json_content):
            if ref.get("orcid") and ref.get("orcid") == "000-0001-7224-925X":
                json_content[i]["orcid"] = "0000-0001-7224-925X"

    # Edge case competing interests
    if article_doi == "10.7554/eLife.00102":
        for i, ref in enumerate(json_content):
            if not ref.get("competingInterests"):
                if ref["name"]["index"].startswith("Chen,"):
                    json_content[i][
                        "competingInterests"
                    ] = "ZJC: Reviewing Editor, <i>eLife</i>"
                elif ref["name"]["index"].startswith("Li,"):
                    json_content[i][
                        "competingInterests"
                    ] = "The remaining authors have no competing interests to declare."
    if article_doi == "10.7554/eLife.00270":
        for i, ref in enumerate(json_content):
            if not ref.get("competingInterests"):
                if ref["name"]["index"].startswith("Patterson,"):
                    json_content[i][
                        "competingInterests"
                    ] = "MP: Managing Executive Editor, <i>eLife</i>"

    # Remainder of competing interests rewrites
    no_competing_interests_msg = (
        "The authors declare that no competing interests exist."
    )

    elife_author_competing_interests = {}
    elife_author_competing_interests["10.7554/eLife.00133"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.00190"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.00230"
    ] = "The authors have declared that no competing interests exist"
    elife_author_competing_interests["10.7554/eLife.00288"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.00352"
    ] = "The author declares that no competing interest exist"
    elife_author_competing_interests["10.7554/eLife.00362"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.00475"
    ] = "The remaining authors have no competing interests to declare."
    elife_author_competing_interests[
        "10.7554/eLife.00592"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.00633"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.02725"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.02935"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.04126"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.04878"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.05322"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.06011"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.06416"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.07383"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.08421"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.08494"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.08648"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.08924"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.09083"
    ] = "The other authors declare that no competing interests exists."
    elife_author_competing_interests["10.7554/eLife.09102"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.09460"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.09591"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.09600"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.10113"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.10230"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.10453"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.10635"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.11407"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.11473"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.11750"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.12217"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.12620"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.12724"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.13023"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.13732"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.14116"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.14258"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.14694"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.15085"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests[
        "10.7554/eLife.15312"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.16011"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.16940"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17023"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17092"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17218"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17267"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17523"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17556"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17769"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.17834"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.18101"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.18515"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.18544"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.18648"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.19071"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.19334"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.19510"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.20183"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.20242"] = no_competing_interests_msg
    elife_author_competing_interests["10.7554/eLife.20375"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.20797"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.21454"] = no_competing_interests_msg
    elife_author_competing_interests[
        "10.7554/eLife.21491"
    ] = "The other authors declare that no competing interests exist."
    elife_author_competing_interests["10.7554/eLife.22187"] = no_competing_interests_msg

    if article_doi in elife_author_competing_interests:
        for i, ref in enumerate(json_content):
            if not ref.get("competingInterests"):
                json_content[i][
                    "competingInterests"
                ] = elife_author_competing_interests[article_doi]

    # Rewrite "other authors declare" ... competing interests statements using a string match
    for i, ref in enumerate(json_content):
        if ref.get("competingInterests") and (
            ref.get("competingInterests").startswith("The other author")
            or ref.get("competingInterests").startswith("The others author")
            or ref.get("competingInterests").startswith("The remaining authors")
            or ref.get("competingInterests").startswith("The remaining have declared")
        ):
            json_content[i]["competingInterests"] = "No competing interests declared."

    return json_content


def rewrite_elife_datasets_json(json_content, doi):
    """ this does the work of rewriting elife datasets json """

    # Add dates in bulk
    elife_dataset_dates = []
    elife_dataset_dates.append(("10.7554/eLife.00348", "used", "dataro17", u"2010"))
    elife_dataset_dates.append(("10.7554/eLife.01179", "used", "dataro4", u"2016"))
    elife_dataset_dates.append(("10.7554/eLife.01603", "used", "dataro2", u"2012"))
    elife_dataset_dates.append(("10.7554/eLife.02304", "used", "dataro15", u"2005"))
    elife_dataset_dates.append(("10.7554/eLife.02935", "used", "dataro2", u"2014"))
    elife_dataset_dates.append(("10.7554/eLife.03583", "used", "dataro5", u"2013"))
    if doi in map(lambda dataset: dataset[0], elife_dataset_dates):
        for (
            match_doi,
            used_or_generated,
            dataset_id,
            dataset_date,
        ) in elife_dataset_dates:
            if doi == match_doi:
                if json_content.get(used_or_generated):
                    for dataset in json_content[used_or_generated]:
                        if dataset.get("id") and dataset["id"] == dataset_id:
                            if not dataset.get("date"):
                                dataset["date"] = dataset_date

    # Continue with individual article JSON rewriting
    if doi == "10.7554/eLife.01311":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] in [
                    "dataro3",
                    "dataro4",
                    "dataro5",
                ]:
                    if not dataset.get("date"):
                        dataset["date"] = u"2012"
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Duke"}]
                if dataset.get("id") and dataset["id"] == "dataro6":
                    if not dataset.get("date"):
                        dataset["date"] = u"2011"
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "FlyBase"}]
                if dataset.get("id") and dataset["id"] == "dataro7":
                    if not dataset.get("date"):
                        dataset["date"] = u"2011"
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {
                                "type": "group",
                                "name": "Baylor College of Medicine (BCM)",
                            }
                        ]
                if dataset.get("id") and dataset["id"] in ["dataro8", "dataro9"]:
                    if not dataset.get("date"):
                        dataset["date"] = u"2012"
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {
                                "type": "group",
                                "name": "University of California, Berkeley",
                            }
                        ]

    if doi == "10.7554/eLife.01440":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "EnsemblMetazoa"}
                        ]

    if doi == "10.7554/eLife.01535":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if dataset.get("date") and dataset.get("date") == "2000, 2005":
                        dataset["date"] = u"2000"

    if doi == "10.7554/eLife.02304":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro11":
                    if not dataset.get("title"):
                        dataset[
                            "title"
                        ] = u"T.gondii LDH1 ternary complex with APAD+ and oxalate"

    if doi == "10.7554/eLife.03574":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("date"):
                        dataset["date"] = u"2006"
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Riley,M."},
                            {"type": "group", "name": "Abe,T."},
                            {"type": "group", "name": "Arnaud,M.B."},
                            {"type": "group", "name": "Berlyn,M.K."},
                            {"type": "group", "name": "Blattner,F.R."},
                            {"type": "group", "name": "Chaudhuri,R.R."},
                            {"type": "group", "name": "Glasner,J.D."},
                            {"type": "group", "name": "Horiuchi,T."},
                            {"type": "group", "name": "Keseler,I.M."},
                            {"type": "group", "name": "Kosuge,T."},
                            {"type": "group", "name": "Mori,H."},
                            {"type": "group", "name": "Perna,N.T."},
                            {"type": "group", "name": "Plunkett,G. III"},
                            {"type": "group", "name": "Rudd,K.E."},
                            {"type": "group", "name": "Serres,M.H."},
                            {"type": "group", "name": "Thomas,G.H."},
                            {"type": "group", "name": "Thomson,N.R."},
                            {"type": "group", "name": "Wishart,D."},
                            {"type": "group", "name": "Wanner,B.L."},
                        ]

    if doi == "10.7554/eLife.03676":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro4":
                    if not dataset.get("date"):
                        dataset["date"] = u"2013"
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Human Gene Sequencing Center"}
                        ]

    if doi == "10.7554/eLife.03971":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Vanderperre B."}
                        ]

    if doi == "10.7554/eLife.04660":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if dataset.get("date") and dataset.get("date") == "2014-2015":
                        dataset["date"] = u"2014"

    if doi == "10.7554/eLife.06421":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if dataset.get("date") and dataset.get("date") == "NA":
                        dataset["date"] = u"2006"

    if doi == "10.7554/eLife.08445":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "data-ro1":
                    if not dataset.get("date"):
                        dataset["date"] = u"2006"
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "BDTNP SELEX"}]

    if doi == "10.7554/eLife.08916":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if (
                        dataset.get("date")
                        and dataset.get("date") == "2008, updated 2014"
                    ):
                        dataset["date"] = u"2008"
                if dataset.get("id") and dataset["id"] == "dataro3":
                    if (
                        dataset.get("date")
                        and dataset.get("date") == "2013, updated 2014"
                    ):
                        dataset["date"] = u"2013"

    if doi == "10.7554/eLife.08955":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Kurdistani S"},
                            {"type": "group", "name": "Marrban C"},
                            {"type": "group", "name": "Su T"},
                        ]

    if doi == "10.7554/eLife.09207":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {
                                "type": "group",
                                "name": "Prostate Cancer Genome Sequencing Project",
                            }
                        ]

    if doi == "10.7554/eLife.10607":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "data-ro4":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Authors"}]

    if doi == "10.7554/eLife.10670":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "data-ro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "HIVdb"}]

    # Add dates, authors, other details
    if doi == "10.7554/eLife.10856":
        if json_content.get("generated"):
            datasets_authors_for_10856 = [
                {"type": "group", "name": "Dagdas YF"},
                {"type": "group", "name": "Belhaj K"},
                {"type": "group", "name": "Maqbool A"},
                {"type": "group", "name": "Chaparro-Garcia A"},
                {"type": "group", "name": "Pandey P"},
                {"type": "group", "name": "Petre B"},
                {"type": "group", "name": "Tabassum N"},
                {"type": "group", "name": "Cruz-Mireles N"},
                {"type": "group", "name": "Hughes RK"},
                {"type": "group", "name": "Sklenar J"},
                {"type": "group", "name": "Win J"},
                {"type": "group", "name": "Menke F"},
                {"type": "group", "name": "Findlay K"},
                {"type": "group", "name": "Banfield MJ"},
                {"type": "group", "name": "Kamoun S"},
                {"type": "group", "name": "Bozkurt TO"},
            ]
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro7":
                    if not dataset.get("date"):
                        dataset["date"] = u"2016"
                    if not dataset.get("title"):
                        dataset["title"] = (
                            u"An effector of the Irish potato famine pathogen antagonizes a "
                            u"host autophagy cargo receptor"
                        )
                    if not dataset.get("authors"):
                        dataset["authors"] = datasets_authors_for_10856
                    if (
                        dataset.get("uri")
                        and dataset["uri"] == "http://www.ncbi.nlm.nih."
                    ):
                        dataset[
                            "uri"
                        ] = "https://www.ncbi.nlm.nih.gov/nuccore/976151098/"
                if dataset.get("id") and dataset["id"] == "dataro8":
                    if not dataset.get("date"):
                        dataset["date"] = u"2015"
                    if not dataset.get("title"):
                        dataset["title"] = (
                            u"An effector of the Irish potato famine pathogen antagonizes a "
                            u"host autophagy cargo receptor"
                        )
                    if not dataset.get("authors"):
                        dataset["authors"] = datasets_authors_for_10856
                    if (
                        dataset.get("uri")
                        and dataset["uri"] == "http://www.ncbi.nlm.nih."
                    ):
                        dataset[
                            "uri"
                        ] = "https://www.ncbi.nlm.nih.gov/nuccore/976151096/"
                if dataset.get("id") and dataset["id"] == "dataro9":
                    if not dataset.get("authors"):
                        dataset["authors"] = datasets_authors_for_10856

    if doi == "10.7554/eLife.10877":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("title"):
                        dataset["title"] = (
                            u"Oct4 ChIP-Seq at G1 and G2/M phase of cell cycle in "
                            u"mouse embryonic stem cells"
                        )

    if doi == "10.7554/eLife.10921":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Floor SN"},
                            {"type": "group", "name": "Doudna JA"},
                        ]
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Sidrauski C"},
                            {"type": "group", "name": "McGeachy A"},
                            {"type": "group", "name": "Ingolia N"},
                            {"type": "group", "name": "Walter P"},
                        ]

    if doi == "10.7554/eLife.11117":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro14":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Authors"}]

    if doi == "10.7554/eLife.12204":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Rhodes DR"},
                            {"type": "group", "name": "Kalyana-Sundaram S"},
                            {"type": "group", "name": "Mahavisno V"},
                            {"type": "group", "name": "Varambally R"},
                            {"type": "group", "name": "Yu J"},
                            {"type": "group", "name": "Briggs BB"},
                            {"type": "group", "name": "Barrette TR"},
                            {"type": "group", "name": "Anstet MJ"},
                            {"type": "group", "name": "Kincead-Beal C"},
                            {"type": "group", "name": "Kulkarni P"},
                            {"type": "group", "name": "Varambally S"},
                            {"type": "group", "name": "Ghosh D"},
                            {"type": "group", "name": "Chinnaiyan AM."},
                        ]
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Gaspar C"},
                            {"type": "group", "name": "Cardoso J"},
                            {"type": "group", "name": "Franken P"},
                            {"type": "group", "name": "Molenaar L"},
                            {"type": "group", "name": "Morreau H"},
                            {"type": "group", "name": "Möslein G"},
                            {"type": "group", "name": "Sampson J"},
                            {"type": "group", "name": "Boer JM"},
                            {"type": "group", "name": "de Menezes RX"},
                            {"type": "group", "name": "Fodde R."},
                        ]
                if dataset.get("id") and dataset["id"] == "dataro3":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Graudens E"},
                            {"type": "group", "name": "Boulanger V"},
                            {"type": "group", "name": "Mollard C"},
                            {"type": "group", "name": "Mariage-Samson R"},
                            {"type": "group", "name": "Barlet X"},
                            {"type": "group", "name": "Grémy G"},
                            {"type": "group", "name": "Couillault C"},
                            {"type": "group", "name": "Lajémi M"},
                            {"type": "group", "name": "Piatier-Tonneau D"},
                            {"type": "group", "name": "Zaborski P"},
                            {"type": "group", "name": "Eveno E"},
                            {"type": "group", "name": "Auffray C"},
                            {"type": "group", "name": "Imbeaud S."},
                        ]
                if dataset.get("id") and dataset["id"] == "dataro4":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Hong Y"},
                            {"type": "group", "name": "Downey T"},
                            {"type": "group", "name": "Eu KW"},
                            {"type": "group", "name": "Koh PK"},
                            {"type": "group", "name": "Cheah PY"},
                        ]
                if dataset.get("id") and dataset["id"] == "dataro5":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Kaiser S"},
                            {"type": "group", "name": "Park YK"},
                            {"type": "group", "name": "Franklin JL"},
                            {"type": "group", "name": "Halberg RB"},
                            {"type": "group", "name": "Yu M"},
                            {"type": "group", "name": "Jessen WJ"},
                            {"type": "group", "name": "Freudenberg J"},
                            {"type": "group", "name": "Chen X"},
                            {"type": "group", "name": "Haigis K"},
                            {"type": "group", "name": "Jegga AG"},
                            {"type": "group", "name": "Kong S"},
                            {"type": "group", "name": "Sakthivel B"},
                            {"type": "group", "name": "Xu H"},
                            {"type": "group", "name": "Reichling T"},
                            {"type": "group", "name": "Azhar M"},
                            {"type": "group", "name": "Boivin GP"},
                            {"type": "group", "name": "Roberts RB"},
                            {"type": "group", "name": "Bissahoyo AC"},
                            {"type": "group", "name": "Gonzales F"},
                            {"type": "group", "name": "Bloom GC"},
                            {"type": "group", "name": "Eschrich S"},
                            {"type": "group", "name": "Carter SL"},
                            {"type": "group", "name": "Aronow JE"},
                            {"type": "group", "name": "Kleimeyer J"},
                            {"type": "group", "name": "Kleimeyer M"},
                            {"type": "group", "name": "Ramaswamy V"},
                            {"type": "group", "name": "Settle SH"},
                            {"type": "group", "name": "Boone B"},
                            {"type": "group", "name": "Levy S"},
                            {"type": "group", "name": "Graff JM"},
                            {"type": "group", "name": "Doetschman T"},
                            {"type": "group", "name": "Groden J"},
                            {"type": "group", "name": "Dove WF"},
                            {"type": "group", "name": "Threadgill DW"},
                            {"type": "group", "name": "Yeatman TJ"},
                            {"type": "group", "name": "Coffey RJ Jr"},
                            {"type": "group", "name": "Aronow BJ."},
                        ]
                if dataset.get("id") and dataset["id"] == "dataro6":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Muzny DM et al"}
                        ]
                if dataset.get("id") and dataset["id"] == "dataro7":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Skrzypczak M"},
                            {"type": "group", "name": "Goryca K"},
                            {"type": "group", "name": "Rubel T"},
                            {"type": "group", "name": "Paziewska A"},
                            {"type": "group", "name": "Mikula M"},
                            {"type": "group", "name": "Jarosz D"},
                            {"type": "group", "name": "Pachlewski J"},
                            {"type": "group", "name": "Oledzki J"},
                            {"type": "group", "name": "Ostrowski J."},
                        ]
                if dataset.get("id") and dataset["id"] == "dataro8":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Cancer Genome Atlas Network"}
                        ]

    if doi == "10.7554/eLife.12876":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {
                                "type": "group",
                                "name": "Department of Human Genetics, University of Utah",
                            }
                        ]

    if doi == "10.7554/eLife.13195":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {
                                "type": "group",
                                "name": "Microbial Ecology Group, Colorado State University",
                            }
                        ]

    if doi == "10.7554/eLife.14158":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "data-ro1":
                    if not dataset.get("title"):
                        dataset["title"] = u"Bacterial initiation protein"
                if dataset.get("id") and dataset["id"] == "data-ro2":
                    if not dataset.get("title"):
                        dataset[
                            "title"
                        ] = u"Bacterial initiation protein in complex with Phage inhibitor protein"
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro3":
                    if not dataset.get("date"):
                        dataset["date"] = u"2007"

    if doi == "10.7554/eLife.14243":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "Tramantano M"},
                            {"type": "group", "name": "Sun L"},
                            {"type": "group", "name": "Au C"},
                            {"type": "group", "name": "Labuz D"},
                            {"type": "group", "name": "Liu Z"},
                            {"type": "group", "name": "Chou M"},
                            {"type": "group", "name": "Shen C"},
                            {"type": "group", "name": "Luk E"},
                        ]

    if doi == "10.7554/eLife.16078":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if (
                        dataset.get("date")
                        and dataset.get("date") == "current manuscript"
                    ):
                        dataset["date"] = u"2016"

    if doi == "10.7554/eLife.17082":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "data-ro4":
                    if not dataset.get("date"):
                        dataset["date"] = u"2012"
                if dataset.get("id") and dataset["id"] == "data-ro5":
                    if not dataset.get("date"):
                        dataset["date"] = u"2014"
                if dataset.get("id") and dataset["id"] == "data-ro6":
                    if not dataset.get("date"):
                        dataset["date"] = u"2014"
                    if not dataset.get("authors"):
                        dataset["authors"] = [
                            {"type": "group", "name": "The Cancer Genome Atlas (TCGA)"}
                        ]

    if doi == "10.7554/eLife.17473":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if dataset.get("date") and dataset.get("date").startswith(
                        "Release date"
                    ):
                        dataset["date"] = u"2016"

    return json_content


def rewrite_elife_decision_letter_json(json_content, doi):
    """ this does the work of rewriting elife decision letter json """

    # Add description
    if doi == "10.7554/eLife.10856":
        if json_content.get("description") is None:
            json_content["description"] = [
                {
                    "type": "paragraph",
                    "text": (
                        "In the interests of transparency, eLife includes the editorial "
                        "decision letter and accompanying author responses. A lightly edited "
                        "version of the letter sent to the authors after peer review is shown, "
                        "indicating the most substantive concerns; minor comments are not "
                        "usually included."
                    ),
                }
            ]

    return json_content


def rewrite_elife_editors_json(json_content, doi):
    """ this does the work of rewriting elife editors json """

    # Remove affiliations with no name value
    for i, ref in enumerate(json_content):
        if ref.get("affiliations"):
            for aff in ref.get("affiliations"):
                if "name" not in aff:
                    del json_content[i]["affiliations"]

    # Add editor role
    editor_roles = {}
    editor_roles["10.7554/eLife.00534"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.09376"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.10056"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.11031"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.12081"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.12241"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.12509"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13023"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13053"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13426"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13620"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13810"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13828"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13887"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.13905"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14000"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14155"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14170"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14226"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14277"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14315"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14316"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14530"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14601"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14618"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14749"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.14814"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15266"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15275"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15292"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15316"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15470"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15545"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15716"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15747"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15828"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15833"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15915"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.15986"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16088"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16093"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16127"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16159"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16178"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16309"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16777"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16793"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.16950"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17101"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17180"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17240"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17262"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17282"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17463"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17551"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17667"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17681"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17978"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.17985"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18103"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18207"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18246"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18249"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18432"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18447"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18458"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18491"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18541"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18542"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18579"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18605"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18633"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18657"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18919"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.18970"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19027"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19088"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19089"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19295"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19377"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19406"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19466"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19484"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19505"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19535"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19568"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19573"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19662"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19671"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19686"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19695"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19720"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19749"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19766"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19804"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19809"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19887"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19976"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.19991"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20010"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20054"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20070"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20183"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20185"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20214"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20236"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20309"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20343"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20357"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20362"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20365"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20390"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20417"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20515"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20533"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20607"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20640"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20667"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20718"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20722"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20777"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20782"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20787"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20797"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20799"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20813"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20954"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20958"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.20985"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21032"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21049"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21052"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21170"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21172"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21290"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21330"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21394"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21397"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21455"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21481"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21491"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21589"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21598"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21616"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21635"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21728"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21771"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21776"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21855"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21886"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21920"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.21989"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22028"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22053"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22170"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22177"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22280"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22409"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22429"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22431"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22467"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22472"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22502"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22771"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22784"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.22866"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.23156"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.23352"] = "Reviewing Editor"
    editor_roles["10.7554/eLife.23804"] = "Reviewing Editor"

    # Edge case fix an affiliation name
    if doi in editor_roles:
        for i, ref in enumerate(json_content):
            if not ref.get("role"):
                json_content[i]["role"] = editor_roles[doi]
            elif ref.get("role"):
                json_content[i]["role"] = "Reviewing Editor"
    else:
        # Fix capitalisation on exiting role values
        for i, ref in enumerate(json_content):
            if ref.get("role") == "Reviewing editor":
                json_content[i]["role"] = "Reviewing Editor"

    # Remove duplicates
    editors_kept = []
    for i, ref in enumerate(json_content):
        editor_values = OrderedDict()
        editor_values["role"] = ref.get("role")
        if ref.get("name"):
            editor_values["name"] = ref.get("name").get("index")
        if editor_values in editors_kept:
            # remove if one is already kept
            del json_content[i]
        else:
            editors_kept.append(editor_values)

    # Merge two role values
    role_replacements = [
        {
            "role_from": ["Senior Editor", "Reviewing Editor"],
            "role_to": "Senior and Reviewing Editor",
        }
    ]
    for replace_rule in role_replacements:
        same_name_map = person_same_name_map(
            json_content, replace_rule.get("role_from")
        )
        role_is_set = None
        for same_id_list in same_name_map.values():
            if not same_id_list or len(same_id_list) <= 1:
                # no more than one name match, nothing to replace
                continue
            deleted_count = 0
            for same_id in same_id_list:
                if not role_is_set:
                    # reset the role for the first person record
                    json_content[same_id]["role"] = replace_rule.get("role_to")
                    role_is_set = True
                else:
                    # first one is already set, remove the duplicates
                    del json_content[same_id - deleted_count]
                    deleted_count += 1

    return json_content


def person_same_name_map(json_content, role_from):
    "to merge multiple editors into one record, filter by role values and group by name"
    matched_editors = [
        (i, person)
        for i, person in enumerate(json_content)
        if person.get("role") in role_from
    ]
    same_name_map = {}
    for i, editor in matched_editors:
        if not editor.get("name"):
            continue
        # compare name of each
        name = editor.get("name").get("index")
        if name not in same_name_map:
            same_name_map[name] = []
        same_name_map[name].append(i)
    return same_name_map


def rewrite_elife_title_prefix_json(json_content, doi):
    """ this does the work of rewriting elife title prefix json values"""
    if not json_content:
        return json_content

    # title prefix rewrites by article DOI
    title_prefix_values = {}
    title_prefix_values["10.7554/eLife.00452"] = "Point of View"
    title_prefix_values["10.7554/eLife.00615"] = "Point of View"
    title_prefix_values["10.7554/eLife.00639"] = "Point of View"
    title_prefix_values["10.7554/eLife.00642"] = "Point of View"
    title_prefix_values["10.7554/eLife.00856"] = "Point of View"
    title_prefix_values["10.7554/eLife.01061"] = "Point of View"
    title_prefix_values["10.7554/eLife.01138"] = "Point of View"
    title_prefix_values["10.7554/eLife.01139"] = "Point of View"
    title_prefix_values["10.7554/eLife.01820"] = "Animal Models of Disease"
    title_prefix_values["10.7554/eLife.02576"] = "Point of View"
    title_prefix_values["10.7554/eLife.04902"] = "Point of View"
    title_prefix_values["10.7554/eLife.05614"] = "Point of View"
    title_prefix_values[
        "10.7554/eLife.05635"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.05826"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.05835"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.05849"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.05861"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.05959"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.06024"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.06100"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.06793"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.06813"
    ] = "The Natural History of Model Organisms"
    title_prefix_values[
        "10.7554/eLife.06956"
    ] = "The Natural History of Model Organisms"
    title_prefix_values["10.7554/eLife.09305"] = "Point of View"
    title_prefix_values["10.7554/eLife.10825"] = "Point of View"
    title_prefix_values["10.7554/eLife.11628"] = "Living Science"
    title_prefix_values["10.7554/eLife.12708"] = "Point of View"
    title_prefix_values["10.7554/eLife.12844"] = "Point of View"
    title_prefix_values["10.7554/eLife.13035"] = "Point of View"
    title_prefix_values["10.7554/eLife.14258"] = "Cutting Edge"
    title_prefix_values["10.7554/eLife.14424"] = "Point of View"
    title_prefix_values["10.7554/eLife.14511"] = "Cell Proliferation"
    title_prefix_values["10.7554/eLife.14721"] = "Intracellular Bacteria"
    title_prefix_values["10.7554/eLife.14790"] = "Decision Making"
    title_prefix_values["10.7554/eLife.14830"] = "Progenitor Cells"
    title_prefix_values["10.7554/eLife.14953"] = "Gene Expression"
    title_prefix_values["10.7554/eLife.14973"] = "Breast Cancer"
    title_prefix_values["10.7554/eLife.15352"] = "Autoimmune Disorders"
    title_prefix_values["10.7554/eLife.15438"] = "Motor Circuits"
    title_prefix_values["10.7554/eLife.15591"] = "Protein Tagging"
    title_prefix_values["10.7554/eLife.15928"] = "Point of View"
    title_prefix_values["10.7554/eLife.15938"] = "Cancer Metabolism"
    title_prefix_values["10.7554/eLife.15957"] = "Stem Cells"
    title_prefix_values["10.7554/eLife.15963"] = "Prediction Error"
    title_prefix_values["10.7554/eLife.16019"] = "Social Networks"
    title_prefix_values["10.7554/eLife.16076"] = "mRNA Decay"
    title_prefix_values["10.7554/eLife.16207"] = "Cardiac Development"
    title_prefix_values["10.7554/eLife.16209"] = "Neural Coding"
    title_prefix_values["10.7554/eLife.16393"] = "Neural Circuits"
    title_prefix_values["10.7554/eLife.16598"] = "RNA Localization"
    title_prefix_values["10.7554/eLife.16758"] = "Adaptive Evolution"
    title_prefix_values["10.7554/eLife.16800"] = "Point of View"
    title_prefix_values["10.7554/eLife.16846"] = "Living Science"
    title_prefix_values["10.7554/eLife.16931"] = "Point of View"
    title_prefix_values["10.7554/eLife.16964"] = "Ion Channels"
    title_prefix_values["10.7554/eLife.17224"] = "Host-virus Interactions"
    title_prefix_values["10.7554/eLife.17293"] = "Ion Channels"
    title_prefix_values["10.7554/eLife.17393"] = "Point of View"
    title_prefix_values["10.7554/eLife.17394"] = "p53 Family Proteins"
    title_prefix_values["10.7554/eLife.18203"] = "Antibody Engineering"
    title_prefix_values["10.7554/eLife.18243"] = "Host-virus Interactions"
    title_prefix_values["10.7554/eLife.18365"] = "DNA Repair"
    title_prefix_values["10.7554/eLife.18431"] = "Unfolded Protein Response"
    title_prefix_values["10.7554/eLife.18435"] = "Long Distance Transport"
    title_prefix_values["10.7554/eLife.18721"] = "Decision Making"
    title_prefix_values["10.7554/eLife.18753"] = "Resource Competition"
    title_prefix_values["10.7554/eLife.18871"] = "Mathematical Modeling"
    title_prefix_values["10.7554/eLife.18887"] = "Sensorimotor Transformation"
    title_prefix_values["10.7554/eLife.19285"] = "Genetic Screen"
    title_prefix_values["10.7554/eLife.19351"] = "Motor Control"
    title_prefix_values["10.7554/eLife.19405"] = "Membrane Structures"
    title_prefix_values["10.7554/eLife.19733"] = "Focal Adhesions"
    title_prefix_values["10.7554/eLife.20043"] = "Amyloid-beta Peptides"
    title_prefix_values["10.7554/eLife.20314"] = "Plant Reproduction"
    title_prefix_values["10.7554/eLife.20468"] = "Endoplasmic Reticulum"
    title_prefix_values["10.7554/eLife.20516"] = "Innate Like Lymphocytes"
    title_prefix_values["10.7554/eLife.21070"] = "Scientific Publishing"
    title_prefix_values["10.7554/eLife.21236"] = "Developmental Neuroscience"
    title_prefix_values["10.7554/eLife.21522"] = "Developmental Neuroscience"
    title_prefix_values["10.7554/eLife.21723"] = "Living Science"
    title_prefix_values["10.7554/eLife.21863"] = "Genetic Screening"
    title_prefix_values["10.7554/eLife.21864"] = "Evolutionary Biology"
    title_prefix_values["10.7554/eLife.22073"] = "Unfolded Protein Response"
    title_prefix_values["10.7554/eLife.22186"] = "Point of View"
    title_prefix_values["10.7554/eLife.22215"] = "Neural Wiring"
    title_prefix_values["10.7554/eLife.22256"] = "Molecular Communication"
    title_prefix_values["10.7554/eLife.22471"] = "Point of View"
    title_prefix_values["10.7554/eLife.22661"] = "Reproducibility in Cancer Biology"
    title_prefix_values["10.7554/eLife.22662"] = "Reproducibility in Cancer Biology"
    title_prefix_values["10.7554/eLife.22735"] = "Motor Networks"
    title_prefix_values["10.7554/eLife.22850"] = "Heat Shock Response"
    title_prefix_values["10.7554/eLife.22915"] = "Reproducibility in Cancer Biology"
    title_prefix_values["10.7554/eLife.22926"] = "Skeletal Stem Cells"
    title_prefix_values["10.7554/eLife.23375"] = "Social Evolution"
    title_prefix_values["10.7554/eLife.23383"] = "Reproducibility in Cancer Biology"
    title_prefix_values["10.7554/eLife.23447"] = "Genetic Rearrangement"
    title_prefix_values["10.7554/eLife.23693"] = "Reproducibility in Cancer Biology"
    title_prefix_values["10.7554/eLife.23804"] = "Point of View"
    title_prefix_values["10.7554/eLife.24038"] = "Cell Division"
    title_prefix_values["10.7554/eLife.24052"] = "DNA Replication"
    title_prefix_values["10.7554/eLife.24106"] = "Germ Granules"
    title_prefix_values["10.7554/eLife.24238"] = "Tumor Angiogenesis"
    title_prefix_values["10.7554/eLife.24276"] = "Stem Cells"
    title_prefix_values["10.7554/eLife.24611"] = "Point of View"
    title_prefix_values["10.7554/eLife.24896"] = "Visual Behavior"
    title_prefix_values["10.7554/eLife.25000"] = "Chromatin Mapping"
    title_prefix_values["10.7554/eLife.25001"] = "Cell Cycle"
    title_prefix_values["10.7554/eLife.25159"] = "Ion Channels"
    title_prefix_values["10.7554/eLife.25358"] = "Cell Division"
    title_prefix_values["10.7554/eLife.25375"] = "Membrane Phase Separation"
    title_prefix_values["10.7554/eLife.25408"] = "Plain-language Summaries of Research"
    title_prefix_values["10.7554/eLife.25410"] = "Plain-language Summaries of Research"
    title_prefix_values["10.7554/eLife.25411"] = "Plain-language Summaries of Research"
    title_prefix_values["10.7554/eLife.25412"] = "Plain-language Summaries of Research"
    title_prefix_values["10.7554/eLife.25431"] = "Genetic Diversity"
    title_prefix_values["10.7554/eLife.25654"] = "Systems Biology"
    title_prefix_values["10.7554/eLife.25669"] = "Paternal Effects"
    title_prefix_values["10.7554/eLife.25700"] = "TOR Signaling"
    title_prefix_values["10.7554/eLife.25835"] = "Cutting Edge"
    title_prefix_values["10.7554/eLife.25858"] = "Developmental Biology"
    title_prefix_values["10.7554/eLife.25956"] = "Point of View"
    title_prefix_values["10.7554/eLife.25996"] = "Cancer Therapeutics"
    title_prefix_values["10.7554/eLife.26295"] = "Point of View"
    title_prefix_values["10.7554/eLife.26401"] = "Object Recognition"
    title_prefix_values["10.7554/eLife.26775"] = "Human Evolution"
    title_prefix_values["10.7554/eLife.26787"] = "Cutting Edge"
    title_prefix_values["10.7554/eLife.26942"] = "Alzheimer’s Disease"
    title_prefix_values["10.7554/eLife.27085"] = "Translational Control"
    title_prefix_values["10.7554/eLife.27198"] = "Cell Signaling"
    title_prefix_values["10.7554/eLife.27438"] = "Point of View"
    title_prefix_values["10.7554/eLife.27467"] = "Evolutionary Developmental Biology"
    title_prefix_values["10.7554/eLife.27605"] = "Population Genetics"
    title_prefix_values["10.7554/eLife.27933"] = "Ion Channels"
    title_prefix_values["10.7554/eLife.27982"] = "Living Science"
    title_prefix_values["10.7554/eLife.28339"] = "Oncogene Regulation"
    title_prefix_values["10.7554/eLife.28514"] = "Maternal Behavior"
    title_prefix_values["10.7554/eLife.28699"] = "Point of View"
    title_prefix_values["10.7554/eLife.28757"] = "Mitochondrial Homeostasis"
    title_prefix_values["10.7554/eLife.29056"] = "Gene Variation"
    title_prefix_values["10.7554/eLife.29104"] = "Cardiac Hypertrophy"
    title_prefix_values["10.7554/eLife.29502"] = "Meiotic Recombination"
    title_prefix_values["10.7554/eLife.29586"] = "Virus Evolution"
    title_prefix_values["10.7554/eLife.29942"] = "Post-translational Modifications"
    title_prefix_values["10.7554/eLife.30076"] = "Scientific Publishing"
    title_prefix_values["10.7554/eLife.30183"] = "Point of View"
    title_prefix_values["10.7554/eLife.30194"] = "Organ Development"
    title_prefix_values["10.7554/eLife.30249"] = "Tissue Regeneration"
    title_prefix_values["10.7554/eLife.30280"] = "Adverse Drug Reactions"
    title_prefix_values["10.7554/eLife.30599"] = "Living Science"
    title_prefix_values["10.7554/eLife.30865"] = "Stone Tool Use"
    title_prefix_values["10.7554/eLife.31106"] = "Sensory Neurons"
    title_prefix_values["10.7554/eLife.31328"] = "Drought Stress"
    title_prefix_values["10.7554/eLife.31697"] = "Scientific Publishing"
    title_prefix_values["10.7554/eLife.31808"] = "Tissue Engineering"
    title_prefix_values["10.7554/eLife.31816"] = "Sound Processing"
    title_prefix_values["10.7554/eLife.32011"] = "Peer Review"
    title_prefix_values["10.7554/eLife.32012"] = "Peer Review"
    title_prefix_values["10.7554/eLife.32014"] = "Peer Review"
    title_prefix_values["10.7554/eLife.32015"] = "Peer Review"
    title_prefix_values["10.7554/eLife.32016"] = "Peer Review"
    title_prefix_values["10.7554/eLife.32715"] = "Point of View"

    # Edge case fix title prefix values
    if doi in title_prefix_values:
        # Do a quick sanity check, only replace if the lowercase comparison is equal
        #  just in case the value has been changed to something else we will not replace it
        if json_content.lower() == title_prefix_values[doi].lower():
            json_content = title_prefix_values[doi]

    return json_content
