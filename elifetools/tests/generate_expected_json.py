import os
import json

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser
from file_utils import sample_xml, json_expected_folder, json_expected_file

"""
This is a helper to generate JSON files containing
the output of a list of functions performed on a set of XML files
These files can be used for comparison in test scenarios
"""

"""
json_functions accepts either
- a string as a function name, or
- a tuple of function name and another tuple for function arguments to pass in
"""
json_functions = []
json_functions.append(("journal_issn", ("electronic",)))
json_functions.append(("author_contributions", ("con",)))
json_functions.append(("competing_interests", (["conflict", "COI-statement"],)))
json_functions.append(("full_author_notes", (None,)))
json_functions += ["abstract", "abstracts", "accepted_date_date", "accepted_date_day",
"accepted_date_month", "accepted_date_timestamp", "accepted_date_year",
"ack", "acknowledgements", "article_type", "author_notes", "authors",
"authors_non_byline", "award_groups", "category", "collection_year",
"component_doi", "components", "conflict", "contributors", "copyright_holder",
"copyright_statement", "copyright_year", "correspondence", "digest",
"display_channel", "doi", "elocation_id", "full_abstract", "full_affiliation",
"full_award_group_funding_source", "full_award_groups", "full_correspondence",
"full_digest", "full_keyword_groups", "full_license",
"full_subject_area", "full_title", "funding_statement", "graphics",
"impact_statement", "inline_graphics", "is_poa", "journal_id",
"journal_issn", "journal_title", "keywords", "license", "license_url", "media", 
"pub_date_timestamp", "pub_date_date", "pub_date_day", "pub_date_month",
"pub_date_year", "publisher", "publisher_id",
"received_date_date", "received_date_day", "received_date_month",
"received_date_timestamp", "received_date_year",
"refs", "related_article", "related_object_ids", "research_organism",
"self_uri", "subject_area", "supplementary_material", "title", "title_short",
"title_slug", "volume", "ymd", "full_research_organism", "full_keywords",
"title_prefix", "full_funding_statement"]


xml_filenames = []
xml_filenames.append("elife-09215-v1.xml")
xml_filenames.append("elife-kitchen-sink.xml")
xml_filenames.append("elife00013.xml")
xml_filenames.append("elife00270.xml")
xml_filenames.append("elife07586.xml")
xml_filenames.append("elife_poa_e06828.xml")
xml_filenames.append("elife02304.xml")
xml_filenames.append("elife02935.xml")
xml_filenames.append("elife00051.xml")
xml_filenames.append("elife00190.xml")
xml_filenames.append("elife00240.xml")
xml_filenames.append("elife04953.xml")
xml_filenames.append("elife00133.xml")
xml_filenames.append("elife00007.xml")
xml_filenames.append("elife00005.xml")
xml_filenames.append("elife05031.xml")
xml_filenames.append("elife04493.xml")
xml_filenames.append("elife06726.xml")
xml_filenames.append("elife00380.xml")
xml_filenames.append("elife-14093-v1.xml")
xml_filenames.append("elife04490.xml")
xml_filenames.append("elife05502.xml")
xml_filenames.append("elife00351.xml")
xml_filenames.append("elife-02833-v2.xml")


for filename in xml_filenames:
    if not os.path.exists(json_expected_folder(filename)):
        os.mkdir(json_expected_folder(filename))

    # Output json files for testing expected output
    for function_attrs in json_functions:
        if type(function_attrs) == str:
            function_name = function_attrs
            function_arguments = None
        elif type(function_attrs) == tuple:
            function_name = function_attrs[0]
            if type(function_attrs[1]) == tuple:
                function_arguments = function_attrs[1]
            else:
                print "arguments for function " + function_name + " must be a tuple"


        soup = parser.parse_document(sample_xml(filename))

        if function_arguments:
            result = getattr(parser, function_name)(soup, *function_arguments)
        else:
            result = getattr(parser, function_name)(soup)

        if result is not None:
            print "writing " + json_expected_file(filename, function_name)
            with open(json_expected_file(filename, function_name), "wb") as json_file_fp:
                json_file_fp.write(json.dumps(result, indent=4))

