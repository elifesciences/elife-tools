import os
from elifetools.utils import unicode_value

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def json_expected_folder(filename):
    return os.path.join(BASE_DIR, "tests", "JSON", filename.split(".")[0])


def json_expected_file(filename, function_name):
    if json_expected_folder(filename):
        return os.path.join(json_expected_folder(filename), function_name + ".json")


def sample_xml(filename):
    return os.path.join(BASE_DIR, "sample-xml", filename)

def fixture_folder(folder_name):
    return os.path.join(BASE_DIR, "tests", "fixtures", folder_name)

def read_fixture(folder_name, filename):
    full_filename = os.path.join(fixture_folder(folder_name), filename)
    with open(full_filename) as file_fp:
        return unicode_value(file_fp.read())

__all__ = [json_expected_file, json_expected_folder, sample_xml,
           fixture_folder, read_fixture]

