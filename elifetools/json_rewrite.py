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
    references_rewrite_json["10.7554/eLife.03819"] = {"bib37": {"date": " 2008"}}
    references_rewrite_json["10.7554/eLife.04069"] = {"bib8": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.04247"] = {"bib19a": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.04333"] = {"bib3": {"date": "1859"}}
    references_rewrite_json["10.7554/eLife.04478"] = {"bib49": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.04580"] = {"bib139": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.05042"] = {"bib78": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.05323"] = {"bib102": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.05423"] = {"bib102": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.05503"] = {"bib94": {"date": "2016"}}
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
    references_rewrite_json["10.7554/eLife.09972"] = {"bib61": {"date": "2007", "discriminator": "a"}}
    references_rewrite_json["10.7554/eLife.09977"] = {"bib41": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.10032"] = {"bib45": {"date": "2016"}}
    references_rewrite_json["10.7554/eLife.10042"] = {"bib14": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10070"] = {"bib15": {"date": "2015"}, "bib38": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.10222"] = {"bib30": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.10670"] = {"bib8": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.11305"] = {"bib68": {"date": "2000"}}
    references_rewrite_json["10.7554/eLife.11416"] = {"bib22": {"date": "1997"}}
    references_rewrite_json["10.7554/eLife.12401"] = {"bib25": {"date": "2011"}}
    references_rewrite_json["10.7554/eLife.12366"] = {"bib10": {"date": "2008"}}
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
    references_rewrite_json["10.7554/eLife.16105"] = {"bib2": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.16349"] = {"bib68": {"date": "2005"}}
    references_rewrite_json["10.7554/eLife.16443"] = {"bib58": {"date": "1987"}}
    references_rewrite_json["10.7554/eLife.16764"] = {"bib4": {"date": "2013"}}
    references_rewrite_json["10.7554/eLife.17092"] = {"bib102": {"date": "1980"}}
    references_rewrite_json["10.7554/eLife.18370"] = {"bib1": {"date": "2006"}}
    references_rewrite_json["10.7554/eLife.18425"] = {"bib54": {"date": "2014"}}
    references_rewrite_json["10.7554/eLife.18683"] = {"bib47": {"date": "2015"}}
    references_rewrite_json["10.7554/eLife.21864"] = {"bib2": {"date": "2016-10-24"}}

    return references_rewrite_json

def rewrite_elife_body_json(json_content, doi):
    """ rewrite elife body json """

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

