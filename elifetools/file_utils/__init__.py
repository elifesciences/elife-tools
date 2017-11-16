import os


BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def json_expected_folder(filename):
    return os.path.join(BASE_DIR, "tests", "JSON", filename.split(".")[0])


def json_expected_file(filename, function_name):
    if json_expected_folder(filename):
        return os.path.join(json_expected_folder(filename), function_name + ".json")


def sample_xml(filename):
    return os.path.join(BASE_DIR, "sample-xml", filename)


__all__ = [json_expected_file, json_expected_folder, sample_xml]

