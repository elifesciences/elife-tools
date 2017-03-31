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
        ("elife-kitchen-sink.xml", 6),
        ("elife-02833-v2.xml", 0)
        )
    def test_ethics_json_by_file(self, filename, expected_length):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(len(parser.ethics_json(soup)), expected_length)


    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><fn-group content-type="ethics-information"><title>Ethics</title><fn fn-type="other"><p>Human subjects: This study was approved by the Institutional Review Board (IRB) of National Institute of Biological Sciences (IRBS030901) and consent was obtained; see the Materials and Methods section for details. The Helsinki guidelines were followed.</p></fn><fn fn-type="other"><p>Animal experimentation: The institutional animal care and use committee (IACUC) of the National Institute of Biological Sciences and the approved animal protocol is 09001T. The institutional guidelines for the care and use of laboratory animals were followed.</p></fn><fn fn-type="other"><p>Clinical trial Registry: NCT.</p><p>Registration ID: NCT00912041.</p><p>Clinical trial Registry: EudraCT.</p><p>Registration ID: EudraCT2004-000446-20.</p></fn></fn-group></back></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Human subjects: This study was approved by the Institutional Review Board (IRB) of National Institute of Biological Sciences (IRBS030901) and consent was obtained; see the Materials and Methods section for details. The Helsinki guidelines were followed.')]), OrderedDict([('type', 'paragraph'), ('text', u'Animal experimentation: The institutional animal care and use committee (IACUC) of the National Institute of Biological Sciences and the approved animal protocol is 09001T. The institutional guidelines for the care and use of laboratory animals were followed.')]), OrderedDict([('type', 'paragraph'), ('text', u'Clinical trial Registry: NCT.')]), OrderedDict([('type', 'paragraph'), ('text', u'Registration ID: NCT00912041.')]), OrderedDict([('type', 'paragraph'), ('text', u'Clinical trial Registry: EudraCT.')]), OrderedDict([('type', 'paragraph'), ('text', u'Registration ID: EudraCT2004-000446-20.')])]
         ),

        )
    def test_ethics_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.ethics_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


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
        ("elife04490.xml", 3)
    )
    def test_appendices_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.appendices_json(soup)
        self.assertEqual(len(tag_content), expected_len)


    @unpack
    @data(
        # example based on 14093 v1 with many sections and content
        ('<root><back><app-group><app id="app1"><title>Appendix 1</title><boxed-text><sec id="s25" sec-type="appendix"><title>1 Definitions related to phyllotaxis</title><p>Phyllotactic patterns emerge ...</p></sec><sec id="s26" sec-type="appendix"><title>2 The classical model of phyllotaxis: a brief recap</title><sec id="s27"><title>2.1 Model description</title><p>We implemented ...</p></sec></sec></boxed-text></sec></app><app id="app2"><title>Appendix 2</title><boxed-text><sec id="s53" sec-type="appendix"><title>Additional videos and initial conditions for all videos</title><p>For all videos, ...</p></sec></boxed-text></app></app-group></back></root>',
        [OrderedDict([('id', u'app1'), ('title', u'Appendix 1'), ('content', [OrderedDict([('type', 'section'), ('id', u's25'), ('title', u'1 Definitions related to phyllotaxis'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Phyllotactic patterns emerge ...')])])]), OrderedDict([('type', 'section'), ('id', u's26'), ('title', u'2 The classical model of phyllotaxis: a brief recap'), ('content', [OrderedDict([('type', 'section'), ('id', u's27'), ('title', u'2.1 Model description'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'We implemented ...')])])])])])])])]
        ),

        # example based on 14022 v3 having a section with no title in it, with some additional scenarios
        ('<root><back><app-group><app id="app1"><title>Appendix 1: Details of the automated linear stability analysis</title><boxed-text><sec id="s15" sec-type="appendix"><p>We consider a reaction-diffusion system of the form<disp-formula id="equ5"><label>(1)</label><mml:math id="m5"><mml:mrow><mml:mi mathvariant="bold">c</mml:mi></mml:mrow></mml:math></disp-formula><p>where etc.</p></sec><sec id="s16" sec-type="appendix"><title>Step 1. Possible networks of size ...</title><p>We first generate a list of possible networks with ...</p></sec><sec id="test1"><p>Test another section with no title</p></sec><sec id="test2"><title>Section with title</title><p>Section content</p></sec><sec id="test3"><p>Second section with no title</p></sec></boxed-text></app></app-group></back></root>',
         [OrderedDict([('id', u'app1'), ('title', u'Appendix 1: Details of the automated linear stability analysis'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'We consider a reaction-diffusion system of the form')]), OrderedDict([('type', 'mathml'), ('id', u'equ5'), ('label', u'(1)'), ('mathml', '<math><mrow><mi mathvariant="bold">c</mi></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'where etc.')]), OrderedDict([('type', 'section'), ('id', u's16'), ('title', u'Step 1. Possible networks of size ...'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'We first generate a list of possible networks with ...')])])]), OrderedDict([('type', 'paragraph'), ('text', u'Test another section with no title')]), OrderedDict([('type', 'section'), ('id', u'test2'), ('title', u'Section with title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Section content')])])]), OrderedDict([('type', 'paragraph'), ('text', u'Second section with no title')])])])]
        ),

        # appendix with no sections, based on 00666 kitchen sink
        ('<root><back><app-group><app id="appendix-3"><title>Appendix 3</title><boxed-text><object-id pub-id-type="doi">10.7554/eLife.00666.034</object-id><p>This is an example of an appendix with no sections.</p></boxed-text></app></app-group></back></root>',
         [OrderedDict([('id', u'appendix-3'), ('title', u'Appendix 3'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'This is an example of an appendix with no sections.')])]), ('doi', u'10.7554/eLife.00666.034')])]
        ),

        # appendix with a section and a box, also based on 00666 kitchen sink
        ('<root><back><app-group><app id="appendix-1"><title>Appendix 1</title><sec sec-type="appendix" id="s8"><title>Preparation</title><boxed-text><object-id pub-id-type="doi">10.7554/eLife.00666.023</object-id><p>Paragraph content.</p></boxed-text></sec></app></app-group></back></root>',
         [OrderedDict([('id', u'appendix-1'), ('title', u'Appendix 1'), ('content', [OrderedDict([('type', 'section'), ('id', u's8'), ('title', u'Preparation'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph content.')])]), ('doi', u'10.7554/eLife.00666.023')])])])]
        ),

        )
    def test_appendices_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.appendices_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        # appendix with inline-graphic, based on 17092 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><app-group><app><title>Appendix 5</title><boxed-text><sec id="s56" sec-type="appendix"><sec id="s61"><title>E. Volatiles</title><p>Paragraph content.</p><table-wrap id="A5-tbl2" position="float"><object-id pub-id-type="doi">10.7554/eLife.17092.035</object-id><label>Appendix 5—table 2.</label><caption><p>Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901). NA = no structural isomer can be determined.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.17092.035">http://dx.doi.org/10.7554/eLife.17092.035</ext-link></p></caption><table frame="hsides" rules="groups"><tbody><tr><td valign="top"><inline-graphic mime-subtype="x-tiff" mimetype="image" xlink:href="elife-17092-inf1-v1"/><break/><inline-graphic mime-subtype="x-tiff" mimetype="image" xlink:href="elife-17092-inf2-v1"/></td></tr></tbody></table></table-wrap></sec></sec></boxed-text></app></app-group></back></root>',
         None,
         [OrderedDict([('title', u'Appendix 5'), ('content', [OrderedDict([('type', 'section'), ('id', u's61'), ('title', u'E. Volatiles'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph content.')]), OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.17092.035'), ('id', u'A5-tbl2'), ('label', u'Appendix 5\u2014table 2.'), ('title', 'Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901)'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901). NA = no structural isomer can be determined.')])]), ('tables', ['<table><tbody><tr><td valign="top"><img src="elife-17092-inf1-v1.jpg"/><br/><img src="elife-17092-inf2-v1.jpg"/></td></tr></tbody></table>'])])])])])])]
        ),

        # appendix with inline-graphic, based on 17092 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><app-group><app><title>Appendix 5</title><boxed-text><sec id="s56" sec-type="appendix"><sec id="s61"><title>E. Volatiles</title><p>Paragraph content.</p><table-wrap id="A5-tbl2" position="float"><object-id pub-id-type="doi">10.7554/eLife.17092.035</object-id><label>Appendix 5—table 2.</label><caption><p>Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901). NA = no structural isomer can be determined.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.17092.035">http://dx.doi.org/10.7554/eLife.17092.035</ext-link></p></caption><table frame="hsides" rules="groups"><tbody><tr><td valign="top"><inline-graphic mime-subtype="x-tiff" mimetype="image" xlink:href="elife-17092-inf1-v1"/><break/><inline-graphic mime-subtype="x-tiff" mimetype="image" xlink:href="elife-17092-inf2-v1"/></td></tr></tbody></table></table-wrap></sec></sec></boxed-text></app></app-group></back></root>',
         'https://example.org/',
         [OrderedDict([('title', u'Appendix 5'), ('content', [OrderedDict([('type', 'section'), ('id', u's61'), ('title', u'E. Volatiles'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph content.')]), OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.17092.035'), ('id', u'A5-tbl2'), ('label', u'Appendix 5\u2014table 2.'), ('title', 'Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901)'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Crushed eggshell sulfur-containing VOC emissions from 2.7 Ma OES (Laetoli LOT 13901). NA = no structural isomer can be determined.')])]), ('tables', ['<table><tbody><tr><td valign="top"><img src="https://example.org/elife-17092-inf1-v1.jpg"/><br/><img src="https://example.org/elife-17092-inf2-v1.jpg"/></td></tr></tbody></table>'])])])])])])]
        ),

        )
    def test_appendices_json_with_base_url(self, xml_content, base_url, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.appendices_json(soup.contents[0], base_url)
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ("elife04490.xml", ['<i>Nicotiana attenuata</i>', '<i>Manduca sexta</i>', u'Geocoris spp.', '<i>Trichobaris mucorea</i>', u'direct and indirect defense', u'diversity']),
        ("elife07586.xml", []),
        )
    def test_keywords_json(self, filename, expected):
        keywords_json = parser.keywords_json(self.soup(filename))
        self.assertEqual(expected, keywords_json)


    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"/>',
         []
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><kwd-group kwd-group-type="research-organism"><title>Research organism</title><kwd><italic>A. thaliana</italic></kwd><kwd>Other</kwd></kwd-group></root>',
         ['<i>A. thaliana</i>']
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><kwd-group kwd-group-type="research-organism"><title>Research organism</title><kwd>None</kwd></kwd-group></root>',
         []
        ),
    )

    def test_research_organism_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.research_organism_json(body_tag)
        self.assertEqual(expected, tag_content)


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
        ("elife02304.xml", 2),
        ("elife02935.xml", 2),
    )
    def test_datasets_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.datasets_json(soup)
        self.assertEqual(len(tag_content), expected_len)


    @unpack
    @data(
        
        # Datasets from 00825 v1, has generated, used, etal and italic tags
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00825.026</object-id><label>Supplementary file 1.</label><caption><title>(<bold>A</bold>) MDS patient characteristics. (<bold>B</bold>) Genes positively correlated with MYBL2 (MYBL2 gene signature). (<bold>C</bold>) qRT-PCR primer sequences.</title><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00825.026">http://dx.doi.org/10.7554/eLife.00825.026</ext-link></p></caption><media mime-subtype="xlsx" mimetype="application" xlink:href="elife-00825-supp1-v1.xlsx"/></supplementary-material><sec sec-type="datasets"><title>Major dataset</title><p>The following dataset was generated:</p><p><related-object content-type="generated-dataset" document-id="Dataset ID and/or url" document-id-type="dataset" document-type="data" id="dataro1"><name><surname>Heinrichs</surname><given-names>S</given-names></name>, <year>2013</year><x>, </x><source><italic>MYBL2</italic> Is a Sub-haploinsufficient Tumor Suppressor Gene in Myeloid Malignancy</source><x>, </x><object-id pub-id-type="art-access-id">GSE43401</object-id><x>; </x><ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE43401">http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE43401</ext-link><x>, </x><comment>Publicly available at GEO (<ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.gov/geo/">http://www.ncbi.nlm.nih.gov/geo/</ext-link>).</comment></related-object></p><p>The following previously published dataset was used:</p><p><related-object content-type="generated-dataset" document-id="Dataset ID and/or url" document-id-type="dataset" document-type="data" id="dataro2"><name><surname>Pellagatti</surname><given-names>A</given-names></name>, <name><surname>Cazzola</surname><given-names>M</given-names></name>, <name><surname>Giagounidis</surname><given-names>A</given-names></name>, <name><surname>Perry</surname><given-names>J</given-names></name>, <etal/>, <year>2010</year><x>, </x><source>Expression data from bone marrow CD34+ cells of MDS patients and healthy controls</source><x>, </x><object-id pub-id-type="art-access-id">GSE19429</object-id><x>; </x><ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE19429">http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE19429</ext-link><x>, </x><comment>Publicly available at GEO (<ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.gov/geo/">http://www.ncbi.nlm.nih.gov/geo/</ext-link>).</comment></related-object></p></sec></sec></back></root>',
        OrderedDict([('generated', [OrderedDict([('id', u'dataro1'), ('date', u'2013'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'S Heinrichs'), ('index', u'Heinrichs, S')]))])]), ('title', '<i>MYBL2</i> Is a Sub-haploinsufficient Tumor Suppressor Gene in Myeloid Malignancy'), ('dataId', u'GSE43401'), ('details', 'Publicly available at GEO (<a href="http://www.ncbi.nlm.nih.gov/geo/">http://www.ncbi.nlm.nih.gov/geo/</a>).'), ('uri', u'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE43401')])]), ('used', [OrderedDict([('id', u'dataro2'), ('date', u'2010'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'A Pellagatti'), ('index', u'Pellagatti, A')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Cazzola'), ('index', u'Cazzola, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'A Giagounidis'), ('index', u'Giagounidis, A')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Perry'), ('index', u'Perry, J')]))])]), ('authorsEtAl', True), ('title', u'Expression data from bone marrow CD34+ cells of MDS patients and healthy controls'), ('dataId', u'GSE19429'), ('details', 'Publicly available at GEO (<a href="http://www.ncbi.nlm.nih.gov/geo/">http://www.ncbi.nlm.nih.gov/geo/</a>).'), ('uri', u'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE19429')])])])
         ),

        # Datasets from 00666 kitchen sink, includes a DOI
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec sec-type="datasets" id="s7"><title>Major datasets</title><p>The following dataset was generated:</p><p><related-object content-type="generated-dataset" source-id="https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml" source-id-type="uri" id="dataset1"><name><surname>Harrison</surname><given-names>M</given-names></name><collab collab-type="author">York University</collab><year iso-8601-date="2016">2016</year><source>xml-mapping</source><ext-link ext-link-type="uri" xlink:href="https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml">https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml</ext-link><comment>Publicly available on GitHub</comment></related-object></p><p>The following previously published datasets were used:</p><p><related-object content-type="existing-dataset" source-id="https://github.com/elifesciences/elife-vendor-workflow-config/blob/master/elife-kitchen-sink.xml" source-id-type="uri" id="dataset2"><collab collab-type="author">M Harrison</collab><year iso-8601-date="2012">2012</year><source>elife-vendor-workflow-config</source><ext-link ext-link-type="uri" xlink:href="https://github.com/elifesciences/elife-vendor-workflow-config">https://github.com/elifesciences/elife-vendor-workflow-config</ext-link><comment>Publicly available on GitHub.</comment></related-object></p><p><related-object content-type="existing-dataset" source-id="https://github.com/elifesciences/elife-vendor-workflow-config/blob/master/elife-kitchen-sink.xml" source-id-type="uri" id="dataset3"><collab collab-type="author">Kok K</collab><collab collab-type="author">Ay A</collab><collab collab-type="author">Li L</collab><collab collab-type="author">Arnosti DN</collab><year iso-8601-date="2015">2015</year><data-title>Data from: Genome-wide errant targeting by Hairy</data-title><source>Dryad Digital Repository</source><pub-id pub-id-type="doi" assigning-authority="Dryad Digital Repository" xlink:href="https://doi.org/10.5061/dryad.cv323">https://doi.org/10.5061/dryad.cv323</pub-id></related-object></p></sec></back></root>',
        OrderedDict([('generated', [OrderedDict([('id', u'dataset1'), ('date', u'2016'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Harrison'), ('index', u'Harrison, M')]))]), OrderedDict([('type', 'group'), ('name', u'York University')])]), ('title', u'xml-mapping'), ('details', u'Publicly available on GitHub'), ('uri', u'https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml')])]), ('used', [OrderedDict([('id', u'dataset2'), ('date', u'2012'), ('authors', [OrderedDict([('type', 'group'), ('name', u'M Harrison')])]), ('title', u'elife-vendor-workflow-config'), ('details', u'Publicly available on GitHub.'), ('uri', u'https://github.com/elifesciences/elife-vendor-workflow-config')]), OrderedDict([('id', u'dataset3'), ('date', u'2015'), ('authors', [OrderedDict([('type', 'group'), ('name', u'Kok K')]), OrderedDict([('type', 'group'), ('name', u'Ay A')]), OrderedDict([('type', 'group'), ('name', u'Li L')]), OrderedDict([('type', 'group'), ('name', u'Arnosti DN')])]), ('title', u'Dryad Digital Repository'), ('doi', u'10.5061/dryad.cv323')])])])
         ),

        # 10856 v2, excerpt, for adding dates to datasets missing a year value
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">10856</article-id><article-id pub-id-type="doi">10.7554/eLife.10856</article-id></front><back><sec id="s5" sec-type="supplementary-material"><title>Additional files</title><sec id="s6" sec-type="datasets"><title>Major datasets</title><p>The following datasets were generated:</p><p><related-object content-type="generated-dataset" id="dataro7" source-id="http://www.ncbi.nlm.nih." source-id-type="uri"><ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.">http://www.ncbi.nlm.nih.</ext-link>gov/geo/<x>,</x><comment>Publicly available at NCBI (Accession no: KR021366)</comment></related-object></p><p><related-object content-type="generated-dataset" id="dataro8" source-id="http://www.ncbi.nlm.nih." source-id-type="uri"><ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.">http://www.ncbi.nlm.nih.</ext-link>gov/geo/<x>,</x><comment>Publicly available at NCBI (Accession no: KR021365)</comment></related-object></p><p><related-object content-type="generated-dataset" id="dataro9" source-id="http://www.ncbi.nlm.nih." source-id-type="uri"><year>2016</year><x>,</x><source>PREDICTED: Solanum tuberosum protein NBR1 homolog (LOC102582603), transcript variant X2, mRNA</source><x>,</x><ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.">http://www.ncbi.nlm.nih.</ext-link>gov/nuccore/ XM_006344410<x>,</x><comment>Publicly available at NCBI nucleotide (Accession no: XM_006344410.2)</comment></related-object></p></sec></sec></back></root>',
        OrderedDict([('generated', [OrderedDict([('id', u'dataro7'), ('details', u'Publicly available at NCBI (Accession no: KR021366)'), ('uri', u'https://www.ncbi.nlm.nih.gov/nuccore/976151098/'), ('date', u'2016'), ('title', u'An effector of the Irish potato famine pathogen antagonizes a host autophagy cargo receptor'), ('authors', [{'type': 'group', 'name': 'Dagdas YF'}, {'type': 'group', 'name': 'Belhaj K'}, {'type': 'group', 'name': 'Maqbool A'}, {'type': 'group', 'name': 'Chaparro-Garcia A'}, {'type': 'group', 'name': 'Pandey P'}, {'type': 'group', 'name': 'Petre B'}, {'type': 'group', 'name': 'Tabassum N'}, {'type': 'group', 'name': 'Cruz-Mireles N'}, {'type': 'group', 'name': 'Hughes RK'}, {'type': 'group', 'name': 'Sklenar J'}, {'type': 'group', 'name': 'Win J'}, {'type': 'group', 'name': 'Menke F'}, {'type': 'group', 'name': 'Findlay K'}, {'type': 'group', 'name': 'Banfield MJ'}, {'type': 'group', 'name': 'Kamoun S'}, {'type': 'group', 'name': 'Bozkurt TO'}])]), OrderedDict([('id', u'dataro8'), ('details', u'Publicly available at NCBI (Accession no: KR021365)'), ('uri', u'https://www.ncbi.nlm.nih.gov/nuccore/976151096/'), ('date', u'2015'), ('title', u'An effector of the Irish potato famine pathogen antagonizes a host autophagy cargo receptor'), ('authors', [{'type': 'group', 'name': 'Dagdas YF'}, {'type': 'group', 'name': 'Belhaj K'}, {'type': 'group', 'name': 'Maqbool A'}, {'type': 'group', 'name': 'Chaparro-Garcia A'}, {'type': 'group', 'name': 'Pandey P'}, {'type': 'group', 'name': 'Petre B'}, {'type': 'group', 'name': 'Tabassum N'}, {'type': 'group', 'name': 'Cruz-Mireles N'}, {'type': 'group', 'name': 'Hughes RK'}, {'type': 'group', 'name': 'Sklenar J'}, {'type': 'group', 'name': 'Win J'}, {'type': 'group', 'name': 'Menke F'}, {'type': 'group', 'name': 'Findlay K'}, {'type': 'group', 'name': 'Banfield MJ'}, {'type': 'group', 'name': 'Kamoun S'}, {'type': 'group', 'name': 'Bozkurt TO'}])]), OrderedDict([('id', u'dataro9'), ('date', u'2016'), ('title', u'PREDICTED: Solanum tuberosum protein NBR1 homolog (LOC102582603), transcript variant X2, mRNA'), ('details', u'Publicly available at NCBI nucleotide (Accession no: XM_006344410.2)'), ('uri', u'http://www.ncbi.nlm.nih.'), ('authors', [{'type': 'group', 'name': 'Dagdas YF'}, {'type': 'group', 'name': 'Belhaj K'}, {'type': 'group', 'name': 'Maqbool A'}, {'type': 'group', 'name': 'Chaparro-Garcia A'}, {'type': 'group', 'name': 'Pandey P'}, {'type': 'group', 'name': 'Petre B'}, {'type': 'group', 'name': 'Tabassum N'}, {'type': 'group', 'name': 'Cruz-Mireles N'}, {'type': 'group', 'name': 'Hughes RK'}, {'type': 'group', 'name': 'Sklenar J'}, {'type': 'group', 'name': 'Win J'}, {'type': 'group', 'name': 'Menke F'}, {'type': 'group', 'name': 'Findlay K'}, {'type': 'group', 'name': 'Banfield MJ'}, {'type': 'group', 'name': 'Kamoun S'}, {'type': 'group', 'name': 'Bozkurt TO'}])])])])
         ),

        )
    def test_datasets_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.datasets_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ("elife02304.xml", 2),
        ("elife02935.xml", 6),
    )
    def test_supplementary_files_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.supplementary_files_json(soup)
        self.assertEqual(len(tag_content), expected_len)


    @unpack
    @data(

        # Datasets from 16996 v1 PoA
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec id="s2" sec-type="supplementary-material"><title>Additional Files</title><sec id="s3" sec-type="datasets"><title>Major datasets</title><p/><p>The following datasets were generated:</p><p><related-object content-type="generated-dataset" id="dataro1" source-id="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?token=idyfyieendgpdoz&amp;acc=GSE81059" source-id-type="uri"><collab>Wang IE</collab>, <collab>Lapan SW</collab>, <collab>Scimone ML</collab>, <collab>Reddien PW</collab>, <year>2016</year><x>,</x> <source>Gene expression profiling of planarian heads or cephalic ganglia after inhibition of Hedgehog signaling pathway genes by RNAi</source><x>,</x> <ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?token=idyfyieendgpdoz&amp;acc=GSE81059">http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?token=idyfyieendgpdoz&amp;acc=GSE81059</ext-link><x>,</x> <comment> Publicly available at the NCBI Gene Expression Omnibus (accession no: GSE81059)</comment></related-object></p></sec><supplementary-material><ext-link xlink:href="elife-16996-supp-v1.zip">Download zip</ext-link><p>Any figures and tables for this article are included in the PDF. The zip folder contains additional supplemental files.</p></supplementary-material></sec></back></root>',
        [OrderedDict([('mediaType', 'application/zip'), ('uri', u'elife-16996-supp-v1.zip'), ('filename', u'elife-16996-supp-v1.zip'), ('id', 'SD1-data'), ('title', 'Supplementary file 1.')])]
         ),

        # Datasets from 08477 v1 VoR
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec id="s6" sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD2-data"><object-id pub-id-type="doi">10.7554/eLife.08477.007</object-id><label>Source code 1.</label><caption><p>A Matlab GUI for synchronized video-taping and song stimulation in <xref ref-type="fig" rid="fig3">Figure 3</xref>.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.08477.007">http://dx.doi.org/10.7554/eLife.08477.007</ext-link></p></caption><media mime-subtype="zip" mimetype="application" xlink:href="elife-08477-code1-v1.zip"/></supplementary-material><supplementary-material id="SD3-data"><object-id pub-id-type="doi">10.7554/eLife.08477.011</object-id><label>Source code 2.</label><caption><p>A Matlab GUI for processing and analyzing the calcium-imaging data in <xref ref-type="fig" rid="fig5">Figure 5</xref>.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.08477.011">http://dx.doi.org/10.7554/eLife.08477.011</ext-link></p></caption><media mime-subtype="zip" mimetype="application" xlink:href="elife-08477-code2-v1.zip"/></supplementary-material></sec></back></root>',
        [OrderedDict([('doi', u'10.7554/eLife.08477.007'), ('id', u'SD2-data'), ('label', u'Source code 1.'), ('title', 'A Matlab GUI for synchronized video-taping and song stimulation in <a href="#fig3">Figure 3</a>.'), ('mediaType', u'application/zip'), ('uri', u'elife-08477-code1-v1.zip'), ('filename', u'elife-08477-code1-v1.zip')]), OrderedDict([('doi', u'10.7554/eLife.08477.011'), ('id', u'SD3-data'), ('label', u'Source code 2.'), ('title', 'A Matlab GUI for processing and analyzing the calcium-imaging data in <a href="#fig5">Figure 5</a>.'), ('mediaType', u'application/zip'), ('uri', u'elife-08477-code2-v1.zip'), ('filename', u'elife-08477-code2-v1.zip')])]
         ),


        # 02184 v1, older style PoA has supplementary files directly in the article-meta
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><supplementary-material><ext-link xlink:href="elife-02184-supp-v1.zip">Download zip</ext-link><p>Any figures and tables for this article are included in the PDF. The zip folder contains additional supplemental files.</p></supplementary-material></article-meta></front></root>',
        [OrderedDict([('mediaType', 'application/zip'), ('uri', u'elife-02184-supp-v1.zip'), ('filename', u'elife-02184-supp-v1.zip'), ('id', 'SD1-data'), ('title', 'Supplementary file 1.')])]
         ),

        # 04493 v1 PoA, multiple old style supplementary files
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><body><article-meta><supplementary-material><ext-link xlink:href="elife-04493-supp-v1.zip">Download zip of figure supplements and supplementary file</ext-link><p>Any figures and tables for this article are included in the PDF. The zip folder contains additional supplemental files.</p></supplementary-material><supplementary-material><ext-link xlink:href="Video_2.zip">Download zip of Video 2</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_8.zip">Download zip of Video 8</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_6.zip">Download zip of Video 6</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_11.zip">Download zip of Video 11</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_17.zip">Download zip of Video 17</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_18.zip">Download zip of Video 18</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_7.zip">Download zip of Video 7</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_10.zip">Download zip of Video 10</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_5.zip">Download zip of Video 5</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_13.zip">Download zip of Video 13</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_19.zip">Download zip of Video 19</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_15.zip">Download zip of Video 15</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_21.zip">Download zip of Video 21</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_22.zip">Download zip of Video 22</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_4.zip">Download zip of Video 4</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_20.zip">Download zip of Video 20</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_12.zip">Download zip of Video 12</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_1.zip">Download zip of Video 1</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_16.zip">Download zip of Video 16</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_3.zip">Download zip of Video 3</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_9.zip">Download zip of Video 9</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_14.zip">Download zip of Video 14</ext-link></supplementary-material></article-meta></front></root>',
        [OrderedDict([('mediaType', 'application/zip'), ('uri', u'elife-04493-supp-v1.zip'), ('filename', u'elife-04493-supp-v1.zip'), ('id', 'SD1-data'), ('title', 'Supplementary file 1.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_2.zip'), ('filename', u'Video_2.zip'), ('id', 'SD2-data'), ('title', 'Supplementary file 2.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_8.zip'), ('filename', u'Video_8.zip'), ('id', 'SD3-data'), ('title', 'Supplementary file 3.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_6.zip'), ('filename', u'Video_6.zip'), ('id', 'SD4-data'), ('title', 'Supplementary file 4.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_11.zip'), ('filename', u'Video_11.zip'), ('id', 'SD5-data'), ('title', 'Supplementary file 5.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_17.zip'), ('filename', u'Video_17.zip'), ('id', 'SD6-data'), ('title', 'Supplementary file 6.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_18.zip'), ('filename', u'Video_18.zip'), ('id', 'SD7-data'), ('title', 'Supplementary file 7.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_7.zip'), ('filename', u'Video_7.zip'), ('id', 'SD8-data'), ('title', 'Supplementary file 8.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_10.zip'), ('filename', u'Video_10.zip'), ('id', 'SD9-data'), ('title', 'Supplementary file 9.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_5.zip'), ('filename', u'Video_5.zip'), ('id', 'SD10-data'), ('title', 'Supplementary file 10.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_13.zip'), ('filename', u'Video_13.zip'), ('id', 'SD11-data'), ('title', 'Supplementary file 11.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_19.zip'), ('filename', u'Video_19.zip'), ('id', 'SD12-data'), ('title', 'Supplementary file 12.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_15.zip'), ('filename', u'Video_15.zip'), ('id', 'SD13-data'), ('title', 'Supplementary file 13.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_21.zip'), ('filename', u'Video_21.zip'), ('id', 'SD14-data'), ('title', 'Supplementary file 14.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_22.zip'), ('filename', u'Video_22.zip'), ('id', 'SD15-data'), ('title', 'Supplementary file 15.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_4.zip'), ('filename', u'Video_4.zip'), ('id', 'SD16-data'), ('title', 'Supplementary file 16.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_20.zip'), ('filename', u'Video_20.zip'), ('id', 'SD17-data'), ('title', 'Supplementary file 17.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_12.zip'), ('filename', u'Video_12.zip'), ('id', 'SD18-data'), ('title', 'Supplementary file 18.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_1.zip'), ('filename', u'Video_1.zip'), ('id', 'SD19-data'), ('title', 'Supplementary file 19.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_16.zip'), ('filename', u'Video_16.zip'), ('id', 'SD20-data'), ('title', 'Supplementary file 20.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_3.zip'), ('filename', u'Video_3.zip'), ('id', 'SD21-data'), ('title', 'Supplementary file 21.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_9.zip'), ('filename', u'Video_9.zip'), ('id', 'SD22-data'), ('title', 'Supplementary file 22.')]), OrderedDict([('mediaType', 'application/zip'), ('uri', u'Video_14.zip'), ('filename', u'Video_14.zip'), ('id', 'SD23-data'), ('title', 'Supplementary file 23.')])]
         ),

        # 10110 v1 excerpt, should only extract the supplementary-material from the back matter
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><body><sec><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.10110.004</object-id><label>Figure 1—source data 1.</label><caption><title>Dauer assay data for individual trials in <xref ref-type="fig" rid="fig1">Figure 1</xref>.</title><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.10110.004">http://dx.doi.org/10.7554/eLife.10110.004</ext-link></p></caption><media mime-subtype="xlsx" mimetype="application" xlink:href="elife-10110-fig1-data1-v1.xlsx"/></supplementary-material></p></sec></body><back><sec id="s6" sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD9-data"><object-id pub-id-type="doi">10.7554/eLife.10110.026</object-id><label>Supplementary file 1.</label><caption><p>List of strains used in this work.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.10110.026">http://dx.doi.org/10.7554/eLife.10110.026</ext-link></p></caption><media mime-subtype="docx" mimetype="application" xlink:href="elife-10110-supp1-v1.docx"/></supplementary-material></back></root>',
        [OrderedDict([('doi', u'10.7554/eLife.10110.026'), ('id', u'SD9-data'), ('label', u'Supplementary file 1.'), ('title', u'List of strains used in this work.'), ('mediaType', u'application/docx'), ('uri', u'elife-10110-supp1-v1.docx'), ('filename', u'elife-10110-supp1-v1.docx')])]
         ),

        # 03405 v1, label and no title tag
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.03405.026</object-id><label>Source code 1.</label><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.03405.026">http://dx.doi.org/10.7554/eLife.03405.026</ext-link></p><media mime-subtype="rar" mimetype="application" xlink:href="elife-03405-code1-v1.rar"/></supplementary-material></sec></back></root>',
        [OrderedDict([('doi', u'10.7554/eLife.03405.026'), ('id', u'SD1-data'), ('title', u'Source code 1.'), ('mediaType', u'application/rar'), ('uri', u'elife-03405-code1-v1.rar'), ('filename', u'elife-03405-code1-v1.rar')])]
         ),

        # 00333 v1, mimetype contains a slash so ignore sub-mimetype
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00333.023</object-id><label>Source code 1.</label><caption><p>Simulation script, s_arrest_hemifusion_simulation.m, and accompanying functions, generate_patch.m, s_randomdist.m, isaN2tuplet.m, findFlippedNeighbors.m, for MATLAB version R2012a.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00333.023">http://dx.doi.org/10.7554/eLife.00333.023</ext-link></p></caption><media mime-subtype="zip" mimetype="application/zip" xlink:href="elife-00333-code1-v1.zip"/></supplementary-material></sec></back></root>',
        [OrderedDict([('doi', u'10.7554/eLife.00333.023'), ('id', u'SD1-data'), ('label', u'Source code 1.'), ('title', u'Simulation script, s_arrest_hemifusion_simulation.m, and accompanying functions, generate_patch.m, s_randomdist.m, isaN2tuplet.m, findFlippedNeighbors.m, for MATLAB version R2012a.'), ('mediaType', u'application/zip'), ('uri', u'elife-00333-code1-v1.zip'), ('filename', u'elife-00333-code1-v1.zip')])]
         ),

        )
    def test_supplementary_files_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.supplementary_files_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ("elife02304.xml", 'The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.')
    )
    def test_funding_statement_json_by_file(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.funding_statement_json(soup)
        self.assertEqual(tag_content, expected)

    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"></root>',
         None),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><funding-statement>Funding statement</funding-statement></root>',
         'Funding statement'),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><funding-statement><italic>Special</italic> funding statement</funding-statement></root>',
         '<i>Special</i> funding statement'),

    )
    def test_funding_statement_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.funding_statement_json(soup)
        self.assertEqual(tag_content, expected)


    @unpack
    @data(
        ("elife02304.xml", 3),
        ("elife02935.xml", 16),
    )
    def test_funding_awards_json_by_file(self, filename, expected_len):
        soup = parser.parse_document(sample_xml(filename))
        tag_content = parser.funding_awards_json(soup)
        self.assertEqual(len(tag_content), expected_len)

    @unpack
    @data(
        # 07383 v1 has an institution as the recipient
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><funding-group><award-group id="par-1"><funding-source><institution-wrap><institution>Laura and John Arnold Foundation</institution></institution-wrap></funding-source><principal-award-recipient><institution>Reproducibility Project: Cancer Biology</institution></principal-award-recipient></award-group><funding-statement>The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.</funding-statement></funding-group></front></root>',
         [OrderedDict([('id', u'par-1'), ('source', OrderedDict([('name', [u'Laura and John Arnold Foundation'])])), ('recipients', [OrderedDict([('type', 'group'), ('name', u'Reproducibility Project: Cancer Biology')])])])]
         ),

        # Funding from new kitchen sink
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><funding-group><award-group id="fund1"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100000011</institution-id><institution>Howard Hughes Medical Institute</institution></institution-wrap></funding-source><award-id>F32 GM089018</award-id><principal-award-recipient><name><surname>Harrison</surname><given-names>Melissa</given-names></name></principal-award-recipient></award-group></funding-group></front></root>',
         [OrderedDict([('id', u'fund1'), ('source', OrderedDict([('funderId', u'10.13039/100000011'), ('name', [u'Howard Hughes Medical Institute'])])), ('awardId', u'F32 GM089018'), ('recipients', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Melissa Harrison'), ('index', u'Harrison, Melissa')]))])])])]
         ),

        # 08245 v1 edge case, unusual principal-award-recipient
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><funding-group><award-group id="par-1"><funding-source><institution-wrap><institution>Laura and John Arnold foundation</institution></institution-wrap></funding-source><principal-award-recipient>Reproducibility Project: Cancer Biology</principal-award-recipient></award-group><funding-statement>The Reproducibility Project: Cancer Biology is funded by the Laura and John Arnold Foundation, provided to the Center for Open Science in collaboration with Science Exchange. The funder had no role in study design or the decision to submit the work for publication.</funding-statement></funding-group></front></root>',
         [OrderedDict([('id', u'par-1'), ('source', OrderedDict([('name', [u'Laura and John Arnold foundation'])])), ('recipients', [OrderedDict([('type', 'group'), ('name', u'Reproducibility Project: Cancer Biology')])])])]
         ),

        # 00801 v1 edge case, rewrite funding award
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">00801</article-id><article-id pub-id-type="doi">10.7554/eLife.00801</article-id><funding-group><award-group id="par-1"><funding-source><institution-wrap><institution>Wellcome Trust</institution></institution-wrap></funding-source><award-id>094874/Z/10/Z</award-id><principal-award-recipient><name><surname>Diedrichsen</surname><given-names>Jörn</given-names></name></principal-award-recipient></award-group><award-group id="par-2"><funding-source><institution-wrap><institution>Strategic Award to the Wellcome Trust Centre for Neuroimaging</institution></institution-wrap></funding-source><award-id>091593/Z/10/Z</award-id></award-group><award-group id="par-3"><funding-source><institution-wrap><institution>James S McDonnell Foundation</institution></institution-wrap></funding-source><award-id>Understanding Human Cognition Scholar Award 2012</award-id><principal-award-recipient><name><surname>Diedrichsen</surname><given-names>Jörn</given-names></name></principal-award-recipient></award-group><funding-statement>The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.</funding-statement></funding-group></front></article-meta></root>',
        [OrderedDict([('id', u'par-1'), ('source', OrderedDict([('name', [u'Wellcome Trust'])])), ('awardId', u'094874/Z/10/Z'), ('recipients', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Jörn Diedrichsen'), ('index', u'Diedrichsen, Jörn')]))])])]), OrderedDict([('id', u'par-3'), ('source', OrderedDict([('name', [u'James S McDonnell Foundation'])])), ('awardId', u'Understanding Human Cognition Scholar Award 2012'), ('recipients', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Jörn Diedrichsen'), ('index', u'Diedrichsen, Jörn')]))])])])]
         ),

        # 04250 v1 edge case, rewrite to add funding award recipients
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">04250</article-id><article-id pub-id-type="doi">10.7554/eLife.04250</article-id><funding-group><award-group id="par-1"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100006978</institution-id><institution>University of California Berkeley (University of California, Berkeley)</institution></institution-wrap></funding-source><award-id>AWS in Education grant</award-id><principal-award-recipient><name><surname>Jonas</surname><given-names>Eric</given-names></name></principal-award-recipient></award-group><award-group id="par-2"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100000001</institution-id><institution>National Science Foundation</institution></institution-wrap></funding-source><award-id>NSF CISE Expeditions Award CCF-1139158</award-id></award-group><award-group id="par-3"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100006235</institution-id><institution>Lawrence Berkely National Laboratory</institution></institution-wrap></funding-source><award-id>Award 7076018</award-id></award-group><award-group id="par-4"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100000185</institution-id><institution>Defense Advanced Research Projects Agency</institution></institution-wrap></funding-source><award-id>XData Award FA8750-12-2-0331</award-id></award-group><award-group id="par-5"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100000002</institution-id><institution>National Institutes of Health</institution></institution-wrap></funding-source><award-id>R01NS074044</award-id><principal-award-recipient><name><surname>Kording</surname><given-names>Konrad</given-names></name></principal-award-recipient></award-group><award-group id="par-6"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100000002</institution-id><institution>National Institutes of Health</institution></institution-wrap></funding-source><award-id>R01NS063399</award-id><principal-award-recipient><name><surname>Kording</surname><given-names>Konrad</given-names></name></principal-award-recipient></award-group><funding-statement>The funders had no role in study design, data collection and interpretation, or the decision to submit the work for publication.</funding-statement></funding-group></front></article-meta></root>',
        [OrderedDict([('id', u'par-1'), ('source', OrderedDict([('funderId', u'10.13039/100006978'), ('name', [u'University of California Berkeley (University of California, Berkeley)'])])), ('awardId', u'AWS in Education grant'), ('recipients', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Eric Jonas'), ('index', u'Jonas, Eric')]))])])]), OrderedDict([('id', u'par-2'), ('source', OrderedDict([('funderId', u'10.13039/100000001'), ('name', [u'National Science Foundation'])])), ('awardId', u'NSF CISE Expeditions Award CCF-1139158'), ('recipients', [{'type': 'person', 'name': {'index': 'Jonas, Eric', 'preferred': 'Eric Jonas'}}])]), OrderedDict([('id', u'par-3'), ('source', OrderedDict([('funderId', u'10.13039/100006235'), ('name', [u'Lawrence Berkely National Laboratory'])])), ('awardId', u'Award 7076018'), ('recipients', [{'type': 'person', 'name': {'index': 'Jonas, Eric', 'preferred': 'Eric Jonas'}}])]), OrderedDict([('id', u'par-4'), ('source', OrderedDict([('funderId', u'10.13039/100000185'), ('name', [u'Defense Advanced Research Projects Agency'])])), ('awardId', u'XData Award FA8750-12-2-0331'), ('recipients', [{'type': 'person', 'name': {'index': 'Jonas, Eric', 'preferred': 'Eric Jonas'}}])]), OrderedDict([('id', u'par-5'), ('source', OrderedDict([('funderId', u'10.13039/100000002'), ('name', [u'National Institutes of Health'])])), ('awardId', u'R01NS074044'), ('recipients', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Konrad Kording'), ('index', u'Kording, Konrad')]))])])]), OrderedDict([('id', u'par-6'), ('source', OrderedDict([('funderId', u'10.13039/100000002'), ('name', [u'National Institutes of Health'])])), ('awardId', u'R01NS063399'), ('recipients', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Konrad Kording'), ('index', u'Kording, Konrad')]))])])])]
         ),

        # 06412 v2 edge case, rewrite to add funding award recipients
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">06412</article-id><article-id pub-id-type="doi">10.7554/eLife.06412</article-id><funding-group><award-group id="par-1"><funding-source><institution-wrap><institution-id institution-id-type="FundRef">http://dx.doi.org/10.13039/100000065</institution-id><institution>National Institute of Neurological Disorders and Stroke (NINDS)</institution></institution-wrap></funding-source><award-id>#NS072030</award-id></award-group><funding-statement>The funder had no role in study design, data collection and interpretation, or the decision to submit the work for publication.</funding-statement></funding-group></front></article-meta></root>',
        [OrderedDict([('id', u'par-1'), ('source', OrderedDict([('funderId', u'10.13039/100000065'), ('name', [u'National Institute of Neurological Disorders and Stroke (NINDS)'])])), ('awardId', u'#NS072030'), ('recipients', [{'type': 'person', 'name': {'index': 'Granger, Adam J', 'preferred': 'Adam J Granger'}}])])]
         ),

    )
    def test_funding_awards_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.funding_awards_json(soup)
        self.assertEqual(tag_content, expected)


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
        # 04871 v2, excerpt, remove unwanted sections
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">04871</article-id><article-id pub-id-type="doi">10.7554/eLife.04871</article-id></article-meta><sub-article article-type="article-commentary" id="SA1"><body><sec id="s7"><sec id="s7-1"><title>Editorial note dated 06 November 2014</title><p>Thank you ...</p></sec></sec></body></sub-article><sub-article article-type="reply" id="SA2"><body><sec id="s8"><sec id="s8-1"><title>Authors response dated 19 December 2014 to editorial note dated 06 November 2014</title><p>Substantive comments:</p></sec></sec></body></sub-article></article></root>',
         OrderedDict([('content', [OrderedDict([('type', 'section'), ('id', u's7-1'), ('title', u'Editorial note dated 06 November 2014'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Thank you ...')])])])])])
         ),

        # 10856 v2, excerpt, add missing description via a rewrite
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">10856</article-id><article-id pub-id-type="doi">10.7554/eLife.10856</article-id></article-meta><sub-article article-type="article-commentary" id="SA1"><front-stub><article-id pub-id-type="doi">10.7554/eLife.10856.056</article-id><title-group><article-title>Decision letter</article-title></title-group><body><p>Content</p></body></sub-article></article></root>',
         OrderedDict([('doi', u'10.7554/eLife.10856.056'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content')])]), ('description', [{'text': 'In the interests of transparency, eLife includes the editorial decision letter and accompanying author responses. A lightly edited version of the letter sent to the authors after peer review is shown, indicating the most substantive concerns; minor comments are not usually included.', 'type': 'paragraph'}])])
         ),

        )
    def test_test_decision_letter_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.decision_letter(body_tag)
        self.assertEqual(expected, tag_content)

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
        # 04871 v2, excerpt, remove unwanted sections
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">04871</article-id><article-id pub-id-type="doi">10.7554/eLife.04871</article-id></article-meta><sub-article article-type="article-commentary" id="SA1"><body><sec id="s7"><sec id="s7-1"><title>Editorial note dated 06 November 2014</title><p>Thank you ...</p></sec></sec></body></sub-article><sub-article article-type="reply" id="SA2"><body><sec id="s8"><sec id="s8-1"><title>Authors response dated 19 December 2014 to editorial note dated 06 November 2014</title><p>Substantive comments:</p><p>Another paragraph</p></sec></sec></body></sub-article></article></root>',
         OrderedDict([('content', [OrderedDict([('type', 'section'), ('id', u's8-1'), ('title', u'Authors response dated 19 December 2014 to editorial note dated 06 November 2014'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Substantive comments:')]), OrderedDict([('type', 'paragraph'), ('text', u'Another paragraph')])])])])])
         ),
        )
    def test_test_author_response_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.author_response(body_tag)
        self.assertEqual(expected, tag_content)


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

    @unpack
    @data(
        # very simple body, wrap in a section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><p>Paragraph</p></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', 's0'), ('title', 'Main text'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph')])])])]
         ),

        # normal boxed-text and section, keep these
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><sec id="s1"><p>Paragraph</p><boxed-text><p><bold>Boxed text</bold></p></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's1'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph')]), OrderedDict([('type', 'box'), ('content', [OrderedDict([('type', 'paragraph'), ('text', '<b>Boxed text</b>')])])])])])]
         ),

        # 00301 v1 do not keep boxed-text and warp in section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><boxed-text id="B1"><p><bold>Related research article</bold> Yan H, Zhong G, Xu G, He W, Jing Z, Gao Z, Huang Y, Qi Y, Peng B, Wang H, Fu L, Song M, Chen P, Gao W, Ren B, Sun Y, Cai T, Feng X, Sui J, Li W. 2012. Sodium taurocholate cotransporting polypeptide is a functional receptor for human hepatitis B and D virus. <italic>eLife</italic> <bold>1</bold>:e00049. doi: <ext-link ext-link-type="uri" xlink:href="http://dx.doi.org/10.7554/eLife.00049">10.7554/eLife.00049</ext-link></p><p><bold>Image</bold> HepG2 cells infected with the hepatitis B virus</p><p><inline-graphic xlink:href="elife-00301-inf1-v1"/></p></boxed-text><p>Approximately two billion people ...</p></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', 's0'), ('title', 'Main text'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Approximately two billion people ...')])])])]
         ),

        # 00646 v1 boxed text to keep, and wrap in section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><boxed-text id="B1"><p>This article by Emma Pewsey (pictured) was the winning entry in the <ext-link ext-link-type="uri" xlink:href="http://europepmc.org/ScienceWritingCompetition">Access to Understanding science-writing competition</ext-link> for PhD students and early career post-doctoral researchers organized by Europe PubMed Central in partnership with The British Library. Entrants were asked to explain to a non-scientific audience, in fewer than 800 words, the research reported in a scientific article and why it mattered.</p><p><inline-graphic xlink:href="elife-00646-inf1-v1"/></p></boxed-text><p>Normal healthy bones can be thought of as nature\'s scaffold poles. The tightly packed minerals that make up the cortical bone form a sheath around an inner core of spongy bone and provide the strength that supports our bodies. Throughout our lives, our skeletons are kept strong by the continuous creation of new, fresh bone and the destruction of old, worn out bone. Unfortunately, as we become older, destruction becomes faster than creation, and so the cortical layer thins, causing the bone to weaken and break more easily. In severe cases, this is known as osteoporosis. As a result, simple trips or falls that would only bruise a younger person can cause serious fractures in the elderly. However, half of the elderly patients admitted to hospital with a broken hip do not suffer from osteoporosis.</p></body></article></root>',
        [OrderedDict([('type', 'section'), ('id', 's0'), ('title', 'Main text'), ('content', [OrderedDict([('type', 'paragraph'), ('text', 'This article by Emma Pewsey (pictured) was the winning entry in the <a href="http://europepmc.org/ScienceWritingCompetition">Access to Understanding science-writing competition</a> for PhD students and early career post-doctoral researchers organized by Europe PubMed Central in partnership with The British Library. Entrants were asked to explain to a non-scientific audience, in fewer than 800 words, the research reported in a scientific article and why it mattered.')]), OrderedDict([('type', 'paragraph'), ('text', '<img src="elife-00646-inf1-v1.jpg"/>')]), OrderedDict([('type', 'paragraph'), ('text', u"Normal healthy bones can be thought of as nature's scaffold poles. The tightly packed minerals that make up the cortical bone form a sheath around an inner core of spongy bone and provide the strength that supports our bodies. Throughout our lives, our skeletons are kept strong by the continuous creation of new, fresh bone and the destruction of old, worn out bone. Unfortunately, as we become older, destruction becomes faster than creation, and so the cortical layer thins, causing the bone to weaken and break more easily. In severe cases, this is known as osteoporosis. As a result, simple trips or falls that would only bruise a younger person can cause serious fractures in the elderly. However, half of the elderly patients admitted to hospital with a broken hip do not suffer from osteoporosis.")])])])]
         ),

        # 02945 v1, correction article keep the boxed-text
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><boxed-text><p>Momeni B, Brileya KA, Fields MW, Shou W. 2013. Strong inter-population cooperation leads to partner intermixing in microbial communities. <italic>eLife</italic> <bold>2</bold>:e00230. doi: <ext-link ext-link-type="uri" xlink:href="http://dx.doi.org/10.7554/eLife.00230">http://dx.doi.org/10.7554/eLife.00230</ext-link>. Published 22 January 2013</p></boxed-text><p>In Equation 3, ...</p></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', 's0'), ('title', 'Main text'), ('content', [OrderedDict([('type', 'paragraph'), ('text', 'Momeni B, Brileya KA, Fields MW, Shou W. 2013. Strong inter-population cooperation leads to partner intermixing in microbial communities. <i>eLife</i> <b>2</b>:e00230. doi: <a href="http://dx.doi.org/10.7554/eLife.00230">http://dx.doi.org/10.7554/eLife.00230</a>. Published 22 January 2013')]), OrderedDict([('type', 'paragraph'), ('text', u'In Equation 3, ...')])])])]
         ),

        # 12844 v1, based on, edge case to rewrite unacceptable sections that have no titles
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">12844</article-id><article-id pub-id-type="doi">10.7554/eLife.12844</article-id></article-meta><body><sec id="s1"><p>Paragraph 1</p></sec><sec id="s2"><title>How failure promotes translation</title><p>Paragraph 2</p></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's1'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 1')]), OrderedDict([('type', 'section'), ('id', u's2'), ('title', u'How failure promotes translation'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Paragraph 2')])])])]), ('title', 'Main text')])]
         ),

        # 09977 v2, based on, edge case to remove a specific section with no content
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">09977</article-id><article-id pub-id-type="doi">10.7554/eLife.09977</article-id></article-meta><body><sec id="s4"><title>Keep this section</title><sec id="s4-10"><title>Keep this inner section</title><p>Content</p></sec><sec id="s4-11"><title>Remove this section</title></sec></sec></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's4'), ('title', u'Keep this section'), ('content', [OrderedDict([('type', 'section'), ('id', u's4-10'), ('title', u'Keep this inner section'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content')])])])])])]
         ),

        # 09977 v3, based on, edge case to keep a specific section that does have content
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">09977</article-id><article-id pub-id-type="doi">10.7554/eLife.09977</article-id></article-meta><body><sec id="s4"><title>Keep this section</title><sec id="s4-10"><title>Keep this inner section</title><p>Content</p></sec><sec id="s4-11"><title>Keep this section too</title><p>More content</p></sec></sec></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's4'), ('title', u'Keep this section'), ('content', [OrderedDict([('type', 'section'), ('id', u's4-10'), ('title', u'Keep this inner section'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content')])])]), OrderedDict([('type', 'section'), ('id', u's4-11'), ('title', u'Keep this section too'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])])])]
         ),

        # 05519 v2, based on, edge case to remove an unwanted section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">05519</article-id><article-id pub-id-type="doi">10.7554/eLife.05519</article-id></article-meta><body><sec id="s4"><title>Keep this section</title><sec><sec id="s4-1-1"><title>Keep this inner section</title><p>Content</p></sec><sec id="s4-1-2"><title>Keep this section too</title><p>More content</p></sec></sec></sec></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's4'), ('title', u'Keep this section'), ('content', [OrderedDict([('type', 'section'), ('id', u's4-1-1'), ('title', u'Keep this inner section'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content')])])]), OrderedDict([('type', 'section'), ('id', u's4-1-2'), ('title', u'Keep this section too'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])])])]
         ),

        # 00013 v1, excerpt, add an id to a section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">00013</article-id><article-id pub-id-type="doi">10.7554/eLife.00013</article-id></article-meta><body><sec><title>Introduction</title><sec></body></article></root>',
         [OrderedDict([('type', 'section'), ('title', u'Introduction'), ('content', [OrderedDict([('type', 'section')])]), ('id', 's1')])]
         ),

        # 04232 v2, excerpt, remove an unwanted section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">04232</article-id><article-id pub-id-type="doi">10.7554/eLife.04232</article-id></article-meta><body><sec id="s4" sec-type="materials|methods"><title>Materials and methods</title><sec id="s4-6"><title>Cell separation</title><sec id="s4-6-1"><p><bold>Splenic erythroid cells:</bold></p></sec></sec></sec></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's4'), ('title', u'Materials and methods'), ('content', [OrderedDict([('type', 'section'), ('id', u's4-6'), ('title', u'Cell separation'), ('content', [OrderedDict([('type', 'paragraph'), ('text', '<b>Splenic erythroid cells:</b>')])])])])])]
         ),

        # 07157 v1, add title to a section
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">07157</article-id><article-id pub-id-type="doi">10.7554/eLife.07157</article-id></article-meta><body><sec id="s1"><p>Content</p></sec></body></article></root>',
         [OrderedDict([('type', 'section'), ('id', u's1'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content')])]), ('title', 'Main text')])]
         ),

        # excerpt of 23383 v1 where there is a boxed-text that was formerly stripped away, check it remains
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><p>What is replication? In one sense, the answer is easy. Replication is independently repeating the methodology of a previous study and obtaining the same results. In another sense, the answer is difficult. What does it mean to repeat the methodology? And what qualifies as the &quot;same&quot; results? Now that the first five Replication Studies in the <ext-link ext-link-type="uri" xlink:href="https://osf.io/e81xl/wiki/home/">Reproducibility Project: Cancer Biology</ext-link> have been published (see <xref ref-type="box" rid="B1">Box 1</xref>), it is timely to explore how we might answer these questions. The results of the first set of Replication Studies are mixed, and while it is too early to draw any conclusions, it is clear that assessing reproducibility in cancer biology is going to be as complex as it was in a similar project in psychology (<xref ref-type="bibr" rid="bib9">Open Science Collaboration, 2015</xref>).</p><boxed-text id="B1"><object-id pub-id-type="doi">10.7554/eLife.23383.002</object-id><label>Box 1:</label><caption><title>The first results from the Reproducibility Project: Cancer Biology</title></caption><p>The first five Replication Studies published are listed below, along with a link to the Open Science Framework, where all the methods, data and analyses associated with the replication are publicly accessible. Each Replication Study also has a figure that shows the original result, the result from the replication, and a meta-analysis that combines these results. The meta-analysis indicates the cumulative evidence across both studies for the size of an effect and the uncertainty of the existing evidence.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.23383.002">http://dx.doi.org/10.7554/eLife.23383.002</ext-link></p></boxed-text></body></article></root>',
        [OrderedDict([('type', 'section'), ('id', 's0'), ('title', 'Main text'), ('content', [OrderedDict([('type', 'paragraph'), ('text', 'What is replication? In one sense, the answer is easy. Replication is independently repeating the methodology of a previous study and obtaining the same results. In another sense, the answer is difficult. What does it mean to repeat the methodology? And what qualifies as the "same" results? Now that the first five Replication Studies in the <a href="https://osf.io/e81xl/wiki/home/">Reproducibility Project: Cancer Biology</a> have been published (see <a href="#B1">Box 1</a>), it is timely to explore how we might answer these questions. The results of the first set of Replication Studies are mixed, and while it is too early to draw any conclusions, it is clear that assessing reproducibility in cancer biology is going to be as complex as it was in a similar project in psychology (<a href="#bib9">Open Science Collaboration, 2015</a>).')]), OrderedDict([('type', 'box'), ('doi', u'10.7554/eLife.23383.002'), ('id', u'B1'), ('label', u'Box 1:'), ('title', u'The first results from the Reproducibility Project: Cancer Biology'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'The first five Replication Studies published are listed below, along with a link to the Open Science Framework, where all the methods, data and analyses associated with the replication are publicly accessible. Each Replication Study also has a figure that shows the original result, the result from the replication, and a meta-analysis that combines these results. The meta-analysis indicates the cumulative evidence across both studies for the size of an effect and the uncertainty of the existing evidence.')])])])])])]
         ),

        )
    def test_body_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.body_json(body_tag)
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><sec id="s1"><p><inline-graphic xlink:href="elife-00240-inf1-v1"/></p></sec></body></article></root>',
         None,
         [OrderedDict([('type', 'section'), ('id', u's1'), ('content', [OrderedDict([('type', 'paragraph'), ('text', '<img src="elife-00240-inf1-v1.jpg"/>')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><sec id="s1"><p><inline-graphic xlink:href="elife-00240-inf1-v1"/></p></sec></body></article></root>',
         'https://example.org/',
         [OrderedDict([('type', 'section'), ('id', u's1'), ('content', [OrderedDict([('type', 'paragraph'), ('text', '<img src="https://example.org/elife-00240-inf1-v1.jpg"/>')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><sec id="s2-6-4"><title>Inline graphics</title><p>Here is an example of pulling in an inline graphic <inline-graphic mimetype="image" mime-subtype="jpeg" xlink:href="elife-00666-inf001.jpeg"/>.</p></sec></body></article></root>',
         None,
         [OrderedDict([('type', 'section'), ('id', u's2-6-4'), ('title', u'Inline graphics'), ('content', [OrderedDict([('type', 'paragraph'), ('text', 'Here is an example of pulling in an inline graphic <img src="elife-00666-inf001.jpeg"/>.')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><body><sec id="s2-6-4"><title>Inline graphics</title><p>Here is an example of pulling in an inline graphic <inline-graphic mimetype="image" mime-subtype="jpeg" xlink:href="elife-00666-inf001.jpeg"/>.</p></sec></body></article></root>',
         'https://example.org/',
         [OrderedDict([('type', 'section'), ('id', u's2-6-4'), ('title', u'Inline graphics'), ('content', [OrderedDict([('type', 'paragraph'), ('text', 'Here is an example of pulling in an inline graphic <img src="https://example.org/elife-00666-inf001.jpeg"/>.')])])])]
         ),

        )
    def test_body_json_with_base_url(self, xml_content, base_url, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.body_json(body_tag, base_url=base_url)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # 08647 v1 PoA editor has blank string in the affiliation tags
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group content-type="section"><contrib contrib-type="editor" id="author-11736"><name><surname>Kramer</surname><given-names>Achim</given-names></name><role>Reviewing editor</role><aff><institution> </institution>, <country> </country></aff></contrib></contrib-group></article-meta></front></root>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Achim Kramer'), ('index', u'Kramer, Achim')])), ('role', u'Reviewing editor')])]
         ),

         # 09560 v1 example, has two editors
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group content-type="section"><contrib contrib-type="editor" id="author-4542"><name><surname>Krause</surname><given-names>Johannes</given-names></name><role>Reviewing editor</role><aff><institution>University of Tübingen</institution>, <country>Germany</country></aff></contrib><contrib contrib-type="editor" id="author-37203"><name><surname>Conard</surname><given-names>Nicholas J</given-names></name><role>Reviewing editor</role><aff><institution>University of Tübingen</institution>, <country>Germany</country></aff></contrib></contrib-group></article-meta></front></root>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Johannes Krause'), ('index', u'Krause, Johannes')])), ('role', u'Reviewing editor'), ('affiliations', [OrderedDict([('name', [u'University of T\xfcbingen']), ('address', OrderedDict([('formatted', [u'Germany']), ('components', OrderedDict([('country', u'Germany')]))]))])])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Nicholas J Conard'), ('index', u'Conard, Nicholas J')])), ('role', u'Reviewing editor'), ('affiliations', [OrderedDict([('name', [u'University of T\xfcbingen']), ('address', OrderedDict([('formatted', [u'Germany']), ('components', OrderedDict([('country', u'Germany')]))]))])])])]
        ),

         # 23804 v3 example, has no role tag and is rewritten
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">23804</article-id><article-id pub-id-type="doi">10.7554/eLife.23804</article-id><contrib-group content-type="section"><contrib contrib-type="editor"><name><surname>Shou</surname><given-names>Wenying</given-names></name><aff id="aff4"><institution>Fred Hutchinson Cancer Research Center</institution>, <country>United States</country></aff></contrib></contrib-group></article-meta></front></article></root>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Wenying Shou'), ('index', u'Shou, Wenying')])), ('affiliations', [OrderedDict([('name', [u'Fred Hutchinson Cancer Research Center']), ('address', OrderedDict([('formatted', [u'United States']), ('components', OrderedDict([('country', u'United States')]))]))])]), ('role', u'Reviewing Editor'), ])]
        ),

         # 22028 v1 example, has a country but no institution
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">22028</article-id><article-id pub-id-type="doi">10.7554/eLife.22028</article-id><contrib-group content-type="section"><contrib contrib-type="editor" id="author-56094"><name><surname>Schlesinger</surname><given-names>Larry</given-names></name><role>Reviewing editor</role><aff><institution></institution>, <country>United States</country></aff></contrib></contrib-group></article-meta></front></article></root>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Larry Schlesinger'), ('index', u'Schlesinger, Larry')])), ('role', u'Reviewing Editor')])]
        ),

        )
    def test_editors_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.editors_json(body_tag)
        self.assertEqual(expected, tag_content)


    @data("elife-kitchen-sink.xml", "elife-02833-v2.xml", "elife00351.xml", "elife-00666.xml")
    def test_authors_json(self, filename):
        """note elife00351.xml has email inside an inline aff tag, very irregular"""
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.authors_json(soup), None)

    @unpack
    @data(
        # Author with phone number, 02833 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" id="author-12496"><name><surname>Bender</surname><given-names>Welcome</given-names></name><xref ref-type="aff" rid="aff3"/><xref ref-type="corresp" rid="cor2">*</xref><xref ref-type="other" rid="par-2"/><xref ref-type="fn" rid="con3"/><xref ref-type="fn" rid="conf1"/><xref ref-type="other" rid="dataro1"/></contrib><aff id="aff3"><institution content-type="dept">Department of Biological Chemistry and Molecular Pharmacology</institution>, <institution>Harvard Medical School</institution>, <addr-line><named-content content-type="city">Boston</named-content></addr-line>, <country>United States</country></aff></contrib-group><author-notes><corresp id="cor2"><label>*</label>For correspondence: <phone>(+1) 617-432-1906</phone> (WB)</corresp></author-notes><sec sec-type="additional-information"><title>Additional information</title><fn-group content-type="competing-interest"><title>Competing interests</title><fn fn-type="conflict" id="conf1"><p>The authors declare that no competing interests exist.</p></fn></fn-group><fn-group content-type="author-contribution"><fn fn-type="con" id="con3"><p>WB, Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting and revising the article</p></fn></article-meta></front></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Welcome Bender'), ('index', u'Bender, Welcome')])), ('affiliations', [OrderedDict([('name', [u'Department of Biological Chemistry and Molecular Pharmacology', u'Harvard Medical School']), ('address', OrderedDict([('formatted', [u'Boston', u'United States']), ('components', OrderedDict([('locality', [u'Boston']), ('country', u'United States')]))]))])]), ('phoneNumbers', [u'+16174321906']), ('contribution', u'WB, Conception and design, Acquisition of data, Analysis and interpretation of data, Drafting and revising the article'), ('competingInterests', u'The authors declare that no competing interests exist.')])]
         ),

        # 02935 v1, group authors (collab) but no members of those groups
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author"><collab>ICGC Breast Cancer Group</collab></contrib></contrib-group></article-meta></front></root>',
        [OrderedDict([('type', 'group'), ('name', u'ICGC Breast Cancer Group')])]
        ),

        # 02935 v2, excerpt for group author parsing
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author"><contrib-id contrib-id-type="group-author-key">group-author-id1</contrib-id><collab>ICGC Breast Cancer Group</collab><xref ref-type="aff" rid="aff1"/></contrib><aff id="aff1"><institution content-type="dept">Cancer Genome Project</institution>, <institution>Wellcome Trust Sanger Institute</institution>, <addr-line><named-content content-type="city">Hinxton</named-content></addr-line>, <country>United Kingdom</country></aff></contrib-group><contrib-group><contrib contrib-type="author non-byline"><contrib-id contrib-id-type="group-author-key">group-author-id1</contrib-id><name><surname>Provenzano</surname><given-names>Elena</given-names></name><aff><institution content-type="dept">Cambridge Breast Unit</institution>, <institution>Addenbrooke’s Hospital, Cambridge University Hospital NHS Foundation Trust and NIHR Cambridge Biomedical Research Centre</institution>, <addr-line><named-content content-type="city">Cambridge CB2 2QQ</named-content></addr-line>, <country>UK</country></aff></contrib></contrib-group></article-meta></front></root>',
         [OrderedDict([('type', 'group'), ('name', u'ICGC Breast Cancer Group'), ('affiliations', [OrderedDict([('name', [u'Cancer Genome Project', u'Wellcome Trust Sanger Institute']), ('address', OrderedDict([('formatted', [u'Hinxton', u'United Kingdom']), ('components', OrderedDict([('locality', [u'Hinxton']), ('country', u'United Kingdom')]))]))])]), ('people', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Elena Provenzano'), ('index', u'Provenzano, Elena')])), ('affiliations', [OrderedDict([('name', [u'Cambridge Breast Unit', u'Addenbrooke\u2019s Hospital, Cambridge University Hospital NHS Foundation Trust and NIHR Cambridge Biomedical Research Centre']), ('address', OrderedDict([('formatted', [u'Cambridge CB2 2QQ', u'UK']), ('components', OrderedDict([('locality', [u'Cambridge CB2 2QQ']), ('country', u'UK')]))]))])])])])])]
         ),

        # 09376 v1, excerpt to rewrite an author ORCID
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">09376</article-id><article-id pub-id-type="doi">10.7554/eLife.09376</article-id><contrib-group><contrib contrib-type="author" corresp="yes" id="author-1201"><name><surname>Weis</surname><given-names>Karsten</given-names></name><contrib-id contrib-id-type="orcid">http://orcid.org/000-0001-7224-925X</contrib-id></contrib-group></article-meta></front></article></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Karsten Weis'), ('index', u'Weis, Karsten')])), ('orcid', '0000-0001-7224-925X')])]
         ),

        # 06956 v1, excerpt, add an affiliation name to an author
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><journal-meta><journal-id journal-id-type="publisher-id">elife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">06956</article-id><article-id pub-id-type="doi">10.7554/eLife.06956</article-id><contrib-group><contrib contrib-type="author" corresp="yes" id="author-17393"><name><surname>Alfred</surname><given-names>Jane</given-names></name><x> </x><role>Consultant Editor</role><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0001-6798-0064</contrib-id><xref ref-type="aff" rid="aff1"/></contrib><aff id="aff1"><addr-line><named-content content-type="city">Cambridge</named-content></addr-line>, <country>United Kingdom</country></aff></contrib-group></article-meta></front></article></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Jane Alfred'), ('index', u'Alfred, Jane')])), ('orcid', u'0000-0001-6798-0064'), ('role', u'Consultant Editor'), ('affiliations', [OrderedDict([('address', OrderedDict([('formatted', [u'Cambridge', u'United Kingdom']), ('components', OrderedDict([('locality', [u'Cambridge']), ('country', u'United Kingdom')]))])), ('name', ['Cambridge'])])])])]
         ),

        # 21337 v1, example to pick up the email of corresponding authors from authors notes
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" id="author-10576"><name><surname>Seydoux</surname><given-names>Geraldine</given-names></name><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0001-8257-0493</contrib-id><xref ref-type="aff" rid="aff1">1</xref><xref ref-type="corresp" rid="cor1">*</xref><xref ref-type="other" rid="par-2"/><xref ref-type="fn" rid="conf1"/></contrib><aff id="aff1"><institution content-type="dept">Department of Molecular Biology and Genetics</institution>, <institution>Howard Hughes Medical Institute, Johns Hopkins University School of Medicine</institution>, <addr-line><named-content content-type="city">Baltimore</named-content></addr-line>, <country>United States</country></aff></contrib-group><author-notes><corresp id="cor1"><label>*</label>For correspondence: <email>gseydoux@jhmi.edu</email> (GS);</corresp></author-notes></article-meta></front><back><sec id="s1" sec-type="additional-information"><title>Additional information</title><fn-group content-type="competing-interest"><title>Competing interest</title><fn fn-type="conflict" id="conf1"><p>The authors declare that no competing interests exist.</p></fn></fn-group></sec></back></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Geraldine Seydoux'), ('index', u'Seydoux, Geraldine')])), ('orcid', u'0000-0001-8257-0493'), ('affiliations', [OrderedDict([('name', [u'Department of Molecular Biology and Genetics', u'Howard Hughes Medical Institute, Johns Hopkins University School of Medicine']), ('address', OrderedDict([('formatted', [u'Baltimore', u'United States']), ('components', OrderedDict([('locality', [u'Baltimore']), ('country', u'United States')]))]))])]), ('emailAddresses', [u'gseydoux@jhmi.edu']), ('competingInterests', u'The authors declare that no competing interests exist.')])]
         ),

        # 00007 v1, example with a present address
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" id="author-1399"><name><surname>Schuman</surname><given-names>Meredith C</given-names></name><xref ref-type="aff" rid="aff1"/><xref ref-type="other" rid="par-1"/><xref ref-type="fn" rid="conf2"/><xref ref-type="fn" rid="con1"/><xref ref-type="other" rid="dataro1"/></contrib><contrib contrib-type="author" id="author-1400"><name><surname>Barthel</surname><given-names>Kathleen</given-names></name><xref ref-type="aff" rid="aff1"/><xref ref-type="fn" rid="pa1">†</xref><xref ref-type="other" rid="par-1"/><xref ref-type="fn" rid="conf2"/><xref ref-type="fn" rid="con2"/><xref ref-type="other" rid="dataro1"/></contrib><contrib contrib-type="author" corresp="yes" id="author-1013"><name><surname>Baldwin</surname><given-names>Ian T</given-names></name><xref ref-type="aff" rid="aff1"/><xref ref-type="corresp" rid="cor1">*</xref><xref ref-type="other" rid="par-1"/><xref ref-type="fn" rid="conf1"/><xref ref-type="fn" rid="con3"/><xref ref-type="other" rid="dataro1"/></contrib><aff id="aff1"><institution content-type="dept">Department of Molecular Ecology</institution>, <institution>Max Planck Institute for Chemical Ecology</institution>, <addr-line><named-content content-type="city">Jena</named-content></addr-line>, <country>Germany</country></aff></contrib-group><contrib-group content-type="section"><contrib contrib-type="editor"><name><surname>Weigel</surname><given-names>Detlef</given-names></name><role>Reviewing editor</role><aff><institution>Max Planck Institute for Developmental Biology</institution>, <country>Germany</country></aff></contrib></contrib-group><author-notes><corresp id="cor1"><label>*</label>For correspondence: <email>baldwin@ice.mpg.de</email></corresp><fn fn-type="present-address" id="pa1"><label>†</label><p>Federal Research Center for Cultivated Plants Institute for Breeding Research on Horticultural And Fruit Crops, Julius Kühn Institute, Dresden, Germany</p></fn></author-notes></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Meredith C Schuman'), ('index', u'Schuman, Meredith C')])), ('affiliations', [OrderedDict([('name', [u'Department of Molecular Ecology', u'Max Planck Institute for Chemical Ecology']), ('address', OrderedDict([('formatted', [u'Jena', u'Germany']), ('components', OrderedDict([('locality', [u'Jena']), ('country', u'Germany')]))]))])])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Kathleen Barthel'), ('index', u'Barthel, Kathleen')])), ('affiliations', [OrderedDict([('name', [u'Department of Molecular Ecology', u'Max Planck Institute for Chemical Ecology']), ('address', OrderedDict([('formatted', [u'Jena', u'Germany']), ('components', OrderedDict([('locality', [u'Jena']), ('country', u'Germany')]))]))])]), ('postalAddresses', [OrderedDict([('formatted', [u'Federal Research Center for Cultivated Plants Institute for Breeding Research on Horticultural And Fruit Crops, Julius K\xfchn Institute, Dresden, Germany']), ('components', OrderedDict([('streetAddress', [u'Federal Research Center for Cultivated Plants Institute for Breeding Research on Horticultural And Fruit Crops, Julius K\xfchn Institute, Dresden, Germany'])]))])])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Ian T Baldwin'), ('index', u'Baldwin, Ian T')])), ('affiliations', [OrderedDict([('name', [u'Department of Molecular Ecology', u'Max Planck Institute for Chemical Ecology']), ('address', OrderedDict([('formatted', [u'Jena', u'Germany']), ('components', OrderedDict([('locality', [u'Jena']), ('country', u'Germany')]))]))])]), ('emailAddresses', [u'baldwin@ice.mpg.de'])])]
         ),

        # 00666 kitchen sink (with extra whitespace removed), example to pick up the email of corresponding author
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" equal-contrib="yes" id="author-00001" deceased="yes"><name><surname>Harrison</surname><given-names>Melissa</given-names><suffix>Jnr</suffix></name><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0003-3523-4408</contrib-id><email>m.harrison@elifesciences.org</email><xref ref-type="aff" rid="aff1">1</xref><xref ref-type="fn" rid="equal-contrib1">†</xref><xref ref-type="fn" rid="pa1">§</xref><xref ref-type="fn" rid="fn1">#</xref><xref ref-type="fn" rid="fn2">¶</xref><xref ref-type="other" rid="fund1"/><xref ref-type="fn" rid="conf1"/><xref ref-type="fn" rid="con1"/><xref ref-type="other" rid="dataset1"/><xref ref-type="other" rid="dataset2"/></contrib><aff id="aff1"><label>1</label><institution content-type="dept">Department of Production</institution><institution>eLife</institution><addr-line><named-content content-type="city">Cambridge</named-content></addr-line><country>United Kingdom</country></aff></contrib-group><author-notes><fn fn-type="con" id="equal-contrib1"><label>†</label><p>These authors contributed equally to this work</p></fn><fn fn-type="con" id="equal-contrib2"><label>‡</label><p>These authors also contributed equally to this work</p></fn><fn fn-type="present-address" id="pa1"><label>§</label><p>Department of Wellcome Trust, Sanger Institute, London, United Kingdom</p></fn><fn fn-type="fn" id="fn1"><label>#</label><p>Deceased. (not really!!)</p></fn><fn fn-type="fn" id="fn2"><label>¶</label><p>This footnote text must work in isolation as nothing is processed on the html view to make it "work"</p></fn></author-notes></article-meta></front><back><sec sec-type="additional-information" id="s5"><fn-group content-type="competing-interest"><title>Additional information</title><fn fn-type="COI-statement" id="conf1"><p>Chair of JATS4R</p></fn></fn-group><fn-group content-type="author-contribution"><title>Author contributions</title><fn fn-type="con" id="con1"><p>Completed the XML mapping exercise and wrote this XML example</p></fn></fn-group></sec></back></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Melissa Harrison Jnr'), ('index', u'Harrison, Melissa, Jnr')])), ('orcid', u'0000-0003-3523-4408'), ('deceased', True), ('affiliations', [OrderedDict([('name', [u'Department of Production', u'eLife']), ('address', OrderedDict([('formatted', [u'Cambridge', u'United Kingdom']), ('components', OrderedDict([('locality', [u'Cambridge']), ('country', u'United Kingdom')]))]))])]), ('additionalInformation', [u'This footnote text must work in isolation as nothing is processed on the html view to make it "work"']), ('emailAddresses', [u'm.harrison@elifesciences.org']), ('contribution', u'Completed the XML mapping exercise and wrote this XML example'), ('competingInterests', u'Chair of JATS4R'), ('equalContributionGroups', [1]), ('postalAddresses', [OrderedDict([('formatted', [u'Department of Wellcome Trust, Sanger Institute, London, United Kingdom']), ('components', OrderedDict([('streetAddress', [u'Department of Wellcome Trust, Sanger Institute, London, United Kingdom'])]))])])])]
         ),

        # 09594 v2 example of non-standard footnote fn-type other and id starting with 'fn'
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" deceased="yes" id="author-37132"><name><surname>Eguchi</surname><given-names>Yukiko</given-names></name><xref ref-type="aff" rid="aff6">6</xref><xref ref-type="fn" rid="con7"/><xref ref-type="fn" rid="conf1"/><xref ref-type="fn" rid="fn1">†</xref></contrib><aff id="aff6"><label>6</label><institution content-type="dept">National Institute for Basic Biology</institution>, <institution>National Institutes for Natural Sciences</institution>, <addr-line><named-content content-type="city">Okazaki</named-content></addr-line>, <country>Japan</country></aff><author-notes><fn fn-type="other" id="fn1"><label>†</label><p>Deceased</p></fn></author-notes></article-meta></front><back><sec id="s5" sec-type="additional-information"><title>Additional information</title><fn-group content-type="competing-interest"><title>Competing interests</title><fn fn-type="conflict" id="conf1"><p>The authors declare that no competing interests exist.</p></fn></fn-group><fn-group content-type="author-contribution"><title>Author contributions</title><fn fn-type="con" id="con7"><p>YE, Contributed reagents</p></fn></fn-group></sec></back></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Yukiko Eguchi'), ('index', u'Eguchi, Yukiko')])), ('deceased', True), ('affiliations', [OrderedDict([('name', [u'National Institute for Basic Biology', u'National Institutes for Natural Sciences']), ('address', OrderedDict([('formatted', [u'Okazaki', u'Japan']), ('components', OrderedDict([('locality', [u'Okazaki']), ('country', u'Japan')]))]))])]), ('contribution', u'YE, Contributed reagents'), ('competingInterests', u'The authors declare that no competing interests exist.')])]
         ),

        # 21230 v1 example of author role to parse
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" id="author-68973"><name><surname>Schekman</surname><given-names>Randy</given-names></name><role>Editor-in-Chief</role><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0001-8615-6409</contrib-id><xref ref-type="fn" rid="conf1"/></contrib><contrib contrib-type="author" corresp="yes" id="author-1002"><name><surname>Patterson</surname><given-names>Mark</given-names></name><role>Executive Director</role><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0001-7237-0797</contrib-id><xref ref-type="fn" rid="conf2"/><email>m.patterson@elifesciences.org</email></contrib></contrib-group></article-meta></front><back><fn-group content-type="competing-interest"><title>Competing interests</title><fn fn-type="conflict" id="conf1"><p>Receives funding from the Howard Hughes Medical Institute</p></fn><fn fn-type="conflict" id="conf2"><p>The other author declares that no competing interests exist.</p></fn></fn-group></back></root>',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Randy Schekman'), ('index', u'Schekman, Randy')])), ('orcid', u'0000-0001-8615-6409'), ('role', u'Editor-in-Chief'), ('competingInterests', u'Receives funding from the Howard Hughes Medical Institute')]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Mark Patterson'), ('index', u'Patterson, Mark')])), ('orcid', u'0000-0001-7237-0797'), ('role', u'Executive Director'), ('emailAddresses', [u'm.patterson@elifesciences.org']), ('competingInterests', u'The other author declares that no competing interests exist.')])]
         ),

        # 00351 v1 example of author role to parse
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" id="author-2919"><name><surname>Smith</surname><given-names>Richard</given-names></name><xref ref-type="fn" rid="conf1"/><x> is the </x><role>Chair of Patients Know Best</role><x> and was the </x><role>Editor of the BMJ from 1991 to 2004</role><aff><email>richardswsmith@yahoo.co.uk</email></aff></contrib></contrib-group></article-meta></front><back><fn-group content-type="competing-interest"><fn fn-type="conflict" id="conf1"><label>Competing interest:</label><p>The author reviewed Goldacre\'s first book for the BMJ, and is mentioned briefly in Bad Pharma. Over the years he has had some meals paid for by drug companies and spoken at meetings sponsored by drug companies (as has Goldacre), which is hard to avoid if you speak at all as a doctor. 30 years ago he won an award from the Medical Journalists\' Association that was sponsored by Eli Lilly, and discovered that the company thought it had bought him. Since then he has avoided prizes awarded by drug companies.</p></fn></fn-group></back></root>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Richard Smith'), ('index', u'Smith, Richard')])), ('role', u'Chair of Patients Know Best'), ('emailAddresses', [u'richardswsmith@yahoo.co.uk']), ('competingInterests', "<label>Competing interest:</label>The author reviewed Goldacre's first book for the BMJ, and is mentioned briefly in Bad Pharma. Over the years he has had some meals paid for by drug companies and spoken at meetings sponsored by drug companies (as has Goldacre), which is hard to avoid if you speak at all as a doctor. 30 years ago he won an award from the Medical Journalists' Association that was sponsored by Eli Lilly, and discovered that the company thought it had bought him. Since then he has avoided prizes awarded by drug companies.")])]
         ),

        # 21723 v1 another example of author role
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" id="author-8100"><name><surname>Raman</surname><given-names>Indira M</given-names></name><x>is an</x><role><italic>eLife</italic> Reviewing Editor</role><xref ref-type="aff" rid="aff1"/><xref ref-type="corresp" rid="cor1">*</xref><xref ref-type="fn" rid="conf1"/><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0001-5245-8177</contrib-id><x>and is in the</x><aff id="aff1"><institution content-type="dept">Department of Neurobiology</institution>, <institution>Northwestern University</institution>, <addr-line><named-content content-type="city">Evanston</named-content></addr-line>, <country>United States</country></aff></contrib><aff id="aff1"><institution content-type="dept">Department of Neurobiology</institution>, <institution>Northwestern University</institution>, <addr-line><named-content content-type="city">Evanston</named-content></addr-line>, <country>United States</country></aff></contrib-group><author-notes><corresp id="cor1"><email>i-raman@northwestern.edu</email></corresp></author-notes></article-meta></front><back><fn-group content-type="competing-interest"><title>Competing interests</title><fn fn-type="conflict" id="conf1"><p>The author declares that no competing interests exist.</p></fn></fn-group></back>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Indira M Raman'), ('index', u'Raman, Indira M')])), ('orcid', u'0000-0001-5245-8177'), ('role', '<i>eLife</i> Reviewing Editor'), ('affiliations', [OrderedDict([('name', [u'Department of Neurobiology', u'Northwestern University']), ('address', OrderedDict([('formatted', [u'Evanston', u'United States']), ('components', OrderedDict([('locality', [u'Evanston']), ('country', u'United States')]))]))])]), ('emailAddresses', [u'i-raman@northwestern.edu']), ('competingInterests', u'The author declares that no competing interests exist.')])]
         ),

        # author with a bio based on kitchen sink 00777
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" id="author-1032" equal-contrib="yes"><name><surname>Schekman</surname><given-names>Randy</given-names></name><role>Editor-in-Chief</role><xref ref-type="fn" rid="conf1"/><xref ref-type="aff" rid="aff1"/><xref ref-type="fn" rid="equal-contrib1">&#x2020;</xref><bio><p>Randy Schekman is eLife\'s Editor-In-Chief and a Howard Hughes Medical Institute investigator.</p></bio></contrib><aff id="aff1"><institution content-type="dept">Department of Biology</institution><institution>University of North Carolina</institution><addr-line><named-content content-type="city">Chapel Hill</named-content></addr-line><country>United States</country></aff></contrib-group></article-meta></front><back><fn-group content-type="competing-interest"><title>Competing interests</title><fn fn-type="conflict" id="conf1"><p>The other authors declare that no competing interests exist.</p></fn><fn fn-type="conflict" id="conf2"><p>Alain Laderach works for a drug company.</p></fn></fn-group></back></root>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Randy Schekman'), ('index', u'Schekman, Randy')])), ('role', u'Editor-in-Chief'), ('biography', [OrderedDict([('type', 'paragraph'), ('text', u"Randy Schekman is eLife's Editor-In-Chief and a Howard Hughes Medical Institute investigator.")])]), ('affiliations', [OrderedDict([('name', [u'Department of Biology', u'University of North Carolina']), ('address', OrderedDict([('formatted', [u'Chapel Hill', u'United States']), ('components', OrderedDict([('locality', [u'Chapel Hill']), ('country', u'United States')]))]))])]), ('competingInterests', u'The other authors declare that no competing interests exist.'), ('equalContributionGroups', [1])])]
         ),

         # 02273 v1 example, equal contribution to parse
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" equal-contrib="yes" id="author-8563"><name><surname>Carazo Salas</surname><given-names>Rafael Edgardo</given-names></name><xref ref-type="aff" rid="aff8"/><xref ref-type="fn" rid="equal-contrib">†</xref><xref ref-type="fn" rid="conf1"/><x> is at </x></contrib><contrib contrib-type="author" corresp="yes" equal-contrib="yes" id="author-10552"><name><surname>Csikász-Nagy</surname><given-names>Attila</given-names></name><xref ref-type="aff" rid="aff9"/><xref ref-type="aff" rid="aff10"/><xref ref-type="fn" rid="equal-contrib">†</xref><xref ref-type="fn" rid="conf1"/><x> is in the </x></contrib><aff id="aff8"><institution content-type="dept">the Gurdon Institute and the Genetics Department</institution>, <institution>University of Cambridge</institution>, <addr-line><named-content content-type="city">Cambridge</named-content></addr-line>, <country>United Kingdom</country> <email>cre20@cam.ac.uk</email></aff><aff id="aff9"><institution content-type="dept">Department of Computational Biology</institution>, <institution>Fondazione Edmund Mach</institution>, <addr-line><named-content content-type="city">San Michele all’Adige</named-content></addr-line>, <country>Italy</country> <email>attila.csikasz-nagy@fmach.it</email></aff><aff id="aff10"><institution content-type="dept">the Randall Division of Cell and Molecular Biophysics and Institute of Mathematical and Molecular Biomedicine</institution>, <institution>King’s College London</institution>, <addr-line><named-content content-type="city">London</named-content></addr-line>, <country>United Kingdom</country></aff></contrib-group></article-meta></front>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Rafael Edgardo Carazo Salas'), ('index', u'Carazo Salas, Rafael Edgardo')])), ('affiliations', [OrderedDict([('name', [u'the Gurdon Institute and the Genetics Department', u'University of Cambridge']), ('address', OrderedDict([('formatted', [u'Cambridge', u'United Kingdom']), ('components', OrderedDict([('locality', [u'Cambridge']), ('country', u'United Kingdom')]))]))])]), ('emailAddresses', [u'cre20@cam.ac.uk']), ('equalContributionGroups', [1])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Attila Csik\xe1sz-Nagy'), ('index', u'Csik\xe1sz-Nagy, Attila')])), ('affiliations', [OrderedDict([('name', [u'Department of Computational Biology', u'Fondazione Edmund Mach']), ('address', OrderedDict([('formatted', [u'San Michele all\u2019Adige', u'Italy']), ('components', OrderedDict([('locality', [u'San Michele all\u2019Adige']), ('country', u'Italy')]))]))]), OrderedDict([('name', [u'the Randall Division of Cell and Molecular Biophysics and Institute of Mathematical and Molecular Biomedicine', u'King\u2019s College London']), ('address', OrderedDict([('formatted', [u'London', u'United Kingdom']), ('components', OrderedDict([('locality', [u'London']), ('country', u'United Kingdom')]))]))])]), ('emailAddresses', [u'attila.csikasz-nagy@fmach.it']), ('equalContributionGroups', [1])])]
        ),

         # 09148 v1 example, and author with two email addresses
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes" id="author-35287"><name><surname>Micera</surname><given-names>Silvestro</given-names></name><contrib-id contrib-id-type="orcid">http://orcid.org/0000-0003-4396-8217</contrib-id><xref ref-type="aff" rid="aff1">1</xref><xref ref-type="aff" rid="aff3">3</xref><xref ref-type="aff" rid="aff2">2</xref><xref ref-type="corresp" rid="cor2">*</xref><xref ref-type="other" rid="par-1"/><xref ref-type="other" rid="par-2"/><xref ref-type="other" rid="par-4"/><xref ref-type="other" rid="par-5"/><xref ref-type="other" rid="par-7"/><xref ref-type="other" rid="par-8"/><xref ref-type="fn" rid="con17"/><xref ref-type="fn" rid="conf8"/></contrib><aff id="aff1"><label>1</label><institution content-type="dept">The BioRobotics Institute</institution>, <institution>Scuola Superiore Sant\'Anna</institution>, <addr-line><named-content content-type="city">Pisa</named-content></addr-line>, <country>Italy</country></aff><aff id="aff2"><label>2</label><institution content-type="dept">Bertarelli Foundation Chair in Translational NeuroEngineering, Institute of Bioengineering, School of Engineering</institution>, <institution>École Polytechnique Fédérale de Lausanne</institution>, <addr-line><named-content content-type="city">Lausanne</named-content></addr-line>, <country>Switzerland</country></aff><aff id="aff3"><label>3</label><institution content-type="dept">Center for Neuroprosthetics</institution>, <institution>École Polytechnique Fédérale de Lausanne</institution>, <addr-line><named-content content-type="city">Lausanne</named-content></addr-line>, <country>Switzerland</country></aff></contrib-group><author-notes><corresp id="cor1"><email>calogero.oddo@sssup.it</email> (CMO);</corresp><corresp id="cor2"><email>silvestro.micera@epfl.ch</email>;<email>silvestro.micera@sssup.it</email> (SM)</corresp><fn fn-type="con" id="equal-contrib"><label>†</label><p>These authors contributed equally to this work</p></fn></author-notes></article-meta></front>',
        [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Silvestro Micera'), ('index', u'Micera, Silvestro')])), ('orcid', u'0000-0003-4396-8217'), ('affiliations', [OrderedDict([('name', [u'The BioRobotics Institute', u"Scuola Superiore Sant'Anna"]), ('address', OrderedDict([('formatted', [u'Pisa', u'Italy']), ('components', OrderedDict([('locality', [u'Pisa']), ('country', u'Italy')]))]))]), OrderedDict([('name', [u'Center for Neuroprosthetics', u'\xc9cole Polytechnique F\xe9d\xe9rale de Lausanne']), ('address', OrderedDict([('formatted', [u'Lausanne', u'Switzerland']), ('components', OrderedDict([('locality', [u'Lausanne']), ('country', u'Switzerland')]))]))]), OrderedDict([('name', [u'Bertarelli Foundation Chair in Translational NeuroEngineering, Institute of Bioengineering, School of Engineering', u'\xc9cole Polytechnique F\xe9d\xe9rale de Lausanne']), ('address', OrderedDict([('formatted', [u'Lausanne', u'Switzerland']), ('components', OrderedDict([('locality', [u'Lausanne']), ('country', u'Switzerland')]))]))])]), ('emailAddresses', [u'silvestro.micera@epfl.ch', u'silvestro.micera@sssup.it'])])]
        ),

        # example of new kitchen sink group authors with multiple email addresses, based on 17044 v1
        ('''
<root xmlns:xlink="http://www.w3.org/1999/xlink">
<front>
<article-meta>
<contrib-group>
<contrib contrib-type="author" id="author-28457">
<name>
<surname>Kandela</surname>
<given-names>Irawati</given-names>
</name>
<xref ref-type="aff" rid="aff1">1</xref>
<xref ref-type="fn" rid="con1"/>
<xref ref-type="fn" rid="conf1"/>
</contrib>
<contrib contrib-type="author" id="author-55803">
<name>
<surname>Aird</surname>
<given-names>Fraser</given-names>
</name>
<xref ref-type="aff" rid="aff1">1</xref>
<xref ref-type="fn" rid="con2"/>
<xref ref-type="fn" rid="conf1"/>
</contrib>
<contrib contrib-type="author" corresp="yes">
<email>tim@cos.io</email>
<email>nicole@scienceexchange.com</email>
<collab>Reproducibility Project: Cancer Biology<contrib-group>
<contrib contrib-type="author">
<name>
<surname>Iorns</surname>
<given-names>Elizabeth</given-names>
</name>
<aff>
<institution>Science Exchange</institution>
<addr-line>
<named-content content-type="city">Palo Alto</named-content>
</addr-line>
<country>United States</country>
</aff>
</contrib>
<contrib contrib-type="author">
<name>
<surname>Williams</surname>
<given-names>Stephen R</given-names>
</name>
<aff>
<institution>Center for Open Science</institution>
<addr-line>
<named-content content-type="city">Charlottesville</named-content>
</addr-line>
<country>United States</country>
</aff>
</contrib>
<contrib contrib-type="author">
<name>
<surname>Perfito</surname>
<given-names>Nicole</given-names>
</name>
<aff>
<institution>Science Exchange</institution>
<addr-line>
<named-content content-type="city">Palo Alto</named-content>
</addr-line>
<country>United States</country>
</aff>
</contrib>
<contrib contrib-type="author" id="author-16276">
<name>
<surname>Errington</surname>
<given-names>Timothy M</given-names>
</name>
<contrib-id contrib-id-type="orcid">http://orcid.org/0000-0002-4959-5143</contrib-id>
<aff>
<institution>Center for Open Science</institution>
<addr-line>
<named-content content-type="city">Charlottesville</named-content>
</addr-line>
<country>United States</country>
</aff>
</contrib>
</contrib-group>
</collab>
<xref ref-type="fn" rid="con3"/>
<xref ref-type="fn" rid="conf2"/>
</contrib>
<aff id="aff1">
<label>1</label>
<institution content-type="dept">Developmental Therapeutics Core</institution>
<institution>Northwestern University</institution>
<addr-line>
<named-content content-type="city">Evanston</named-content>
</addr-line>
<country>United States</country>
</aff>
</contrib-group>
<contrib-group content-type="section">
<contrib contrib-type="editor">
<name>
<surname>Dang</surname>
<given-names>Chi Van</given-names>
</name>
<role>Reviewing editor</role>
<aff>
<institution>University of Pennsylvania</institution>
<country>United States</country>
</aff>
</contrib>
</contrib-group></article-meta></front><back><sec id="s4" sec-type="additional-information">
<title>Additional information</title>
<fn-group content-type="competing-interest">
<title>Competing interests</title>
<fn fn-type="COI-statement" id="conf1">
<p>Developmental Therapeutics Core is a Science Exchange associated lab</p>
</fn>
<fn fn-type="COI-statement" id="conf2">
<p>EI, NP: Employed by and hold shares in Science Exchange Inc.</p>
</fn>
</fn-group>
<fn-group content-type="author-contribution">
<title>Author contributions</title>
<fn fn-type="con" id="con1">
<p>Acquisition of data, Drafting or revising the article</p>
</fn>
<fn fn-type="con" id="con2">
<p>Acquisition of data, Drafting or revising the article</p>
</fn>
<fn fn-type="con" id="con3">
<p>Analysis and interpretation of data, Drafting or revising the article</p>
</fn>
</fn-group>
</back>
</root>
''',
         [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Irawati Kandela'), ('index', u'Kandela, Irawati')])), ('affiliations', [OrderedDict([('name', [u'Developmental Therapeutics Core', u'Northwestern University']), ('address', OrderedDict([('formatted', [u'Evanston', u'United States']), ('components', OrderedDict([('locality', [u'Evanston']), ('country', u'United States')]))]))])]), ('contribution', u'Acquisition of data, Drafting or revising the article'), ('competingInterests', u'Developmental Therapeutics Core is a Science Exchange associated lab')]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Fraser Aird'), ('index', u'Aird, Fraser')])), ('affiliations', [OrderedDict([('name', [u'Developmental Therapeutics Core', u'Northwestern University']), ('address', OrderedDict([('formatted', [u'Evanston', u'United States']), ('components', OrderedDict([('locality', [u'Evanston']), ('country', u'United States')]))]))])]), ('contribution', u'Acquisition of data, Drafting or revising the article'), ('competingInterests', u'Developmental Therapeutics Core is a Science Exchange associated lab')]), OrderedDict([('type', 'group'), ('name', u'Reproducibility Project: Cancer Biology'), ('emailAddresses', [u'tim@cos.io', u'nicole@scienceexchange.com']), ('contribution', u'Analysis and interpretation of data, Drafting or revising the article'), ('competingInterests', u'EI, NP: Employed by and hold shares in Science Exchange Inc.'), ('people', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Elizabeth Iorns'), ('index', u'Iorns, Elizabeth')])), ('affiliations', [OrderedDict([('name', [u'Science Exchange']), ('address', OrderedDict([('formatted', [u'Palo Alto', u'United States']), ('components', OrderedDict([('locality', [u'Palo Alto']), ('country', u'United States')]))]))])])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Stephen R Williams'), ('index', u'Williams, Stephen R')])), ('affiliations', [OrderedDict([('name', [u'Center for Open Science']), ('address', OrderedDict([('formatted', [u'Charlottesville', u'United States']), ('components', OrderedDict([('locality', [u'Charlottesville']), ('country', u'United States')]))]))])])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Nicole Perfito'), ('index', u'Perfito, Nicole')])), ('affiliations', [OrderedDict([('name', [u'Science Exchange']), ('address', OrderedDict([('formatted', [u'Palo Alto', u'United States']), ('components', OrderedDict([('locality', [u'Palo Alto']), ('country', u'United States')]))]))])])]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Timothy M Errington'), ('index', u'Errington, Timothy M')])), ('orcid', u'0000-0002-4959-5143'), ('affiliations', [OrderedDict([('name', [u'Center for Open Science']), ('address', OrderedDict([('formatted', [u'Charlottesville', u'United States']), ('components', OrderedDict([('locality', [u'Charlottesville']), ('country', u'United States')]))]))])])])])])]
         ),

        )
    def test_authors_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.authors_json(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # 00855 v1, example of just person authors
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" id="author-1032"><name><surname>Schekman</surname><given-names>Randy</given-names></name><role>Editor-in-Chief</role><xref ref-type="fn" rid="conf1"/></contrib><contrib contrib-type="author" corresp="yes" id="author-1002"><name><surname>Patterson</surname><given-names>Mark</given-names></name><role>Executive Director</role><email>editorial@elifesciences.org</email><xref ref-type="fn" rid="conf1"/></contrib></contrib-group></article-meta></front></root>',
         u'Randy Schekman, Mark Patterson'
         ),

        # 08714 v1, group authors only
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><contrib-group><contrib contrib-type="author" corresp="yes"><contrib-id contrib-id-type="group-author-key">group-author-id1</contrib-id><collab>MalariaGEN Plasmodium falciparum Community Project</collab><xref ref-type="corresp" rid="cor1">*</xref><xref ref-type="corresp" rid="cor2">*</xref><xref ref-type="corresp" rid="cor3">*</xref><xref ref-type="other" rid="par-1"/><xref ref-type="fn" rid="con1"/><xref ref-type="fn" rid="conf1"/></contrib></contrib-group><author-notes><corresp id="cor1"><email>dominic@sanger.ac.uk</email> (DPK);</corresp><corresp id="cor2"><email>ra4@sanger.ac.uk</email> (RA);</corresp><corresp id="cor3"><email>olivo@tropmedres.ac.uk</email> (OM)</corresp></author-notes></article-meta></front></root>',
         u'MalariaGEN Plasmodium falciparum Community Project'
         ),

        )
    def test_author_line_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        article_tag = soup.contents[0]
        tag_content = parser.author_line(article_tag)
        self.assertEqual(expected, tag_content)

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
        ('(+1) 800-555-5555', '+18005555555')
        )
    def test_phone_number_json(self, phone, expected):
        self.assertEqual(parser.phone_number_json(phone), expected)

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

    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00051.xml", "elife-10421-v1.xml", "elife-00666.xml")
    def test_references_json(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.references_json(soup), None)

    @unpack
    @data(
        # Web reference with no title, use the uri from 01892
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib1"><element-citation publication-type="web"><person-group person-group-type="author"><collab>The World Health Organization</collab></person-group><year>2014</year><ext-link ext-link-type="uri" xlink:href="http://www.who.int/topics/dengue/en/">http://www.who.int/topics/dengue/en/</ext-link></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'web'), ('id', u'bib1'), ('date', u'2014'), ('authors', [OrderedDict([('type', 'group'), ('name', 'The World Health Organization')])]), ('title', u'http://www.who.int/topics/dengue/en/'), ('uri', u'http://www.who.int/topics/dengue/en/')])]
         ),

        # Thesis title from 00626, also in converted to unknown because of its comment tag
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib36"><element-citation publication-type="thesis"><person-group person-group-type="author"><name><surname>Schneider</surname><given-names>P</given-names></name></person-group><year>2006</year><comment>PhD Thesis</comment><article-title>Submicroscopic<italic>Plasmodium falciparum</italic>gametocytaemia and the contribution to malaria transmission</article-title><publisher-name>Radboud University Nijmegen Medical Centre</publisher-name><publisher-loc>Nijmegen, The Netherlands</publisher-loc></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'unknown'), ('id', u'bib36'), ('date', u'2006'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Schneider'), ('index', u'Schneider, P')]))])]), ('title', u'Submicroscopic<i>Plasmodium falciparum</i>gametocytaemia and the contribution to malaria transmission'), ('details', 'PhD Thesis, Radboud University Nijmegen Medical Centre, Nijmegen, The Netherlands')])]
         ),

        # fpage value with usual characters from 00170
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib14"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Feng</surname><given-names>J</given-names></name><name><surname>Liu</surname><given-names>T</given-names></name><name><surname>Zhang</surname><given-names>Y</given-names></name></person-group><year>2011</year><article-title>Using MACS to identify peaks from ChIP-Seq data</article-title><source>Curr Protoc Bioinformatics</source><volume>Chapter 2</volume><fpage>Unit 2.14</fpage></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib14'), ('date', u'2011'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Feng'), ('index', u'Feng, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'T Liu'), ('index', u'Liu, T')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Y Zhang'), ('index', u'Zhang, Y')]))])]), ('articleTitle', u'Using MACS to identify peaks from ChIP-Seq data'), ('journal', u'Curr Protoc Bioinformatics'), ('volume', u'Chapter 2'), ('pages', u'Unit 2.14')])]
         ),

        # fpage contains dots, 00569
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib96"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Zerbino</surname><given-names>DR</given-names></name></person-group><year>2010</year><article-title>Using the Velvet de novo assembler for short-read sequencing technologies</article-title><source>Curr Protoc Bioinformatics</source><volume>11</volume><fpage>11.5.1</fpage><lpage>11.5.12</lpage><pub-id pub-id-type="doi">10.1002/0471250953.bi1105s31</pub-id></element-citation></ref></ref-list></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib96'), ('date', u'2010'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'DR Zerbino'), ('index', u'Zerbino, DR')]))])]), ('articleTitle', u'Using the Velvet de novo assembler for short-read sequencing technologies'), ('journal', u'Curr Protoc Bioinformatics'), ('volume', u'11'), ('pages', OrderedDict([('first', u'11.5.1'), ('last', u'11.5.12'), ('range', u'11.5.1\u201311.5.12')])), ('doi', u'10.1002/0471250953.bi1105s31')])]
         ),

        # pages value of in press, 00109
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib32"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Kyoung</surname><given-names>M</given-names></name><name><surname>Zhang</surname><given-names>Y</given-names></name><name><surname>Diao</surname><given-names>J</given-names></name><name><surname>Chu</surname><given-names>S</given-names></name><name><surname>Brunger</surname><given-names>AT</given-names></name></person-group><year>2012</year><article-title>Studying calcium triggered vesicle fusion in a single vesicle content/lipid mixing system</article-title><source>Nature Protocols</source><volume>7</volume><ext-link ext-link-type="uri" xlink:href="http://dx.doi.org/10.1038/nprot.2012.134">10.1038/nprot.2012.134</ext-link><comment>, in press</comment></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib32'), ('date', u'2012'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Kyoung'), ('index', u'Kyoung, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Y Zhang'), ('index', u'Zhang, Y')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Diao'), ('index', u'Diao, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'S Chu'), ('index', u'Chu, S')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AT Brunger'), ('index', u'Brunger, AT')]))])]), ('articleTitle', u'Studying calcium triggered vesicle fusion in a single vesicle content/lipid mixing system'), ('journal', u'Nature Protocols'), ('volume', u'7'), ('pages', 'In press'), ('uri', u'http://dx.doi.org/10.1038/nprot.2012.134')])]
         ),

        # year value of in press, 02535
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib12"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Culumber</surname><given-names>ZW</given-names></name><name><surname>Ochoa</surname><given-names>OM</given-names></name><name><surname>Rosenthal</surname><given-names>GG</given-names></name></person-group><year>in press</year><article-title>Assortative mating and the maintenance of population structure in a natural hybrid zone</article-title><source>American Naturalist</source></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib12'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'ZW Culumber'), ('index', u'Culumber, ZW')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'OM Ochoa'), ('index', u'Ochoa, OM')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'GG Rosenthal'), ('index', u'Rosenthal, GG')]))])]), ('articleTitle', u'Assortative mating and the maintenance of population structure in a natural hybrid zone'), ('journal', u'American Naturalist'), ('pages', 'In press')])]
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
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib41"><element-citation publication-type="clinicaltrial"><person-group person-group-type="sponsor"><collab>Scripps Translational Science Institute</collab></person-group><year iso-8601-date="2015">2015</year><article-title>Scripps Wired for Health Study</article-title><ext-link ext-link-type="uri" xlink:href="https://clinicaltrials.gov/ct2/show/NCT01975428">NCT01975428</ext-link></element-citation></ref></ref-list></root>',
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
         [OrderedDict([('type', u'software'), ('id', u'bib55'), ('date', u'2014'), ('authors', [OrderedDict([('type', 'group'), ('name', u'Schr\xf6dinger, LLC')])]), ('title', u'The PyMOL Molecular Graphics System'), ('source', u'The PyMOL Molecular Graphics System'), ('publisher', OrderedDict([('name', [u'Schrodinger, LLC'])])), ('version', u'Version 1.7.2')])]
         ),

        # data reference with no source, 16800 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib10"><element-citation publication-type="data"><person-group person-group-type="author"><collab>Biosharing.org</collab></person-group><year iso-8601-date="2016">2016</year><data-title>A catalogue of data preservation, management and sharing policies from international funding agencies, regulators and journals</data-title><pub-id pub-id-type="accession" xlink:href="https://biosharing.org/policies">biosharing.org/policies</pub-id></element-citation></ref></ref-list>',
         [OrderedDict([('type', 'unknown'), ('id', u'bib10'), ('date', u'2016'), ('authors', [OrderedDict([('type', 'group'), ('name', u'Biosharing.org')])]), ('title', u'A catalogue of data preservation, management and sharing policies from international funding agencies, regulators and journals'), ('details', u'A catalogue of data preservation, management and sharing policies from international funding agencies, regulators and journals, biosharing.org/policies')])]
         ),

        # reference with an lpage and not fpage still gets pages value set, 13905 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib71"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Yasuda</surname><given-names>R</given-names></name><name><surname>Nimchinsky</surname><given-names>EA</given-names></name><name><surname>Scheuss</surname><given-names>V</given-names></name><name><surname>Pologruto</surname><given-names>TA</given-names></name><name><surname>Oertner</surname><given-names>TG</given-names></name><name><surname>Sabatini</surname><given-names>BL</given-names></name><name><surname>Svoboda</surname><given-names>K</given-names></name></person-group><year iso-8601-date="2004">2004</year><article-title>Imaging calcium concentration dynamics in small neuronal compartments</article-title><source>Science\'s STKE</source><volume>2004</volume><lpage>, pl5.</lpage><pub-id pub-id-type="doi">10.1126/stke.2192004pl5</pub-id></element-citation></ref></ref-list>',
         [OrderedDict([('type', u'journal'), ('id', u'bib71'), ('date', u'2004'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Yasuda'), ('index', u'Yasuda, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'EA Nimchinsky'), ('index', u'Nimchinsky, EA')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'V Scheuss'), ('index', u'Scheuss, V')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TA Pologruto'), ('index', u'Pologruto, TA')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TG Oertner'), ('index', u'Oertner, TG')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'BL Sabatini'), ('index', u'Sabatini, BL')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'K Svoboda'), ('index', u'Svoboda, K')]))])]), ('articleTitle', u'Imaging calcium concentration dynamics in small neuronal compartments'), ('journal', u"Science's STKE"), ('volume', u'2004'), ('pages', u', pl5.'), ('doi', u'10.1126/stke.2192004pl5')])]
         ),

        # Reference with a collab using italic tag, from 05423 v2
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib101"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Wood</surname><given-names>WB</given-names></name><collab>The Community of <italic>C. elegans</italic>Researchers</collab></person-group><year>1988</year><source>The nematode Caenorhabditis elegans</source><publisher-loc>Cold Spring Harbor, New York</publisher-loc><publisher-name>Cold Spring Harbor Laboratory Press</publisher-name></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'book'), ('id', u'bib101'), ('date', u'1988'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'WB Wood'), ('index', u'Wood, WB')]))]), OrderedDict([('type', 'group'), ('name', u'The Community of <i>C. elegans</i>Researchers')])]), ('bookTitle', u'The nematode Caenorhabditis elegans'), ('publisher', OrderedDict([('name', [u'Cold Spring Harbor Laboratory Press']), ('address', OrderedDict([('formatted', [u'Cold Spring Harbor, New York']), ('components', OrderedDict([('locality', [u'Cold Spring Harbor, New York'])]))]))]))])]
         ),

        # Reference with a non-numeric year, from 09215 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib13"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Castro-Alamancos</surname><given-names>MA</given-names></name><name><surname>Connors</surname><given-names>BW</given-names></name></person-group><year iso-8601-date="1996">1996a</year><article-title>Cellular mechanisms of the augmenting response: short-term plasticity in a thalamocortical pathway</article-title><source>Journal of Neuroscience</source><volume>16</volume><fpage>7742</fpage><lpage>7756</lpage></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'journal'), ('id', u'bib13'), ('date', '1996'), ('discriminator', 'a'),('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'MA Castro-Alamancos'), ('index', u'Castro-Alamancos, MA')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'BW Connors'), ('index', u'Connors, BW')]))])]), ('articleTitle', u'Cellular mechanisms of the augmenting response: short-term plasticity in a thalamocortical pathway'), ('journal', u'Journal of Neuroscience'), ('volume', u'16'), ('pages', OrderedDict([('first', u'7742'), ('last', u'7756'), ('range', u'7742\u20137756')]))])]
         ),

        # no year value, 00051, with json rewriting enabled by adding elife XML metadata
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">00051</article-id><article-id pub-id-type="doi">10.7554/eLife.00051</article-id></article-meta><ref-list><ref id="bib25"><element-citation publication-type="web"><person-group person-group-type="author"><name><surname>Jha</surname><given-names>P</given-names></name><name><surname>Nugent</surname><given-names>R</given-names></name><name><surname>Verguet</surname><given-names>S</given-names></name><name><surname>Bloom</surname><given-names>D</given-names></name><name><surname>Hum</surname><given-names>R</given-names></name></person-group><article-title>Chronic Disease Prevention and Control. Copenhagen Consensus 2012 Challenge Paper</article-title><ext-link ext-link-type="uri" xlink:href="http://www.copenhagenconsensus.com/files/Filer/CC12%20papers/Chronic%20Disease.pdf">http://www.copenhagenconsensus.com/files/Filer/CC12%20papers/Chronic%20Disease.pdf</ext-link></element-citation></ref></ref-list></article></root>',
         [OrderedDict([('type', u'web'), ('id', u'bib25'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Jha'), ('index', u'Jha, P')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Nugent'), ('index', u'Nugent, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'S Verguet'), ('index', u'Verguet, S')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'D Bloom'), ('index', u'Bloom, D')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Hum'), ('index', u'Hum, R')]))])]), ('title', u'Chronic Disease Prevention and Control. Copenhagen Consensus 2012 Challenge Paper'), ('uri', u'http://www.copenhagenconsensus.com/files/Filer/CC12%20papers/Chronic%20Disease.pdf'), ('date', '2012')])]
         ),

        # elife 12125 v3 bib11 will get deleted in the JSON rewriting
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">12125</article-id><article-id pub-id-type="doi">10.7554/eLife.12125</article-id></article-meta><ref-list><ref id="bib11"><element-citation publication-type="other"><person-group person-group-type="author"><name><surname>Elazar</surname> <given-names>Assaf</given-names></name><name><surname>Weinstein</surname><given-names>Jonathan</given-names></name><name><surname>Prilusky</surname><given-names>Jaime</given-names></name><name><surname>Fleishman</surname><given-names>Sarel J.</given-names></name></person-group></element-citation></ref></ref-list></article></root>',
         []
         ),

        # 19532 v2 bib27 has a date-in-citation and no year tag, will get rewritten
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">19532</article-id><article-id pub-id-type="doi">10.7554/eLife.19532</article-id></article-meta><ref-list><ref id="bib27"><element-citation publication-type="web"><person-group person-group-type="author"><collab>Nature</collab></person-group><article-title>Challenges in irreproducible research</article-title><source>Nature News and Comment</source><ext-link ext-link-type="uri" xlink:href="http://www.nature.com/news/reproducibility-1.17552">http://www.nature.com/news/reproducibility-1.17552</ext-link><date-in-citation iso-8601-date="2015-12-14">December 14, 2015</date-in-citation></element-citation></ref></ref-list></article></root>',
         [OrderedDict([('type', u'web'), ('id', u'bib27'), ('accessed', u'2015-12-14'), ('authors', [OrderedDict([('type', 'group'), ('name', u'Nature')])]), ('title', u'Challenges in irreproducible research'), ('website', u'Nature News and Comment'), ('uri', u'http://www.nature.com/news/reproducibility-1.17552'), ('date', u'2015')])]
         ),

        # 00666 kitchen sink reference of type patent
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib32"><element-citation publication-type="patent"><person-group person-group-type="inventor"><name><surname>Patterson</surname><given-names>JB</given-names></name><name><surname>Lonergan</surname><given-names>DG</given-names></name><name><surname>Flynn</surname><given-names>GA</given-names></name><name><surname>Qingpeng</surname><given-names>Z</given-names></name><name><surname>Pallai</surname><given-names>PV</given-names></name></person-group><person-group person-group-type="assignee"><collab>Mankind Corp</collab></person-group><year iso-8601-date="2011">2011</year><article-title>IRE-1alpha inhibitors</article-title><source>United States patent</source><patent country="United States">US20100941530</patent><ext-link ext-link-type="uri" xlink:href="http://europepmc.org/patents/PAT/US2011065162">http://europepmc.org/patents/PAT/US2011065162</ext-link></element-citation></ref></ref-list></root>',
         [OrderedDict([('type', u'patent'), ('id', u'bib32'), ('date', u'2011'), ('inventors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'JB Patterson'), ('index', u'Patterson, JB')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'DG Lonergan'), ('index', u'Lonergan, DG')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'GA Flynn'), ('index', u'Flynn, GA')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'Z Qingpeng'), ('index', u'Qingpeng, Z')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'PV Pallai'), ('index', u'Pallai, PV')]))])]), ('assignees', [OrderedDict([('type', 'group'), ('name', u'Mankind Corp')])]), ('title', u'IRE-1alpha inhibitors'), ('patentType', u'United States patent'), ('number', u'US20100941530'), ('country', u'United States'), ('uri', u'http://europepmc.org/patents/PAT/US2011065162')])]
         ),

        # 20352 v2 reference of type patent, with a rewrite of the country value
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">20352</article-id><article-id pub-id-type="doi">10.7554/eLife.20352</article-id></article-meta><ref-list><ref id="bib53"><element-citation publication-type="patent"><person-group person-group-type="inventor"><name><surname>Wang</surname><given-names>L</given-names></name><name><surname>Doherty</surname><given-names>G</given-names></name><name><surname>Wang</surname><given-names>X</given-names></name><name><surname>Tao</surname><given-names>ZF</given-names></name><name><surname>Brunko</surname><given-names>M</given-names></name><name><surname>Kunzer</surname><given-names>AR</given-names></name><name><surname>Wendt</surname><given-names>MD</given-names></name><name><surname>Song</surname><given-names>X</given-names></name><name><surname>Frey</surname><given-names>R</given-names></name><name><surname>Hansen</surname><given-names>TM</given-names></name></person-group><year iso-8601-date="2013">2013</year><article-title>8-carbamoyl-2-(2,3-disubstituted pyrid-6-yl)-1,2,3,4-tetrahydroisoquinoline derivatives as apoptosis - inducing agents for the treatment of cancer and immune and autoimmune diseases</article-title><source>United States Patent</source><patent>WO2013139890 A1</patent></element-citation></ref></ref-list></article></root>',
         [OrderedDict([('type', u'patent'), ('id', u'bib53'), ('date', u'2013'), ('inventors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'L Wang'), ('index', u'Wang, L')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'G Doherty'), ('index', u'Doherty, G')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'X Wang'), ('index', u'Wang, X')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'ZF Tao'), ('index', u'Tao, ZF')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Brunko'), ('index', u'Brunko, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'AR Kunzer'), ('index', u'Kunzer, AR')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'MD Wendt'), ('index', u'Wendt, MD')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'X Song'), ('index', u'Song, X')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Frey'), ('index', u'Frey, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'TM Hansen'), ('index', u'Hansen, TM')]))])]), ('title', u'8-carbamoyl-2-(2,3-disubstituted pyrid-6-yl)-1,2,3,4-tetrahydroisoquinoline derivatives as apoptosis - inducing agents for the treatment of cancer and immune and autoimmune diseases'), ('patentType', u'United States Patent'), ('number', u'WO2013139890 A1'), ('country', u'United States')])]
         ),

        # 20492 v3, report type reference with no publisher-name gets converted to unknown
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib42"><element-citation publication-type="report"><person-group person-group-type="author"><name><surname>World Health Organization</surname></name></person-group><year iso-8601-date="2015">2015</year><source>WHO Glocal Tuberculosis Report 2015</source></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', 'unknown'), ('id', u'bib42'), ('date', u'2015'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'World Health Organization'), ('index', u'World Health Organization')]))])]), ('title', u'WHO Glocal Tuberculosis Report 2015'), ('details', u'WHO Glocal Tuberculosis Report 2015')])]
         ),

        # 15504 v2, reference with a pmid
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib6"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Berni</surname><given-names>J</given-names></name></person-group><year iso-8601-date="2015">2015</year><article-title>Genetic dissection of a regionally differentiated network for exploratory behavior in Drosophila larvae</article-title><source>Current Biology</source><volume><bold>25</bold></volume><fpage>1319</fpage><lpage>1326</lpage><pub-id pub-id-type="doi">10.1016/j.cub.2015.03.023</pub-id><pub-id pub-id-type="pmid">25959962</pub-id></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'journal'), ('id', u'bib6'), ('date', u'2015'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Berni'), ('index', u'Berni, J')]))])]), ('articleTitle', u'Genetic dissection of a regionally differentiated network for exploratory behavior in Drosophila larvae'), ('journal', u'Current Biology'), ('volume', u'25'), ('pages', OrderedDict([('first', u'1319'), ('last', u'1326'), ('range', u'1319\u20131326')])), ('doi', u'10.1016/j.cub.2015.03.023'), ('pmid', 25959962)])]
         ),

        # 15504 v2, reference with an isbn
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib18"><element-citation publication-type="book"><person-group person-group-type="author"><name><surname>Fung</surname><given-names>YC</given-names></name></person-group><year iso-8601-date="2013">2013</year><source>Biomechanics: Mechanical Properties of Living Tissues</source><publisher-loc>New York</publisher-loc><publisher-name>Springer Science &amp; Business Media</publisher-name><pub-id pub-id-type="isbn">978-1-4757-2257-4</pub-id></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'book'), ('id', u'bib18'), ('date', u'2013'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'YC Fung'), ('index', u'Fung, YC')]))])]), ('bookTitle', u'Biomechanics: Mechanical Properties of Living Tissues'), ('publisher', OrderedDict([('name', [u'Springer Science & Business Media']), ('address', OrderedDict([('formatted', [u'New York']), ('components', OrderedDict([('locality', [u'New York'])]))]))])), ('isbn', u'978-1-4757-2257-4')])]
         ),

        # 18296 v3, reference of type preprint
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib78"><element-citation publication-type="preprint"><person-group person-group-type="author"><name><surname>Ochoa</surname><given-names>D</given-names></name><name><surname>Jonikas</surname><given-names>M</given-names></name><name><surname>Lawrence</surname><given-names>RT</given-names></name><name><surname>El Debs</surname><given-names>B</given-names></name><name><surname>Selkrig</surname><given-names>J</given-names></name><name><surname>Typas</surname><given-names>A</given-names></name><name><surname>Villen</surname><given-names>J</given-names></name><name><surname>Santos</surname><given-names>S</given-names></name><name><surname>Beltrao</surname><given-names>P</given-names></name></person-group><year iso-8601-date="2016">2016</year><article-title>An atlas of human kinase regulation</article-title><source>bioRxiv</source><pub-id pub-id-type="doi">10.1101/067900</pub-id></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'preprint'), ('id', u'bib78'), ('date', u'2016'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'D Ochoa'), ('index', u'Ochoa, D')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Jonikas'), ('index', u'Jonikas, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'RT Lawrence'), ('index', u'Lawrence, RT')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'B El Debs'), ('index', u'El Debs, B')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Selkrig'), ('index', u'Selkrig, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'A Typas'), ('index', u'Typas, A')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Villen'), ('index', u'Villen, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'S Santos'), ('index', u'Santos, S')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Beltrao'), ('index', u'Beltrao, P')]))])]), ('articleTitle', u'An atlas of human kinase regulation'), ('source', u'bioRxiv'), ('doi', u'10.1101/067900'), ('uri', u'https://doi.org/10.1101/067900')])]
         ),

        # 16394 v2, reference of type thesis with no publisher, convert to unknown
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib6"><element-citation publication-type="thesis"><person-group person-group-type="author"><name><surname>Berret</surname><given-names>B</given-names></name></person-group><year iso-8601-date="2009">2009</year><article-title>Intégration de la force gravitaire dans la planification motrice et le contrôle des mouvements du bras et du corps</article-title><source>PhD. Thesis</source></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', 'unknown'), ('id', u'bib6'), ('date', u'2009'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'B Berret'), ('index', u'Berret, B')]))])]), ('title', u'Int\xe9gration de la force gravitaire dans la planification motrice et le contr\xf4le des mouvements du bras et du corps'), ('details', u'PhD. Thesis')])]
         ),

        # 09672 v2, reference of type conference-proceeding with no conference
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">20352</article-id><article-id pub-id-type="doi">10.7554/eLife.20352</article-id></article-meta><ref-list><ref id="bib25"><element-citation publication-type="confproc"><person-group person-group-type="author"><collab>RBM</collab></person-group><article-title>Changes to guidance for vector vontrol indicators</article-title><article-title>Meeting Report of the 17th MERG Meeting</article-title><conf-date>15–17th June 2011.</conf-date> <year iso-8601-date="2011">2011</year><conf-loc>New York, USA</conf-loc><uri xlink:href="http://www.rollbackmalaria.org/files/files/partnership/wg/wg_monitoring/docs/17merg_meeting_report.pdf">http://www.rollbackmalaria.org/files/files/partnership/wg/wg_monitoring/docs/17merg_meeting_report.pdf</uri></element-citation></ref></ref-list></article></root>',
        [OrderedDict([('type', 'unknown'), ('id', u'bib25'), ('date', u'2011'), ('authors', [OrderedDict([('type', 'group'), ('name', u'RBM')])]), ('title', u'Changes to guidance for vector vontrol indicators'), ('details', u'15\u201317th June 2011., New York, USA, http://www.rollbackmalaria.org/files/files/partnership/wg/wg_monitoring/docs/17merg_meeting_report.pdf'), ('uri', u'http://www.rollbackmalaria.org/files/files/partnership/wg/wg_monitoring/docs/17merg_meeting_report.pdf')])]
         ),

        # 07460 v1, reference rewriting test, rewrites date and authors
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">07460</article-id><article-id pub-id-type="doi">10.7554/eLife.07460</article-id></article-meta><ref-list><ref id="bib1"><element-citation publication-type="web"><article-title>Fraxinus version1 data analysis</article-title><comment>URL: <ext-link ext-link-type="uri" xlink:href="https://github.com/shyamrallapalli/fraxinus_version1_data_analysis">https://github.com/shyamrallapalli/fraxinus_version1_data_analysis</ext-link></comment></element-citation></ref><ref id="bib2"><element-citation publication-type="web"><article-title>Google api ruby client samples</article-title><comment>URL: <ext-link ext-link-type="uri" xlink:href="https://github.com/google/google-api-ruby-client-samples/tree/master/service_account">https://github.com/google/google-api-ruby-client-samples/tree/master/service_account</ext-link></comment></element-citation></ref></ref-list></article></root>',
        [OrderedDict([('type', u'unknown'), ('id', u'bib1'), ('date', '2013'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', 'Ghanasyam Rallapalli'), ('index', 'Rallapalli, Ghanasyam')]))])]), ('title', u'Fraxinus version1 data analysis'), ('details', u'URL: https://github.com/shyamrallapalli/fraxinus_version1_data_analysis'), ('uri', u'https://github.com/shyamrallapalli/fraxinus_version1_data_analysis')]), OrderedDict([('type', u'unknown'), ('id', u'bib2'), ('date', '2014'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', 'Steven Bazyl'), ('index', 'Bazyl, Steven')]))])]), ('title', u'Google api ruby client samples'), ('details', u'URL: https://github.com/google/google-api-ruby-client-samples/tree/master/service_account'), ('uri', u'https://github.com/google/google-api-ruby-client-samples/tree/master/service_account')])]
         ),

        # 20522 v1, reference rewriting year value in json output
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">20522</article-id><article-id pub-id-type="doi">10.7554/eLife.20522</article-id></article-meta><ref-list><ref id="bib42"><element-citation publication-type="journal"><person-group person-group-type="author"><name><surname>Ellegren</surname><given-names>H</given-names></name><name><surname>Galtier</surname><given-names>N</given-names></name></person-group><year iso-8601-date=" 2016"> 2016</year><article-title>Self fertilization and population variability in the higher plants (vol 91, pg 41, 1957)</article-title><source>Nature Reviews Genetics</source><volume>17</volume><fpage>422</fpage><lpage>433</lpage><pub-id pub-id-type="doi">10.1038/nrg.2016.58</pub-id></element-citation></ref></ref-list></article></root>',
        [OrderedDict([('type', u'journal'), ('id', u'bib42'), ('date', '2016'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'H Ellegren'), ('index', u'Ellegren, H')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'N Galtier'), ('index', u'Galtier, N')]))])]), ('articleTitle', u'Self fertilization and population variability in the higher plants (vol 91, pg 41, 1957)'), ('journal', u'Nature Reviews Genetics'), ('volume', u'17'), ('pages', OrderedDict([('first', u'422'), ('last', u'433'), ('range', u'422\u2013433')])), ('doi', u'10.1038/nrg.2016.58')])]
         ),

        # 09520 v2, reference rewriting conference data
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">09520</article-id><article-id pub-id-type="doi">10.7554/eLife.09520</article-id></article-meta><ref-list><ref id="bib35"><element-citation publication-type="confproc"><person-group person-group-type="author"><collab>World Health Organization</collab></person-group><year iso-8601-date="1971">1971</year><conf-name>WHO Expert Committee on Malaria [meeting held in Geneva from 19 to 30 October 1970]: fifteenth report</conf-name></element-citation></ref></ref-list></article></root>',
        [OrderedDict([('type', 'conference-proceeding'), ('id', u'bib35'), ('date', u'1971'), ('authors', [OrderedDict([('type', 'group'), ('name', u'World Health Organization')])]), ('conference', {'name': ['WHO Expert Committee on Malaria']}), ('articleTitle', 'WHO Expert Committee on Malaria [meeting held in Geneva from 19 to 30 October 1970]: fifteenth report'), ('publisher', {'name': ['World Health Organization'], 'address': {'formatted': ['Geneva'], 'components': {'locality': ['Geneva']}}})])]
         ),

        # from 00666 kitchen sink example, will add a uri to the references json from the doi value
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib3"><element-citation publication-type="preprint"><person-group person-group-type="author"><name><surname>Bloss</surname><given-names>CS</given-names></name><name><surname>Wineinger</surname><given-names>NE</given-names></name><name><surname>Peters</surname><given-names>M</given-names></name><name><surname>Boeldt</surname><given-names>DL</given-names></name><name><surname>Ariniello</surname><given-names>L</given-names></name><name><surname>Kim</surname><given-names>JL</given-names></name><name><surname>Judy Sheard</surname><given-names>J</given-names></name><name><surname>Komatireddy</surname><given-names>R</given-names></name><name><surname>Barrett</surname><given-names>P</given-names></name><name><surname>Topol</surname><given-names>EJ</given-names></name></person-group><year iso-8601-date="2016">2016</year><article-title>A prospective randomized trial examining health care utilization in individuals using multiple smartphone-enabled biosensors</article-title><source>bioRxiv</source><pub-id pub-id-type="doi">https://doi.org/10.1101/029983</pub-id></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'preprint'), ('id', u'bib3'), ('date', u'2016'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'CS Bloss'), ('index', u'Bloss, CS')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'NE Wineinger'), ('index', u'Wineinger, NE')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Peters'), ('index', u'Peters, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'DL Boeldt'), ('index', u'Boeldt, DL')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'L Ariniello'), ('index', u'Ariniello, L')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'JL Kim'), ('index', u'Kim, JL')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Judy Sheard'), ('index', u'Judy Sheard, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Komatireddy'), ('index', u'Komatireddy, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Barrett'), ('index', u'Barrett, P')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'EJ Topol'), ('index', u'Topol, EJ')]))])]), ('articleTitle', u'A prospective randomized trial examining health care utilization in individuals using multiple smartphone-enabled biosensors'), ('source', u'bioRxiv'), ('doi', u'10.1101/029983'), ('uri', u'https://doi.org/10.1101/029983')])]
         ),

        # from 00666 kitchen sink example, reference of type periodical
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib40"><element-citation publication-type="periodical"><person-group person-group-type="author"><name><surname>Schwartz</surname><given-names>J</given-names></name></person-group><string-date><month>September</month> <day>9</day>, <year iso-8601-date="1993-09-09">1993</year></string-date><article-title>Obesity affects economic, social status</article-title><source>The Washington Post</source><fpage>A1</fpage><lpage>A4</lpage></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'periodical'), ('id', u'bib40'), ('date', u'1993-09-09'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Schwartz'), ('index', u'Schwartz, J')]))])]), ('articleTitle', u'Obesity affects economic, social status'), ('periodical', u'The Washington Post'), ('pages', OrderedDict([('first', u'A1'), ('last', u'A4'), ('range', u'A1\u2013A4')]))])]
         ),

         # 00666 kitchen sink example with a version tag
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib2"><element-citation publication-type="software"><person-group person-group-type="author"><name><surname>Bates</surname><given-names>D</given-names></name><name><surname>Maechler</surname><given-names>M</given-names></name><name><surname>Bolker</surname><given-names>B</given-names></name><name><surname>Walker</surname><given-names>S</given-names></name><name><surname>Haubo Bojesen Christensen</surname><given-names>R</given-names></name><name><surname>Singmann</surname><given-names>H</given-names></name><name><surname>Dai</surname><given-names>B</given-names></name><name><surname>Grothendieck</surname><given-names>G</given-names></name><name><surname>Green</surname><given-names>P</given-names></name></person-group><person-group person-group-type="curator"><name><surname>Bolker</surname><given-names>B</given-names></name></person-group><year iso-8601-date="2016">2016</year><data-title>Lme4: Linear Mixed-Effects Models Using Eigen and S4</data-title><source>CRAN</source><ext-link ext-link-type="uri" xlink:href="https://cran.r-project.org/web/packages/lme4/index.html">https://cran.r-project.org/web/packages/lme4/index.html</ext-link><!-- designator attribute added for version - Feb 8 2017 --><version designator="1.1-12">1.1-12</version></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'software'), ('id', u'bib2'), ('date', u'2016'), ('authors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'D Bates'), ('index', u'Bates, D')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'M Maechler'), ('index', u'Maechler, M')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'B Bolker'), ('index', u'Bolker, B')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'S Walker'), ('index', u'Walker, S')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'R Haubo Bojesen Christensen'), ('index', u'Haubo Bojesen Christensen, R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'H Singmann'), ('index', u'Singmann, H')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'B Dai'), ('index', u'Dai, B')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'G Grothendieck'), ('index', u'Grothendieck, G')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'P Green'), ('index', u'Green, P')]))])]), ('curators', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'B Bolker'), ('index', u'Bolker, B')]))])]), ('title', u'Lme4: Linear Mixed-Effects Models Using Eigen and S4'), ('source', u'CRAN'), ('publisher', OrderedDict([('name', [u'CRAN'])])), ('version', u'1.1-12'), ('uri', u'https://cran.r-project.org/web/packages/lme4/index.html')])]
        ),

         # 23193 v2 book references has editors and no authors
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><ref-list><ref id="bib10"><element-citation publication-type="book"><person-group person-group-type="editor"><name><surname>Ekstrom</surname> <given-names>J</given-names></name></person-group><person-group person-group-type="editor"><name><surname>Garrett</surname> <given-names>J. R</given-names></name></person-group><person-group person-group-type="editor"><name><surname>Anderson</surname> <given-names>L. C</given-names></name></person-group><year iso-8601-date="1998">1998</year><edition>1st edn</edition><source>Glandular Mechanisms of Salivary Secretion (Frontiers of Oral Biology , Vol. 10)</source><publisher-loc>Basel</publisher-loc><publisher-name>S Karger</publisher-name><pub-id pub-id-type="isbn">978-3805566308</pub-id></element-citation></ref></ref-list></root>',
        [OrderedDict([('type', u'book'), ('id', u'bib10'), ('date', u'1998'), ('editors', [OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J Ekstrom'), ('index', u'Ekstrom, J')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'J. R Garrett'), ('index', u'Garrett, J. R')]))]), OrderedDict([('type', 'person'), ('name', OrderedDict([('preferred', u'L. C Anderson'), ('index', u'Anderson, L. C')]))])]), ('bookTitle', u'Glandular Mechanisms of Salivary Secretion (Frontiers of Oral Biology , Vol. 10)'), ('publisher', OrderedDict([('name', [u'S Karger']), ('address', OrderedDict([('formatted', [u'Basel']), ('components', OrderedDict([('locality', [u'Basel'])]))]))])), ('edition', u'1st edn'), ('isbn', u'978-3805566308')])]
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
        (None, 0),
        ("<root><italic></italic></root>", 0),
        ("<root><sec><p>Content</p></sec></root>", 1),
    )
    def test_body_blocks(self, xml_content, expected_len):
        if xml_content:
            soup = parser.parse_xml(xml_content)
            body_tag = soup.contents[0].contents[0]
        else:
            body_tag = xml_content
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

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><caption><title>Fig title not in a paragraph</title></caption><graphic xlink:href="elife-00639-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig1'), ('title', u'Fig title not in a paragraph'), ('image', {'alt': '', 'uri': u'elife-00639-fig1-v1.tif'})])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig1-v1.tif'})])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig8" position="float"><label>Reviewers’ figure 1</label><caption/><graphic xlink:href="elife-00723-resp-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig8'), ('title', u'Reviewers\u2019 figure 1'), ('image', {'alt': '', 'uri': u'elife-00723-resp-fig1-v1.tif'})])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig8" position="float"><label>Reviewers’ figure 1</label><caption><p>First sentence</p></caption><graphic xlink:href="elife-00723-resp-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig8'), ('label', u'Reviewers\u2019 figure 1'), ('title', u'First sentence'), ('image', {'alt': '', 'uri': u'elife-00723-resp-fig1-v1.tif'})])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig8" position="float"><label>Reviewers’ figure 1</label><caption><p>First sentence. Second sentence.</p></caption><graphic xlink:href="elife-00723-resp-fig1-v1.tif"/></fig></root>',
         OrderedDict([('type', 'image'), ('id', u'fig8'), ('label', u'Reviewers\u2019 figure 1'), ('title', u'First sentence'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'First sentence. Second sentence.')])]), ('image', {'alt': '', 'uri': u'elife-00723-resp-fig1-v1.tif'})])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/><attrib>PHOTO CREDIT</attrib></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig1-v1.tif'}), ('attribution', [u'PHOTO CREDIT'])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/><permissions><copyright-statement>© 1991, Publisher 1, All Rights Reserved</copyright-statement><copyright-year>1991</copyright-year><copyright-holder>Publisher 1</copyright-holder><license><license-p>The in situ image in panel 3 is reprinted with permission from Figure 2D, <xref ref-type="bibr" rid="bib72">Small et al. (1991)</xref>, <italic>Test &amp; Automated</italic>.</license-p></license></permissions><permissions><copyright-statement>© 1991, Publisher 2, All Rights Reserved</copyright-statement><copyright-year>1991</copyright-year><copyright-holder>Publisher 2</copyright-holder><license><license-p>In situ images in panels 4 and 5 are reprinted with permission from Figure 3A and 3C, <xref ref-type="bibr" rid="bib74">Stanojevic et al. (1991)</xref>, <italic>Journal</italic>.</license-p></license></permissions></fig></root>',
         OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig1-v1.tif'}), ('attribution', ['The in situ image in panel 3 is reprinted with permission from Figure 2D, <a href="#bib72">Small et al. (1991)</a>, <i>Test &amp; Automated</i>.', 'In situ images in panels 4 and 5 are reprinted with permission from Figure 3A and 3C, <a href="#bib74">Stanojevic et al. (1991)</a>, <i>Journal</i>.'])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig3s1" position="float" specific-use="child-fig"><object-id pub-id-type="doi">10.7554/eLife.00666.012</object-id><label>Figure 3—figure supplement 1.</label><caption><title>Title of the figure supplement</title><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00666.013</object-id><label>Figure 3—figure supplement 1—Source data 1.</label><caption><title>Title of the figure supplement source data.</title><p>Legend of the figure supplement source data.</p></caption><media mime-subtype="xlsx" mimetype="application" xlink:href="elife-00666-fig3-figsupp1-data1-v1.xlsx"/></supplementary-material></p></caption><graphic xlink:href="elife-00666-fig3-figsupp1-v1.tiff"/></fig></root>',
        OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.012'), ('id', u'fig3s1'), ('label', u'Figure 3\u2014figure supplement 1.'), ('title', u'Title of the figure supplement'), ('image', {'alt': '', 'uri': u'elife-00666-fig3-figsupp1-v1.tiff'}), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.00666.013'), ('id', u'SD1-data'), ('label', u'Figure 3\u2014figure supplement 1\u2014Source data 1.'), ('title', u'Title of the figure supplement source data.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Legend of the figure supplement source data.')])]), ('mediaType', u'application/xlsx'), ('uri', u'elife-00666-fig3-figsupp1-data1-v1.xlsx'), ('filename', u'elife-00666-fig3-figsupp1-data1-v1.xlsx')])])])
         ),

        ('<root><table-wrap id="tbl2" position="float"><object-id pub-id-type="doi">10.7554/eLife.00013.011</object-id><label>Table 2.</label><caption><p>Caption <xref ref-type="table-fn" rid="tblfn2">*</xref>content</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00013.011">http://dx.doi.org/10.7554/eLife.00013.011</ext-link></p></caption><table frame="hsides" rules="groups"><thead><tr><th>Species</th><th>Reference<xref ref-type="table-fn" rid="tblfn3">*</xref></th></tr></thead><tbody><tr><td><italic>Algoriphagus machipongonensis</italic> PR1</td><td><xref ref-type="bibr" rid="bib3">Alegado et al. (2012)</xref></td></tr></tbody></table><table-wrap-foot><fn id="tblfn1"><label>*</label><p>Footnote 1</p></fn><fn id="tblfn3"><label>§</label><p>CM = conditioned medium;</p></fn><fn><p>MP, Middle Pleistocene.</p></fn><fn id="id_not_used"><p>Footnote parsed with no id</p></fn></table-wrap-foot></table-wrap></root>',
         OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.00013.011'), ('id', u'tbl2'), ('label', u'Table 2.'), ('title', u'Caption <a href="#tblfn2">*</a>content'), ('tables', ['<table><thead><tr><th>Species</th><th>Reference<a href="#tblfn3">*</a></th></tr></thead><tbody><tr><td><i>Algoriphagus machipongonensis</i> PR1</td><td><a href="#bib3">Alegado et al. (2012)</a></td></tr></tbody></table>']), ('footnotes', [OrderedDict([('id', u'tblfn1'), ('label', u'*'), ('text', [OrderedDict([('type', 'paragraph'), ('text', 'Footnote 1')])])]), OrderedDict([('id', u'tblfn3'), ('label', u'\xa7'), ('text', [OrderedDict([('type', 'paragraph'), ('text', 'CM = conditioned medium;')])])]), OrderedDict([('text', [OrderedDict([('type', 'paragraph'), ('text', 'MP, Middle Pleistocene.')])])]), OrderedDict([('text', [OrderedDict([('type', 'paragraph'), ('text', 'Footnote parsed with no id')])])])])])
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
         OrderedDict([('type', 'list'), ('prefix', 'none'), ('items', [[OrderedDict([('type', 'paragraph'), ('text', u'List paragraph one')])], [OrderedDict([('type', 'paragraph'), ('text', u'List paragraph two')])]])])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media mime-subtype="xlsx" mimetype="application" xlink:href="elife00051s001.xlsx"/></root>',
         OrderedDict()
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media content-type="glencoe play-in-place height-250 width-310" id="video1" mime-subtype="avi" mimetype="video" xlink:href="elife00007v001.AVI"><object-id pub-id-type="doi">10.7554/eLife.00007.016</object-id><label>Video 1.</label><caption><p>On-plant assay, plant 7u, WT, June 18, 2011.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00007.016">http://dx.doi.org/10.7554/eLife.00007.016</ext-link></p></caption></media></root>',
        OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.00007.016'), ('id', u'video1'), ('label', u'Video 1.'), ('title', u'On-plant assay, plant 7u, WT, June 18, 2011'), ('uri', u'elife00007v001.AVI')])
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media content-type="glencoe play-in-place height-250 width-310" id="media2" mime-subtype="mov" mimetype="video" xlink:href="elife-00005-media2.mov"><object-id pub-id-type="doi">10.7554/eLife.00005.016</object-id><label>Movie 2.</label><caption><title>3D reconstruction of the human PRC2-AEBP2 complex.</title><p>Docking of crystal structure for EED and RbAp48 WD40s (PDB: 2QXV; 2YB8) are indicated respectively in green and red. Docking of crystal structures of homologue SANT, SET and Zn finger domains (PDB: 3HM5, 3H6L and 2VY5) are shown in blue and purple.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00005.016">http://dx.doi.org/10.7554/eLife.00005.016</ext-link></p><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00005.017</object-id><label>Movie 2—source code 1.</label><caption><p>Overall architecture of the PRC2 complex.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00005.017">http://dx.doi.org/10.7554/eLife.00005.017</ext-link></p></caption><media mime-subtype="wrl" mimetype="application" xlink:href="elife-00005-media2-code1-v1.wrl"/></supplementary-material></p></caption></media>',
        OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.00005.016'), ('id', u'media2'), ('label', u'Movie 2.'), ('title', u'3D reconstruction of the human PRC2-AEBP2 complex.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Docking of crystal structure for EED and RbAp48 WD40s (PDB: 2QXV; 2YB8) are indicated respectively in green and red. Docking of crystal structures of homologue SANT, SET and Zn finger domains (PDB: 3HM5, 3H6L and 2VY5) are shown in blue and purple.')])]), ('uri', u'elife-00005-media2.mov'), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.00005.017'), ('id', u'SD1-data'), ('label', u'Movie 2\u2014source code 1.'), ('title', u'Overall architecture of the PRC2 complex.'), ('mediaType', u'application/wrl'), ('uri', u'elife-00005-media2-code1-v1.wrl'), ('filename', u'elife-00005-media2-code1-v1.wrl')])])])
         ),

        ('<root><disp-quote><p>content</p></disp-quote></root>',
         OrderedDict([('type', 'quote'), ('text', [OrderedDict([('type', 'paragraph'), ('text', u'content')])])])
         ),

        # 00109 v1, figure with a supplementary file that has multiple caption paragraphs
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig2" position="float"><object-id pub-id-type="doi">10.7554/eLife.00109.004</object-id><label>Figure 2.</label><caption><p>Imaging of donor/acceptor interface morphologies by cryo-EM before and after Ca<sup>2+</sup> addition. (<bold>A–F</bold>) Cryo-EM images of mixtures of donor (synaptobrevin and synaptotagmin 1) and acceptor (syntaxin and SNAP-25) vesicles before (<bold>A–C</bold>) and approximately 35 s after (<bold>D–F</bold>) 500 μM Ca<sup>2+</sup> addition (panels B, C, E, and F are close-up views). Vesicles were imaged in the holes of the substrate carbon film, visible as the darker areas in the image, in conditions that clearly show the lipid bilayers (‘Materials and methods’). The particular images shown in this figure were selected out of total of 16 (before Ca<sup>2+</sup> addition) and 21 (after Ca<sup>2+</sup> addition) EM micrographs, respectively, with emphasis on showing point contacts before Ca<sup>2+</sup> addition and extended interfaces after Ca<sup>2+</sup> addition in order to illustrate the variety of these particular states. Arrows indicate interfaces between vesicles that are approximately perpendicular to the direction of the projection (see ‘Materials and methods’ for definitions of all contact and interface types). Large black arrow: point contact (representative close-up in B), small black/white arrow: hemifusion diaphragm (representative close-ups in C and E), and large white arrow: extended close contact (representative close-up in F). Scale bars in A and D are 100 nm, and 20 nm in B, C, E, and F. (<bold>G</bold>) Distribution of vesicle sizes before and after Ca<sup>2+</sup> addition. Vesicle diameters were calculated from all cryo-EM images in both conditions (‘Materials and methods’). (<bold>H</bold>) Bar graph of the percentage of various vesicle interfaces, that is, point contacts, hemifusion diaphragms, and extended close contacts (including a few instances of mixed, i.e., extended/hemifused, interfaces), normalized with respect to the total number of interfaces observed before and after addition of 500 μM Ca<sup>2+</sup>, respectively (‘Materials and methods’). In addition to the changes in the distribution of vesicle interfaces upon Ca<sup>2+</sup> addition, some amount of complete fusion between vesicles occurred as indicated by the shift of the diameter distribution in panel G towards larger values. Source files of all cryo-EM micrographs used for the quantitative analysis are available in the <xref ref-type="supplementary-material" rid="SD1-data">Figure 2—source data 1</xref>.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00109.004">http://dx.doi.org/10.7554/eLife.00109.004</ext-link></p><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00109.005</object-id><label>Figure 2—source data 1.</label><caption><title>Source files for cryo-EM data.</title><p>This zip archive contains all cryo-EM images used for the quantitative analyses shown in Fig. 2. The folder named “No_Ca++” contains the images before Ca++ addition (individual files are named P3_1_**. tif or jpg), and folder named “With_Ca++” contains the images ∼35s after Ca++ addition (individual files are named P3_3_**.tif or jpg).</p><p>Images were collected in low dose conditions at 200 kV acceleration voltage on a CM200 FEG electron microscope (FEI) with a 2k × 2k Gatan UltraScan 1000 camera, at 50,000× magnification and 1.5 mm underfocus.</p><p>The full resolution data were exported as 16 bit “tif” files (2048 × 2048 pixels, scale 0.2 nm/pixel at specimen (the corresponding files have the extension “tif”). Note that these files cannot not be viewed with a standard picture viewer, but must be viewed with a program, such as “ImageJ”. To facilitate easier viewing, the original images were converted to smaller (1024×1024, 0.4 nm/pixel), contrast adjusted jpeg images (8 bits) for easy and immediate visualization with commonly used picture viewers (the corresponding files have the extension “jpg”).</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00109.005">http://dx.doi.org/10.7554/eLife.00109.005</ext-link></p></caption><media mime-subtype="zip" mimetype="application" xlink:href="elife-00109-fig2-data1-v1.zip"/></supplementary-material></p></caption><graphic xlink:href="elife-00109-fig2-v1.tif"/></fig>',
        OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00109.004'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Imaging of donor/acceptor interface morphologies by cryo-EM before and after Ca<sup>2+</sup> addition'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Imaging of donor/acceptor interface morphologies by cryo-EM before and after Ca<sup>2+</sup> addition. (<b>A\u2013F</b>) Cryo-EM images of mixtures of donor (synaptobrevin and synaptotagmin 1) and acceptor (syntaxin and SNAP-25) vesicles before (<b>A\u2013C</b>) and approximately 35 s after (<b>D\u2013F</b>) 500 \u03bcM Ca<sup>2+</sup> addition (panels B, C, E, and F are close-up views). Vesicles were imaged in the holes of the substrate carbon film, visible as the darker areas in the image, in conditions that clearly show the lipid bilayers (\u2018Materials and methods\u2019). The particular images shown in this figure were selected out of total of 16 (before Ca<sup>2+</sup> addition) and 21 (after Ca<sup>2+</sup> addition) EM micrographs, respectively, with emphasis on showing point contacts before Ca<sup>2+</sup> addition and extended interfaces after Ca<sup>2+</sup> addition in order to illustrate the variety of these particular states. Arrows indicate interfaces between vesicles that are approximately perpendicular to the direction of the projection (see \u2018Materials and methods\u2019 for definitions of all contact and interface types). Large black arrow: point contact (representative close-up in B), small black/white arrow: hemifusion diaphragm (representative close-ups in C and E), and large white arrow: extended close contact (representative close-up in F). Scale bars in A and D are 100 nm, and 20 nm in B, C, E, and F. (<b>G</b>) Distribution of vesicle sizes before and after Ca<sup>2+</sup> addition. Vesicle diameters were calculated from all cryo-EM images in both conditions (\u2018Materials and methods\u2019). (<b>H</b>) Bar graph of the percentage of various vesicle interfaces, that is, point contacts, hemifusion diaphragms, and extended close contacts (including a few instances of mixed, i.e., extended/hemifused, interfaces), normalized with respect to the total number of interfaces observed before and after addition of 500 \u03bcM Ca<sup>2+</sup>, respectively (\u2018Materials and methods\u2019). In addition to the changes in the distribution of vesicle interfaces upon Ca<sup>2+</sup> addition, some amount of complete fusion between vesicles occurred as indicated by the shift of the diameter distribution in panel G towards larger values. Source files of all cryo-EM micrographs used for the quantitative analysis are available in the <a href="#SD1-data">Figure 2\u2014source data 1</a>.')])]), ('image', {'alt': '', 'uri': u'elife-00109-fig2-v1.tif'}), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.00109.005'), ('id', u'SD1-data'), ('label', u'Figure 2\u2014source data 1.'), ('title', u'Source files for cryo-EM data.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'This zip archive contains all cryo-EM images used for the quantitative analyses shown in Fig. 2. The folder named \u201cNo_Ca++\u201d contains the images before Ca++ addition (individual files are named P3_1_**. tif or jpg), and folder named \u201cWith_Ca++\u201d contains the images \u223c35s after Ca++ addition (individual files are named P3_3_**.tif or jpg).')]), OrderedDict([('type', 'paragraph'), ('text', u'Images were collected in low dose conditions at 200 kV acceleration voltage on a CM200 FEG electron microscope (FEI) with a 2k \xd7 2k Gatan UltraScan 1000 camera, at 50,000\xd7 magnification and 1.5 mm underfocus.')]), OrderedDict([('type', 'paragraph'), ('text', u'The full resolution data were exported as 16 bit \u201ctif\u201d files (2048 \xd7 2048 pixels, scale 0.2 nm/pixel at specimen (the corresponding files have the extension \u201ctif\u201d). Note that these files cannot not be viewed with a standard picture viewer, but must be viewed with a program, such as \u201cImageJ\u201d. To facilitate easier viewing, the original images were converted to smaller (1024\xd71024, 0.4 nm/pixel), contrast adjusted jpeg images (8 bits) for easy and immediate visualization with commonly used picture viewers (the corresponding files have the extension \u201cjpg\u201d).')])]), ('mediaType', u'application/zip'), ('uri', u'elife-00109-fig2-data1-v1.zip'), ('filename', u'elife-00109-fig2-data1-v1.zip')])])])
         ),

        # code block, based on elife 20352 v2, contains new lines too
        ('''<root><code>&lt;MotifGraft name=&quot;motif_grafting&quot;
      context_structure=&quot;%%context%%&quot;
      motif_structure=&quot;truncatedBH3.pdb&quot;
      RMSD_tolerance=&quot;3.0&quot;
      NC_points_RMSD_tolerance=&quot;2.0&quot;
      clash_score_cutoff=&quot;0&quot;
      clash_test_residue=&quot;ALA&quot;
      hotspots=&quot;9:12:13:14:16:17&quot;
      combinatory_fragment_size_delta=&quot;0:0&quot;
      max_fragment_replacement_size_delta=&quot;0:0&quot;
      full_motif_bb_alignment=&quot;1&quot;
      allow_independent_alignment_per_fragment=&quot;0&quot;
      graft_only_hotspots_by_replacement=&quot;0&quot;
      only_allow_if_N_point_match_aa_identity=&quot;0&quot;
      only_allow_if_C_point_match_aa_identity=&quot;0&quot;
      revert_graft_to_native_sequence=&quot;1&quot;
      allow_repeat_same_graft_output=&quot;1&quot;/&gt;</code></root>''',
        OrderedDict([('type', 'code'), ('code', u'<MotifGraft name="motif_grafting"\n      context_structure="%%context%%"\n      motif_structure="truncatedBH3.pdb"\n      RMSD_tolerance="3.0"\n      NC_points_RMSD_tolerance="2.0"\n      clash_score_cutoff="0"\n      clash_test_residue="ALA"\n      hotspots="9:12:13:14:16:17"\n      combinatory_fragment_size_delta="0:0"\n      max_fragment_replacement_size_delta="0:0"\n      full_motif_bb_alignment="1"\n      allow_independent_alignment_per_fragment="0"\n      graft_only_hotspots_by_replacement="0"\n      only_allow_if_N_point_match_aa_identity="0"\n      only_allow_if_C_point_match_aa_identity="0"\n      revert_graft_to_native_sequence="1"\n      allow_repeat_same_graft_output="1"/>')])
        ),

        # example of a table with a break tag, based on 7141 v1
        ('<root><table-wrap id="tbl3" position="float"><object-id pub-id-type="doi">10.7554/eLife.07141.007</object-id><label>Table 3.</label><caption><p>Residues modeled for each chain of α (1–761) and β (1–375) in all four α<sub>4</sub>β<sub>4</sub> structures. In all four structures, the following regions are disordered and cannot be seen in the experimental electron density: the last ~24 C-terminal residues of α that contain redox active cysteines Cys754 and Cys759 and the ~20 residues of β that connect residue 330 to the ~15 C-terminal residues (360–375) that bind to the α subunit.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.07141.007">http://dx.doi.org/10.7554/eLife.07141.007</ext-link></p></caption><table frame="hsides" rules="groups"><thead><tr><th/><th colspan="8">Chain</th></tr></thead><tbody><tr><td>Structure</td><td>A (α)</td><td>B (α)</td><td>C (α)</td><td>D (α)</td><td>E (β)</td><td>F (β)</td><td>G (β)</td><td>H (β)</td></tr><tr><td>CDP/dATP</td><td>5-736</td><td>4-737</td><td>5-736</td><td>4-737</td><td>1-339, 363-375</td><td>1-341, 360-375</td><td>1-341, 360-375</td><td>1-340,<break/>361-375</td></tr><tr><td>UDP/dATP</td><td>4-737</td><td>4-737</td><td>4-737</td><td>4-736</td><td>1-339,<break/>363-373</td><td>1-341,<break/>360-375</td><td>1-341,<break/>360-375</td><td>1-340,<break/>361-375</td></tr><tr><td>ADP/dGTP</td><td>5-736</td><td>4-736</td><td>4-736</td><td>4-736</td><td>1-339,<break/>363-375</td><td>1-341,<break/>360-375</td><td>1-341,<break/>360-375</td><td>1-340,<break/>361-375</td></tr><tr><td>GDP/TTP</td><td>1-736</td><td>5-736</td><td>4-737</td><td>4-737</td><td>1-339,<break/>363-375</td><td>1-341,<break/>360-375</td><td>1-341,<break/>360-375</td><td>1-344,<break/>361-375</td></tr></tbody></table></table-wrap></root>',
         OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.07141.007'), ('id', u'tbl3'), ('label', u'Table 3.'), ('title', u'Residues modeled for each chain of \u03b1 (1\u2013761) and \u03b2 (1\u2013375) in all four \u03b1<sub>4</sub>\u03b2<sub>4</sub> structures'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Residues modeled for each chain of \u03b1 (1\u2013761) and \u03b2 (1\u2013375) in all four \u03b1<sub>4</sub>\u03b2<sub>4</sub> structures. In all four structures, the following regions are disordered and cannot be seen in the experimental electron density: the last ~24 C-terminal residues of \u03b1 that contain redox active cysteines Cys754 and Cys759 and the ~20 residues of \u03b2 that connect residue 330 to the ~15 C-terminal residues (360\u2013375) that bind to the \u03b1 subunit.')])]), ('tables', [u'<table><thead><tr><th></th><th colspan="8">Chain</th></tr></thead><tbody><tr><td>Structure</td><td>A (\u03b1)</td><td>B (\u03b1)</td><td>C (\u03b1)</td><td>D (\u03b1)</td><td>E (\u03b2)</td><td>F (\u03b2)</td><td>G (\u03b2)</td><td>H (\u03b2)</td></tr><tr><td>CDP/dATP</td><td>5-736</td><td>4-737</td><td>5-736</td><td>4-737</td><td>1-339, 363-375</td><td>1-341, 360-375</td><td>1-341, 360-375</td><td>1-340,<br/>361-375</td></tr><tr><td>UDP/dATP</td><td>4-737</td><td>4-737</td><td>4-737</td><td>4-736</td><td>1-339,<br/>363-373</td><td>1-341,<br/>360-375</td><td>1-341,<br/>360-375</td><td>1-340,<br/>361-375</td></tr><tr><td>ADP/dGTP</td><td>5-736</td><td>4-736</td><td>4-736</td><td>4-736</td><td>1-339,<br/>363-375</td><td>1-341,<br/>360-375</td><td>1-341,<br/>360-375</td><td>1-340,<br/>361-375</td></tr><tr><td>GDP/TTP</td><td>1-736</td><td>5-736</td><td>4-737</td><td>4-737</td><td>1-339,<br/>363-375</td><td>1-341,<br/>360-375</td><td>1-341,<br/>360-375</td><td>1-344,<br/>361-375</td></tr></tbody></table>'])])
        ),

        # example of a figure, based on 00007 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig5" position="float"><object-id pub-id-type="doi">10.7554/eLife.00007.008</object-id><label>Figure 5.</label><caption><p>Predation of <italic>M. sexta</italic> larvae and eggs by <italic>Geocoris</italic> spp. (<bold>A</bold>) Examples of predated <italic>M. sexta</italic> larva (left panel) and egg (right panel). Left, the carcass of a predated first-instar <italic>M. sexta</italic> larva and typical feeding damage from early-instar <italic>Manduca</italic> spp. larvae....</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00007.008">http://dx.doi.org/10.7554/eLife.00007.008</ext-link></p></caption><graphic xlink:href="elife-00007-fig5-v1.tif"/></fig></root>',
        OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00007.008'), ('id', u'fig5'), ('label', u'Figure 5.'), ('title', 'Predation of <i>M. sexta</i> larvae and eggs by <i>Geocoris</i> spp.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', 'Predation of <i>M. sexta</i> larvae and eggs by <i>Geocoris</i> spp. (<b>A</b>) Examples of predated <i>M. sexta</i> larva (left panel) and egg (right panel). Left, the carcass of a predated first-instar <i>M. sexta</i> larva and typical feeding damage from early-instar <i>Manduca</i> spp. larvae....')])]), ('image', {'alt': '', 'uri': u'elife-00007-fig5-v1.tif'})])
        ),

        # example table with a caption and no title needs a title added, based on 05604 v1
        ('<root><table-wrap id="tblu1" position="anchor"><caption><p>PCR primer sets and reaction conditions for genotyping</p></caption><table frame="hsides" rules="groups"><thead><tr><th>Locus</th><th>Primers sequence</th><th>Group</th></tr></thead><tbody><tr><td rowspan="2">MYB29 gene</td><td>myb29-1 RP 5′-TATGTTTGCATCATCTCGTCTTC-3′</td><td rowspan="2">1</td></tr></tbody></table></table-wrap></root>',
        OrderedDict([('type', 'table'), ('id', u'tblu1'), ('title', u'PCR primer sets and reaction conditions for genotyping'), ('tables', [u'<table><thead><tr><th>Locus</th><th>Primers sequence</th><th>Group</th></tr></thead><tbody><tr><td rowspan="2">MYB29 gene</td><td>myb29-1 RP 5\u2032-TATGTTTGCATCATCTCGTCTTC-3\u2032</td><td rowspan="2">1</td></tr></tbody></table>'])])
        ),

        # example video with only the DOI in the caption paragraph, based on 02277 v1
        ('<root><media content-type="glencoe play-in-place height-250 width-310" id="media1" mime-subtype="mp4" mimetype="video" xlink:href="elife-02277-media1.mp4"><object-id pub-id-type="doi">10.7554/eLife.02277.012</object-id><label>Video 1.</label><caption><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.02277.012">http://dx.doi.org/10.7554/eLife.02277.012</ext-link></p></caption></media></root>',
        OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.02277.012'), ('id', u'media1'), ('title', u'Video 1.')])
        ),

        # example animated gif as a video in 00666 kitchen sink
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><media mimetype="video" mime-subtype="gif" id="video2" xlink:href="elife-00666-video2.gif"><object-id pub-id-type="doi">10.7554/eLife.00666.038</object-id><label>Animation 1.</label><caption><title>A demonstration of how to tag an animated gif file to ensure it is autolooped when on the eLife website.</title></caption></media></root>',
        OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.00666.038'), ('id', u'video2'), ('label', u'Animation 1.'), ('title', u'A demonstration of how to tag an animated gif file to ensure it is autolooped when on the eLife website.'), ('uri', u'elife-00666-video2.gif'), ('autoplay', True), ('loop', True)])
        ),

        # example of named-content to be converted to HTML from new kitchen sink 00666
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Here is an example of making text display in different colours: <named-content content-type="author-callout-style-a1">Blue text: #366BFB</named-content>; <named-content content-type="author-callout-style-a2">Purple text: #9C27B0</named-content>; and <named-content content-type="author-callout-style-a3">Red text: #D50000</named-content>.</p></root>',
        OrderedDict([('type', 'paragraph'), ('text', 'Here is an example of making text display in different colours: <span class="author-callout-style-a1">Blue text: #366BFB</span>; <span class="author-callout-style-a2">Purple text: #9C27B0</span>; and <span class="author-callout-style-a3">Red text: #D50000</span>.')])
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
        [OrderedDict([('content', [OrderedDict([('type', 'section'), ('content', [OrderedDict([('type', 'box'), ('title', u'Strange content for test coverage'), ('content', [OrderedDict([('type', 'table'), ('title', u'A label'), ('tables', [])]), OrderedDict([('type', 'image')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024')])])])])])])])]
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
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig1-v1.tif'})])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-v1.tif'}), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-figsupp1-v1.tif'})])])])])])]
         ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><p>This <disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'This')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Caption')])]), ('image', {'alt': '', 'uri': u'elife-01944-fig3-v1.tif'})])])])]
        ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><p>This <disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption <bold>b</bold> <disp-formula id="equ3"><label>(3)</label><mml:math id="m3"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>where m<sub>i</sub> given by: <disp-formula id="equ4"><label>(4)</label><mml:math id="m4"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>More caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'This')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', 'Caption <b>b</b>')]), OrderedDict([('type', 'mathml'), ('id', u'equ3'), ('label', u'(3)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', 'where m<sub>i</sub> given by:')]), OrderedDict([('type', 'mathml'), ('id', u'equ4'), ('label', u'(4)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'More caption')])]), ('image', {'alt': '', 'uri': u'elife-01944-fig3-v1.tif'})])])])]
        ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><p>This <xref ref-type="fig" rid="fig3">Figure 3A</xref> test<disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption <bold>b</bold> <disp-formula id="equ3"><label>(3)</label><mml:math id="m3"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>where m<sub>i</sub> given by: <disp-formula id="equ4"><label>(4)</label><mml:math id="m4"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>More caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', 'This <a href="#fig3">Figure 3A</a> test')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', 'Caption <b>b</b>')]), OrderedDict([('type', 'mathml'), ('id', u'equ3'), ('label', u'(3)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', 'where m<sub>i</sub> given by:')]), OrderedDict([('type', 'mathml'), ('id', u'equ4'), ('label', u'(4)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'More caption')])]), ('image', {'alt': '', 'uri': u'elife-01944-fig3-v1.tif'})])])])]
        ),

        ('<root xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink><p><bold>This</bold> is <xref ref-type="fig" rid="fig3">Figure 3A</xref> test<disp-formula id="equ2"><label>(2)</label><mml:math id="m2"><mml:mrow></mml:mrow></mml:math></disp-formula>was also<fig id="fig3" position="float"><object-id pub-id-type="doi">10.7554/eLife.01944.005</object-id><label>Figure 3.</label><caption><title>Title</title><p>Caption <bold>b</bold> <disp-formula id="equ3"><label>(3)</label><mml:math id="m3"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>where m<sub>i</sub> given by: <disp-formula id="equ4"><label>(4)</label><mml:math id="m4"><mml:mrow></mml:mrow></mml:math></disp-formula></p><p>More caption</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.01944.005">http://dx.doi.org/10.7554/eLife.01944.005</ext-link></p></caption><graphic xlink:href="elife-01944-fig3-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', '<b>This</b> is <a href="#fig3">Figure 3A</a> test')]), OrderedDict([('type', 'mathml'), ('id', u'equ2'), ('label', u'(2)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'was also')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.01944.005'), ('id', u'fig3'), ('label', u'Figure 3.'), ('title', u'Title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', 'Caption <b>b</b>')]), OrderedDict([('type', 'mathml'), ('id', u'equ3'), ('label', u'(3)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', 'where m<sub>i</sub> given by:')]), OrderedDict([('type', 'mathml'), ('id', u'equ4'), ('label', u'(4)'), ('mathml', '<math><mrow></mrow></math>')]), OrderedDict([('type', 'paragraph'), ('text', u'More caption')])]), ('image', {'alt': '', 'uri': u'elife-01944-fig3-v1.tif'})])])])]
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink><p><bold>This</bold> <fig id="fig7" position="float"><graphic xlink:href="elife-00012-resp-fig2-v1.tif"/></fig></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', '<b>This</b>')]), OrderedDict([('type', 'image'), ('id', u'fig7'), ('image', {'alt': '', 'uri': u'elife-00012-resp-fig2-v1.tif'})])])])]
         ),

        ('<root><disp-quote><p>content</p></disp-quote></root>',
         [OrderedDict([('content', [OrderedDict([('type', 'quote'), ('text', [OrderedDict([('type', 'paragraph'), ('text', u'content')])])])])])]
         ),

        # Boxed text with no title tag uses the first sentence of the caption paragraph, 00288 v1
        ('<root><boxed-text id="box1"><object-id pub-id-type="doi">10.7554/eLife.00288.004</object-id><label>Box 1.</label><caption><p>Cohort A</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00288.004">http://dx.doi.org/10.7554/eLife.00288.004</ext-link></p></caption><p>Cohort A included three subjects who were seen within 12 hr of HSV-2 recurrence, and who collected genital swabs every 5 min for 4 hr. This experiment assessed whether there were alterations in viral load related to the PCR assay or collection technique. Only small changes occurred during 5-min intervals (<xref ref-type="fig" rid="fig1">Figure 1A</xref>, <xref ref-type="fig" rid="fig1s1">Figure 1—figure supplement 1A,B</xref>, <xref ref-type="supplement-material" rid="SD1-data">Figure 1—source data 1</xref>). The mean absolute value of viral DNA copy difference between successive swabs was 0.20, 0.28, and 0.34 log<sub>10</sub> genomic copies in the three participants, and generally increased with time between swabs (<xref ref-type="fig" rid="fig1">Figure 1B</xref>, <xref ref-type="fig" rid="fig1s1">Figure 1—figure supplement 1C</xref>). The mean difference in HSV DNA copies between swabs correlated tightly with time between swabs in two participants (<xref ref-type="fig" rid="fig1">Figure 1C</xref>, <xref ref-type="fig" rid="fig1s1">Figure 1—figure supplement 1D</xref>), with virtually no difference in viral quantity between swabs separated by 5-min intervals in all three subjects (<xref ref-type="fig" rid="fig1">Figure 1C</xref>, <xref ref-type="fig" rid="fig1s1">Figure 1—figure supplement 1D</xref>). Two episodes had negative mean differences in viral quantity with increasing time between swabs (<xref ref-type="fig" rid="fig1">Figure 1C</xref> , <xref ref-type="fig" rid="fig1s1">Figure 1—figure supplement 1D</xref>), while one episode had a slightly positive mean difference (<xref ref-type="fig" rid="fig1s1">Figure 1—figure supplement 1D</xref>), suggesting that we captured two episodes during a decay phase and one episode near a peak of viral production. The standard deviation of the mean absolute value of viral DNA copy difference between successive swabs was 0.16, 0.22, and 0.26 in the three participants, respectively, suggesting that differences of &gt;0.5 log<sub>10</sub> HSV-2 DNA copies that may occur over hours usually reflect true changes in viral load rather than noise in the data attributable to clinical collection or PCR technique.</p></boxed-text></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'box'), ('doi', u'10.7554/eLife.00288.004'), ('id', u'box1'), ('label', u'Box 1.'), ('title', u'Cohort A'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Cohort A')]), OrderedDict([('type', 'paragraph'), ('text', u'Cohort A included three subjects who were seen within 12 hr of HSV-2 recurrence, and who collected genital swabs every 5 min for 4 hr. This experiment assessed whether there were alterations in viral load related to the PCR assay or collection technique. Only small changes occurred during 5-min intervals (<a href="#fig1">Figure 1A</a>, <a href="#fig1s1">Figure 1\u2014figure supplement 1A,B</a>, <a href="#SD1-data">Figure 1\u2014source data 1</a>). The mean absolute value of viral DNA copy difference between successive swabs was 0.20, 0.28, and 0.34 log<sub>10</sub> genomic copies in the three participants, and generally increased with time between swabs (<a href="#fig1">Figure 1B</a>, <a href="#fig1s1">Figure 1\u2014figure supplement 1C</a>). The mean difference in HSV DNA copies between swabs correlated tightly with time between swabs in two participants (<a href="#fig1">Figure 1C</a>, <a href="#fig1s1">Figure 1\u2014figure supplement 1D</a>), with virtually no difference in viral quantity between swabs separated by 5-min intervals in all three subjects (<a href="#fig1">Figure 1C</a>, <a href="#fig1s1">Figure 1\u2014figure supplement 1D</a>). Two episodes had negative mean differences in viral quantity with increasing time between swabs (<a href="#fig1">Figure 1C</a> , <a href="#fig1s1">Figure 1\u2014figure supplement 1D</a>), while one episode had a slightly positive mean difference (<a href="#fig1s1">Figure 1\u2014figure supplement 1D</a>), suggesting that we captured two episodes during a decay phase and one episode near a peak of viral production. The standard deviation of the mean absolute value of viral DNA copy difference between successive swabs was 0.16, 0.22, and 0.26 in the three participants, respectively, suggesting that differences of &gt;0.5 log<sub>10</sub> HSV-2 DNA copies that may occur over hours usually reflect true changes in viral load rather than noise in the data attributable to clinical collection or PCR technique.')])])])])])]
         ),

        # Example of boxed-text with content inside its caption tag
        ('<root><boxed-text id="box1"><object-id pub-id-type="doi">10.7554/eLife.00013.009</object-id><label>Box 1.</label><caption><title>Box title</title><p>content</p></caption></boxed-text></root>',
         [OrderedDict([('content', [OrderedDict([('type', 'box'), ('doi', u'10.7554/eLife.00013.009'), ('id', u'box1'), ('label', u'Box 1.'), ('title', u'Box title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'content')])])])])])]
         ),

        # code block, based on elife 20352 v2, contains new lines too
        ('''<root><p>A paragraph</p><p><code>&lt;MotifGraft name=&quot;motif_grafting&quot;
      context_structure=&quot;%%context%%&quot;
      motif_structure=&quot;truncatedBH3.pdb&quot;
      RMSD_tolerance=&quot;3.0&quot;
      NC_points_RMSD_tolerance=&quot;2.0&quot;
      clash_score_cutoff=&quot;0&quot;
      clash_test_residue=&quot;ALA&quot;
      hotspots=&quot;9:12:13:14:16:17&quot;
      combinatory_fragment_size_delta=&quot;0:0&quot;
      max_fragment_replacement_size_delta=&quot;0:0&quot;
      full_motif_bb_alignment=&quot;1&quot;
      allow_independent_alignment_per_fragment=&quot;0&quot;
      graft_only_hotspots_by_replacement=&quot;0&quot;
      only_allow_if_N_point_match_aa_identity=&quot;0&quot;
      only_allow_if_C_point_match_aa_identity=&quot;0&quot;
      revert_graft_to_native_sequence=&quot;1&quot;
      allow_repeat_same_graft_output=&quot;1&quot;/&gt;</code></p></root>''',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'A paragraph')]), OrderedDict([('type', 'code'), ('code', u'<MotifGraft name="motif_grafting"\n      context_structure="%%context%%"\n      motif_structure="truncatedBH3.pdb"\n      RMSD_tolerance="3.0"\n      NC_points_RMSD_tolerance="2.0"\n      clash_score_cutoff="0"\n      clash_test_residue="ALA"\n      hotspots="9:12:13:14:16:17"\n      combinatory_fragment_size_delta="0:0"\n      max_fragment_replacement_size_delta="0:0"\n      full_motif_bb_alignment="1"\n      allow_independent_alignment_per_fragment="0"\n      graft_only_hotspots_by_replacement="0"\n      only_allow_if_N_point_match_aa_identity="0"\n      only_allow_if_C_point_match_aa_identity="0"\n      revert_graft_to_native_sequence="1"\n      allow_repeat_same_graft_output="1"/>')])])])]
        ),

        # Example of monospace tags
        ('<root><p>The following is an example of monotype text within the body of an eLife article.</p><p><monospace>P<sub>NRE+AP-1</sub>: 5’– CTTCGTGACTAGTCTTGACTCAGA –3’</monospace></p><p><monospace>P<sub>RAM</sub>: 5’– CTAGAAGTTTGTTCGTGACTCAGA –3’</monospace></p><p><monospace>E1: 5’– CTAGAAGTTTGTTGACTCACCCGA –3’</monospace></p><p><monospace>E2: 5’– CTAGAAGTTTGTTGACTCATTAGA –3’</monospace></p><p><monospace>E3: 5’– CTAGAAGTTTGTGTATGACTCAGA –3’</monospace></p><p><monospace>CME: 5’– CTAGAAATTTGTACGTGCCACAGA –3’</monospace></p></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'paragraph'), ('text', u'The following is an example of monotype text within the body of an eLife article.')]), OrderedDict([('type', 'paragraph'), ('text', u'<span class="monospace">P<sub>NRE+AP-1</sub>: 5\u2019\u2013 CTTCGTGACTAGTCTTGACTCAGA \u20133\u2019</span>')]), OrderedDict([('type', 'paragraph'), ('text', u'<span class="monospace">P<sub>RAM</sub>: 5\u2019\u2013 CTAGAAGTTTGTTCGTGACTCAGA \u20133\u2019</span>')]), OrderedDict([('type', 'paragraph'), ('text', u'<span class="monospace">E1: 5\u2019\u2013 CTAGAAGTTTGTTGACTCACCCGA \u20133\u2019</span>')]), OrderedDict([('type', 'paragraph'), ('text', u'<span class="monospace">E2: 5\u2019\u2013 CTAGAAGTTTGTTGACTCATTAGA \u20133\u2019</span>')]), OrderedDict([('type', 'paragraph'), ('text', u'<span class="monospace">E3: 5\u2019\u2013 CTAGAAGTTTGTGTATGACTCAGA \u20133\u2019</span>')]), OrderedDict([('type', 'paragraph'), ('text', u'<span class="monospace">CME: 5\u2019\u2013 CTAGAAATTTGTACGTGCCACAGA \u20133\u2019</span>')])])])]
         ),

        # example of a table to not pickup a child element title, based on 22264 v2
        ('<root><table-wrap id="tbl1" position="float"><object-id pub-id-type="doi">10.7554/eLife.22264.016</object-id><label>Table 1.</label><caption><p>Progeny of <italic>Fn1<sup>syn/+</sup>;Itgb3<sup>+/-</sup></italic> x <italic>Fn1<sup>syn/+</sup>;Itgb3<sup>+/-</sup></italic> intercrosses.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.22264.016">http://dx.doi.org/10.7554/eLife.22264.016</ext-link></p><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.22264.017</object-id><label>Table 1—source data 1.</label><caption><title>Progeny of <italic>Fn1<sup>syn/syn</sup>;Itgb3<sup>+/-</sup></italic> x <italic>Fn1<sup>syn/syn</sup>;Itgb3<sup>+/-</sup></italic> crosses</title><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.22264.017">http://dx.doi.org/10.7554/eLife.22264.017</ext-link></p></caption><media mime-subtype="docx" mimetype="application" xlink:href="elife-22264-table1-data1-v2.docx"/></supplementary-material></p></caption><table frame="hsides" rules="groups"><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table></table-wrap></root>',
         [OrderedDict([('content', [OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.22264.016'), ('id', u'tbl1'), ('label', u'Table 1.'), ('title', 'Progeny of <i>Fn1<sup>syn/+</sup>;Itgb3<sup>+/-</sup></i> x <i>Fn1<sup>syn/+</sup>;Itgb3<sup>+/-</sup></i> intercrosses'), ('tables', ['<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>']), ('sourceData', [OrderedDict([('doi', u'10.7554/eLife.22264.017'), ('id', u'SD1-data'), ('label', u'Table 1\u2014source data 1.'), ('title', 'Progeny of <i>Fn1<sup>syn/syn</sup>;Itgb3<sup>+/-</sup></i> x <i>Fn1<sup>syn/syn</sup>;Itgb3<sup>+/-</sup></i> crosses'), ('mediaType', u'application/docx')])])])])])]
        ),

        # example table: a label, no title, no caption
        ('<root><table-wrap id="tbl1" position="float"><object-id pub-id-type="doi">10.7554/eLife.22264.016</object-id><label>Table label.</label><caption><p></p></caption><table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table></table-wrap></root>',
         [OrderedDict([('content', [OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.22264.016'), ('id', u'tbl1'), ('title', u'Table label.'), ('tables', ['<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'])])])])]
        ),

        # example table: a label, a title, no caption
        ('<root><table-wrap id="tbl1" position="float"><object-id pub-id-type="doi">10.7554/eLife.22264.016</object-id><label>Table label.</label><caption><title>Table title.</title></caption><table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table></table-wrap></root>',
         [OrderedDict([('content', [OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.22264.016'), ('id', u'tbl1'), ('label', u'Table label.'), ('title', u'Table title.'), ('tables', ['<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'])])])])]
        ),

        # example table: a label, no title, a caption
        ('<root><table-wrap id="tbl1" position="float"><object-id pub-id-type="doi">10.7554/eLife.22264.016</object-id><label>Table label.</label><caption><p>Table caption.</p></caption><table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table></table-wrap></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.22264.016'), ('id', u'tbl1'), ('label', u'Table label.'), ('title', u'Table caption'), ('tables', ['<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'])])])])]
        ),

        # example table: a label, a title, and a caption
        ('<root><table-wrap id="tbl1" position="float"><object-id pub-id-type="doi">10.7554/eLife.22264.016</object-id><label>Table label.</label><caption><title>Table title.</title><p>Table caption.</p></caption><table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table></table-wrap></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.22264.016'), ('id', u'tbl1'), ('label', u'Table label.'), ('title', u'Table title.'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Table caption.')])]), ('tables', ['<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'])])])])]
        ),

        # example table: no label, no title, and a caption
        ('<root><table-wrap id="tbl1" position="float"><object-id pub-id-type="doi">10.7554/eLife.22264.016</object-id><caption><p>Table caption. A second sentence.</p></caption><table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table></table-wrap></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'table'), ('doi', u'10.7554/eLife.22264.016'), ('id', u'tbl1'), ('title', u'Table caption'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Table caption. A second sentence.')])]), ('tables', ['<table><thead><tr><th valign="top">Age</th></tr></thead><tbody><tr><td valign="top">E11.5</td></tr></tbody></table>'])])])])]
        ),

        # example fig with a caption and no title needs a title added, based on 00281 v1
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><fig id="fig1" position="float"><caption><p>Fog doubles the risk of an car accident, which is why researchers are keen to understand how it influences how drivers perceive their speed.</p></caption><graphic xlink:href="elife-00281-fig1-v1.tif"/><attrib>FIGURE CREDIT: TIM MCCORMACK.</attrib></fig></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'image'), ('id', u'fig1'), ('title', u'Fog doubles the risk of an car accident, which is why researchers are keen to understand how it influences how drivers perceive their speed'), ('image', {'alt': '', 'uri': u'elife-00281-fig1-v1.tif'}), ('attribution', [u'FIGURE CREDIT: TIM MCCORMACK.'])])])])]
        ),

        # example media with a label and no title, based on 00007 v1
        ('<root><media content-type="glencoe play-in-place height-250 width-310" id="media1" mime-subtype="avi" mimetype="video" xlink:href="elife-00007-media1.avi"><object-id pub-id-type="doi">10.7554/eLife.00007.016</object-id><label>Video 1.</label><caption><p>On-plant assay, plant 7u, WT, June 18, 2011.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00007.016">http://dx.doi.org/10.7554/eLife.00007.016</ext-link></p></caption></media></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'video'), ('doi', u'10.7554/eLife.00007.016'), ('id', u'media1'), ('label', u'Video 1.'), ('title', u'On-plant assay, plant 7u, WT, June 18, 2011')])])])]
        ),

        # example test from 02935 v2 of list within a list to not add child list-item to the parent list twice
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><list list-type="order"><list-item><p>At least 4 unique reads supporting variants and all variant reads at least 20 phred scale sequencing quality score (Q 20 = 1% sequencing error rate) and at least 3% variant allele fractions (VAFs).</p><list list-type="simple"><list-item><p>A. Regardless of in WGS and in WES, the ≥4 mismatches and the ≥3% VAF criteria must be satisfied simultaneously.</p></list-item><list-item><p>B. However, in WGS, the minimum number of reads (n = 4) criterion is not essential, because the ≥3% VAF criterion is much more stringent (3% VAF request at least 240 mismatches (&gt;&gt;4) given mtDNA coverage is ∼8000 for WGS).</p></list-item><list-item><p>C. In WES, the ≥3% VAF criterion is relatively less important than in WGS, because the ≥4 mismatches criterion is more stringent. For example, 4 mismatches in 90x (WXS average) coverage region (VAF = 4.4%) automatically fulfill the ≥3% VAF criterion. For less covered regions (i.e. &lt;40x coverage; n = 285 out of total 1907 substitutions), the VAF criterion becomes less important, because 4 mismatches would generate ≥10% VAF, much higher than the minimum threshold (i.e. 3%). As results, we are missing lower heteroplasmic variants (i.e. variants with 3–10% heteroplasmic levels) from low coverage samples (mostly by WXS). The lower sensitivity of WXS is also confirmed in our validation study (see “Validation of somatic variants” below).</p></list-item></list></list-item></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'list'), ('prefix', 'number'), ('items', [[OrderedDict([('type', 'paragraph'), ('text', u'At least 4 unique reads supporting variants and all variant reads at least 20 phred scale sequencing quality score (Q 20 = 1% sequencing error rate) and at least 3% variant allele fractions (VAFs).')]), OrderedDict([('type', 'list'), ('prefix', 'none'), ('items', [[OrderedDict([('type', 'paragraph'), ('text', u'A. Regardless of in WGS and in WES, the \u22654 mismatches and the \u22653% VAF criteria must be satisfied simultaneously.')])], [OrderedDict([('type', 'paragraph'), ('text', u'B. However, in WGS, the minimum number of reads (n = 4) criterion is not essential, because the \u22653% VAF criterion is much more stringent (3% VAF request at least 240 mismatches (&gt;&gt;4) given mtDNA coverage is \u223c8000 for WGS).')])], [OrderedDict([('type', 'paragraph'), ('text', u'C. In WES, the \u22653% VAF criterion is relatively less important than in WGS, because the \u22654 mismatches criterion is more stringent. For example, 4 mismatches in 90x (WXS average) coverage region (VAF = 4.4%) automatically fulfill the \u22653% VAF criterion. For less covered regions (i.e. &lt;40x coverage; n = 285 out of total 1907 substitutions), the VAF criterion becomes less important, because 4 mismatches would generate \u226510% VAF, much higher than the minimum threshold (i.e. 3%). As results, we are missing lower heteroplasmic variants (i.e. variants with 3\u201310% heteroplasmic levels) from low coverage samples (mostly by WXS). The lower sensitivity of WXS is also confirmed in our validation study (see \u201cValidation of somatic variants\u201d below).')])]])])]])])])])]
         ),

        )
    def test_body_block_content_render(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_block_content_render(soup.contents[0])
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="s1"><title>Section title</title><p>Content.<fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group></p><p>More content</p></sec></root>',
        [OrderedDict([('type', 'section'), ('id', u's1'), ('title', u'Section title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-v1.tif'}), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-figsupp1-v1.tif'})])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="s1"><title>Section title</title><p>Content.</p><fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group><p>More content</p></sec></root>',
        [OrderedDict([('type', 'section'), ('id', u's1'), ('title', u'Section title'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-v1.tif'}), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-figsupp1-v1.tif'})])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])])])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><boxed-text><p>Content 1</p><p>Content 2</p></boxed-text></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content 1')]), OrderedDict([('type', 'paragraph'), ('text', u'Content 2')])]
         ),

        # Below when there is a space between paragraph tags, it should not render as a paragraph
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><boxed-text><p>Content 1</p> <p>Content 2</p></boxed-text></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content 1')]), OrderedDict([('type', 'paragraph'), ('text', u'Content 2')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink><p><bold>This</bold> <fig id="fig7" position="float"><graphic xlink:href="elife-00012-resp-fig2-v1.tif"/></fig></p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', '<b>This</b>')]), OrderedDict([('type', 'image'), ('id', u'fig7'), ('image', {'alt': '', 'uri': u'elife-00012-resp-fig2-v1.tif'})])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.<fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig>More content</p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig1-v1.tif'})]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.</p><fig id="fig1"><object-id pub-id-type="doi">10.7554/eLife.00666.024</object-id><label>Figure 1.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig1-v1.tif"/></fig><p>More content</p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.024'), ('id', u'fig1'), ('label', u'Figure 1.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig1-v1.tif'})]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><p>Content.</p><fig-group><fig id="fig2"><object-id pub-id-type="doi">10.7554/eLife.00666.008</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-v1.tif"/></fig><fig id="fig2s1"><object-id pub-id-type="doi">10.7554/eLife.00666.009</object-id><label>Figure 2.</label><caption><title>Figure title</title><p>Figure caption</p></caption><graphic xlink:href="elife-00666-fig2-figsupp1-v1.tif"/></fig></fig-group><p>More content</p></root>',
        [OrderedDict([('type', 'paragraph'), ('text', u'Content.')]), OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.008'), ('id', u'fig2'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-v1.tif'}), ('supplements', [OrderedDict([('type', 'image'), ('doi', u'10.7554/eLife.00666.009'), ('id', u'fig2s1'), ('label', u'Figure 2.'), ('title', u'Figure title'), ('caption', [OrderedDict([('type', 'paragraph'), ('text', u'Figure caption')])]), ('image', {'alt': '', 'uri': u'elife-00666-fig2-figsupp1-v1.tif'})])])]), OrderedDict([('type', 'paragraph'), ('text', u'More content')])]
         ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><body><p><boxed-text id="B1"><p>Boxed text with no title</p></boxed-text></p></body></root>',
        [OrderedDict([('content', [OrderedDict([('type', 'box'), ('id', u'B1'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Boxed text with no title')])])])])])]
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
        OrderedDict([('doi', u'10.7554/eLife.00001.001'), ('content', [OrderedDict([('type', 'paragraph'), ('text', u'Example <sub>in</sub> <i>cis</i> <span class="small-caps">or</span> <i>trans</i> <span class="underline">and</span> <i>Gfrα2</i> <math id="inf1"><mstyle displaystyle="true" scriptlevel="0"><mrow><munder><mo></mo><mi>m</mi></munder><mrow><msub><mover accent="true"><mi>p</mi><mo></mo></mover><mi>m</mi></msub><mo>=</mo><mn>0</mn></mrow></mrow></mstyle></math> <sup>by</sup> <b>its</b> co-receptors as *p&lt;0.05 &gt;0.25% <a href="#bib25">Schneider et al., 2006</a> and ligands.')])])])
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
          "elife02935.xml", "elife00270.xml", "elife00351.xml", "elife-00666.xml")
    def test_authors(self, filename):
        self.assertEqual(self.json_expected(filename, "authors"),
                         parser.authors(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-00666.xml")
    def test_authors_non_byline(self, filename):
        self.assertEqual(self.json_expected(filename, "authors_non_byline"),
                         parser.authors_non_byline(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00013.xml", "elife-00666.xml")
    def test_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "award_groups"),
                         parser.award_groups(self.soup(filename)))

    @unpack
    @data(
        # 07383 v1 has a institution in the principal award recipient
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><funding-group><award-group id="par-1"><funding-source><institution-wrap><institution>Laura and John Arnold Foundation</institution></institution-wrap></funding-source><principal-award-recipient><institution>Reproducibility Project: Cancer Biology</institution></principal-award-recipient></award-group></funding-group></root>',
        [{'award_id': None, 'funding_source': [u'Laura and John Arnold Foundation'], 'recipient': [u'Reproducibility Project: Cancer Biology']}]
         ),
        )
    def test_award_groups_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.award_groups(soup.contents[0])
        self.assertEqual(expected, tag_content)

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
          "elife-14093-v1.xml", "elife-00666.xml")
    def test_components(self, filename):
        self.assertEqual(self.json_expected(filename, "components"),
                         parser.components(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_conflict(self, filename):
        self.assertEqual(self.json_expected(filename, "conflict"),
                         parser.conflict(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-02833-v2.xml", "elife-00666.xml")
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
    def test_full_funding_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "full_funding_statement"),
                         parser.full_funding_statement(self.soup(filename)))

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

    @unpack
    @data(
        # example license from 00666
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article-meta><permissions><copyright-statement>© 2016, Harrison et al</copyright-statement><copyright-year>2016</copyright-year><copyright-holder>Harrison et al</copyright-holder><ali:free_to_read/><license xlink:href="http://creativecommons.org/licenses/by/4.0/"><ali:license_ref>http://creativecommons.org/licenses/by/4.0/</ali:license_ref><license-p>This article is distributed under the terms of the <ext-link ext-link-type="uri" xlink:href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution License</ext-link>, which permits unrestricted use and redistribution provided that the original author and source are credited.</license-p></license></permissions></article-meta></root>',
        'This article is distributed under the terms of the <a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution License</a>, which permits unrestricted use and redistribution provided that the original author and source are credited.'
        ),
    )
    def test_license_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.license_json(body_tag)
        self.assertEqual(expected, tag_content)

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

    @unpack
    @data(
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"></root>',
        None
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>Plant biology</subject></subj-group></root>',
        u'Plant Biology'
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>The Natural History Of Model Organisms</subject></subj-group></root>',
        u'The Natural History of Model Organisms'
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>p53 Family proteins</subject></subj-group></root>',
        u'p53 Family Proteins'
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>TOR signaling</subject></subj-group></root>',
        u'TOR Signaling'
        ),

        )
    def test_title_prefix_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.title_prefix_json(body_tag)
        self.assertEqual(expected, tag_content)

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

    def test_parse_mixed_citations(self):
        data = parser.mixed_citations(self.soup('elife-kitchen-sink.xml'))
        expected = [{'article': {'authors': [{'given': u'R', 'surname': u'Straussman'}, {'given': u'T', 'surname': u'Morikawa'}, {'given': u'K', 'surname': u'Shee'}, {'given': u'M', 'surname': u'Barzily-Rokni'}, {'given': u'ZR', 'surname': u'Qian'}, {'given': u'J', 'surname': u'Du'}, {'given': u'A', 'surname': u'Davis'}, {'given': u'MM', 'surname': u'Mongare'}, {'given': u'J', 'surname': u'Gould'}, {'given': u'DT', 'surname': u'Frederick'}, {'given': u'ZA', 'surname': u'Cooper'}, {'given': u'PB', 'surname': u'Chapman'}, {'given': u'DB', 'surname': u'Solit'}, {'given': u'A', 'surname': u'Ribas'}, {'given': u'RS', 'surname': u'Lo'}, {'given': u'KT', 'surname': u'Flaherty'}, {'given': u'S', 'surname': u'Ogino'}, {'given': u'JA', 'surname': u'Wargo'}, {'given': u'TR', 'surname': u'Golub'}], 'doi': u'10.1038/nature11183', 'pub-date': [2014, 2, 28], 'title': u'Tumour micro-environment elicits innate resistance to RAF inhibitors through HGF secretion'}, 'journal': {'volume': u'487', 'lpage': u'504', 'name': u'Nature', 'fpage': u'500'}}]
        self.assertEqual(expected, data)

if __name__ == '__main__':
    unittest.main()
