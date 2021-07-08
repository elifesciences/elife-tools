# coding=utf-8

import unittest
import os
from ddt import ddt, data, unpack
import copy
import elifetools.parseJATS as parser
import elifetools.json_rewrite as json_rewrite


@ddt
class TestJsonRewrite(unittest.TestCase):
    def setUp(self):
        pass

    @unpack
    @data(
        ("", None, None, None),
        (
            "",
            '<root><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta></root>',
            None,
            None,
        ),
        (
            "not_a_rewrite_function",
            '<root><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="doi">10.7554/eLife.00051</article-id></article-meta></root>',
            None,
            None,
        ),
    )
    def test_rewrite_json(self, rewrite_type, xml_content, json_content, expected):
        soup = None
        if xml_content:
            soup = parser.parse_xml(xml_content)
        self.assertEqual(
            json_rewrite.rewrite_json(rewrite_type, soup, json_content), expected
        )

    @unpack
    @data(
        (None, None, None),
        ("elife", "func", "rewrite_elife_func"),
        ("eLife", "func", "rewrite_elife_func"),
        ("other_journal", "func", "rewrite_other_journal_func"),
    )
    def test_rewrite_function_name(self, journal_id, rewrite_type, expected):
        self.assertEqual(
            json_rewrite.rewrite_function_name(journal_id, rewrite_type), expected
        )

    @unpack
    @data(
        ({"used": [{"id": "dataro17"}]}, "10.7554/eLife.00348"),
        ({"used": [{"id": "dataro3"}]}, "10.7554/eLife.01311"),
        ({"used": [{"id": "dataro6"}]}, "10.7554/eLife.01311"),
        ({"used": [{"id": "dataro7"}]}, "10.7554/eLife.01311"),
        ({"used": [{"id": "dataro8"}]}, "10.7554/eLife.01311"),
        ({"used": [{"id": "dataro1"}]}, "10.7554/eLife.01440"),
        ({"used": [{"id": "dataro1", "date": "2000, 2005"}]}, "10.7554/eLife.01535"),
        ({"used": [{"id": "dataro11"}]}, "10.7554/eLife.02304"),
        ({"used": [{"id": "dataro2"}]}, "10.7554/eLife.03574"),
        ({"used": [{"id": "dataro4"}]}, "10.7554/eLife.03676"),
        ({"used": [{"id": "dataro2"}]}, "10.7554/eLife.03971"),
        (
            {"generated": [{"id": "dataro1", "date": "2014-2015"}]},
            "10.7554/eLife.04660",
        ),
        ({"used": [{"id": "dataro2", "date": "NA"}]}, "10.7554/eLife.06421"),
        ({"used": [{"id": "data-ro1"}]}, "10.7554/eLife.08445"),
        (
            {"used": [{"id": "dataro2", "date": "2008, updated 2014"}]},
            "10.7554/eLife.08916",
        ),
        (
            {"used": [{"id": "dataro3", "date": "2013, updated 2014"}]},
            "10.7554/eLife.08916",
        ),
        ({"generated": [{"id": "dataro2"}]}, "10.7554/eLife.08955"),
        ({"used": [{"id": "dataro1"}]}, "10.7554/eLife.09207"),
        ({"generated": [{"id": "data-ro4"}]}, "10.7554/eLife.10607"),
        ({"used": [{"id": "data-ro1"}]}, "10.7554/eLife.10670"),
        ({"generated": [{"id": "dataro7"}]}, "10.7554/eLife.10856"),
        ({"generated": [{"id": "dataro8"}]}, "10.7554/eLife.10856"),
        ({"generated": [{"id": "dataro9"}]}, "10.7554/eLife.10856"),
        ({"generated": [{"id": "dataro1"}]}, "10.7554/eLife.10877"),
        ({"generated": [{"id": "dataro1"}]}, "10.7554/eLife.10921"),
        ({"used": [{"id": "dataro2"}]}, "10.7554/eLife.10921"),
        ({"used": [{"id": "dataro14"}]}, "10.7554/eLife.11117"),
        ({"used": [{"id": "dataro1"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro2"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro3"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro4"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro5"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro6"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro7"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro8"}]}, "10.7554/eLife.12204"),
        ({"used": [{"id": "dataro1"}]}, "10.7554/eLife.12876"),
        ({"generated": [{"id": "dataro1"}]}, "10.7554/eLife.13195"),
        ({"generated": [{"id": "data-ro1"}]}, "10.7554/eLife.14158"),
        ({"generated": [{"id": "data-ro2"}]}, "10.7554/eLife.14158"),
        ({"used": [{"id": "dataro3"}]}, "10.7554/eLife.14158"),
        ({"generated": [{"id": "dataro2"}]}, "10.7554/eLife.14243"),
        (
            {"generated": [{"id": "dataro1", "date": "current manuscript"}]},
            "10.7554/eLife.16078",
        ),
        ({"used": [{"id": "data-ro4"}]}, "10.7554/eLife.17082"),
        ({"used": [{"id": "data-ro5"}]}, "10.7554/eLife.17082"),
        ({"used": [{"id": "data-ro6"}]}, "10.7554/eLife.17082"),
        (
            {"generated": [{"id": "dataro1", "date": "Release date: "}]},
            "10.7554/eLife.17473",
        ),
    )
    def test_rewrite_elife_datasets_json(self, json_content, doi):
        """simple tests for coverage assert the result is different"""
        original_json_content = copy.deepcopy(json_content)
        self.assertNotEqual(
            json_rewrite.rewrite_elife_datasets_json(json_content, doi),
            original_json_content,
        )

    @unpack
    @data(
        ([{}], "10.7554/eLife.00001", [{}]),
        (
            [{}],
            "10.7554/eLife.00230",
            [
                {
                    "competingInterests": "The authors have declared that no competing interests exist"
                }
            ],
        ),
        (
            [
                {"name": {"index": "Chen, Zhijian J"}},
                {"name": {"index": "Li, Xiao-Dong"}},
            ],
            "10.7554/eLife.00102",
            [
                {
                    "name": {"index": "Chen, Zhijian J"},
                    "competingInterests": "ZJC: Reviewing Editor, <i>eLife</i>",
                },
                {
                    "name": {"index": "Li, Xiao-Dong"},
                    "competingInterests": "No competing interests declared.",
                },
            ],
        ),
        (
            [{"name": {"index": "Patterson, Mark"}}],
            "10.7554/eLife.00270",
            [
                {
                    "name": {"index": "Patterson, Mark"},
                    "competingInterests": "MP: Managing Executive Editor, <i>eLife</i>",
                }
            ],
        ),
        (
            [{}],
            "10.7554/eLife.507424566981410635",
            [
                {
                    "competingInterests": "The authors declare that no competing interests exist."
                }
            ],
        ),
    )
    def test_rewrite_elife_authors_json(self, json_content, doi, expected):
        original_json_content = copy.deepcopy(json_content)
        self.assertEqual(
            json_rewrite.rewrite_elife_authors_json(json_content, doi), expected
        )

    @unpack
    @data(
        ([{}], "10.7554/eLife.23804", [{"role": "Reviewing Editor"}]),
        (
            [{"role": "Reviewing editor"}],
            "10.7554/eLife.00001",
            [{"role": "Reviewing Editor"}],
        ),
        (
            [{"role": "Specialised Role"}],
            "10.7554/eLife.00001",
            [{"role": "Specialised Role"}],
        ),
    )
    def test_rewrite_elife_editors_json(self, json_content, doi, expected):
        """simple tests for coverage assert the result is different"""
        original_json_content = copy.deepcopy(json_content)
        self.assertEqual(
            json_rewrite.rewrite_elife_editors_json(json_content, doi), expected
        )


if __name__ == "__main__":
    unittest.main()
