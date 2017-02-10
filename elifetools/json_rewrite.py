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
    references_rewrite_json["10.7554/eLife.09520"] = {
        "bib35": {"conference": {"name": ["WHO Expert Committee on Malaria"]},
        "articleTitle": "WHO Expert Committee on Malaria [meeting held in Geneva from 19 to 30 October 1970]: fifteenth report",
        "publisher": {"name": ["World Health Organization"], "address": {"formatted": ["Geneva"], "components": {"locality": ["Geneva"]}}}}}
    references_rewrite_json["10.7554/eLife.09579"] = {
        "bib19": {"date": "2007"},
        "bib49": {"date": "2002"}}
    references_rewrite_json["10.7554/eLife.09600"] = {"bib13": {"date": "2009"}}
    references_rewrite_json["10.7554/eLife.09672"] = {
        "bib25": {"conference": {"name": ["Seventeenth Meeting of the RBM Partnership Monitoring and Evaluation Reference Group (MERG)"]}}}
    references_rewrite_json["10.7554/eLife.09771"] = {"bib22": {"date": "2012"}}
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
    references_rewrite_json["10.7554/eLife.19571"] = {"bib56": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.20352"] = {"bib53": {"country": "United States"}}
    references_rewrite_json["10.7554/eLife.21864"] = {"bib2": {"date": "2016-10-24"}}
    references_rewrite_json["10.7554/eLife.20522"] = {
        "bib42": {"date": "2016"},
        "bib110": {"date": "1996"}}

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

    # Edge case remove unwanted sections
    if doi == "10.7554/eLife.04871":
        if (json_content and len(json_content) > 0):
            for i, outer_block in enumerate(json_content):
                if (outer_block.get("id") and outer_block.get("id") in ["s7", "s8"]
                    and not outer_block.get("title")):
                    if outer_block.get("content"):
                        json_content[i] = outer_block.get("content")[0]

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

    # Edge case add a title to a section
    if doi == "10.7554/eLife.07157":
        if (json_content and len(json_content) > 0):
            if (json_content[0].get("type") and json_content[0].get("type") == "section"
                and json_content[0].get("id") and json_content[0].get("id") == "s1"):
                json_content[0]["title"] = "Main text"

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


def rewrite_elife_funding_awards(json_content, doi):
    """ rewrite elife funding awards """

    # remove a funding award
    if doi == "10.7554/eLife.00801":
        for i, award in enumerate(json_content):
            if "id" in award and award["id"] == "par-2":
                del json_content[i]

    # add funding award recipient
    if doi == "10.7554/eLife.04250":
        recipients_for_04250 = [{"type": "person", "name": {"preferred": "Eric Jonas", "index": "Jonas, Eric"}}]
        for i, award in enumerate(json_content):
            if "id" in award and award["id"] in ["par-2", "par-3", "par-4"]:
                if "recipients" not in award:
                    json_content[i]["recipients"] = recipients_for_04250

    # add funding award recipient
    if doi == "10.7554/eLife.06412":
        recipients_for_06412 = [{"type": "person", "name": {"preferred": "Adam J Granger", "index": "Granger, Adam J"}}]
        for i, award in enumerate(json_content):
            if "id" in award and award["id"] == "par-1":
                if "recipients" not in award:
                    json_content[i]["recipients"] = recipients_for_06412

    return json_content

def rewrite_elife_authors_json(json_content, doi):
    """ this does the work of rewriting elife authors json """

    # Edge case fix an affiliation name
    if doi == "10.7554/eLife.06956":
        for i, ref in enumerate(json_content):
            if ref.get("orcid") and ref.get("orcid") == "0000-0001-6798-0064":
                json_content[i]["affiliations"][0]["name"] = ["Cambridge"]

    # Edge case fix an ORCID
    if doi == "10.7554/eLife.09376":
        for i, ref in enumerate(json_content):
            if ref.get("orcid") and ref.get("orcid") == "000-0001-7224-925X":
                json_content[i]["orcid"] = "0000-0001-7224-925X"

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
        for (match_doi, used_or_generated, id, dataset_date) in elife_dataset_dates:
            if doi == match_doi:
                if json_content.get(used_or_generated):
                    for dataset in json_content[used_or_generated]:
                        if dataset.get("id") and dataset["id"] == id:
                            if not dataset.get("date"):
                                dataset["date"] = dataset_date

    # Continue with individual article JSON rewriting
    if doi == "10.7554/eLife.01311":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] in ["dataro3", "dataro4", "dataro5"]:
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
                        dataset["authors"] = [{"type": "group", "name": "Baylor College of Medicine (BCM)"}]
                if dataset.get("id") and dataset["id"] in ["dataro8", "dataro9"]:
                    if not dataset.get("date"):
                        dataset["date"] = u"2012"
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "University of California, Berkeley"}]

    if doi == "10.7554/eLife.01440":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "EnsemblMetazoa"}]

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
                        dataset["title"] = u"T.gondii LDH1 ternary complex with APAD+ and oxalate"

    if doi == "10.7554/eLife.03574":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("date"):
                        dataset["date"] = u"2006"
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Riley,M."}, {"type": "group", "name": "Abe,T."}, {"type": "group", "name": "Arnaud,M.B."}, {"type": "group", "name": "Berlyn,M.K."}, {"type": "group", "name": "Blattner,F.R."}, {"type": "group", "name": "Chaudhuri,R.R."}, {"type": "group", "name": "Glasner,J.D."}, {"type": "group", "name": "Horiuchi,T."}, {"type": "group", "name": "Keseler,I.M."}, {"type": "group", "name": "Kosuge,T."}, {"type": "group", "name": "Mori,H."}, {"type": "group", "name": "Perna,N.T."}, {"type": "group", "name": "Plunkett,G. III"}, {"type": "group", "name": "Rudd,K.E."}, {"type": "group", "name": "Serres,M.H."}, {"type": "group", "name": "Thomas,G.H."}, {"type": "group", "name": "Thomson,N.R."}, {"type": "group", "name": "Wishart,D."}, {"type": "group", "name": "Wanner,B.L."}]

    if doi == "10.7554/eLife.03676":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro4":
                    if not dataset.get("date"):
                        dataset["date"] = u"2013"
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Human Gene Sequencing Center"}]

    if doi == "10.7554/eLife.03971":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Vanderperre B."}]

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
                    if dataset.get("date") and dataset.get("date") == "2008, updated 2014":
                        dataset["date"] = u"2008"
                if dataset.get("id") and dataset["id"] == "dataro3":
                    if dataset.get("date") and dataset.get("date") == "2013, updated 2014":
                        dataset["date"] = u"2013"

    if doi == "10.7554/eLife.08955":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Kurdistani S"}, {"type": "group", "name": "Marrban C"}, {"type": "group", "name": "Su T"}]

    if doi == "10.7554/eLife.09207":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Prostate Cancer Genome Sequencing Project"}]

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
            datasets_authors_for_10856 = [{"type": "group", "name": "Dagdas YF"}, {"type": "group", "name": "Belhaj K"}, {"type": "group", "name": "Maqbool A"}, {"type": "group", "name": "Chaparro-Garcia A"}, {"type": "group", "name": "Pandey P"}, {"type": "group", "name": "Petre B"}, {"type": "group", "name": "Tabassum N"}, {"type": "group", "name": "Cruz-Mireles N"}, {"type": "group", "name": "Hughes RK"}, {"type": "group", "name": "Sklenar J"}, {"type": "group", "name": "Win J"}, {"type": "group", "name": "Menke F"}, {"type": "group", "name": "Findlay K"}, {"type": "group", "name": "Banfield MJ"}, {"type": "group", "name": "Kamoun S"}, {"type": "group", "name": "Bozkurt TO"}]
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro7":
                    if not dataset.get("date"):
                        dataset["date"] = u"2016"
                    if not dataset.get("title"):
                        dataset["title"] = u"An effector of the Irish potato famine pathogen antagonizes a host autophagy cargo receptor"
                    if not dataset.get("authors"):
                        dataset["authors"] = datasets_authors_for_10856
                    if dataset.get("uri") and dataset["uri"] == "http://www.ncbi.nlm.nih.":
                         dataset["uri"] = "https://www.ncbi.nlm.nih.gov/nuccore/976151098/"
                if dataset.get("id") and dataset["id"] == "dataro8":
                    if not dataset.get("date"):
                        dataset["date"] = u"2015"
                    if not dataset.get("title"):
                        dataset["title"] = u"An effector of the Irish potato famine pathogen antagonizes a host autophagy cargo receptor"
                    if not dataset.get("authors"):
                        dataset["authors"] = datasets_authors_for_10856
                    if dataset.get("uri") and dataset["uri"] == "http://www.ncbi.nlm.nih.":
                         dataset["uri"] = "https://www.ncbi.nlm.nih.gov/nuccore/976151096/"
                if dataset.get("id") and dataset["id"] == "dataro9":
                    if not dataset.get("authors"):
                        dataset["authors"] = datasets_authors_for_10856

    if doi == "10.7554/eLife.10877":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("title"):
                        dataset["title"] = u"Oct4 ChIP-Seq at G1 and G2/M phase of cell cycle in mouse embryonic stem cells"

    if doi == "10.7554/eLife.10921":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Floor SN"}, {"type": "group", "name": "Doudna JA"}]
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Sidrauski C"}, {"type": "group", "name": "McGeachy A"}, {"type": "group", "name": "Ingolia N"}, {"type": "group", "name": "Walter P"}]

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
                        dataset["authors"] = [{"type": "group", "name": "Rhodes DR"}, {"type": "group", "name": "Kalyana-Sundaram S"}, {"type": "group", "name": "Mahavisno V"}, {"type": "group", "name": "Varambally R"}, {"type": "group", "name": "Yu J"}, {"type": "group", "name": "Briggs BB"}, {"type": "group", "name": "Barrette TR"}, {"type": "group", "name": "Anstet MJ"}, {"type": "group", "name": "Kincead-Beal C"}, {"type": "group", "name": "Kulkarni P"}, {"type": "group", "name": "Varambally S"}, {"type": "group", "name": "Ghosh D"}, {"type": "group", "name": "Chinnaiyan AM."}]
                if dataset.get("id") and dataset["id"] == "dataro2":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Gaspar C"}, {"type": "group", "name": "Cardoso J"}, {"type": "group", "name": "Franken P"}, {"type": "group", "name": "Molenaar L"}, {"type": "group", "name": "Morreau H"}, {"type": "group", "name": "Möslein G"}, {"type": "group", "name": "Sampson J"}, {"type": "group", "name": "Boer JM"}, {"type": "group", "name": "de Menezes RX"}, {"type": "group", "name": "Fodde R."}]
                if dataset.get("id") and dataset["id"] == "dataro3":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Graudens E"}, {"type": "group", "name": "Boulanger V"}, {"type": "group", "name": "Mollard C"}, {"type": "group", "name": "Mariage-Samson R"}, {"type": "group", "name": "Barlet X"}, {"type": "group", "name": "Grémy G"}, {"type": "group", "name": "Couillault C"}, {"type": "group", "name": "Lajémi M"}, {"type": "group", "name": "Piatier-Tonneau D"}, {"type": "group", "name": "Zaborski P"}, {"type": "group", "name": "Eveno E"}, {"type": "group", "name": "Auffray C"}, {"type": "group", "name": "Imbeaud S."}]
                if dataset.get("id") and dataset["id"] == "dataro4":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Hong Y"}, {"type": "group", "name": "Downey T"}, {"type": "group", "name": "Eu KW"}, {"type": "group", "name": "Koh PK"},{"type": "group", "name": "Cheah PY"}]
                if dataset.get("id") and dataset["id"] == "dataro5":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Kaiser S"}, {"type": "group", "name": "Park YK"}, {"type": "group", "name": "Franklin JL"}, {"type": "group", "name": "Halberg RB"}, {"type": "group", "name": "Yu M"}, {"type": "group", "name": "Jessen WJ"}, {"type": "group", "name": "Freudenberg J"}, {"type": "group", "name": "Chen X"}, {"type": "group", "name": "Haigis K"}, {"type": "group", "name": "Jegga AG"}, {"type": "group", "name": "Kong S"}, {"type": "group", "name": "Sakthivel B"}, {"type": "group", "name": "Xu H"}, {"type": "group", "name": "Reichling T"}, {"type": "group", "name": "Azhar M"}, {"type": "group", "name": "Boivin GP"}, {"type": "group", "name": "Roberts RB"}, {"type": "group", "name": "Bissahoyo AC"}, {"type": "group", "name": "Gonzales F"}, {"type": "group", "name": "Bloom GC"}, {"type": "group", "name": "Eschrich S"}, {"type": "group", "name": "Carter SL"}, {"type": "group", "name": "Aronow JE"}, {"type": "group", "name": "Kleimeyer J"}, {"type": "group", "name": "Kleimeyer M"}, {"type": "group", "name": "Ramaswamy V"}, {"type": "group", "name": "Settle SH"}, {"type": "group", "name": "Boone B"}, {"type": "group", "name": "Levy S"}, {"type": "group", "name": "Graff JM"}, {"type": "group", "name": "Doetschman T"}, {"type": "group", "name": "Groden J"}, {"type": "group", "name": "Dove WF"}, {"type": "group", "name": "Threadgill DW"}, {"type": "group", "name": "Yeatman TJ"}, {"type": "group", "name": "Coffey RJ Jr"}, {"type": "group", "name": "Aronow BJ."}]
                if dataset.get("id") and dataset["id"] == "dataro6":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Muzny DM et al"}]
                if dataset.get("id") and dataset["id"] == "dataro7":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Skrzypczak M"}, {"type": "group", "name": "Goryca K"}, {"type": "group", "name": "Rubel T"}, {"type": "group", "name": "Paziewska A"}, {"type": "group", "name": "Mikula M"}, {"type": "group", "name": "Jarosz D"}, {"type": "group", "name": "Pachlewski J"}, {"type": "group", "name": "Oledzki J"}, {"type": "group", "name": "Ostrowski J."}]
                if dataset.get("id") and dataset["id"] == "dataro8":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Cancer Genome Atlas Network"}]

    if doi == "10.7554/eLife.12876":
        if json_content.get("used"):
            for dataset in json_content["used"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Department of Human Genetics, University of Utah"}]

    if doi == "10.7554/eLife.13195":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if not dataset.get("authors"):
                        dataset["authors"] = [{"type": "group", "name": "Microbial Ecology Group, Colorado State University"}]

    if doi == "10.7554/eLife.14158":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "data-ro1":
                    if not dataset.get("title"):
                        dataset["title"] = u"Bacterial initiation protein"
                if dataset.get("id") and dataset["id"] == "data-ro2":
                    if not dataset.get("title"):
                        dataset["title"] = u"Bacterial initiation protein in complex with Phage inhibitor protein"
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
                        dataset["authors"] = [{"type": "group", "name": "Tramantano M"}, {"type": "group", "name": "Sun L"}, {"type": "group", "name": "Au C"}, {"type": "group", "name": "Labuz D"}, {"type": "group", "name": "Liu Z"}, {"type": "group", "name": "Chou M"}, {"type": "group", "name": "Shen C"}, {"type": "group", "name": "Luk E"}]


    if doi == "10.7554/eLife.16078":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if dataset.get("date") and dataset.get("date") == "current manuscript":
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
                        dataset["authors"] = [{"type": "group", "name": "The Cancer Genome Atlas (TCGA)"}]

    if doi == "10.7554/eLife.17473":
        if json_content.get("generated"):
            for dataset in json_content["generated"]:
                if dataset.get("id") and dataset["id"] == "dataro1":
                    if dataset.get("date") and dataset.get("date").startswith("Release date"):
                        dataset["date"] = u"2016"

    return json_content

def rewrite_elife_decision_letter_json(json_content, doi):
    """ this does the work of rewriting elife decision letter json """

    # Add description
    if doi == "10.7554/eLife.10856":
        if json_content.get("description") is None:
            json_content["description"] = [{"type": "paragraph", "text": "In the interests of transparency, eLife includes the editorial decision letter and accompanying author responses. A lightly edited version of the letter sent to the authors after peer review is shown, indicating the most substantive concerns; minor comments are not usually included."}]

    return json_content
