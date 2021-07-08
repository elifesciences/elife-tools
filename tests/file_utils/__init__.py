import os
import io
import importlib

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def json_expected_folder(filename):
    return os.path.join(BASE_DIR, "JSON", filename.split(".")[0])


def json_expected_file(filename, function_name):
    if json_expected_folder(filename):
        return os.path.join(json_expected_folder(filename), function_name + ".json")
    return None


def sample_xml(filename):
    return os.path.join(BASE_DIR, "sample-xml", filename)


def fixture_folder(folder_name):
    return os.path.join(BASE_DIR, "fixtures", folder_name)


def fixture_module_name(folder_name, filename):
    return ".".join(
        ["tests", "fixtures", folder_name, filename.rstrip(".py")]
    )


def fixture_file(folder_name, filename):
    return os.path.join(fixture_folder(folder_name), filename)


def read_fixture(folder_name, filename):
    full_filename = fixture_file(folder_name, filename)
    if full_filename.endswith(".py"):
        # import the fixture and return the value of expected
        module_name = fixture_module_name(folder_name, filename)
        mod = importlib.import_module(module_name)
        # assert expected exists before continuing
        assert hasattr(
            mod, "expected"
        ), "expected property not found in module {module_name}".format(
            module_name=module_name
        )
        return mod.expected
    else:
        with io.open(full_filename, mode="r", encoding="utf-8") as file_fp:
            return file_fp.read()


__all__ = [
    "json_expected_file",
    "json_expected_folder",
    "sample_xml",
    "fixture_folder",
    "read_fixture",
]
