# coding=utf-8

import unittest
import os
import json
from ddt import ddt, data, unpack
from bs4 import BeautifulSoup

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser
import rawJATS as raw_parser
from utils import date_struct, node_contents_str
from collections import OrderedDict

from file_utils import sample_xml, json_expected_folder, json_expected_file




@ddt
class TestParseJats(unittest.TestCase):

    def setUp(self):
        pass

    def soup(self, filename):
        # return soup
        return parser.parse_document(sample_xml(filename))

    def json_expected(self, filename, function_name):
        json_expected = None
        json_file = json_expected_file(filename, function_name)
        try:
            with open(json_file, 'rb') as json_file_fp:
                json_expected = json.loads(json_file_fp.read())
        except IOError:
            # file may not exist or the value is None for this article
            pass
        return json_expected

    @data("elife-kitchen-sink.xml")
    def test_parse_document(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertTrue(isinstance(soup, BeautifulSoup))

    """
    Quick test cases during development checking syntax errors and coverage
    """

    @unpack
    @data(
        ("elife04493.xml", "Neuron hemilineages provide the functional ground plan for the <i>Drosophila</i> ventral nervous system"))
    def test_full_title_json(self, filename, expected):
        full_title_json = parser.full_title_json(self.soup(filename))
        self.assertEqual(expected, full_title_json)


    @unpack
    @data(
        ("elife04490.xml", "Both the frequency of sesquiterpene-emitting individuals and the defense capacity of individual plants determine the consequences of sesquiterpene volatile emission for individuals and their neighbors in populations of the wild tobacco <i>Nicotiana attenuata</i>."),
        ("elife_poa_e06828.xml", ""))
    def test_impact_statement_json(self, filename, expected):
        impact_statement_json = parser.impact_statement_json(self.soup(filename))
        self.assertEqual(expected, impact_statement_json)



    @unpack
    @data(
        ("elife-kitchen-sink.xml", list),
        ("elife_poa_e06828.xml", None))
    def test_acknowledgements_json_by_file(self, filename, expected):
        acknowledgements_json = parser.acknowledgements_json(self.soup(filename))
        if expected is None:
            self.assertEqual(expected, acknowledgements_json)
        else:
            self.assertEqual(expected, type(acknowledgements_json))

    @unpack
    @data(
        ('<root></root>',
         None
         ),

        ('<root><ack></ack></root>',
         None
         ),

        ('<root><ack><title>Acknowledgements</title><p>Paragraph</p></ack></root>',
         [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph')])]
         ),

        ('<root><ack><title>Acknowledgements</title><p>Paragraph</p><p><italic>italic</italic></p></ack></root>',
         [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph')]), OrderedDict([('type', 'paragraph'), ('text', u'<i>italic</i>')])]
         ),
    )
    def test_acknowledgements_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.acknowledgements_json(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, OrderedDict()),
        ("elife_poa_e06828.xml", OrderedDict(), None))
    def test_decision_letter(self, filename, expected, not_expected):
        sub_article_content = parser.decision_letter(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, sub_article_content)
        if not_expected is not None:
            self.assertNotEqual(not_expected, sub_article_content)

    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, OrderedDict()),
        ("elife_poa_e06828.xml", OrderedDict(), None))
    def test_author_response(self, filename, expected, not_expected):
        sub_article_content = parser.author_response(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, sub_article_content)
        if not_expected is not None:
            self.assertNotEqual(not_expected, sub_article_content)


    @unpack
    @data(
        ("elife-kitchen-sink.xml", None, []),
        ("elife_poa_e06828.xml", [], None))
    def test_body(self, filename, expected, not_expected):
        body = parser.body(self.soup(filename))
        if expected is not None:
            self.assertEqual(expected, body)
        if not_expected is not None:
            self.assertNotEqual(not_expected, body)


    @data("elife-kitchen-sink.xml", "elife-02833-v2.xml", "elife00351.xml")
    def test_authors_json(self, filename):
        """note elife00351.xml has email inside an inline aff tag, very irregular"""
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.authors_json(soup), None)


    @unpack
    @data(
        (None, None),
        (["Randy Schekman"], "Randy Schekman"),
        (["Randy Schekman", "Mark Patterson"], "Randy Schekman, Mark Patterson"),
        (["Randy Schekman", "Mark Patterson", "eLife"], "Randy Schekman et al"),
        )
    def test_format_author_line(self, author_names, expected):
        self.assertEqual(parser.format_author_line(author_names), expected)


    @unpack
    @data(
        (None, []),
        ([{"name": {"preferred": "Randy Schekman"}}, {"name": {"preferred": "Mark Patterson"}}, {"name": "eLife"}],
            ["Randy Schekman", "Mark Patterson", "eLife"])
        )
    def test_extract_author_line_names(self, authors_json, expected):
        self.assertEqual(parser.extract_author_line_names(authors_json), expected)


    @unpack
    @data(
        ("elife_poa_e06828.xml", "Michael S Fleming et al"),
        ("elife00351.xml", "Richard Smith"),
        )
    def test_author_line(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(parser.author_line(soup), expected)

    @unpack
    @data(
        (None,
         OrderedDict(),
         OrderedDict()
         ),

        ([{"surname": "One", "given-names": "Person", "group-type": "sponsor"}, {"etal": True, "group-type": "sponsor"}],
         OrderedDict([('type', u'clinical-trial')]),
         OrderedDict([('type', u'clinical-trial'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', 'Person One'), ('index', 'One, Person')]))])]), ('authorsEtAl', True), ('authorsType', 'sponsors')])
         ),

        ([{"surname": "One", "given-names": "Person", "group-type": "inventor"}, {"etal": True, "group-type": "inventor"}],
         OrderedDict([('type', u'patent')]),
         OrderedDict([('type', u'patent'), ('inventors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', 'Person One'), ('index', 'One, Person')]))])]), ('inventorsEtAl', True)])
         ),

        ([{"surname": "One", "given-names": "Person", "group-type": "author"}],
         OrderedDict([('type', u'thesis')]),
         OrderedDict([('type', u'thesis'), ('author', OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', 'Person One'), ('index', 'One, Person')]))]))])
         ),

        )
    def test_references_json_authors(self, ref_authors, ref_content, expected):
        references_json = parser.references_json_authors(ref_authors, ref_content)
        self.assertEqual(expected, references_json)

    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00051.xml", "elife-10421-v1.xml")
    def test_references_json(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.references_json(soup), None)

    @unpack
    @data(
        # Web reference with no title, use the uri from 01892
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib1"><element-citation publication-type="web"><person-group person-group-type="author"><collab>The World Health Organization</collab></person-group><year>2014</year><ext-link ext-link-type="uri" xlink:href="http://www.who.int/topics/dengue/en/">http://www.who.int/topics/dengue/en/</ext-link></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'web'), ('id', u'bib1'), ('date', u'2014'), ('authors', [OrderedDict([('type', 'group'), ('name', 'The World Health Organization')])]), ('title', u'http://www.who.int/topics/dengue/en/'), ('uri', u'http://www.who.int/topics/dengue/en/')])]
         ),

        # Thesis title from 00626
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib36"><element-citation publication-type="thesis"><person-group person-group-type="author"><name><surname>Schneider</surname><given-names>P</given-names></name></person-group><year>2006</year><comment>PhD Thesis</comment><article-title>Submicroscopic<italic>Plasmodium falciparum</italic>gametocytaemia and the contribution to malaria transmission</article-title><publisher-name>Radboud University Nijmegen Medical Centre</publisher-name><publisher-loc>Nijmegen, The Netherlands</publisher-loc></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'thesis'), ('id', u'bib36'), ('date', u'2006'), ('author', OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Schneider'), ('index', u'Schneider, P')]))])), ('title', u'Submicroscopic<i>Plasmodium falciparum</i>gametocytaemia and the contribution to malaria transmission'), ('publisher', OrderedDict([('name', [u'Radboud University Nijmegen Medical Centre']), ('address', OrderedDict([('formatted', [u'Nijmegen, The Netherlands']), ('components', OrderedDict([('locality', [u'Nijmegen, The Netherlands'])]))]))]))])]
         ),

        # fpage value with usual characters from 00170
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib14"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Feng</surname><given-names>J</given-names></name><name><surname>Liu</surname><given-names>T</given-names></name><name><surname>Zhang</surname><given-names>Y</given-names></name></person-group><year>2011</year><article-title>Using MACS to identify peaks from ChIP-Seq data</article-title><source>Curr Protoc Bioinformatics</source><volume>Chapter 2</volume><fpage>Unit 2.14</fpage></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib14'), ('date', u'2011'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Feng'), ('index', u'Feng, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'T Liu'), ('index', u'Liu, T')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Y Zhang'), ('index', u'Zhang, Y')]))])]), ('articleTitle', u'Using MACS to identify peaks from ChIP-Seq data'), ('journal', OrderedDict([('name', [u'Curr Protoc Bioinformatics'])])), ('volume', u'Chapter 2'), ('pages', u'Unit 2.14')])]
         ),

        # fpage contains dots, 00569
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib96"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Zerbino</surname><given-names>DR</given-names></name></person-group><year>2010</year><article-title>Using the Velvet de novo assembler for short-read sequencing technologies</article-title><source>Curr Protoc Bioinformatics</source><volume>11</volume><fpage>11.5.1</fpage><lpage>11.5.12</lpage><pub-id pub-id-type="doi">10.1002/0471250953.bi1105s31</pub-id></element-citation></ref></ref-list></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib96'), ('date', u'2010'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'DR Zerbino'), ('index', u'Zerbino, DR')]))])]), ('articleTitle', u'Using the Velvet de novo assembler for short-read sequencing technologies'), ('journal', OrderedDict([('name', [u'Curr Protoc Bioinformatics'])])), ('volume', u'11'), ('pages', OrderedDict([('first', u'11.5.1'), ('last', u'11.5.12'), ('range', u'11.5.1\u201311.5.12')])), ('doi', u'10.1002/0471250953.bi1105s31')])]
         ),

        # pages value of in press, 00109
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib32"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Kyoung</surname><given-names>M</given-names></name><name><surname>Zhang</surname><given-names>Y</given-names></name><name><surname>Diao</surname><given-names>J</given-names></name><name><surname>Chu</surname><given-names>S</given-names></name><name><surname>Brunger</surname><given-names>AT</given-names></name></person-group><year>2012</year><article-title>Studying calcium triggered vesicle fusion in a single vesicle content/lipid mixing system</article-title><source>Nature Protocols</source><volume>7</volume><ext-link ext-link-type="uri" xlink:href="http://dx.doi.org/10.1038/nprot.2012.134">10.1038/nprot.2012.134</ext-link><comment>, in press</comment></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib32'), ('date', u'2012'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Kyoung'), ('index', u'Kyoung, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Y Zhang'), ('index', u'Zhang, Y')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Diao'), ('index', u'Diao, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'S Chu'), ('index', u'Chu, S')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AT Brunger'), ('index', u'Brunger, AT')]))])]), ('articleTitle', u'Studying calcium triggered vesicle fusion in a single vesicle content/lipid mixing system'), ('journal', OrderedDict([('name', [u'Nature Protocols'])])), ('volume', u'7'), ('pages', 'in press'), ('uri', u'http://dx.doi.org/10.1038/nprot.2012.134')])]
         ),

        # year value of in press, 02535
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib12"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Culumber</surname><given-names>ZW</given-names></name><name><surname>Ochoa</surname><given-names>OM</given-names></name><name><surname>Rosenthal</surname><given-names>GG</given-names></name></person-group><year>in press</year><article-title>Assortative mating and the maintenance of population structure in a natural hybrid zone</article-title><source>American Naturalist</source></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib12'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'ZW Culumber'), ('index', u'Culumber, ZW')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'OM Ochoa'), ('index', u'Ochoa, OM')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'GG Rosenthal'), ('index', u'Rosenthal, GG')]))])]), ('articleTitle', u'Assortative mating and the maintenance of population structure in a natural hybrid zone'), ('journal', OrderedDict([('name', [u'American Naturalist'])])), ('pages', 'in press')])]
         ),

        # conference, 03532 v3
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib21"><element-citation publication-type="confproc"><person-group person-group-type="author"><name><surname>Haiyan</surname><given-names>L</given-names></name><name><surname>Jihua</surname><given-names>W</given-names></name></person-group><year iso-8601-date="2009">2009</year><article-title>Network properties of protein structures at three different length scales</article-title><conf-name>Proceedings of the 2009 Second Pacific-Asia Conference on Web Mining and Web-Based Application, IEEE Computer Society</conf-name></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', 'conference-proceeding'), ('id', u'bib21'), ('date', u'2009'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'L Haiyan'), ('index', u'Haiyan, L')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'W Jihua'), ('index', u'Jihua, W')]))])]), ('articleTitle', u'Network properties of protein structures at three different length scales'), ('conference', OrderedDict([('name', [u'Proceedings of the 2009 Second Pacific-Asia Conference on Web Mining and Web-Based Application, IEEE Computer Society'])]))])]
         ),

        # web with doi but no uri, 04775 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib45"><element-citation publication-type="web"><person-group person-group-type="author"><name><surname>Mikheyev</surname><given-names>AS</given-names></name><name><surname>Linksvayer</surname><given-names>TA</given-names></name></person-group><year>2014</year><article-title>Data from: genes associated with ant social behavior show distinct transcriptional and evolutionary patterns</article-title><source>Dryad Digital Repository.</source><pub-id pub-id-type="doi">10.5061/dryad.cv0q3</pub-id></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'web'), ('id', u'bib45'), ('date', u'2014'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AS Mikheyev'), ('index', u'Mikheyev, AS')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TA Linksvayer'), ('index', u'Linksvayer, TA')]))])]), ('title', u'Data from: genes associated with ant social behavior show distinct transcriptional and evolutionary patterns'), ('website', u'Dryad Digital Repository.'), ('uri', u'https://doi.org/10.5061/dryad.cv0q3')])]
         ),

        # Clinical trial example, from new kitchen sink 00666
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib41"><element-citation publication-type="clinicaltrial"><person-group person-group-type="sponsor"><collab>Scripps Translational Science Institute</collab></person-group><year iso-8601-date="2006">2015</year><article-title>Scripps Wired for Health Study</article-title><ext-link ext-link-type="uri" xlink:href="https://clinicaltrials.gov/ct2/show/NCT01975428">NCT01975428</ext-link></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', 'clinical-trial'), ('id', u'bib41'), ('date', u'2015'), ('authors', [OrderedDict([('type', 'group'), ('name', 'Scripps Translational Science Institute')])]), ('authorsType', 'sponsors'), ('title', u'Scripps Wired for Health Study'), ('uri', u'https://clinicaltrials.gov/ct2/show/NCT01975428')])]
         ),

        # Journal reference with no article-title, 05462 v3
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib20"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Elzinga</surname><given-names>SDJ</given-names></name><name><surname>Bednarz</surname><given-names>AL</given-names></name><name><surname>van Oosterum</surname><given-names>K</given-names></name><name><surname>Dekker</surname><given-names>PJT</given-names></name><name><surname>Grivell</surname><given-names>L</given-names></name></person-group><year iso-8601-date="1993">1993</year><source>Nucleic Acids Research</source><volume>21</volume><fpage>5328</fpage><lpage>5331</lpage><pub-id pub-id-type="doi">10.1093/nar/21.23.5328</pub-id></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib20'), ('date', u'1993'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'SDJ Elzinga'), ('index', u'Elzinga, SDJ')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AL Bednarz'), ('index', u'Bednarz, AL')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'K van Oosterum'), ('index', u'van Oosterum, K')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'PJT Dekker'), ('index', u'Dekker, PJT')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'L Grivell'), ('index', u'Grivell, L')]))])]), ('title', u'Nucleic Acids Research'), ('details', u'5328\u20135331, Nucleic Acids Research, 21, 10.1093/nar/21.23.5328')])]
         ),

        # book reference, gets converted to book-chapter, and has no editors, 16412 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib35"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Walsh</surname><given-names>PD</given-names></name><name><surname>Bermejo</surname><given-names>M</given-names></name><name><surname>Rodriguez-Teijeiro</surname><given-names>JD</given-names></name></person-group><year iso-8601-date="2009">2009</year><chapter-title>Disease avoidance and the evolution of primate social connectivity</chapter-title><source>Primate Parasite Ecology: The Dynamics and Study of Host-Parasite Relationships</source><fpage>183</fpage><lpage>197</lpage></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib35'), ('date', u'2009'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'PD Walsh'), ('index', u'Walsh, PD')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Bermejo'), ('index', u'Bermejo, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'JD Rodriguez-Teijeiro'), ('index', u'Rodriguez-Teijeiro, JD')]))])]), ('title', u'Primate Parasite Ecology: The Dynamics and Study of Host-Parasite Relationships'), ('details', u'183\u2013197, Disease avoidance and the evolution of primate social connectivity, Primate Parasite Ecology: The Dynamics and Study of Host-Parasite Relationships')])]
         ),

        # journal reference with no article title and no lpage, 11282 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib63"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Palmer</surname><given-names>D</given-names></name><name><surname>Frater</surname><given-names>J</given-names></name><name><surname>Phillips</surname><given-names>R</given-names></name><name><surname>McLean</surname><given-names>AR</given-names></name><name><surname>McVean</surname><given-names>G</given-names></name></person-group><year iso-8601-date="2013">2013</year><source>Proceedings of the Royal Society of London B</source><volume>280</volume><fpage>20130696</fpage></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib63'), ('date', u'2013'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'D Palmer'), ('index', u'Palmer, D')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Frater'), ('index', u'Frater, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Phillips'), ('index', u'Phillips, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AR McLean'), ('index', u'McLean, AR')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'G McVean'), ('index', u'McVean, G')]))])]), ('title', u'Proceedings of the Royal Society of London B'), ('details', u'20130696, Proceedings of the Royal Society of London B, 280')])]
         ),

        # reference with no title uses detail as the titel, 00311 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib9"><element-citation publication-type="other"><person-group person-group-type="author"><name><surname>Bricogne</surname><given-names>G</given-names></name><name><surname>Blanc</surname><given-names>E</given-names></name><name><surname>Brandi</surname><given-names>M</given-names></name><name><surname>Flensburg</surname><given-names>C</given-names></name><name><surname>Keller</surname><given-names>P</given-names></name><name><surname>Paciorek</surname><given-names>W</given-names></name><etal/></person-group><year>2009</year><comment>BUSTER, version 2.8.0. Retrieved from about:home</comment></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib9'), ('date', u'2009'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'G Bricogne'), ('index', u'Bricogne, G')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'E Blanc'), ('index', u'Blanc, E')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Brandi'), ('index', u'Brandi, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'C Flensburg'), ('index', u'Flensburg, C')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Keller'), ('index', u'Keller, P')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'W Paciorek'), ('index', u'Paciorek, W')]))])]), ('authorsEtAl', True), ('title', u'BUSTER, version 2.8.0. Retrieved from about:home'), ('details', u'BUSTER, version 2.8.0. Retrieved from about:home')])]
         ),

        # reference of type other with no details, 15266 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib12"><element-citation publication-type="other"><person-group person-group-type="author"><name><surname>Blench</surname><given-names>R</given-names></name></person-group><year iso-8601-date="2006">2006</year><article-title>Archaeology-Language-and-the-African-Past</article-title></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib12'), ('date', u'2006'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Blench'), ('index', u'Blench, R')]))])]), ('title', u'Archaeology-Language-and-the-African-Past')])]
         ),

        # reference of type journal with no journal name, 00340 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib10"><element-citation publication-type="journal"><person-group person-group-type="author"><collab>WHO</collab></person-group><year>2012</year><article-title>Press release: 65th World Health Assembly closes with new global health measures</article-title><ext-link ext-link-type="uri" xlink:href="http://www.who.int/mediacentre/news/releases/2012/wha65_closes_20120526/en/index.html">http://www.who.int/mediacentre/news/releases/2012/wha65_closes_20120526/en/index.html</ext-link></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib10'), ('date', u'2012'), ('authors', [OrderedDict([('type', 'group'), ('name', 'WHO')])]), ('title', u'Press release: 65th World Health Assembly closes with new global health measures'), ('details', u'http://www.who.int/mediacentre/news/releases/2012/wha65_closes_20120526/en/index.html'), ('uri', u'http://www.who.int/mediacentre/news/releases/2012/wha65_closes_20120526/en/index.html')])]
         ),

        # reference of type book with no source, 00051 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib11"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Cutler</surname><given-names>DM</given-names></name><name><surname>Deaton</surname><given-names>AS</given-names></name><name><surname>Lleras-Muney</surname><given-names>A</given-names></name></person-group><year>2006</year><article-title>The determinants of mortality (No. w11963)</article-title><publisher-loc>Cambridge</publisher-loc><publisher-name>National Bureau of Economic Research</publisher-name></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib11'), ('date', u'2006'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'DM Cutler'), ('index', u'Cutler, DM')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AS Deaton'), ('index', u'Deaton, AS')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'A Lleras-Muney'), ('index', u'Lleras-Muney, A')]))])]), ('title', u'The determinants of mortality (No. w11963)'), ('details', u'Cambridge, National Bureau of Economic Research')])]
         ),

        # reference of type book with no publisher, 00031 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib4"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Engel</surname><given-names>W</given-names></name></person-group><year>2005</year><source>SHADERX3: Advanced Rendering with DirectX and OpenGL: Charles River Media</source><publisher-loc>Hingham, MA, USA</publisher-loc></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib4'), ('date', u'2005'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'W Engel'), ('index', u'Engel, W')]))])]), ('title', u'SHADERX3: Advanced Rendering with DirectX and OpenGL: Charles River Media'), ('details', 'SHADERX3: Advanced Rendering with DirectX and OpenGL: Charles River Media, Hingham, MA, USA')])]
         ),

        # reference of type book with no bookTitle, 03069 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib24"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Laue</surname><given-names>TM</given-names></name><name><surname>Shah</surname><given-names>BD</given-names></name><name><surname>Ridgeway</surname><given-names>RM</given-names></name><name><surname>Pelletier</surname><given-names>SL</given-names></name></person-group><year>1992</year><publisher-loc>Cambridge</publisher-loc><publisher-name>The Royal Society of Chemistry</publisher-name><fpage>90</fpage><lpage>125</lpage></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib24'), ('date', u'1992'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TM Laue'), ('index', u'Laue, TM')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'BD Shah'), ('index', u'Shah, BD')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'RM Ridgeway'), ('index', u'Ridgeway, RM')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'SL Pelletier'), ('index', u'Pelletier, SL')]))])]), ('title', u'90\u2013125, Cambridge, The Royal Society of Chemistry'), ('details', u'90\u2013125, Cambridge, The Royal Society of Chemistry')])]
         ),

        # reference with unicode in collab tag, also gets turned into unknown type, 18023 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib55"><element-citation publication-type="software"><person-group person-group-type="author"><collab>Schrödinger, LLC</collab></person-group><year iso-8601-date="2014">2014</year><source>The PyMOL Molecular Graphics System</source><edition>Version 1.7.2</edition><publisher-name>Schrodinger, LLC</publisher-name></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib55'), ('date', u'2014'), ('authors', [OrderedDict([('type', 'group'), ('name', u'Schr\xf6dinger, LLC')])]), ('title', u'The PyMOL Molecular Graphics System'), ('details', u'The PyMOL Molecular Graphics System, Version 1.7.2, Schrodinger, LLC')])]
         ),

        # data reference with no source, 16800 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib10"><element-citation publication-type="data"><person-group person-group-type="author"><collab>Biosharing.org</collab></person-group><year iso-8601-date="2016">2016</year><data-title>A catalogue of data preservation, management and sharing policies from international funding agencies, regulators and journals</data-title><pub-id pub-id-type="accession" xlink:href="https://biosharing.org/policies">biosharing.org/policies</pub-id></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib10'), ('date', u'2016'), ('authors', [OrderedDict([('type', 'group'), ('name', u'Biosharing.org')])]), ('title', u'A catalogue of data preservation, management and sharing policies from international funding agencies, regulators and journals'), ('details', u'A catalogue of data preservation, management and sharing policies from international funding agencies, regulators and journals, biosharing.org/policies')])]
         ),

        # reference with an lpage and not fpage still gets pages value set, 13905 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib71"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Yasuda</surname><given-names>R</given-names></name><name><surname>Nimchinsky</surname><given-names>EA</given-names></name><name><surname>Scheuss</surname><given-names>V</given-names></name><name><surname>Pologruto</surname><given-names>TA</given-names></name><name><surname>Oertner</surname><given-names>TG</given-names></name><name><surname>Sabatini</surname><given-names>BL</given-names></name><name><surname>Svoboda</surname><given-names>K</given-names></name></person-group><year iso-8601-date="2004">2004</year><article-title>Imaging calcium concentration dynamics in small neuronal compartments</article-title><source>Science\'s STKE</source><volume>2004</volume><lpage>, pl5.</lpage><pub-id pub-id-type="doi">10.1126/stke.2192004pl5</pub-id></element-citation></ref></ref-list>',
         [OrderedDict([('type', u'journal'), ('id', u'bib71'), ('date', u'2004'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Yasuda'), ('index', u'Yasuda, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'EA Nimchinsky'), ('index', u'Nimchinsky, EA')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'V Scheuss'), ('index', u'Scheuss, V')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TA Pologruto'), ('index', u'Pologruto, TA')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TG Oertner'), ('index', u'Oertner, TG')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'BL Sabatini'), ('index', u'Sabatini, BL')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'K Svoboda'), ('index', u'Svoboda, K')]))])]), ('articleTitle', u'Imaging calcium concentration dynamics in small neuronal compartments'), ('journal', OrderedDict([('name', [u"Science's STKE"])])), ('volume', u'2004'), ('pages', u', pl5.'), ('doi', u'10.1126/stke.2192004pl5')])]
         ),

        # Reference with a collab using italic tag, from 05423 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib101"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Wood</surname><given-names>WB</given-names></name><collab>The Community of <italic>C. elegans</italic>Researchers</collab></person-group><year>1988</year><source>The nematode Caenorhabditis elegans</source><publisher-loc>Cold Spring Harbor, New York</publisher-loc><publisher-name>Cold Spring Harbor Laboratory Press</publisher-name></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'book'), ('id', u'bib101'), ('date', u'1988'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'WB Wood'), ('index', u'Wood, WB')]))]), OrderedDict([('type', 'group'), ('name', u'The Community of <i>C. elegans</i>Researchers')])]), ('bookTitle', u'The nematode Caenorhabditis elegans'), ('publisher', OrderedDict([('name', [u'Cold Spring Harbor Laboratory Press']), ('address', OrderedDict([('formatted', [u'Cold Spring Harbor, New York']), ('components', OrderedDict([('locality', [u'Cold Spring Harbor, New York'])]))]))]))])]
         ),

        )
    def test_references_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.references_json(body_tag)
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        (None, None, None)
         )
    def test_references_publisher(self, publisher_name, publisher_loc, expected):
        self.assertEqual(parser.references_publisher(publisher_name, publisher_loc), expected)


    @unpack
    @data(
        ("<root><italic></italic></root>", 0),
        ("<root><sec><p>Content</p></sec></root>", 1),
    )
    def test_body_blocks(self, xml_content, expected_len):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        body_block_tags = parser.body_blocks(body_tag)
        self.assertEqual(len(body_block_tags), expected_len)


    @unpack
    @data(
        ('<root><sec sec-type="intro" id="s1"><title>Introduction <italic>section</italic></title><p>content</p></sec></root>',
         OrderedDict([('type', 'section'), ('id', u's1'), ('title', u'Introduction <i>section</i>')])
         ),

        ('<root><boxed-text id="box1"><object-id pub-id-type="doi">10.7554/eLife.00013.009</object-id><label>Box 1.</label><caption><title>Box title</title><p>content</p></caption></boxed-text></root>',
         OrderedDict([('type', 'box'), ('doi', u'10.7554/eLife.00013.009'), ('id', u'box1'), ('label', u'Box 1.'), ('title', u'Box title')])
         ),

        ('<root><p>content</p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<table-wrap><table><thead><tr><th/><th></tr><tbody><tr><td></td></tr></tbody></table></table-wrap></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<disp-formula><mml:math><mml:mtext>Body\u2009Mass</mml:mtext></mml:mtext></disp-formula></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<fig-group><fig></fig><fig></fig></fig-group></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p>content<fig></fig></p></root>',
         OrderedDict([('type', 'paragraph'), ('text', u'content')])
         ),

        ('<root><p><fig id="fig7" position="float"><graphic xlink:href="elife-00498-fig7-v1.tif"/></fig></p></root>',
         OrderedDict([('type', 'paragraph')])
         ),

        ('<root><fig id="fig1"><caption><title>Fig title not in a paragraph</title></caption><graphic xlink:href="elife-00639-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig1'), ('title', u'Fig title not in a paragraph'), ('alt', '')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig8" position="float"><label>Reviewers’ figure 1</label><caption/><graphic xlink:href="elife-00723-resp-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig8'), ('label', u'Reviewers\u2019 figure 1'), ('title', u'Reviewers\u2019 figure 1'),('alt', ''), ('uri', u'elife-00723-resp-fig1-v1.tif')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig8" position="float"><label>Reviewers’ figure 1</label><caption><p>First sentence</p></caption><graphic xlink:href="elife-00723-resp-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig8'), ('label', u'Reviewers\u2019 figure 1'), ('title', u'First sentence'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'First sentence')])]), ('alt', ''), ('uri', u'elife-00723-resp-fig1-v1.tif')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig8" position="float"><label>Reviewers’ figure 1</label><caption><p>First sentence. Second sentence.</p></caption><graphic xlink:href="elife-00723-resp-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig8'), ('label', u'Reviewers\u2019 figure 1'), ('title', u'First sentence'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'First sentence. Second sentence.')])]), ('alt', ''), ('uri', u'elife-00723-resp-fig1-v1.tif')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/><attrib>PHOTO CREDIT</attrib></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif'), ('attribution', [u'PHOTO CREDIT'])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/><permissions><copyright-statement>© 1991, Publisher 1, All Rights Reserved</copyright-statement><copyright-year>1991</copyright-year><copyright-holder>Publisher 1</copyright-holder><license><license-p>The in situ image in panel 3 is reprinted with permission from Figure 2D, <xref ref-type="bibr" rid="bib72">Small et al. (1991)</xref>, <italic>Test &amp; Automated</italic>.</license-p></license></permissions><permissions><copyright-statement>© 1991, Publisher 2, All Rights Reserved</copyright-statement><copyright-year>1991</copyright-year><copyright-holder>Publisher 2</copyright-holder><license><license-p>In situ images in panels 4 and 5 are reprinted with permission from Figure 3A and 3C, <xref ref-type="bibr" rid="bib74">Stanojevic et al. (1991)</xref>, <italic>Journal</italic>.</license-p></license></permissions></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif'), ('attribution', ['The in situ image in panel 3 is reprinted with permission from Figure 2D, <a href="#bib72">Small et al. (1991)</a>, <i>Test &amp; Automated</i>.', 'In situ images in panels 4 and 5 are reprinted with permission from Figure 3A and 3C, <a href="#bib74">Stanojevic et al. (1991)</a>, <i>Journal</i>.'])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig3s1" position="float" specific-use="child-fig"><object-id pub-id-type="doi">10.7554/eLife.00666.012</object-id><label>Figure 3—figure supplement 1.</label><caption><title>Title of the figure supplement</title><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00666.013</object-id><label>Figure 3—figure supplement 1—Source data 1.</label><caption><title>Title of the figure supplement source data.</title><p>Legend of the figure supplement source data.</p></caption><media mime-subtype="xlsx" mimetype="application" xlink:href="elife-00666-fig3-figsupp1-data1-v1.xlsx"/></supplementary-material></p></caption><graphic xlink:href="elife-00666-fig3-figsupp1-v1.tiff"/></fig></root>',
        OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.012'), ('id', u'fig3s1'), ('label', u'Figure 3\u2014figure supplement 1.'), ('title', u'Title of the figure supplement'), ('alt', ''), ('uri', u'elife-00666-fig3-figsupp1-v1.tiff'), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.00666.013'), ('id', u'SD1-data'), ('label', u'Figure 3\u2014figure supplement 1\u2014Source data 1.'), ('title', u'Title of the figure supplement source data.'), ('mediaType', u'application/xlsx'), ('uri', u'elife-00666-fig3-figsupp1-data1-v1.xlsx')])])])
         ),

        ('<root><table-wrap id="tbl2" position="float"><object-id pub-id-type="doi">10.7554/eLife.00013.011</object-id><label>Table 2.</label><caption><p>Caption <xref ref-type="table-fn" rid="tblfn2">*</xref>content</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00013.011">http://dx.doi.org/10.7554/eLife.00013.011</ext-link></p></caption><table frame="hsides" rules="groups"><thead><tr><th>Species</th><th>Reference<xref ref-type="table-fn" rid="tblfn3">*</xref></th></tr></thead><tbody><tr><td><italic>Algoriphagus machipongonensis</italic> PR1</td><td><xref ref-type="bibr" rid="bib3">Alegado et al. (2012)</xref></td></tr></tbody></table><table-wrap-foot><fn id="tblfn1"><label>*</label><p>Footnote 1</p></fn><fn id="tblfn3"><label>§</label><p>CM = conditioned medium;</p></fn><fn><p>MP, Middle Pleistocene.</p></fn><fn id="id_not_used"><p>Footnote parsed with no id</p></fn></table-wrap-foot></table-wrap></root>',
         OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.00013.011'), ('id', u'tbl2'), ('label', u'Table 2.'), ('title', u'Caption <a href="#tblfn2">*</a>content'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Caption <a href="#tblfn2">*</a>content')])]), ('tables', ['<table><thead><tr><th>Species</th><th>Reference<a href="#tblfn3">*</a></th></tr></thead><tbody><tr><td><i>Algoriphagus machipongonensis</i> PR1</td><td><a href="#bib3">Alegado et al. (2012)</a></td></tr></tbody></table>']), ('footnotes', [OrderedDict([('id', u'tblfn1'), ('label', u'*'), ('text', [OrderedDict([('type', 'paragraph'), ('text', 'Footnote 1')])])]), OrderedDict([('id', u'tblfn3'), ('label', u'\xa7'), ('text', [OrderedDict([('type', 'paragraph'), ('text', 'CM = conditioned medium;')])])]), OrderedDict([('text', [OrderedDict([('type', 'paragraph'), ('text', 'MP, Middle Pleistocene.')])])]), OrderedDict([('text', [OrderedDict([('type', 'paragraph'), ('text', 'Footnote parsed with no id')])])])])])
            ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML"><disp-formula id="equ7"><label>(3)</label><mml:math id="m7"><mml:mrow><mml:msub><mml:mi>P</mml:mi><mml:mrow><mml:mi>k</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:msub><mml:mrow><mml:mo>(</mml:mo><mml:mi>I</mml:mi><mml:mi>O</mml:mi><mml:mo>)</mml:mo></mml:mrow><mml:mo>=</mml:mo><mml:mn>0.1</mml:mn><mml:mo>+</mml:mo><mml:mfrac><mml:mrow><mml:mn>0.5</mml:mn></mml:mrow><mml:mrow><mml:mo>(</mml:mo><mml:mn>1</mml:mn><mml:mo>+</mml:mo><mml:msup><mml:mi>e</mml:mi><mml:mrow><mml:mo>-</mml:mo><mml:mn>0.3</mml:mn><mml:mrow><mml:mo>(</mml:mo><mml:mi>I</mml:mi><mml:msub><mml:mi>N</mml:mi><mml:mrow><mml:mi>k</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:msub><mml:mo>-</mml:mo><mml:mn>100</mml:mn><mml:mo>)</mml:mo></mml:mrow></mml:mrow></mml:msup><mml:mo>)</mml:mo></mml:mrow></mml:mfrac></mml:mrow></mml:math></disp-formula></root>',
        OrderedDict([('type', 'mathml'), ('id', u'equ7'), ('label', u'(3)'), ('mathml', u'<math><mrow><msub><mi>P</mi><mrow><mi>k</mi><mo>,</mo><mi>j</mi></mrow></msub><mrow><mo>(</mo><mi>I</mi><mi>O</mi><mo>)</mo></mrow><mo>=</mo><mn>0.1</mn><mo>+</mo><mfrac><mrow><mn>0.5</mn></mrow><mrow><mo>(</mo><mn>1</mn><mo>+</mo><msup><mi>e</mi><mrow><mo>-</mo><mn>0.3</mn><mrow><mo>(</mo><mi>I</mi><msub><mi>N</mi><mrow><mi>k</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>-</mo><mn>100</mn><mo>)</mo></mrow></mrow></msup><mo>)</mo></mrow></mfrac></mrow></math>')])
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><list><list-item>List item one</list-item><list-item>List item two</list-item></root>',
         OrderedDict([('type', 'list'), ('prefix', 'none'), ('items', [u'List item one', u'List item two'])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><list list-type="order"><list-item>List item one</list-item><list-item>List item two</list-item></root>',
         OrderedDict([('type', 'list'), ('prefix', 'number'), ('items', [u'List item one', u'List item two'])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><list list-type="alpha-upper"><list-item><p>List paragraph one</p></list-item><list-item><p>List paragraph two</p></list-item></root>',
         OrderedDict([('type', 'list'), ('prefix', 'alpha-upper'), ('items', [[OrderedDict([('type', 'paragraph'), ('text', u'List paragraph one')])], [OrderedDict([('type', 'paragraph'), ('text', u'List paragraph two')])]])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><list list-type="simple"><list-item><p>List paragraph one</p></list-item><list-item><p>List paragraph two</p></list-item></root>',
         OrderedDict([('type', 'list'), ('prefix', 'bullet'), ('items', [[OrderedDict([('type', 'paragraph'), ('text', u'List paragraph one')])], [OrderedDict([('type', 'paragraph'), ('text', u'List paragraph two')])]])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media mime-subtype="xlsx" mimetype="application" xlink:href="elife00051s001.xlsx"/></root>',
         OrderedDict()
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media content-type="glencoe play-in-place height-250 width-310" id="video1" mime-subtype="avi" mimetype="video" xlink:href="elife00007v001.AVI"><object-id pub-id-type="doi">10.7554/eLife.00007.016</object-id><label>Video 1.</label><caption><p>On-plant assay, plant 7u, WT, June 18, 2011.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00007.016">http://dx.doi.org/10.7554/eLife.00007.016</ext-link></p></caption></media></root>',
        OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.00007.016'), ('id', u'video1'), ('label', u'Video 1.'), ('title', u'On-plant assay, plant 7u, WT, June 18, 2011.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'On-plant assay, plant 7u, WT, June 18, 2011.')])]), ('uri', u'elife00007v001.AVI')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media content-type="glencoe play-in-place height-250 width-310" id="media2" mime-subtype="mov" mimetype="video" xlink:href="elife-00005-media2.mov"><object-id pub-id-type="doi">10.7554/eLife.00005.016</object-id><label>Movie 2.</label><caption><title>3D reconstruction of the human PRC2-AEBP2 complex.</title><p>Docking of crystal structure for EED and RbAp48 WD40s (PDB: 2QXV; 2YB8) are indicated respectively in green and red. Docking of crystal structures of homologue SANT, SET and Zn finger domains (PDB: 3HM5, 3H6L and 2VY5) are shown in blue and purple.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00005.016">http://dx.doi.org/10.7554/eLife.00005.016</ext-link></p><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00005.017</object-id><label>Movie 2—source code 1.</label><caption><p>Overall architecture of the PRC2 complex.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00005.017">http://dx.doi.org/10.7554/eLife.00005.017</ext-link></p></caption><media mime-subtype="wrl" mimetype="application" xlink:href="elife-00005-media2-code1-v1.wrl"/></supplementary-material></p></caption></media>',
        OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.00005.016'), ('id', u'media2'), ('label', u'Movie 2.'), ('title', u'3D reconstruction of the human PRC2-AEBP2 complex.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Docking of crystal structure for EED and RbAp48 WD40s (PDB: 2QXV; 2YB8) are indicated respectively in green and red. Docking of crystal structures of homologue SANT, SET and Zn finger domains (PDB: 3HM5, 3H6L and 2VY5) are shown in blue and purple.')])]), ('uri', u'elife-00005-media2.mov'), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.00005.017'), ('id', u'SD1-data'), ('label', u'Movie 2\u2014source code 1.'), ('title', u'Overall architecture of the PRC2 complex.'), ('mediaType', u'application/wrl'), ('uri', u'elife-00005-media2-code1-v1.wrl')])])])
         ),

        ('<root><disp-quote><p>content</p></disp-quote></root>',
         OrderedDict([('type', 'quote'), ('text', [OrderedDict([('type', 'paragraph'), ('text', u'content')])])])
         ),

    )
    def test_body_block_content(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.body_block_content(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ('<root><sec><boxed-text><title>Strange content for test coverage</title><table-wrap><label>A label</label></table-wrap><fig></fig><fig><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id></fig></boxed-text></sec></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'section'), ('content', [OrderedDict([('type', 'box'), ('title', u'Strange content for test coverage'), ('content', [OrderedDict([('type', 'table'), ('label', u'A label'), ('title', u'A label'), ('tables', [])]), OrderedDict([('type', 'image'), ('alt', '')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('alt', '')])])])])])])])]
         ),

        ('<root><p>content <italic>test</italic></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'content <i>test</i>')])])])]
         ),
        
        ('<root><p>content<table-wrap><table><thead><tr><th/></tr></thead><tbody><tr><td></td></tr></tbody></table></table-wrap></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'content')]), OrderedDict([('type', 'table'), ('tables', ['<table><thead><tr><th></th></tr></thead><tbody><tr><td></td></tr></tbody></table>'])])])])]
         ),

        ('<root><p>content</p><table-wrap><table><thead><tr><th/></tr></thead><tbody><tr><td></td></tr></tbody></table></table-wrap></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'content')]), OrderedDict([('type', 'table'), ('tables', [u'<table><thead><tr><th></th></tr></thead><tbody><tr><td></td></tr></tbody></table>'])])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')])])])]
         ),


        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])])])])]
         ),


        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML"><p>This <disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'This ')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Caption')])]), ('alt', '')])])])]
        ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML"><p>This <disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption <bold>b</bold> <disp-formula id="equ3"><label>(3)</label><mml:math id="m3"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>where m<sub>i</sub> given by: <disp-formula id="equ4"><label>(4)</label><mml:math id="m4"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>More caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'This ')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Caption <b>b</b> ')]), OrderedDict([('type', 'mathml'), ('id', u'equ3'), ('label', u'(3)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'where m<sub>i</sub> given by: ')]), OrderedDict([('type', 'mathml'), ('id', u'equ4'), ('label', u'(4)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'More caption')])]), ('alt', '')])])])]
        ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML"><p>This <xref ref-type="fig" rid="fig3">Figure 3A</xref> test<disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption <bold>b</bold> <disp-formula id="equ3"><label>(3)</label><mml:math id="m3"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>where m<sub>i</sub> given by: <disp-formula id="equ4"><label>(4)</label><mml:math id="m4"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>More caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'This <a href="#fig3">Figure 3A</a> test')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Caption <b>b</b> ')]), OrderedDict([('type', 'mathml'), ('id', u'equ3'), ('label', u'(3)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'where m<sub>i</sub> given by: ')]), OrderedDict([('type', 'mathml'), ('id', u'equ4'), ('label', u'(4)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'More caption')])]), ('alt', '')])])])]
        ),
        
        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML"><p><bold>This</bold> is <xref ref-type="fig" rid="fig3">Figure 3A</xref> test<disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption <bold>b</bold> <disp-formula id="equ3"><label>(3)</label><mml:math id="m3"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>where m<sub>i</sub> given by: <disp-formula id="equ4"><label>(4)</label><mml:math id="m4"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>More caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'<b>This</b> is <a href="#fig3">Figure 3A</a> test')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Caption <b>b</b> ')]), OrderedDict([('type', 'mathml'), ('id', u'equ3'), ('label', u'(3)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'where m<sub>i</sub> given by: ')]), OrderedDict([('type', 'mathml'), ('id', u'equ4'), ('label', u'(4)'), ('mathml', u'<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'More caption')])]), ('alt', '')])])])]
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink><p><bold>This</bold> <fig id="fig7" position="float"><graphic xlink:href="elife-00012-resp-fig2-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'<b>This</b> ')]), OrderedDict([('type', 'image'), ('id', u'fig7'), ('alt', ''), ('uri', u'elife-00012-resp-fig2-v1.tif')])])])]
        ),

        ('<root><disp-quote><p>content</p></disp-quote></root>',
         [OrderedDict([('content', [OrderedDict([('type', 'quote'), ('text', [OrderedDict([('type', 'paragraph'), ('text', u'content')])])])])])]
         ),

        )
    def test_body_block_content_render(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_block_content_render(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="s1"><title>Section title</title><p>Content.<fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group></p><p>More content</p></sec></root>',
        [OrderedDict([('type', 'section'), ('id', u's1'), ('title', u'Section title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="s1"><title>Section title</title><p>Content.</p><fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group><p>More content</p></sec></root>',
        [OrderedDict([('type', 'section'), ('id', u's1'), ('title', u'Section title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><boxed-text><p>Content 1</p><p>Content 2</p></boxed-text></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content 1')]), OrderedDict([('type', 'paragraph'), ('text', u'Content 2')])]
         ),

        # Below when there is a space between paragraph tags, it should not render as a paragraph
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><boxed-text><p>Content 1</p> <p>Content 2</p></boxed-text></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content 1')]), OrderedDict([('type', 'paragraph'), ('text', u'Content 2')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink><p><bold>This</bold> <fig id="fig7" position="float"><graphic xlink:href="elife-00012-resp-fig2-v1.tif"/></fig></p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'<b>This</b> ')]), OrderedDict([('type', 'image'), ('id', u'fig7'), ('alt', ''), ('uri', u'elife-00012-resp-fig2-v1.tif')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig>More content</p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.</p><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig><p>More content</p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig1-v1.tif')]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])]
         ),
         
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.</p><fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group><p>More content</p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-v1.tif'), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('alt', ''), ('uri', u'elife-00666-fig2-figsupp1-v1.tif')])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])]
         ),

        )
    def test_render_raw_body(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.render_raw_body(soup.contents[0])
        self.assertEqual(expected, tag_content)



    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><abstract><object-id pub-id-type="doi">10.7554/eLife.00070.001</object-id><p>Paragraph 1</p><p>Paragraph 2</p></root>',
        OrderedDict([('doi', u'10.7554/eLife.00070.001'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 1')]), OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 2')])])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><abstract abstract-type="executive-summary"><object-id pub-id-type="doi">10.7554/eLife.00070.002</object-id><title>eLife digest</title><p>Paragraph 1</p><p>Paragraph 2</p><p>Paragraph 3</p></root>',
        None
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"><abstract><object-id pub-id-type="doi">10.7554/eLife.00001.001</object-id><p>Example <sub>in</sub> <italic>cis</italic> <sc>or</sc> <italic>trans</italic> <underline>and</underline> <italic>Gfrα2</italic> <inline-formula><mml:math id="inf1"><mml:mstyle displaystyle="true" scriptlevel="0"><mml:mrow><mml:munder><mml:mo/><mml:mi>m</mml:mi></mml:munder><mml:mrow><mml:msub><mml:mover accent="true"><mml:mi>p</mml:mi><mml:mo/></mml:mover><mml:mi>m</mml:mi></mml:msub><mml:mo>=</mml:mo><mml:mn>0</mml:mn></mml:mrow></mml:mrow></mml:mstyle></mml:math></inline-formula> <sup>by</sup> <bold>its</bold> co-receptors as *p&lt;0.05 &gt;0.25% <xref ref-type="bibr" rid="bib25">Schneider et al., 2006</xref> and ligands.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00001.001">http://dx.doi.org/10.7554/eLife.00001.001</ext-link></p></abstract></root>',
        OrderedDict([('doi', u'10.7554/eLife.00001.001'), ('content', [OrderedDict([('type', 'paragraph'), ('text', 'Example <sub>in</sub> <i>cis</i> <span class="small-caps">or</span> <i>trans</i> <span class="underline">and</span> <i>Gfr\xce\xb12</i> <math id="inf1"><mstyle displaystyle="true" scriptlevel="0"><mrow><munder><mo></mo><mi>m</mi></munder><mrow><msub><mover accent="true"><mi>p</mi><mo></mo></mover><mi>m</mi></msub><mo>=</mo><mn>0</mn></mrow></mrow></mstyle></math> <sup>by</sup> <b>its</b> co-receptors as *p&lt;0.05 &gt;0.25% <a href="#bib25">Schneider et al., 2006</a> and ligands.')])])])
         ),

        )
    def test_abstract_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstract_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><abstract abstract-type="executive-summary"><object-id pub-id-type="doi">10.7554/eLife.00070.002</object-id><title>eLife digest</title><p>Paragraph 1</p><p>Paragraph 2</p><p>Paragraph 3</p></root>',
        OrderedDict([('doi', u'10.7554/eLife.00070.002'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 1')]), OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 2')]), OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 3')])])])
         ),
        )
    def test_digest_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.digest_json(soup.contents[0])
        self.assertEqual(expected, tag_content)

    """
    Unit test small or special cases
    """
    @unpack
    @data(("elife-kitchen-sink.xml", "pub", ('28', '02', '2014')))
    def test_ymd(self, filename, test_date_type, expected):
        soup = self.soup(filename)
        date_tag = raw_parser.pub_date(soup, date_type=test_date_type)
        self.assertEqual(expected, parser.ymd(date_tag))

    @unpack
    @data(("elife-kitchen-sink.xml", "received", date_struct(2012, 6, 22)),
        ("elife-kitchen-sink.xml", None, None),
        ("elife-kitchen-sink.xml", "not_a_date_type", None))
    def test_history_date(self, filename, date_type, expected):
        self.assertEqual(expected, parser.history_date(self.soup(filename), date_type))

    @unpack
    @data(("<p></p>", "paragraph", "<p/>"),
        ("<p>§ <italic>*</italic></p>", "paragraph", u"<p>§ <italic>*</italic></p>"),)
    def test_duplicate_tag(self, xml, parser_function, expected_xml):
        # To test, first parse the XML into a tag, then duplicate it, then check the contents
        soup = parser.parse_xml(xml)
        tags = getattr(raw_parser, parser_function)(soup)
        tag_copy = parser.duplicate_tag(tags[0])
        self.assertEqual(expected_xml, unicode(tag_copy))

    """
    Functions that require more than one argument to test against json output
    """

    @data("elife-kitchen-sink.xml")
    def test_journal_issn(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_issn"),
                         parser.journal_issn(self.soup(filename), "electronic"))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_author_contributions(self, filename):
        self.assertEqual(self.json_expected(filename, "author_contributions"),
                         parser.author_contributions(self.soup(filename), "con"))

    @data("elife-kitchen-sink.xml", "elife00190.xml")
    def test_competing_interests(self, filename):
        self.assertEqual(self.json_expected(filename, "competing_interests"),
                         parser.competing_interests(self.soup(filename), "conflict"))

    @data("elife-kitchen-sink.xml")
    def test_full_author_notes(self, filename):
        self.assertEqual(self.json_expected(filename, "full_author_notes"),
                         parser.full_author_notes(self.soup(filename), None))

    """
    Functions that only need soup to test them against json output
    """

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_abstract(self, filename):
        self.assertEqual(self.json_expected(filename, "abstract"),
                         parser.abstract(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml")
    def test_abstracts(self, filename):
        self.assertEqual(self.json_expected(filename, "abstracts"),
                         parser.abstracts(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_date"),
                         parser.accepted_date_date(self.soup(filename)))


    @data("elife-kitchen-sink.xml")
    def test_accepted_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_day"),
                         parser.accepted_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_month"),
                         parser.accepted_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_timestamp"),
                         parser.accepted_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_year"),
                         parser.accepted_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_ack(self, filename):
        self.assertEqual(self.json_expected(filename, "ack"),
                         parser.ack(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_acknowledgements(self, filename):
        self.assertEqual(self.json_expected(filename, "acknowledgements"),
                         parser.acknowledgements(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_article_type(self, filename):
        self.assertEqual(self.json_expected(filename, "article_type"),
                         parser.article_type(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml")
    def test_author_notes(self, filename):
        self.assertEqual(self.json_expected(filename, "author_notes"),
                         parser.author_notes(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml",
          "elife02935.xml", "elife00270.xml", "elife00351.xml")
    def test_authors(self, filename):
        self.assertEqual(self.json_expected(filename, "authors"),
                         parser.authors(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_authors_non_byline(self, filename):
        self.assertEqual(self.json_expected(filename, "authors_non_byline"),
                         parser.authors_non_byline(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00013.xml")
    def test_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "award_groups"),
                         parser.award_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_category(self, filename):
        self.assertEqual(self.json_expected(filename, "category"),
                         parser.category(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_collection_year(self, filename):
        self.assertEqual(self.json_expected(filename, "collection_year"),
                         parser.collection_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_component_doi(self, filename):
        self.assertEqual(self.json_expected(filename, "component_doi"),
                         parser.component_doi(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife05502.xml", "elife04490.xml",
          "elife-14093-v1.xml")
    def test_components(self, filename):
        self.assertEqual(self.json_expected(filename, "components"),
                         parser.components(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_conflict(self, filename):
        self.assertEqual(self.json_expected(filename, "conflict"),
                         parser.conflict(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-02833-v2.xml")
    def test_contributors(self, filename):
        self.assertEqual(self.json_expected(filename, "contributors"),
                         parser.contributors(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_holder(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_holder"),
                         parser.copyright_holder(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_statement"),
                         parser.copyright_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_year(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_year"),
                         parser.copyright_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "correspondence"),
                         parser.correspondence(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_digest(self, filename):
        self.assertEqual(self.json_expected(filename, "digest"),
                         parser.digest(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_display_channel(self, filename):
        self.assertEqual(self.json_expected(filename, "display_channel"),
                         parser.display_channel(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_doi(self, filename):
        self.assertEqual(self.json_expected(filename, "doi"),
                         parser.doi(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_elocation_id(self, filename):
        self.assertEqual(self.json_expected(filename, "elocation_id"),
                         parser.elocation_id(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml", "elife00013.xml")
    def test_full_abstract(self, filename):
        self.assertEqual(self.json_expected(filename, "full_abstract"),
                         parser.full_abstract(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_affiliation(self, filename):
        self.assertEqual(self.json_expected(filename, "full_affiliation"),
                         parser.full_affiliation(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_award_group_funding_source(self, filename):
        self.assertEqual(self.json_expected(filename, "full_award_group_funding_source"),
                         parser.full_award_group_funding_source(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "full_award_groups"),
                         parser.full_award_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife-02833-v2.xml")
    def test_full_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "full_correspondence"),
                         parser.full_correspondence(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_full_digest(self, filename):
        self.assertEqual(self.json_expected(filename, "full_digest"),
                         parser.full_digest(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_keyword_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "full_keyword_groups"),
                         parser.full_keyword_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_full_keywords(self, filename):
        self.assertEqual(self.json_expected(filename, "full_keywords"),
                         parser.full_keywords(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_license(self, filename):
        self.assertEqual(self.json_expected(filename, "full_license"),
                         parser.full_license(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_full_research_organism(self, filename):
        self.assertEqual(self.json_expected(filename, "full_research_organism"),
                         parser.full_research_organism(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_subject_area(self, filename):
        self.assertEqual(self.json_expected(filename, "full_subject_area"),
                         parser.full_subject_area(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_title(self, filename):
        self.assertEqual(self.json_expected(filename, "full_title"),
                         parser.full_title(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_funding_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "funding_statement"),
                         parser.funding_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml",
          "elife04953.xml", "elife00133.xml")
    def test_graphics(self, filename):
        self.assertEqual(self.json_expected(filename, "graphics"),
                         parser.graphics(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_impact_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "impact_statement"),
                         parser.impact_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_inline_graphics(self, filename):
        self.assertEqual(self.json_expected(filename, "inline_graphics"),
                         parser.inline_graphics(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_is_poa(self, filename):
        self.assertEqual(self.json_expected(filename, "is_poa"),
                         parser.is_poa(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_journal_id(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_id"),
                         parser.journal_id(self.soup(filename)))



    @data("elife-kitchen-sink.xml")
    def test_journal_title(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_title"),
                         parser.journal_title(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_keywords(self, filename):
        self.assertEqual(self.json_expected(filename, "keywords"),
                         parser.keywords(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_license(self, filename):
        self.assertEqual(self.json_expected(filename, "license"),
                         parser.license(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_license_url(self, filename):
        self.assertEqual(self.json_expected(filename, "license_url"),
                         parser.license_url(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife00007.xml", "elife04953.xml",
          "elife00005.xml", "elife05031.xml", "elife04493.xml", "elife06726.xml")
    def test_media(self, filename):
        self.assertEqual(self.json_expected(filename, "media"),
                         parser.media(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_timestamp"),
                         parser.pub_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_date"),
                         parser.pub_date_date(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_day"),
                         parser.pub_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_month"),
                         parser.pub_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_year"),
                         parser.pub_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_publisher(self, filename):
        self.assertEqual(self.json_expected(filename, "publisher"),
                         parser.publisher(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_publisher_id(self, filename):
        self.assertEqual(self.json_expected(filename, "publisher_id"),
                         parser.publisher_id(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_date"),
                         parser.received_date_date(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_day"),
                         parser.received_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_month"),
                         parser.received_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_timestamp"),
                         parser.received_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_year"),
                         parser.received_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_references(self, filename):
        # Alias of refs
        self.assertEqual(self.json_expected(filename, "refs"),
                         parser.references(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife02935.xml", "elife00051.xml",
          "elife_poa_e06828.xml", "elife02304.xml", "elife-14093-v1.xml")
    def test_refs(self, filename):
        self.assertEqual(self.json_expected(filename, "refs"),
                         parser.refs(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_related_article(self, filename):
        self.assertEqual(self.json_expected(filename, "related_article"),
                         parser.related_article(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_related_object_ids(self, filename):
        self.assertEqual(self.json_expected(filename, "related_object_ids"),
                         parser.related_object_ids(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_research_organism(self, filename):
        self.assertEqual(self.json_expected(filename, "research_organism"),
                         parser.research_organism(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_self_uri(self, filename):
        self.assertEqual(self.json_expected(filename, "self_uri"),
                         parser.self_uri(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_subject_area(self, filename):
        self.assertEqual(self.json_expected(filename, "subject_area"),
                         parser.subject_area(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife02304.xml")
    def test_supplementary_material(self, filename):
        self.assertEqual(self.json_expected(filename, "supplementary_material"),
                         parser.supplementary_material(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title(self, filename):
        self.assertEqual(self.json_expected(filename, "title"),
                         parser.title(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00240.xml", "elife00270.xml", "elife00351.xml")
    def test_title_prefix(self, filename):
        self.assertEqual(self.json_expected(filename, "title_prefix"),
                         parser.title_prefix(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title_short(self, filename):
        self.assertEqual(self.json_expected(filename, "title_short"),
                         parser.title_short(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title_slug(self, filename):
        self.assertEqual(self.json_expected(filename, "title_slug"),
                         parser.title_slug(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_volume(self, filename):
        self.assertEqual(self.json_expected(filename, "volume"),
                         parser.volume(self.soup(filename)))








if __name__ == '__main__':
    unittest.main()
