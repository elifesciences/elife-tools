import json
import os

from elifetools import parseJATS as parser
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
json_functions.append(("author_contributions", ("con",)))
json_functions += [
"impact_statement",
"is_poa",
"supplementary_material",
]


xml_filenames = []
xml_filenames.append("elife-kitchen-sink.xml")
xml_filenames.append("elife00013.xml")
xml_filenames.append("elife07586.xml")
xml_filenames.append("elife_poa_e06828.xml")
xml_filenames.append("elife02304.xml")
xml_filenames.append("elife02935.xml")
xml_filenames.append("elife00240.xml")
xml_filenames.append("elife04953.xml")
xml_filenames.append("elife00133.xml")
xml_filenames.append("elife04493.xml")
xml_filenames.append("elife04490.xml")
xml_filenames.append("elife-02833-v2.xml")
xml_filenames.append("elife-00666.xml")


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
                print("arguments for function " + function_name + " must be a tuple")


        soup = parser.parse_document(sample_xml(filename))

        if function_arguments:
            result = getattr(parser, function_name)(soup, *function_arguments)
        else:
            result = getattr(parser, function_name)(soup)

        if result is not None:
            print("writing " + json_expected_file(filename, function_name))
            with open(json_expected_file(filename, function_name), "w") as json_file_fp:
                json_file_fp.write(json.dumps(result, indent=4))

