# coding=utf-8

import parseJATS as parser
from collections import OrderedDict

def rewrite_json(rewrite_type, soup, json_content):
    """
    Due to XML content that will not conform with the strict JSON schema validation rules,
    for elife articles only, rewrite the JSON to make it valid
    """
    if not soup:
        return json_content
    if not parser.doi(soup) or not parser.journal_id(soup):
        return json_content

    # Hook only onto elife articles for rewriting currently
    if parser.journal_id(soup).lower() == "elife":
        function_name = rewrite_function_name(parser.journal_id(soup), rewrite_type)
        if function_name:
            try:
                json_content = globals()[function_name](json_content, parser.doi(soup))
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
        json_content = rewrite_references_json(json_content, references_rewrite_json[doi])

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
            for key, value in rewrite_json.get(ref.get("id")).iteritems():
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
    references_rewrite_json["10.7554/eLife.02030"] = {"bib53": {"date": "2013"}, "bib56": {"date": "2013"}}
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
        "bib37": {"date": "1959"}}
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
        "bib2": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.08500"] = {"bib55": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.09066"] = {"bib46": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.09100"] = {"bib50": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.09148"] = {
        "bib47": {"articleTitle": "97–104"},
        "bib59": {"articleTitle": "1913–1918"}}
    references_rewrite_json["10.7554/eLife.09186"] = {
        "bib31": {"date": "2015"},
        "bib54": {"date": "2014"},
        "bib56": {"date": "2014"},
        "bib65": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.09215"] = {"bib5": {"date": "2012"}}
    references_rewrite_json["10.7554/eLife.09579"] = {
        "bib19": {"date": "2007"},
        "bib49": {"date": "2002"}}
    references_rewrite_json["10.7554/eLife.09600"] = {"bib13": {"date": "2009"}}
    references_rewrite_json["10.7554/eLife.09771"] = {"bib22": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.09972"] = {"bib61": {"date": "2007", "discriminator": "a"}}
    references_rewrite_json["10.7554/eLife.09977"] = {"bib41": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.10032"] = {"bib45": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.10042"] = {"bib14": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10070"] = {"bib15": {"date": "2015"}, "bib38": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.10222"] = {"bib30": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10670"] = {"bib8": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10781"] = {"bib32": {"date": "2003"}}
    references_rewrite_json["10.7554/eLife.11273"] = {"bib43": {"date": "2004"}}
    references_rewrite_json["10.7554/eLife.11305"] = {"bib68": {"date": "2000"}}
    references_rewrite_json["10.7554/eLife.11416"] = {"bib22": {"date": "1997"}}
    references_rewrite_json["10.7554/eLife.11860"] = {"bib48": {"title": "Light-switchable gene expression system"}}
    references_rewrite_json["10.7554/eLife.12401"] = {"bib25": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.12366"] = {"bib10": {"date": "2008"}}
    references_rewrite_json["10.7554/eLife.12703"] = {"bib27": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.12735"] = {"bib35": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.12830"] = {"bib118": {"date": "1982"}}
    references_rewrite_json["10.7554/eLife.13133"] = {"bib11": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.13152"] = {"bib25": {"date": "2000"}}
    references_rewrite_json["10.7554/eLife.13195"] = {"bib6": {"date": "2013"}, "bib12": {"date": "2003"}}
    references_rewrite_json["10.7554/eLife.13479"] = {"bib5": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.13463"] = {"bib15": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.14119"] = {"bib40": {"date": "2007"}}
    references_rewrite_json["10.7554/eLife.14169"] = {"bib6": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.14523"] = {"bib7": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.15272"] = {"bib78": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.15504"] = {"bib67": {"isbn": "9780198524304"}}
    references_rewrite_json["10.7554/eLife.16105"] = {"bib2": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.16349"] = {"bib68": {"date": "2005"}}
    references_rewrite_json["10.7554/eLife.16394"] = {
        "bib6": {"type": "thesis",
        "author": {"type": "person", "name": {"preferred": "B Berret","index": "Berret, B" }},
        "publisher": {"name": ["Université de Bourgogne"]}}}
    references_rewrite_json["10.7554/eLife.16443"] = {"bib58": {"date": "1987"}}
    references_rewrite_json["10.7554/eLife.16764"] = {"bib4": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.17092"] = {"bib102": {"date": "1980"}}
    references_rewrite_json["10.7554/eLife.18044"] = {"bib25": {"date": "2005"}}
    references_rewrite_json["10.7554/eLife.18370"] = {"bib1": {"date": "2006"}}
    references_rewrite_json["10.7554/eLife.18425"] = {"bib54": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.18683"] = {"bib47": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.19545"] = {"bib51": {"date": "1996"}}
    references_rewrite_json["10.7554/eLife.20352"] = {"bib53": {"country": "United States"}}
    references_rewrite_json["10.7554/eLife.21864"] = {"bib2": {"date": "2016-10-24"}}

    # Reference authors data to replace, processed further below into json
    references_authors = []
    references_authors.append(("10.7554/eLife.00036", "bib8", "authors", [
        {"surname": "Butler", "given-names": "H"},
        {"surname": "Juurlink", "given-names": "BHJ"}
        ]))
    references_authors.append(("10.7554/eLife.00036", "bib30", "authors", [
        {"surname": "Joyner", "given-names": "AL"}
        ]))

    references_authors.append(("10.7554/eLife.00048", "bib15", "authors", [
        {"surname": "Guthrie", "given-names": "C"},
        {"surname": "Fink", "given-names": "GR"}
        ]))

    references_authors.append(("10.7554/eLife.00051", "bib21", "authors", [
        {"surname": "Jamison", "given-names": "DT"},
        {"surname": "Breman", "given-names": "JG"},
        {"surname": "Measham", "given-names": "AR"},
        {"surname": "Alleyne", "given-names": "G"},
        {"surname": "Claeson", "given-names": "M"},
        {"surname": "Evans", "given-names": "DB"},
        {"surname": "Jha", "given-names": "P"},
        {"surname": "Mills", "given-names": "A"},
        {"surname": "Musgrove", "given-names": "P"}
        ]))
    references_authors.append(("10.7554/eLife.00051", "bib36", "authors", [
        {"surname": "Rogers", "given-names": "RG"},
        {"surname": "Crimmins", "given-names": "EM"}
        ]))

    references_authors.append(("10.7554/eLife.00668", "bib39", "authors", [
        {"surname": "Rice", "given-names": "SA"}
        ]))

    references_authors.append(("10.7554/eLife.01730", "bib75", "authors", [
        {"collab": "Look AHEAD Research Group"}
        ]))

    references_authors.append(("10.7554/eLife.03714", "bib64", "authors", [
        {"surname": "Otwinowski", "given-names": "Z"},
        {"surname": "Minor", "given-names": "W"}
        ]))

    references_authors.append(("10.7554/eLife.04220", "bib31", "authors", [
        {"surname": "Tishby", "given-names": "N"},
        {"surname": "Polani", "given-names": "D"}
        ]))

    references_authors.append(("10.7554/eLife.04395", "bib67", "authors", [
        {"surname": "King", "given-names": "AMQ"},
        {"surname": "Adams", "given-names": "MJ"},
        {"surname": "Carstens", "given-names": "EB"},
        {"surname": "Lefkowitz", "given-names": "E"}
        ]))

    references_authors.append(("10.7554/eLife.04449", "bib62", "authors", [
        {"surname": "Shaham", "given-names": "S"}
        ]))

    references_authors.append(("10.7554/eLife.04659", "bib57", "authors", [
        {"surname": "Sambrook", "given-names": "J"},
        {"surname": "Russell", "given-names": "TW"}
        ]))

    references_authors.append(("10.7554/eLife.05423", "bib4", "authors", [
        {"surname": "Birkhead", "given-names": "TR"},
        {"surname": "Møller", "given-names": "AP"}
        ]))
    references_authors.append(("10.7554/eLife.05423", "bib5", "authors", [
        {"surname": "Birkhead", "given-names": "TR"},
        {"surname": "Møller", "given-names": "AP"}
        ]))
    references_authors.append(("10.7554/eLife.05423", "bib90", "authors", [
        {"surname": "Smith", "given-names": "RL"}
        ]))

    references_authors.append(("10.7554/eLife.05564", "bib39", "authors", [
        {"surname": "Pattyn", "given-names": "S"}
        ]))

    references_authors.append(("10.7554/eLife.05959", "bib76", "authors", [
        {"surname": "Macholán", "given-names": "M"},
        {"surname": "Baird", "given-names": "SJE"},
        {"surname": "Munclinger", "given-names": "P"},
        {"surname": "Piálek", "given-names": "J"}
        ]))

    references_authors.append(("10.7554/eLife.06565", "bib1", "authors", [
        {"surname": "Ahringer", "given-names": "J"}
        ]))

    references_authors.append(("10.7554/eLife.06576", "bib57", "authors", [
        {"surname": "Moller", "given-names": "AR"}
        ]))

    references_authors.append(("10.7554/eLife.06813", "bib54", "authors", [
        {"surname": "King", "given-names": "JA"}
        ]))

    references_authors.append(("10.7554/eLife.06813", "bib55", "authors", [
        {"surname": "Kirkland", "given-names": "Gl"},
        {"surname": "Layne", "given-names": "JN"}
        ]))

    references_authors.append(("10.7554/eLife.07460", "bib1", "authors", [
        {"surname": "Rallapalli", "given-names": "Ghanasyam"}
        ]))
    references_authors.append(("10.7554/eLife.07460", "bib2", "authors", [
        {"surname": "Bazyl", "given-names": "Steven"}
        ]))

    references_authors.append(("10.7554/eLife.07847", "bib40", "authors", [
        {"collab": "Nature Immunology"}
        ]))

    references_authors.append(("10.7554/eLife.09666", "bib9", "authors", [
        {"surname": "Schüler", "given-names": "D"}
        ]))

    references_authors.append(("10.7554/eLife.09868", "bib5", "authors", [
        {"surname": "Barlow", "given-names": "HB"}
        ]))

    references_authors.append(("10.7554/eLife.10222", "bib30", "authors", [
        {"collab": "PharmaMar"}
        ]))

    references_authors.append(("10.7554/eLife.11860", "bib48", "authors", [
        {"surname": "Yang", "given-names": "Y"},
        {"surname": "Wang", "given-names": "X"},
        {"surname": "Chen", "given-names": "X"},
        ]))

    references_authors.append(("10.7554/eLife.11945", "bib23", "authors", [
        {"surname": "Glimcher", "given-names": "P"},
        {"surname": "Fehr", "given-names": "E"}
        ]))

    references_authors.append(("10.7554/eLife.13135", "bib26", "authors", [
        {"surname": "Ivanova", "given-names": "S"},
        {"surname": "Herbreteau", "given-names": "B"},
        {"surname": "Blasdell", "given-names": "K"},
        {"surname": "Chaval", "given-names": "Y"},
        {"surname": "Buchy", "given-names": "P"},
        {"surname": "Guillard", "given-names": "B"},
        {"surname": "Morand", "given-names": "S"},
        ]))

    references_authors.append(("10.7554/eLife.13135", "bib27", "authors", [
        {"surname": "King", "given-names": "AMQ"},
        {"surname": "Adams", "given-names": "J"},
        {"surname": "Carstens", "given-names": "EB"},
        {"surname": "Lefkowitz", "given-names": "EJ"}
        ]))

    references_authors.append(("10.7554/eLife.14188", "bib1", "authors", [
        {"collab": "Avisoft Bioacoustics"}
        ]))

    references_authors.append(("10.7554/eLife.17716", "bib7", "authors", [
        {"collab": "World Health Organization"}
        ]))

    references_authors.append(("10.7554/eLife.17956", "bib4", "authors", [
        {"surname": "Barrett", "given-names": "SCH"}
        ]))

    references_authors.append(("10.7554/eLife.18109", "bib39", "authors", [
        {"surname": "Weber", "given-names": "EH"}
        ]))


    # Now turn the authors data into the json
    for author_row in references_authors:
        ref_json = OrderedDict()
        doi, id, author_type, authors = author_row
        #if id not in ref_json:
        ref_json[id] = OrderedDict()
        ref_json[id][author_type] = []
        for ref_author in authors:
            if  "collab" in ref_author:
                author_json = parser.references_author_collab(ref_author)
            else:
                author_json = parser.references_author_person(ref_author)
            if author_json:
                ref_json[id][author_type].append(author_json)
        # Add to json array, and do not verwrite existing rule of a specific bib id (if present)
        if doi not in references_rewrite_json:
            references_rewrite_json[doi] = ref_json
        else:
            for key, value in ref_json.iteritems():
                if key not in references_rewrite_json[doi]:
                    references_rewrite_json[doi][key] = value
                else:
                    # Append dict items
                    for k, v in value.iteritems():
                        references_rewrite_json[doi][key][k] = v

    return references_rewrite_json

def rewrite_elife_body_json(json_content, doi):
    """ rewrite elife body json """

    # Edge case add an id to a section
    if doi == "10.7554/eLife.00013":
        if (json_content and len(json_content) > 0):
            if (json_content[0].get("type") and json_content[0].get("type") == "section"
                and json_content[0].get("title") and json_content[0].get("title") =="Introduction"
                and not json_content[0].get("id")):
                json_content[0]["id"] = "s1"

    # Edge case remove an extra section
    if doi == "10.7554/eLife.04232":
        if (json_content and len(json_content) > 0):
            for outer_block in json_content:
                if outer_block.get("id") and outer_block.get("id") == "s4":
                    for mid_block in outer_block.get("content"):
                        if mid_block.get("id") and mid_block.get("id") == "s4-6":
                            for inner_block in mid_block.get("content"):
                                if inner_block.get("content") and not inner_block.get("title"):
                                    mid_block["content"] = inner_block.get("content")

    # Edge case remove an extra section
    if doi == "10.7554/eLife.05519":
        if (json_content and len(json_content) > 0):
            for outer_block in json_content:
                if outer_block.get("id") and outer_block.get("id") == "s4":
                    for mid_block in outer_block.get("content"):
                        if mid_block.get("content") and not mid_block.get("id"):
                            new_blocks = []
                            for inner_block in mid_block.get("content"):
                                 new_blocks.append(inner_block)
                            outer_block["content"] = new_blocks

    # Edge case remove a section with no content
    if doi == "10.7554/eLife.09977":
        if (json_content and len(json_content) > 0):
            i_index = j_index = None
            for i, outer_block in enumerate(json_content):
                if (outer_block.get("id") and outer_block.get("id") == "s4"
                    and outer_block.get("content")):
                    # We have i
                    i_index = i
                    break
            if i_index is not None:
                for j, inner_block in enumerate(json_content[i_index].get("content")):
                    if (inner_block.get("id") and inner_block.get("id") == "s4-11"
                        and inner_block.get("content") is None):
                        # Now we have i and j for deletion outside of the loop
                        j_index = j
                        break
            # Do the deletion on the original json
            if i_index is not None and j_index is not None:
                del json_content[i_index]["content"][j_index]

    # Edge case wrap sections differently
    if doi == "10.7554/eLife.12844":
        if (json_content and len(json_content) > 0 and json_content[0].get("type")
            and json_content[0]["type"] == "section"):
            new_body = OrderedDict()
            for i, tag_block in enumerate(json_content):
                if i == 0:
                    tag_block["title"] = "Main text"
                    new_body = tag_block
                elif i > 0:
                    new_body["content"].append(tag_block)
            json_content = [new_body]

    return json_content

