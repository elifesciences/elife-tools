import parseJATS as parser

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

    references_rewrite_json["10.7554/eLife.00051"] = {"bib25":  {"date": "2012"}}

    return references_rewrite_json
