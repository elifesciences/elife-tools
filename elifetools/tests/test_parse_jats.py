# coding=utf-8

from __future__ import absolute_import

import json
import os
import unittest

from bs4 import BeautifulSoup
from ddt import ddt, data, unpack

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elifetools import parseJATS as parser
from elifetools import rawJATS as raw_parser
from elifetools.utils import date_struct, unicode_value
from collections import OrderedDict

from elifetools.file_utils import sample_xml, json_expected_file, read_fixture




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
                json_expected = json.loads(json_file_fp.read().decode('utf-8'))
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
        (read_fixture('test_ethics_json', 'content_01.xml'),
         read_fixture('test_ethics_json', 'content_01_expected.py')
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
        (read_fixture('test_appendices_json', 'content_01.xml'),
         read_fixture('test_appendices_json', 'content_01_expected.py')
        ),

        # example based on 14022 v3 having a section with no title in it, with some additional scenarios
        (read_fixture('test_appendices_json', 'content_02.xml'),
         read_fixture('test_appendices_json', 'content_02_expected.py')
        ),

        # appendix with no sections, based on 00666 kitchen sink
        (read_fixture('test_appendices_json', 'content_03.xml'),
         read_fixture('test_appendices_json', 'content_03_expected.py')
        ),

        # appendix with a section and a box, also based on 00666 kitchen sink
        (read_fixture('test_appendices_json', 'content_04.xml'),
         read_fixture('test_appendices_json', 'content_04_expected.py')
        ),

        # appendix with a boxed-text in a subsequent section based on article 
        (read_fixture('test_appendices_json', 'content_05.xml'),
         read_fixture('test_appendices_json', 'content_05_expected.py')
        ),

        )
    def test_appendices_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.appendices_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        # appendix with inline-graphic, based on 17092 v1
        (read_fixture('test_appendices_json_base_url', 'content_01.xml'),
         None,
         read_fixture('test_appendices_json_base_url', 'content_01_expected.py')
        ),

        # appendix with inline-graphic, based on 17092 v1
        (read_fixture('test_appendices_json_base_url', 'content_02.xml'),
         'https://example.org/',
         read_fixture('test_appendices_json_base_url', 'content_02_expected.py')
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
        [
            OrderedDict([
                ('mediaType', 'application/zip'), 
                ('uri', u'elife-16996-supp-v1.zip'),
                ('filename', u'elife-16996-supp-v1.zip'),
                ('id', 'SD1-data'), 
                ('label', 'All additional files'),
                ('caption', [OrderedDict([
                    ('text', 'Any figure supplements, source code, source data, videos or supplementary files associated with this article are contained within this zip.'),
                    ('type', 'paragraph'),
                ])])
            ])
        ]
         ),

        # Datasets from 08477 v1 VoR
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec id="s6" sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD2-data"><object-id pub-id-type="doi">10.7554/eLife.08477.007</object-id><label>Source code 1.</label><caption><p>A Matlab GUI for synchronized video-taping and song stimulation in <xref ref-type="fig" rid="fig3">Figure 3</xref>.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.08477.007">http://dx.doi.org/10.7554/eLife.08477.007</ext-link></p></caption><media mime-subtype="zip" mimetype="application" xlink:href="elife-08477-code1-v1.zip"/></supplementary-material><supplementary-material id="SD3-data"><object-id pub-id-type="doi">10.7554/eLife.08477.011</object-id><label>Source code 2.</label><caption><p>A Matlab GUI for processing and analyzing the calcium-imaging data in <xref ref-type="fig" rid="fig5">Figure 5</xref>.</p><p><bold>DOI:</bold> <ext-link ext-link-type="doi" xlink:href="10.7554/eLife.08477.011">http://dx.doi.org/10.7554/eLife.08477.011</ext-link></p></caption><media mime-subtype="zip" mimetype="application" xlink:href="elife-08477-code2-v1.zip"/></supplementary-material></sec></back></root>',
        [
            OrderedDict([
                ('doi', u'10.7554/eLife.08477.007'),
                ('id', u'SD2-data'),
                ('label', u'Source code 1'),
                ('caption', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'A Matlab GUI for synchronized video-taping and song stimulation in <a href="#fig3">Figure 3</a>.')
                    ])
                ]),
                ('mediaType', u'application/zip'),
                ('uri', u'elife-08477-code1-v1.zip'),
                ('filename', u'elife-08477-code1-v1.zip')
            ]),
            OrderedDict([
                ('doi', u'10.7554/eLife.08477.011'),
                ('id', u'SD3-data'),
                ('label', u'Source code 2'),
                ('caption', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'A Matlab GUI for processing and analyzing the calcium-imaging data in <a href="#fig5">Figure 5</a>.')
                    ])
                ]),
                ('mediaType', u'application/zip'),
                ('uri', u'elife-08477-code2-v1.zip'),
                ('filename', u'elife-08477-code2-v1.zip')
            ])
        ]
         ),


        # 02184 v1, older style PoA has supplementary files directly in the article-meta
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><supplementary-material><ext-link xlink:href="elife-02184-supp-v1.zip">Download zip</ext-link><p>Any figures and tables for this article are included in the PDF. The zip folder contains additional supplemental files.</p></supplementary-material></article-meta></front></root>',
        [
            OrderedDict([
                ('mediaType', 'application/zip'),
                ('uri', u'elife-02184-supp-v1.zip'),
                ('filename', u'elife-02184-supp-v1.zip'), 
                ('id', 'SD1-data'),
                ('label', 'All additional files'),
                ('caption', [OrderedDict([
                    ('text', 'Any figure supplements, source code, source data, videos or supplementary files associated with this article are contained within this zip.'),
                    ('type', 'paragraph'),
                ])])
            ])
        ]
         ),

        # 04493 v1 PoA, multiple old style supplementary files
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><body><article-meta><supplementary-material><ext-link xlink:href="elife-04493-supp-v1.zip">Download zip of figure supplements and supplementary file</ext-link><p>Any figures and tables for this article are included in the PDF. The zip folder contains additional supplemental files.</p></supplementary-material><supplementary-material><ext-link xlink:href="Video_2.zip">Download zip of Video 2</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_8.zip">Download zip of Video 8</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_6.zip">Download zip of Video 6</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_11.zip">Download zip of Video 11</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_17.zip">Download zip of Video 17</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_18.zip">Download zip of Video 18</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_7.zip">Download zip of Video 7</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_10.zip">Download zip of Video 10</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_5.zip">Download zip of Video 5</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_13.zip">Download zip of Video 13</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_19.zip">Download zip of Video 19</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_15.zip">Download zip of Video 15</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_21.zip">Download zip of Video 21</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_22.zip">Download zip of Video 22</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_4.zip">Download zip of Video 4</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_20.zip">Download zip of Video 20</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_12.zip">Download zip of Video 12</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_1.zip">Download zip of Video 1</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_16.zip">Download zip of Video 16</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_3.zip">Download zip of Video 3</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_9.zip">Download zip of Video 9</ext-link></supplementary-material><supplementary-material><ext-link xlink:href="Video_14.zip">Download zip of Video 14</ext-link></supplementary-material></article-meta></front></root>',
        [
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'elife-04493-supp-v1.zip'),
            ('filename', u'elife-04493-supp-v1.zip'),
            ('id', 'SD1-data'),
            ('label', 'Supplementary file 1.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_2.zip'),
            ('filename', u'Video_2.zip'),
            ('id', 'SD2-data'),
            ('label', 'Supplementary file 2.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_8.zip'),
            ('filename', u'Video_8.zip'),
            ('id', 'SD3-data'),
            ('label', 'Supplementary file 3.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_6.zip'),
            ('filename', u'Video_6.zip'),
            ('id', 'SD4-data'),
            ('label', 'Supplementary file 4.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_11.zip'),
            ('filename', u'Video_11.zip'),
            ('id', 'SD5-data'),
            ('label', 'Supplementary file 5.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_17.zip'),
            ('filename', u'Video_17.zip'),
            ('id', 'SD6-data'),
            ('label', 'Supplementary file 6.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_18.zip'),
            ('filename', u'Video_18.zip'),
            ('id', 'SD7-data'),
            ('label', 'Supplementary file 7.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_7.zip'),
            ('filename', u'Video_7.zip'),
            ('id', 'SD8-data'),
            ('label', 'Supplementary file 8.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_10.zip'),
            ('filename', u'Video_10.zip'),
            ('id', 'SD9-data'),
            ('label', 'Supplementary file 9.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_5.zip'),
            ('filename', u'Video_5.zip'),
            ('id', 'SD10-data'),
            ('label', 'Supplementary file 10.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_13.zip'),
            ('filename', u'Video_13.zip'),
            ('id', 'SD11-data'),
            ('label', 'Supplementary file 11.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_19.zip'),
            ('filename', u'Video_19.zip'),
            ('id', 'SD12-data'),
            ('label', 'Supplementary file 12.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_15.zip'),
            ('filename', u'Video_15.zip'),
            ('id', 'SD13-data'),
            ('label', 'Supplementary file 13.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_21.zip'),
            ('filename', u'Video_21.zip'),
            ('id', 'SD14-data'),
            ('label', 'Supplementary file 14.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_22.zip'),
            ('filename', u'Video_22.zip'),
            ('id', 'SD15-data'),
            ('label', 'Supplementary file 15.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_4.zip'),
            ('filename', u'Video_4.zip'),
            ('id', 'SD16-data'),
            ('label', 'Supplementary file 16.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_20.zip'),
            ('filename', u'Video_20.zip'),
            ('id', 'SD17-data'),
            ('label', 'Supplementary file 17.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_12.zip'),
            ('filename', u'Video_12.zip'),
            ('id', 'SD18-data'),
            ('label', 'Supplementary file 18.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_1.zip'),
            ('filename', u'Video_1.zip'),
            ('id', 'SD19-data'),
            ('label', 'Supplementary file 19.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_16.zip'),
            ('filename', u'Video_16.zip'),
            ('id', 'SD20-data'),
            ('label', 'Supplementary file 20.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_3.zip'),
            ('filename', u'Video_3.zip'),
            ('id', 'SD21-data'),
            ('label', 'Supplementary file 21.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_9.zip'),
            ('filename', u'Video_9.zip'),
            ('id', 'SD22-data'),
            ('label', 'Supplementary file 22.')
        ]),
        OrderedDict([
            ('mediaType', 'application/zip'),
            ('uri', u'Video_14.zip'),
            ('filename', u'Video_14.zip'),
            ('id', 'SD23-data'),
            ('label', 'Supplementary file 23.')
        ])
        ]
        ),

        # 10110 v1 excerpt, should only extract the supplementary-material from the back matter
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><body><sec><p><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.10110.004</object-id><label>Figure 1—source data 1.</label><caption><title>Dauer assay data for individual trials in <xref ref-type="fig" rid="fig1">Figure 1</xref>.</title><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.10110.004">http://dx.doi.org/10.7554/eLife.10110.004</ext-link></p></caption><media mime-subtype="xlsx" mimetype="application" xlink:href="elife-10110-fig1-data1-v1.xlsx"/></supplementary-material></p></sec></body><back><sec id="s6" sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD9-data"><object-id pub-id-type="doi">10.7554/eLife.10110.026</object-id><label>Supplementary file 1.</label><caption><p>List of strains used in this work.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.10110.026">http://dx.doi.org/10.7554/eLife.10110.026</ext-link></p></caption><media mime-subtype="docx" mimetype="application" xlink:href="elife-10110-supp1-v1.docx"/></supplementary-material></back></root>',
        [
            OrderedDict([
                ('doi', u'10.7554/eLife.10110.026'),
                ('id', u'SD9-data'),
                ('label', u'Supplementary file 1'),
                ('caption', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'List of strains used in this work.')
                    ])
                ]),
                ('mediaType', u'application/docx'),
                ('uri', u'elife-10110-supp1-v1.docx'),
                ('filename', u'elife-10110-supp1-v1.docx')
            ])
        ]
         ),

        # 03405 v1, label and no title tag
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.03405.026</object-id><label>Source code 1.</label><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.03405.026">http://dx.doi.org/10.7554/eLife.03405.026</ext-link></p><media mime-subtype="rar" mimetype="application" xlink:href="elife-03405-code1-v1.rar"/></supplementary-material></sec></back></root>',
        [
            OrderedDict([
                ('doi', u'10.7554/eLife.03405.026'), 
                ('id', u'SD1-data'),
                ('label', u'Source code 1'), 
                ('mediaType', u'application/rar'),
                ('uri', u'elife-03405-code1-v1.rar'),
                ('filename', u'elife-03405-code1-v1.rar')
            ])]
         ),

       # 00333 v1, mimetype contains a slash so ignore sub-mimetype
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="SD1-data"><object-id pub-id-type="doi">10.7554/eLife.00333.023</object-id><label>Source code 1.</label><caption><p>Simulation script, s_arrest_hemifusion_simulation.m, and accompanying functions, generate_patch.m, s_randomdist.m, isaN2tuplet.m, findFlippedNeighbors.m, for MATLAB version R2012a.</p><p><bold>DOI:</bold><ext-link ext-link-type="doi" xlink:href="10.7554/eLife.00333.023">http://dx.doi.org/10.7554/eLife.00333.023</ext-link></p></caption><media mime-subtype="zip" mimetype="application/zip" xlink:href="elife-00333-code1-v1.zip"/></supplementary-material></sec></back></root>',
        [
            OrderedDict([
                ('doi', u'10.7554/eLife.00333.023'),
                ('id', u'SD1-data'),
                ('label', u'Source code 1'),
                ('caption', [
                    OrderedDict([
                        ('type', 'paragraph'),
                        ('text', u'Simulation script, s_arrest_hemifusion_simulation.m, and accompanying functions, generate_patch.m, s_randomdist.m, isaN2tuplet.m, findFlippedNeighbors.m, for MATLAB version R2012a.')
                    ])
                ]),
                ('mediaType', u'application/zip'),
                ('uri', u'elife-00333-code1-v1.zip'),
                ('filename', u'elife-00333-code1-v1.zip')
            ])
        ]
         ),

        # 26759 v2, example of title tag and no label tag
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><sec id="s6" sec-type="supplementary-material"><title>Additional files</title><supplementary-material id="supp1"><object-id pub-id-type="doi">10.7554/eLife.26759.018</object-id><label>Supplementary file 1.</label><caption><title>All primer sequences used in this study.</title></caption><media mime-subtype="docx" mimetype="application" xlink:href="elife-26759-supp1-v2.docx"/></supplementary-material><supplementary-material id="transrepform"><object-id pub-id-type="doi">10.7554/eLife.26759.019</object-id><caption><title>Transparent reporting form</title></caption><media mime-subtype="pdf" mimetype="application" xlink:href="elife-26759-transrepform-v2.pdf"/></supplementary-material></sec></back></root>',
        [
            OrderedDict([
                ('doi', u'10.7554/eLife.26759.018'),
                ('id', u'supp1'),
                ('label', u'Supplementary file 1'),
                ('title', u'All primer sequences used in this study.'),
                ('mediaType', u'application/docx'),
                ('uri', u'elife-26759-supp1-v2.docx'),
                ('filename', u'elife-26759-supp1-v2.docx')
            ]), OrderedDict([
                ('doi', u'10.7554/eLife.26759.019'),
                ('id', u'transrepform'),
                ('label', u'Transparent reporting form'),
                ('mediaType', u'application/pdf'),
                ('uri', u'elife-26759-transrepform-v2.pdf'),
                ('filename', u'elife-26759-transrepform-v2.pdf')
            ])
        ]
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
        (read_fixture('test_funding_awards_json', 'content_01.xml'),
         read_fixture('test_funding_awards_json', 'content_01_expected.py')
         ),

        # Funding from new kitchen sink
        (read_fixture('test_funding_awards_json', 'content_02.xml'),
         read_fixture('test_funding_awards_json', 'content_02_expected.py')
         ),

        # 08245 v1 edge case, unusual principal-award-recipient
        (read_fixture('test_funding_awards_json', 'content_03.xml'),
         read_fixture('test_funding_awards_json', 'content_03_expected.py')
         ),

        # 00801 v1 edge case, rewrite funding award
        (read_fixture('test_funding_awards_json', 'content_04.xml'),
         read_fixture('test_funding_awards_json', 'content_04_expected.py')
         ),

        # 04250 v1 edge case, rewrite to add funding award recipients
        (read_fixture('test_funding_awards_json', 'content_05.xml'),
         read_fixture('test_funding_awards_json', 'content_05_expected.py')
         ),

        # 06412 v2 edge case, rewrite to add funding award recipients
        (read_fixture('test_funding_awards_json', 'content_06.xml'),
         read_fixture('test_funding_awards_json', 'content_06_expected.py')
         ),

        # 03609 v1 example funding award with multiple recipients
        (read_fixture('test_funding_awards_json', 'content_07.xml'),
         read_fixture('test_funding_awards_json', 'content_07_expected.py')
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
        (read_fixture('test_decision_letter', 'content_01.xml'),
         read_fixture('test_decision_letter', 'content_01_expected.py')
         ),

        # 10856 v2, excerpt, add missing description via a rewrite
        (read_fixture('test_decision_letter', 'content_02.xml'),
         read_fixture('test_decision_letter', 'content_02_expected.py')
         ),

        )
    def test_decision_letter_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.decision_letter(soup)
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
        (read_fixture('test_author_response', 'content_01.xml'),
         read_fixture('test_author_response', 'content_01_expected.py')
         ),
        )
    def test_author_response_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.author_response(soup)
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
        (read_fixture('test_body_json', 'content_01.xml'),
         read_fixture('test_body_json', 'content_01_expected.py')
         ),

        # normal boxed-text and section, keep these
        (read_fixture('test_body_json', 'content_02.xml'),
         read_fixture('test_body_json', 'content_02_expected.py')
         ),

        # boxed-text paragraphs inside the caption tag, based on 05519 v2
        (read_fixture('test_body_json', 'content_03.xml'),
         read_fixture('test_body_json', 'content_03_expected.py')
         ),

        # 00301 v1 do not keep boxed-text and wrap in section
        (read_fixture('test_body_json', 'content_04.xml'),
         read_fixture('test_body_json', 'content_04_expected.py')
         ),

        # 00646 v1 boxed text to keep, and wrap in section
        (read_fixture('test_body_json', 'content_05.xml'),
         read_fixture('test_body_json', 'content_05_expected.py')
         ),

        # 02945 v1, correction article keep the boxed-text
        (read_fixture('test_body_json', 'content_06.xml'),
         read_fixture('test_body_json', 'content_06_expected.py')
         ),

        # 12844 v1, based on, edge case to rewrite unacceptable sections that have no titles
        (read_fixture('test_body_json', 'content_07.xml'),
         read_fixture('test_body_json', 'content_07_expected.py')
         ),

        # 09977 v2, based on, edge case to remove a specific section with no content
        (read_fixture('test_body_json', 'content_08.xml'),
         read_fixture('test_body_json', 'content_08_expected.py')
         ),

        # 09977 v3, based on, edge case to keep a specific section that does have content
        (read_fixture('test_body_json', 'content_09.xml'),
         read_fixture('test_body_json', 'content_09_expected.py')
         ),

        # 05519 v2, based on, edge case to remove an unwanted section
        (read_fixture('test_body_json', 'content_10.xml'),
         read_fixture('test_body_json', 'content_10_expected.py')
         ),

        # 00013 v1, excerpt, add an id to a section
        (read_fixture('test_body_json', 'content_11.xml'),
         read_fixture('test_body_json', 'content_11_expected.py')
         ),

        # 04232 v2, excerpt, remove an unwanted section
        (read_fixture('test_body_json', 'content_12.xml'),
         read_fixture('test_body_json', 'content_12_expected.py')
         ),

        # 07157 v1, add title to a section
        (read_fixture('test_body_json', 'content_13.xml'),
         read_fixture('test_body_json', 'content_13_expected.py')
         ),

        # excerpt of 23383 v1 where there is a boxed-text that was formerly stripped away, check it remains
        (read_fixture('test_body_json', 'content_14.xml'),
         read_fixture('test_body_json', 'content_14_expected.py')
         ),

        )
    def test_body_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_json(soup)
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        (read_fixture('test_body_json_base_url', 'content_01.xml'),
         None,
         read_fixture('test_body_json_base_url', 'content_01_expected.py')
         ),

        (read_fixture('test_body_json_base_url', 'content_02.xml'),
         'https://example.org/',
         read_fixture('test_body_json_base_url', 'content_02_expected.py')
         ),

        (read_fixture('test_body_json_base_url', 'content_03.xml'),
         None,
         read_fixture('test_body_json_base_url', 'content_03_expected.py')
         ),

        (read_fixture('test_body_json_base_url', 'content_04.xml'),
         'https://example.org/',
         read_fixture('test_body_json_base_url', 'content_04_expected.py')
         ),

        )
    def test_body_json_with_base_url(self, xml_content, base_url, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_json(soup, base_url=base_url)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # 08647 v1 PoA editor has blank string in the affiliation tags
        (read_fixture('test_editors_json', 'content_01.xml'),
         read_fixture('test_editors_json', 'content_01_expected.py')
         ),

         # 09560 v1 example, has two editors
        (read_fixture('test_editors_json', 'content_02.xml'),
         read_fixture('test_editors_json', 'content_02_expected.py')
        ),

         # 23804 v3 example, has no role tag and is rewritten
        (read_fixture('test_editors_json', 'content_03.xml'),
         read_fixture('test_editors_json', 'content_03_expected.py')
        ),

         # 22028 v1 example, has a country but no institution
        (read_fixture('test_editors_json', 'content_04.xml'),
         read_fixture('test_editors_json', 'content_04_expected.py')
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
        (read_fixture('test_authors_json', 'content_01.xml'),
         read_fixture('test_authors_json', 'content_01_expected.py')
         ),

        # 02935 v1, group authors (collab) but no members of those groups
        (read_fixture('test_authors_json', 'content_02.xml'),
         read_fixture('test_authors_json', 'content_02_expected.py')
        ),

        # 02935 v2, excerpt for group author parsing
        (read_fixture('test_authors_json', 'content_03.xml'),
         read_fixture('test_authors_json', 'content_03_expected.py')
         ),

        # 09376 v1, excerpt to rewrite an author ORCID
        (read_fixture('test_authors_json', 'content_04.xml'),
         read_fixture('test_authors_json', 'content_04_expected.py')
         ),

        # 06956 v1, excerpt, add an affiliation name to an author
        (read_fixture('test_authors_json', 'content_05.xml'),
         read_fixture('test_authors_json', 'content_05_expected.py')
         ),

        # 21337 v1, example to pick up the email of corresponding authors from authors notes
        (read_fixture('test_authors_json', 'content_06.xml'),
         read_fixture('test_authors_json', 'content_06_expected.py')
         ),

        # 00007 v1, example with a present address
        (read_fixture('test_authors_json', 'content_07.xml'),
         read_fixture('test_authors_json', 'content_07_expected.py')
         ),

        # 00666 kitchen sink (with extra whitespace removed), example to pick up the email of corresponding author
        (read_fixture('test_authors_json', 'content_08.xml'),
         read_fixture('test_authors_json', 'content_08_expected.py')
         ),

        # 09594 v2 example of non-standard footnote fn-type other and id starting with 'fn'
        (read_fixture('test_authors_json', 'content_09.xml'),
         read_fixture('test_authors_json', 'content_09_expected.py')
         ),

        # 21230 v1 example of author role to parse
        (read_fixture('test_authors_json', 'content_10.xml'),
         read_fixture('test_authors_json', 'content_10_expected.py')
         ),

        # 21230 v1 as an example of competing interests rewrite rule for elife
        (read_fixture('test_authors_json', 'content_11.xml'),
         read_fixture('test_authors_json', 'content_11_expected.py')
         ),

        # 00351 v1 example of author role to parse
        (read_fixture('test_authors_json', 'content_12.xml'),
         read_fixture('test_authors_json', 'content_12_expected.py')
         ),

        # 21723 v1 another example of author role
        (read_fixture('test_authors_json', 'content_13.xml'),
         read_fixture('test_authors_json', 'content_13_expected.py')
         ),

        # author with a bio based on kitchen sink 00777
        (read_fixture('test_authors_json', 'content_14.xml'),
         read_fixture('test_authors_json', 'content_14_expected.py')
         ),

         # 02273 v1 example, equal contribution to parse
        (read_fixture('test_authors_json', 'content_15.xml'),
         read_fixture('test_authors_json', 'content_15_expected.py')
        ),

         # 09148 v1 example, and author with two email addresses
        (read_fixture('test_authors_json', 'content_16.xml'),
         read_fixture('test_authors_json', 'content_16_expected.py')
        ),

        # example of new kitchen sink group authors with multiple email addresses, based on 17044 v1
        (read_fixture('test_authors_json', 'content_17.xml'),
         read_fixture('test_authors_json', 'content_17_expected.py')
         ),

        # example of inline email address
        (read_fixture('test_authors_json', 'content_18.xml'),
         read_fixture('test_authors_json', 'content_18_expected.py')
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
        (read_fixture('test_author_line', 'content_01.xml'),
         u'Randy Schekman, Mark Patterson'
         ),

        # 08714 v1, group authors only
        (read_fixture('test_author_line', 'content_02.xml'),
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
        (["Randy Schekman", "Mark Patterson", "eLife"], "Randy Schekman et al."),
        )
    def test_format_author_line(self, author_names, expected):
        self.assertEqual(parser.format_author_line(author_names), expected)


    @data(
        # aff tag linked via an rid to id attribute
        (read_fixture('test_format_aff', 'content_01.xml'),
         read_fixture('test_format_aff', 'content_01_expected.py'),
        ),
        # inline aff tag example, no id attribute
        (read_fixture('test_format_aff', 'content_02.xml'),
         read_fixture('test_format_aff', 'content_02_expected.py'),
        ),
        # aff example mostly just text with no subtags
        (read_fixture('test_format_aff', 'content_03.xml'),
         read_fixture('test_format_aff', 'content_03_expected.py'),
        ),
        # edge case, no aff tag or the rid idoes not match an aff id
        (None,
        (None, {})
        ),
    )
    @unpack
    def test_format_aff_edge_cases(self, xml_content, expected):
        if xml_content:
            soup = parser.parse_xml(xml_content)
            aff_tag = soup.contents[0]
        else:
            # where the tag is None
            aff_tag = xml_content
        tag_content = parser.format_aff(aff_tag)
        self.assertEqual(expected, tag_content)


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
        ("elife_poa_e06828.xml", "Michael S Fleming et al."),
        ("elife00351.xml", "Richard Smith"),
        )
    def test_author_line(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(parser.author_line(soup), expected)


    @data(
        # standard expected author with name tag
        (read_fixture('test_format_contributor', 'content_01.xml'),
         read_fixture('test_format_contributor', 'content_01_expected.py'),
        ),
        # edge case, no valid contrib tags
        (read_fixture('test_format_contributor', 'content_02.xml'),
         read_fixture('test_format_contributor', 'content_02_expected.py'),
        ),
        # edge case, string-name wrapper
        (read_fixture('test_format_contributor', 'content_03.xml'),
         read_fixture('test_format_contributor', 'content_03_expected.py'),
        ),
        # edge case, incorrect aff tag xref values will not cause an error if aff tag is not found
        (read_fixture('test_format_contributor', 'content_04.xml'),
         read_fixture('test_format_contributor', 'content_04_expected.py'),
        ),
    )
    @unpack
    def test_format_contributor_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        contrib_tag = raw_parser.article_contributors(soup)[0]
        tag_content = parser.format_contributor(contrib_tag, soup)
        self.assertEqual(expected, tag_content)


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
        # example of clinical trial contributors
         (read_fixture('test_references_json_authors', 'content_01.py'),
         OrderedDict([('type', u'clinical-trial')]),
         read_fixture('test_references_json_authors', 'content_01_expected.py'),
         ),
        # example of patent contributors
         (read_fixture('test_references_json_authors', 'content_02.py'),
         OrderedDict([('type', u'patent')]),
         read_fixture('test_references_json_authors', 'content_02_expected.py'),
         ),
        # example of thesis contributors
         (read_fixture('test_references_json_authors', 'content_03.py'),
         OrderedDict([('type', u'thesis')]),
         read_fixture('test_references_json_authors', 'content_03_expected.py'),
         ),
        )
    def test_references_json_authors(self, ref_authors, ref_content, expected):
        references_json = parser.references_json_authors(ref_authors, ref_content)
        self.assertEqual(expected, references_json)


    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00051.xml", "elife-10421-v1.xml", "elife-00666.xml")
    def test_references_json(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertNotEqual(parser.references_json(soup), None)


    @data(
        # Web reference with no title, use the uri from 01892
         (read_fixture('test_references_json', 'content_01.xml'),
          read_fixture('test_references_json', 'content_01_expected.py'),
         ),

        # Thesis title from 00626, also in converted to unknown because of its comment tag
         (read_fixture('test_references_json', 'content_02.xml'),
          read_fixture('test_references_json', 'content_02_expected.py'),
         ),

        # fpage value with usual characters from 00170
         (read_fixture('test_references_json', 'content_03.xml'),
          read_fixture('test_references_json', 'content_03_expected.py'),
         ),

        # fpage contains dots, 00569
         (read_fixture('test_references_json', 'content_04.xml'),
          read_fixture('test_references_json', 'content_04_expected.py'),
         ),

        # pages value of in press, 00109
         (read_fixture('test_references_json', 'content_05.xml'),
          read_fixture('test_references_json', 'content_05_expected.py'),
         ),

        # year value of in press, 02535
         (read_fixture('test_references_json', 'content_06.xml'),
          read_fixture('test_references_json', 'content_06_expected.py'),
         ),

        # conference, 03532 v3
         (read_fixture('test_references_json', 'content_07.xml'),
          read_fixture('test_references_json', 'content_07_expected.py'),
         ),

        # web with doi but no uri, 04775 v2
         (read_fixture('test_references_json', 'content_08.xml'),
          read_fixture('test_references_json', 'content_08_expected.py'),
         ),

        # Clinical trial example, from new kitchen sink 00666
         (read_fixture('test_references_json', 'content_09.xml'),
          read_fixture('test_references_json', 'content_09_expected.py'),
         ),

        # Journal reference with no article-title, 05462 v3
         (read_fixture('test_references_json', 'content_10.xml'),
          read_fixture('test_references_json', 'content_10_expected.py'),
         ),

        # book reference, gets converted to book-chapter, and has no editors, 16412 v1
         (read_fixture('test_references_json', 'content_11.xml'),
          read_fixture('test_references_json', 'content_11_expected.py'),
         ),

        # journal reference with no article title and no lpage, 11282 v2
         (read_fixture('test_references_json', 'content_12.xml'),
          read_fixture('test_references_json', 'content_12_expected.py'),
         ),

        # reference with no title uses detail as the titel, 00311 v1
         (read_fixture('test_references_json', 'content_13.xml'),
          read_fixture('test_references_json', 'content_13_expected.py'),
         ),

        # reference of type other with no details, 15266 v1
         (read_fixture('test_references_json', 'content_14.xml'),
          read_fixture('test_references_json', 'content_14_expected.py'),
         ),

        # reference of type journal with no journal name, 00340 v1
         (read_fixture('test_references_json', 'content_15.xml'),
          read_fixture('test_references_json', 'content_15_expected.py'),
         ),

        # reference of type book with no source, 00051 v1
         (read_fixture('test_references_json', 'content_16.xml'),
          read_fixture('test_references_json', 'content_16_expected.py'),
         ),

        # reference of type book with no publisher, 00031 v1
         (read_fixture('test_references_json', 'content_17.xml'),
          read_fixture('test_references_json', 'content_17_expected.py'),
         ),

        # reference of type book with no bookTitle, 03069 v2
         (read_fixture('test_references_json', 'content_18.xml'),
          read_fixture('test_references_json', 'content_18_expected.py'),
         ),

        # reference with unicode in collab tag, also gets turned into unknown type, 18023 v1
         (read_fixture('test_references_json', 'content_19.xml'),
          read_fixture('test_references_json', 'content_19_expected.py'),
         ),

        # data reference with no source, 16800 v2
         (read_fixture('test_references_json', 'content_20.xml'),
          read_fixture('test_references_json', 'content_20_expected.py'),
         ),

        # reference with an lpage and not fpage still gets pages value set, 13905 v2
         (read_fixture('test_references_json', 'content_21.xml'),
          read_fixture('test_references_json', 'content_21_expected.py'),
         ),

        # Reference with a collab using italic tag, from 05423 v2
         (read_fixture('test_references_json', 'content_22.xml'),
          read_fixture('test_references_json', 'content_22_expected.py'),
         ),

        # Reference with a non-numeric year, from 09215 v1
         (read_fixture('test_references_json', 'content_23.xml'),
          read_fixture('test_references_json', 'content_23_expected.py'),
         ),

        # no year value, 00051, with json rewriting enabled by adding elife XML metadata
         (read_fixture('test_references_json', 'content_24.xml'),
          read_fixture('test_references_json', 'content_24_expected.py'),
         ),

        # elife 12125 v3 bib11 will get deleted in the JSON rewriting
         (read_fixture('test_references_json', 'content_25.xml'),
          read_fixture('test_references_json', 'content_25_expected.py'),
         ),

        # 19532 v2 bib27 has a date-in-citation and no year tag, will get rewritten
         (read_fixture('test_references_json', 'content_26.xml'),
          read_fixture('test_references_json', 'content_26_expected.py'),
         ),

        # 00666 kitchen sink reference of type patent
         (read_fixture('test_references_json', 'content_27.xml'),
          read_fixture('test_references_json', 'content_27_expected.py'),
         ),

        # 20352 v2 reference of type patent, with a rewrite of the country value
         (read_fixture('test_references_json', 'content_28.xml'),
          read_fixture('test_references_json', 'content_28_expected.py'),
         ),

        # 20492 v3, report type reference with no publisher-name gets converted to unknown
         (read_fixture('test_references_json', 'content_29.xml'),
          read_fixture('test_references_json', 'content_29_expected.py'),
         ),

        # 15504 v2, reference with a pmid
         (read_fixture('test_references_json', 'content_30.xml'),
          read_fixture('test_references_json', 'content_30_expected.py'),
         ),

        # 15504 v2, reference with an isbn
         (read_fixture('test_references_json', 'content_31.xml'),
          read_fixture('test_references_json', 'content_31_expected.py'),
         ),

        # 18296 v3, reference of type preprint
         (read_fixture('test_references_json', 'content_32.xml'),
          read_fixture('test_references_json', 'content_32_expected.py'),
         ),

        # 16394 v2, reference of type thesis with no publisher, convert to unknown
         (read_fixture('test_references_json', 'content_33.xml'),
          read_fixture('test_references_json', 'content_33_expected.py'),
         ),

        # 09672 v2, reference of type conference-proceeding with no conference
         (read_fixture('test_references_json', 'content_34.xml'),
          read_fixture('test_references_json', 'content_34_expected.py'),
         ),

        # 07460 v1, reference rewriting test, rewrites date and authors
         (read_fixture('test_references_json', 'content_35.xml'),
          read_fixture('test_references_json', 'content_35_expected.py'),
         ),

        # 20522 v1, reference rewriting year value in json output
         (read_fixture('test_references_json', 'content_36.xml'),
          read_fixture('test_references_json', 'content_36_expected.py'),
         ),

        # 09520 v2, reference rewriting conference data
         (read_fixture('test_references_json', 'content_37.xml'),
          read_fixture('test_references_json', 'content_37_expected.py'),
        ),

        # from 00666 kitchen sink example, will add a uri to the references json from the doi value
         (read_fixture('test_references_json', 'content_38.xml'),
          read_fixture('test_references_json', 'content_38_expected.py'),
         ),

        # from 00666 kitchen sink example, reference of type periodical
         (read_fixture('test_references_json', 'content_39.xml'),
          read_fixture('test_references_json', 'content_39_expected.py'),
         ),

         # 00666 kitchen sink example with a version tag
         (read_fixture('test_references_json', 'content_40.xml'),
          read_fixture('test_references_json', 'content_40_expected.py'),
        ),

         # 23193 v2 book references has editors and no authors
         (read_fixture('test_references_json', 'content_41.xml'),
          read_fixture('test_references_json', 'content_41_expected.py'),
        ),

         # example of data citation with a pub-id accession, based on article 07836
         (read_fixture('test_references_json', 'content_42.xml'),
          read_fixture('test_references_json', 'content_42_expected.py'),
        ),

         # example of data citation with a object-id tag accession, gets converted to unknown because of the comment tag, based on article 07048
         (read_fixture('test_references_json', 'content_43.xml'),
          read_fixture('test_references_json', 'content_43_expected.py'),
        ),

         # example of data citation with a pub-id pub-id-type="archive", parse it as an accession number, based on 00666 kitchen sink example
         (read_fixture('test_references_json', 'content_44.xml'),
          read_fixture('test_references_json', 'content_44_expected.py'),
        ),
        )
    @unpack
    def test_references_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.references_json(soup)
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
        (None, None, None, None, None, None, None, None, None),
        ('title', None, None, None, None, None, 'title', None, None),
        (None, 'label', None, None, None, None, None, 'label', None),
        ('title', 'label', 'caption', None, None, None, 'title', 'label', None),
        ('title', 'label', 'caption', True, None, None, 'title', 'label', 'caption'),
        (None, 'label', None, None, True, None, 'label', None, None),
        (None, 'label', None, None, True, True, 'label', None, None),
        ('title', None, None, None, True, True, None, 'title', None),
        ('title', None, None, None, None, True, None, 'title', None),
        ('title', 'label', None, None, True, None, 'title', 'label', None),
        ('title.', None, None, None, None, True, None, 'title', None),
        (None, 'label:', None, None, True, None, 'label:', None, None),
    )
    def test_body_block_title_label_caption(self, title_value, label_value, caption_content,
                                            set_caption, prefer_title, prefer_label,
                                            expected_title, expected_label, expected_caption):
        tag_content = OrderedDict()
        parser.body_block_title_label_caption(tag_content, title_value, label_value,
                                              caption_content, set_caption,
                                              prefer_title, prefer_label)
        self.assertEqual(tag_content.get('label'), expected_label)
        self.assertEqual(tag_content.get('title'), expected_title)
        self.assertEqual(tag_content.get('caption'), expected_caption)


    @unpack
    @data(
         (read_fixture('test_body_block_content', 'content_01.xml'),
          read_fixture('test_body_block_content', 'content_01_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_02.xml'),
          read_fixture('test_body_block_content', 'content_02_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_03.xml'),
          read_fixture('test_body_block_content', 'content_03_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_04.xml'),
          read_fixture('test_body_block_content', 'content_04_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_05.xml'),
          read_fixture('test_body_block_content', 'content_05_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_06.xml'),
          read_fixture('test_body_block_content', 'content_06_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_07.xml'),
          read_fixture('test_body_block_content', 'content_07_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_08.xml'),
          read_fixture('test_body_block_content', 'content_08_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_09.xml'),
          read_fixture('test_body_block_content', 'content_09_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_10.xml'),
          read_fixture('test_body_block_content', 'content_10_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_11.xml'),
          read_fixture('test_body_block_content', 'content_11_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_12.xml'),
          read_fixture('test_body_block_content', 'content_12_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_13.xml'),
          read_fixture('test_body_block_content', 'content_13_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_14.xml'),
          read_fixture('test_body_block_content', 'content_14_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_15.xml'),
          read_fixture('test_body_block_content', 'content_15_expected.py'),
         ),

        # example of copyright statements ending in a full stop, based on article 27041
         (read_fixture('test_body_block_content', 'content_16.xml'),
          read_fixture('test_body_block_content', 'content_16_expected.py'),
         ),

         # example of video with attributions, based on article 17243
         (read_fixture('test_body_block_content', 'content_17.xml'),
          read_fixture('test_body_block_content', 'content_17_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_18.xml'),
          read_fixture('test_body_block_content', 'content_18_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_19.xml'),
          read_fixture('test_body_block_content', 'content_19_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_20.xml'),
          read_fixture('test_body_block_content', 'content_20_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_21.xml'),
          read_fixture('test_body_block_content', 'content_21_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_22.xml'),
          read_fixture('test_body_block_content', 'content_22_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_23.xml'),
          read_fixture('test_body_block_content', 'content_23_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_24.xml'),
          read_fixture('test_body_block_content', 'content_24_expected.py'),
         ),

        # media tag that is not a video
         (read_fixture('test_body_block_content', 'content_25.xml'),
          read_fixture('test_body_block_content', 'content_25_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_26.xml'),
          read_fixture('test_body_block_content', 'content_26_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_27.xml'),
          read_fixture('test_body_block_content', 'content_27_expected.py'),
         ),

         (read_fixture('test_body_block_content', 'content_28.xml'),
          read_fixture('test_body_block_content', 'content_28_expected.py'),
         ),

        # disp-quote content-type="editor-comment" is turned into an excerpt block
         (read_fixture('test_body_block_content', 'content_29.xml'),
          read_fixture('test_body_block_content', 'content_29_expected.py'),
         ),

        # 00109 v1, figure with a supplementary file that has multiple caption paragraphs
         (read_fixture('test_body_block_content', 'content_30.xml'),
          read_fixture('test_body_block_content', 'content_30_expected.py'),
         ),

        # code block, based on elife 20352 v2, contains new lines too
         (read_fixture('test_body_block_content', 'content_31.xml'),
          read_fixture('test_body_block_content', 'content_31_expected.py'),
         ),

        # example of a table with a break tag, based on 7141 v1
         (read_fixture('test_body_block_content', 'content_32.xml'),
          read_fixture('test_body_block_content', 'content_32_expected.py'),
         ),

        # example of a figure, based on 00007 v1
         (read_fixture('test_body_block_content', 'content_33.xml'),
          read_fixture('test_body_block_content', 'content_33_expected.py'),
         ),

        # example table with a caption and no title needs a title added, based on 05604 v1
         (read_fixture('test_body_block_content', 'content_34.xml'),
          read_fixture('test_body_block_content', 'content_34_expected.py'),
         ),

        # example video with only the DOI in the caption paragraph, based on 02277 v1
         (read_fixture('test_body_block_content', 'content_35.xml'),
          read_fixture('test_body_block_content', 'content_35_expected.py'),
         ),

        # example animated gif as a video in 00666 kitchen sink
         (read_fixture('test_body_block_content', 'content_36.xml'),
          read_fixture('test_body_block_content', 'content_36_expected.py'),
         ),


        # example of named-content to be converted to HTML from new kitchen sink 00666
         (read_fixture('test_body_block_content', 'content_37.xml'),
          read_fixture('test_body_block_content', 'content_37_expected.py'),
         ),

        # example of table author-callout-style styles to replace as a class attribute, based on 24231 v1
         (read_fixture('test_body_block_content', 'content_38.xml'),
          read_fixture('test_body_block_content', 'content_38_expected.py'),
         ),

        # example inline table adapted from 00666 kitchen sink
         (read_fixture('test_body_block_content', 'content_39.xml'),
          read_fixture('test_body_block_content', 'content_39_expected.py'),
         ),

        # example key resources inline table that has a label will be turned into a figure block
         (read_fixture('test_body_block_content', 'content_40.xml'),
          read_fixture('test_body_block_content', 'content_40_expected.py'),
         ),

        )
    def test_body_block_content(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        # find the first tag in the root with a name
        for child in soup.root.children:
            if child.name:
                body_tag = child
                break
        tag_content = parser.body_block_content(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (read_fixture('test_body_block_content_render', 'content_01.xml'),
         read_fixture('test_body_block_content_render', 'content_01_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_02.xml'),
         read_fixture('test_body_block_content_render', 'content_02_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_03.xml'),
         read_fixture('test_body_block_content_render', 'content_03_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_04.xml'),
         read_fixture('test_body_block_content_render', 'content_04_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_05.xml'),
         read_fixture('test_body_block_content_render', 'content_05_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_06.xml'),
         read_fixture('test_body_block_content_render', 'content_06_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_07.xml'),
         read_fixture('test_body_block_content_render', 'content_07_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_08.xml'),
         read_fixture('test_body_block_content_render', 'content_08_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_09.xml'),
         read_fixture('test_body_block_content_render', 'content_09_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_10.xml'),
         read_fixture('test_body_block_content_render', 'content_10_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_11.xml'),
         read_fixture('test_body_block_content_render', 'content_11_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_12.xml'),
         read_fixture('test_body_block_content_render', 'content_12_expected.py'),
         ),

        (read_fixture('test_body_block_content_render', 'content_13.xml'),
         read_fixture('test_body_block_content_render', 'content_13_expected.py'),
         ),

        # disp-quote content-type="editor-comment" is turned into an excerpt block
        (read_fixture('test_body_block_content_render', 'content_14.xml'),
         read_fixture('test_body_block_content_render', 'content_14_expected.py'),
         ),

        # Boxed text with no title tag uses the first sentence of the caption paragraph, 00288 v1
        (read_fixture('test_body_block_content_render', 'content_15.xml'),
         read_fixture('test_body_block_content_render', 'content_15_expected.py'),
         ),

        # Example of boxed-text with content inside its caption tag
        (read_fixture('test_body_block_content_render', 'content_16.xml'),
         read_fixture('test_body_block_content_render', 'content_16_expected.py'),
         ),

        # code block, based on elife 20352 v2, contains new lines too
        (read_fixture('test_body_block_content_render', 'content_17.xml'),
         read_fixture('test_body_block_content_render', 'content_17_expected.py'),
         ),

        # Example of monospace tags
        (read_fixture('test_body_block_content_render', 'content_18.xml'),
         read_fixture('test_body_block_content_render', 'content_18_expected.py'),
         ),

        # example of a table to not pickup a child element title, based on 22264 v2
        (read_fixture('test_body_block_content_render', 'content_19.xml'),
         read_fixture('test_body_block_content_render', 'content_19_expected.py'),
         ),

        # example table: a label, no title, no caption
        (read_fixture('test_body_block_content_render', 'content_20.xml'),
         read_fixture('test_body_block_content_render', 'content_20_expected.py'),
         ),

        # example table: a label, a title, no caption
        (read_fixture('test_body_block_content_render', 'content_21.xml'),
         read_fixture('test_body_block_content_render', 'content_21_expected.py'),
         ),

        # example table: a label, no title, a caption
        (read_fixture('test_body_block_content_render', 'content_22.xml'),
         read_fixture('test_body_block_content_render', 'content_22_expected.py'),
         ),

        # example table: a label, a title, and a caption
        (read_fixture('test_body_block_content_render', 'content_23.xml'),
         read_fixture('test_body_block_content_render', 'content_23_expected.py'),
         ),

        # example table: no label, no title, and a caption
        (read_fixture('test_body_block_content_render', 'content_24.xml'),
         read_fixture('test_body_block_content_render', 'content_24_expected.py'),
         ),

        # example fig with a caption and no title, based on 00281 v1
        (read_fixture('test_body_block_content_render', 'content_25.xml'),
         read_fixture('test_body_block_content_render', 'content_25_expected.py'),
         ),

        # example media with a label and no title, based on 00007 v1
        (read_fixture('test_body_block_content_render', 'content_26.xml'),
         read_fixture('test_body_block_content_render', 'content_26_expected.py'),
         ),

        # example test from 02935 v2 of list within a list to not add child list-item to the parent list twice
        (read_fixture('test_body_block_content_render', 'content_27.xml'),
         read_fixture('test_body_block_content_render', 'content_27_expected.py'),
         ),

        # example list from 00666 kitchen sink with paragraphs and list inside a list-item
        (read_fixture('test_body_block_content_render', 'content_28.xml'),
         read_fixture('test_body_block_content_render', 'content_28_expected.py'),
         ),

        # example of a video inside a fig group based on 00666 kitchen sink
        (read_fixture('test_body_block_content_render', 'content_29.xml'),
         read_fixture('test_body_block_content_render', 'content_29_expected.py'),
         ),

        # example of a video as supplementary material inside a fig-group based on 06726 v2
        (read_fixture('test_body_block_content_render', 'content_30.xml'),
         read_fixture('test_body_block_content_render', 'content_30_expected.py'),
         ),

        # example of fig supplementary-material with only a title tag, based on elife-26759-v1.xml except
        #  this example is fixed so the caption tag wraps the entire caption, and values are abbreviated
        #  to test how the punctuation is stripped from the end of the supplementary-material title value
        #  when it is converted to a label
        (read_fixture('test_body_block_content_render', 'content_31.xml'),
         read_fixture('test_body_block_content_render', 'content_31_expected.py'),
        ),

        )
    def test_body_block_content_render(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.body_block_content_render(soup.contents[0])
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        (read_fixture('test_render_raw_body', 'content_01.xml'),
         read_fixture('test_render_raw_body', 'content_01_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_02.xml'),
         read_fixture('test_render_raw_body', 'content_02_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_03.xml'),
         read_fixture('test_render_raw_body', 'content_03_expected.py'),
         ),

        # Below when there is a space between paragraph tags, it should not render as a paragraph
        (read_fixture('test_render_raw_body', 'content_04.xml'),
         read_fixture('test_render_raw_body', 'content_04_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_05.xml'),
         read_fixture('test_render_raw_body', 'content_05_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_06.xml'),
         read_fixture('test_render_raw_body', 'content_06_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_07.xml'),
         read_fixture('test_render_raw_body', 'content_07_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_08.xml'),
         read_fixture('test_render_raw_body', 'content_08_expected.py'),
         ),

        (read_fixture('test_render_raw_body', 'content_09.xml'),
         read_fixture('test_render_raw_body', 'content_09_expected.py'),
         ),

        # excerpt from 00646 v1 with a boxed-text inline-graphic
        (read_fixture('test_render_raw_body', 'content_10.xml'),
         read_fixture('test_render_raw_body', 'content_10_expected.py'),
        ),
    )
    def test_render_raw_body(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.render_raw_body(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        (read_fixture('test_abstract_json', 'content_01.xml'),
         read_fixture('test_abstract_json', 'content_01_expected.py'),
         ),

        # executive-summary will return None
        (read_fixture('test_abstract_json', 'content_02.xml'),
         read_fixture('test_abstract_json', 'content_02_expected.py'),
         ),

        # test lots of inline tagging
        (read_fixture('test_abstract_json', 'content_03.xml'),
         read_fixture('test_abstract_json', 'content_03_expected.py'),
         ),

        )
    def test_abstract_json(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstract_json(soup.contents[0])
        self.assertEqual(expected, tag_content)


    @unpack
    @data(
        (read_fixture('test_digest_json', 'content_01.xml'),
         read_fixture('test_digest_json', 'content_01_expected.py'),
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
        date_tag = raw_parser.pub_date(soup, date_type=test_date_type)[0]
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
        self.assertEqual(expected_xml, unicode_value(tag_copy))

    """
    Functions that require more than one argument to test against json output
    """

    @unpack
    @data(
        # typical eLife format
        (read_fixture('test_journal_issn', 'content_01.xml'),
         'electronic',
         None,
         '2050-084X'
         ),

        # eLife format with specifying the publication format
        (read_fixture('test_journal_issn', 'content_02.xml'),
         None,
         None,
         '2050-084X'
         ),

        # a non-eLife format
        (read_fixture('test_journal_issn', 'content_03.xml'),
         None,
         'epub',
         '2057-4991'
         ),

        )
    def test_journal_issn_edge_cases(self, xml_content, pub_format, pub_type, expected):
        soup = parser.parse_xml(xml_content)
        content_tag = soup.contents[0]
        tag_content = parser.journal_issn(content_tag, pub_format=pub_format, pub_type=pub_type)
        self.assertEqual(expected, tag_content)

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

    @unpack
    @data(
        # example based on eLife format
        (read_fixture('test_abstract', 'content_01.xml'),
         read_fixture('test_abstract', 'content_01_expected.py'),
        ),

        # example based on BMJ Open bmjopen-4-e003269.xml
        (read_fixture('test_abstract', 'content_02.xml'),
         read_fixture('test_abstract', 'content_02_expected.py'),
        ),
    )
    def test_abstract_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.abstract(soup)
        self.assertEqual(expected, tag_content)

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
        expected = self.json_expected(filename, "authors_non_byline")
        actual = parser.authors_non_byline(self.soup(filename))
        self.assertEqual(expected, actual)

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
        expected = self.json_expected(filename, "conflict")
        actual = parser.conflict(self.soup(filename))
        self.assertEqual(expected, actual)

    @data("elife-kitchen-sink.xml", "elife-02833-v2.xml", "elife-00666.xml")
    def test_contributors(self, filename):
        expected = self.json_expected(filename, "contributors")
        actual = parser.contributors(self.soup(filename))
        self.assertEqual(expected, actual)

    @data("elife-kitchen-sink.xml")
    def test_copyright_holder(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_holder"), parser.copyright_holder(self.soup(filename)))

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_copyright_holder_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.copyright_holder(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        ('elife-kitchen-sink.xml', u'Alegado et al.'),
        ('elife00240.xml', u'Pickett'),
        ('elife09853.xml', 'Becker and Gitler'),
        ('elife02935.xml', None)
        )
    def test_copyright_holder_json(self, filename, expected):
        soup = parser.parse_document(sample_xml(filename))
        self.assertEqual(expected, parser.copyright_holder_json(soup))

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_copyright_holder_json_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.copyright_holder_json(body_tag)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_copyright_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_statement"),
                         parser.copyright_statement(self.soup(filename)))

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_copyright_statement_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.copyright_statement(body_tag)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml")
    def test_copyright_year(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_year"),
                         parser.copyright_year(self.soup(filename)))

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_copyright_year_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.copyright_year(body_tag)
        self.assertEqual(expected, tag_content)

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

    @data(
        # edge case, no id attribute on award-group tag, and id will be generated, based on 10.1098/rsob.150230
        ('''<root>
            <article>
            <front>
            <article-meta>
            <funding-group specific-use="FundRef">
            <award-group>
            <funding-source>
            <institution-wrap>
            <institution>Grant-in-Aid for Scientific Research (S) from the Ministry of Education, Culture, Sports, Science and Technology (MEXT) of Japan</institution>
            </institution-wrap>
            </funding-source>
            </award-group>
            </funding-group>
            <funding-group specific-use="FundRef">
            <award-group>
            <funding-source>
            <institution-wrap>
            <institution>Wellcome Trust</institution>
            <institution-id>http://dx.doi.org/10.13039/100004440</institution-id>
            </institution-wrap>
            </funding-source>
            <award-id>077707</award-id>
            <award-id>084229</award-id>
            <award-id>091020</award-id>
            <award-id>092076</award-id>
            <award-id>107022</award-id>
            </award-group>
            </funding-group>
            </article-meta>
            </front>
            </article>
         </root>''',
        [
            {'award-group-1': {
                'institution': 'Grant-in-Aid for Scientific Research (S) from the Ministry of Education, Culture, Sports, Science and Technology (MEXT) of Japan'}
            }, {'award-group-2': {
                'award-id': u'077707', 'institution': u'Wellcome Trust', 'id': u'http://dx.doi.org/10.13039/100004440'}
            }
        ]
        ),
        )
    @unpack
    def test_full_award_groups_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.full_award_groups(body_tag)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife-02833-v2.xml")
    def test_full_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "full_correspondence"),
                         parser.full_correspondence(self.soup(filename)))

    @data(
        # edge case, no id attribute on corresp tag, will be empty but not cause an error, based on 10.2196/resprot.3838
        ('<root><article><author-notes><corresp>Corresponding Author: Elisa J Gordon<email>eg@example.org</email></corresp></author-notes></article></root>',
        {}
        ),
        )
    @unpack
    def test_full_correspondence_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.full_correspondence(body_tag)
        self.assertEqual(expected, tag_content)

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

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_full_license_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.full_license(body_tag)
        self.assertEqual(expected, tag_content)

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

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_license_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.license(body_tag)
        self.assertEqual(expected, tag_content)

    @unpack
    @data(
        # example license from 00666
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article-meta><permissions><copyright-statement>© 2016, Harrison et al</copyright-statement><copyright-year>2016</copyright-year><copyright-holder>Harrison et al</copyright-holder><ali:free_to_read/><license xlink:href="http://creativecommons.org/licenses/by/4.0/"><ali:license_ref>http://creativecommons.org/licenses/by/4.0/</ali:license_ref><license-p>This article is distributed under the terms of the <ext-link ext-link-type="uri" xlink:href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution License</ext-link>, which permits unrestricted use and redistribution provided that the original author and source are credited.</license-p></license></permissions></article-meta></root>',
        'This article is distributed under the terms of the <a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution License</a>, which permits unrestricted use and redistribution provided that the original author and source are credited.'
        ),
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
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

    @data(
        # edge case, no permissions tag
        ('<root><article></article></root>',
         None
        )
    )
    @unpack
    def test_license_url_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0]
        tag_content = parser.license_url(body_tag)
        self.assertEqual(expected, tag_content)

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife00007.xml", "elife04953.xml",
          "elife00005.xml", "elife05031.xml", "elife04493.xml", "elife06726.xml")
    def test_media(self, filename):
        self.assertEqual(self.json_expected(filename, "media"),
                         parser.media(self.soup(filename)))

    @unpack
    @data(
        # pub-date values from 00666 kitchen sink
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><pub-date publication-format="electronic" date-type="update"><day>11</day><month>08</month><year>2016</year></pub-date><pub-date publication-format="electronic" date-type="publication"><day>25</day><month>04</month><year>2016</year></pub-date><pub-date pub-type="collection"><year>2016</year></pub-date></article></root>',
        [
            OrderedDict([
                ('publication-format', u'electronic'),
                ('date-type', u'update'),
                ('day', u'11'),
                ('month', u'08'),
                ('year', u'2016'),
                (u'date', date_struct(2016, 8, 11))
            ]),
            OrderedDict([
                ('publication-format', u'electronic'),
                ('date-type', u'publication'),
                ('day', u'25'),
                ('month', u'04'),
                ('year', u'2016'),
                (u'date', date_struct(2016, 4, 25))
            ]),
            OrderedDict([
                ('pub-type', u'collection'),
                ('day', None),
                ('month', None),
                ('year', u'2016'),
                (u'date', date_struct(2016, 1, 1))
            ]),
        ]
        ),

        # example from cstp77
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><pub-date publication-format="electronic" date-type="pub" iso-8601-date="2017-07-04"><day>04</day><month>07</month><year>2017</year></pub-date></article></root>',
        [
            OrderedDict([
                ('publication-format', u'electronic'),
                ('date-type', u'pub'),
                ('day', u'04'),
                ('month', u'07'),
                ('year', u'2017'),
                (u'date', date_struct(2017, 7, 4))
            ])
        ]
        ),

        # example from bmjopen-2013-003269
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><pub-date pub-type="ppub"><month>1</month><year>2014</year></pub-date><pub-date pub-type="epub-original"><day>30</day><month>1</month><year>2014</year></pub-date><pub-date pub-type="epub"><day>31</day><month>1</month><year>2014</year></pub-date></article></root>',
        [
            OrderedDict([
                ('pub-type', u'ppub'),
                ('day', None),
                ('month', u'1'),
                ('year', u'2014'),
                (u'date', date_struct(2014, 1, 1))
            ]),
            OrderedDict([
                ('pub-type', u'epub-original'),
                ('day', u'30'),
                ('month', u'1'),
                ('year', u'2014'),
                (u'date', date_struct(2014, 1, 30))
            ]),
            OrderedDict([
                ('pub-type', u'epub'),
                ('day',  u'31'),
                ('month', u'1'),
                ('year', u'2014'),
                (u'date', date_struct(2014, 1, 31))
            ]),
        ]
        ),
    )
    def test_pub_dates_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.pub_dates(soup)
        self.assertEqual(expected, tag_content)


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

    @unpack
    @data(
         # non-elife example with issue tag from cstp77
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">10.5334/cstp.77</article-id></article-meta></front><back>
<ref-list><ref id="B7">
<label>7</label>
<element-citation publication-type="journal">
<person-group person-group-type="author">
<name>
<surname>Conrad</surname>
<given-names>C.C.</given-names>
</name>
<name>
<surname>Hilchey</surname>
<given-names>K.G.</given-names>
</name>
</person-group>
<article-title>A review of citizen science and community-based environmental monitoring: Issues and opportunities</article-title>
<source>Environmental Monitoring and Assessment</source>
<year iso-8601-date="2011">2011</year>
<volume>176</volume>
<issue>1&#8211;4</issue>
<fpage>273</fpage>
<lpage>291</lpage>
<pub-id pub-id-type="doi">10.1007/s10661-010-1582-5</pub-id>
</element-citation>
</ref></ref-list></back></article></root>''',
        [{
            'article_doi': u'10.5334/cstp.77',
            'article_title': u'A review of citizen science and community-based environmental monitoring: Issues and opportunities',
            'authors': [{
                'given-names': u'C.C.',
                'group-type': u'author',
                'surname': u'Conrad'
                },
                {
                'given-names': u'K.G.',
                'group-type': u'author',
                'surname': u'Hilchey'
                }],
            'doi': u'10.1007/s10661-010-1582-5',
            'fpage': u'273',
            'full_article_title': u'A review of citizen science and community-based environmental monitoring: Issues and opportunities',
            'id': u'B7',
            'issue': u'1\u20134',
            'lpage': u'291',
            'position': 1,
            'publication-type': u'journal',
            'ref': u'7 Conrad C.C. Hilchey K.G. A review of citizen science and community-based environmental monitoring: Issues and opportunities Environmental Monitoring and Assessment 2011 176 1\u20134 273 291 10.1007/s10661-010-1582-5',
            'reference_id': u'10.1007/s10661-010-1582-5',
            'source': u'Environmental Monitoring and Assessment',
            'volume': u'176',
            'year': u'2011',
            'year-iso-8601-date': u'2011'
        }]
        ),

        # mixed-citation example 1 from bmjopen
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">10.1136/bmjopen-2013-003269</article-id></article-meta></front><back><ref-list><title>References</title><ref id="R15"><label>15</label><mixed-citation><person-group person-group-type="author"><name><surname>Atkinson</surname><given-names>W</given-names></name><name><surname>Hamborsky</surname><given-names>J</given-names></name><name><surname>McIntyre</surname><given-names>L</given-names></name><etal/></person-group>. <source>Epidemiology and prevention of vaccine-preventable diseases</source>. <publisher-loc>Washington, DC</publisher-loc>: <publisher-name>Public Health Foundation</publisher-name>, <year>2008</year>.</mixed-citation></ref></ref-list></back></article></root>''',
        [{
            'article_doi': u'10.1136/bmjopen-2013-003269',
            'authors': [{
                'given-names': u'W',
                'group-type': u'author',
                'surname': u'Atkinson'
                },
                {
                'given-names': u'J',
                'group-type': u'author',
                'surname': u'Hamborsky'
                },
                {
                'given-names': u'L',
                'group-type': u'author',
                'surname': u'McIntyre'
                },
                {
                'etal': True,
                'group-type': u'author'
                }],
            'id': u'R15',
            'position': 1,
            'publisher_loc': u'Washington, DC',
            'publisher_name': u'Public Health Foundation',
            'ref': u'15AtkinsonWHamborskyJMcIntyreL. Epidemiology and prevention of vaccine-preventable diseases. Washington, DC: Public Health Foundation, 2008.',
            'source': u'Epidemiology and prevention of vaccine-preventable diseases',
            'year': u'2008'
        }]
        ),

        # mixed-citation example 2 from bmjopen
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">10.1136/bmjopen-2013-003269</article-id></article-meta></front><back><ref-list><title>References</title><ref id="R29"><label>29</label><mixed-citation><person-group person-group-type="author"><name><surname>Armah</surname><given-names>GE</given-names></name><name><surname>Steele</surname><given-names>AD</given-names></name><name><surname>Esona</surname><given-names>MD</given-names></name><etal/></person-group>. <article-title>Diversity of rotavirus strains circulating in West Africa from 1996 to 2000</article-title>. <source>J Infect Dis</source> <year>2010</year>;<volume>202</volume><issue>(Suppl)</issue>:<fpage>S64</fpage>–<lpage>71</lpage>.</mixed-citation></ref></ref-list></back></article></root>''',
        [{
            'article_doi': u'10.1136/bmjopen-2013-003269',
            'article_title': u'Diversity of rotavirus strains circulating in West Africa from 1996 to 2000',
            'authors': [{
                'given-names': u'GE',
                'group-type': u'author',
                'surname': u'Armah'
                },
                {
                'given-names': u'AD',
                'group-type': u'author',
                'surname': u'Steele'
                },
                {
                'given-names': u'MD',
                'group-type': u'author',
                'surname': u'Esona'
                },
                {
                'etal': True,
                'group-type': u'author'
                }],
            'fpage': u'S64',
            'full_article_title': u'Diversity of rotavirus strains circulating in West Africa from 1996 to 2000',
            'id': u'R29',
            'issue': u'(Suppl)',
            'lpage': u'71',
            'position': 1,
            'ref': u'29ArmahGESteeleADEsonaMD. Diversity of rotavirus strains circulating in West Africa from 1996 to 2000. J Infect Dis 2010;202(Suppl):S64\u201371.',
            'source': u'J Infect Dis',
            'volume': u'202',
            'year': u'2010'
        }]
        ),

        # mixed-citation example 3 from bmjopen
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">10.1136/bmjopen-2013-003269</article-id></article-meta></front><back>
<ref-list><title>References</title><ref id="R31"><label>31</label><mixed-citation><collab>World Health Organization</collab>. <article-title>Rotavirus surveillance in the African Region. Updates of Rotavirus surveillance in the African Region</article-title>. <comment><ext-link xlink:href="http://www.afro.who.int/index.php?option=com_content&amp;view=article&amp;id=2486:rotavirus-surveillance-in-the-african-region&amp;catid=1980&amp;Itemid=2737" ext-link-type="uri">http://www.afro.who.int/index.php?option=com_content&amp;view=article&amp;id=2486:rotavirus-surveillance-in-the-african-region&amp;catid=1980&amp;Itemid=2737</ext-link> (accessed 26 Jul 2013</comment>).</mixed-citation></ref></ref-list></back></article></root>''',
        [{
            'article_doi': u'10.1136/bmjopen-2013-003269',
            'article_title': u'Rotavirus surveillance in the African Region. Updates of Rotavirus surveillance in the African Region',
            'authors': [{
                'collab': u'World Health Organization',
                'group-type': u'author',
                }],
            'collab': u'World Health Organization',
            'comment': u'http://www.afro.who.int/index.php?option=com_content&view=article&id=2486:rotavirus-surveillance-in-the-african-region&catid=1980&Itemid=2737 (accessed 26 Jul 2013',
            'full_article_title': u'Rotavirus surveillance in the African Region. Updates of Rotavirus surveillance in the African Region',
            'id': u'R31',
            'position': 1,
            'ref': u'31World Health Organization. Rotavirus surveillance in the African Region. Updates of Rotavirus surveillance in the African Region. http://www.afro.who.int/index.php?option=com_content&view=article&id=2486:rotavirus-surveillance-in-the-african-region&catid=1980&Itemid=2737 (accessed 26 Jul 2013).',
            'uri': u'http://www.afro.who.int/index.php?option=com_content&view=article&id=2486:rotavirus-surveillance-in-the-african-region&catid=1980&Itemid=2737',
            'uri_text': u'http://www.afro.who.int/index.php?option=com_content&view=article&id=2486:rotavirus-surveillance-in-the-african-region&catid=1980&Itemid=2737',
        }]
        ),

        # citation example from redalyc - udea
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">DOI:10.17533/udea.rfnsp.v34n2a02</article-id></article-meta></front><back>
<ref-list><ref id="redalyc_12045638002_ref32">
<label>1</label>
<mixed-citation> Al Sahaf OS, Vega–Carrascal I. Chemical composition of smoke produced by high–frequency electrosurgery. Ir J Med Sci. [Revista en Internet] 2007 [Acceso 13 de mayo de 2014]; 176(3):229–32. Disponible en:  <ext-link ext-link-type="uri" xlink:href="www.ncbi.nlm.nih.gov/pubmed/17653513">www.ncbi.nlm.nih.gov/pubmed/17653513</ext-link> </mixed-citation>
<element-citation publication-type="journal">
<person-group person-group-type="author">
<name>
<surname>Al</surname>
<given-names>Sahaf OS</given-names>
</name>
<name>
<surname>Vega–Carrascal</surname>
<given-names>I</given-names>
</name>
</person-group>
<source>Ir J Med Sci</source>
<year>2007</year>
</element-citation>
</ref>
</ref-list></back></article></root>''',
        [{
            'article_doi': u'DOI:10.17533/udea.rfnsp.v34n2a02',
            'authors': [{
                'given-names': u'Sahaf OS',
                'group-type': u'author',
                'surname': u'Al'
                },
                {
                'given-names': u'I',
                'group-type': u'author',
                'surname': u'Vega\u2013Carrascal'
                }],
            'id': u'redalyc_12045638002_ref32',
            'position': 1,
            'ref': u'1 Al Sahaf OS, Vega\u2013Carrascal I. Chemical composition of smoke produced by high\u2013frequency electrosurgery. Ir J Med Sci. [Revista en Internet] 2007 [Acceso 13 de mayo de 2014]; 176(3):229\u201332. Disponible en: www.ncbi.nlm.nih.gov/pubmed/17653513 Al Sahaf OS Vega\u2013Carrascal I Ir J Med Sci 2007',
            'publication-type': u'journal',
            'source': u'Ir J Med Sci',
            'uri': u'www.ncbi.nlm.nih.gov/pubmed/17653513',
            'uri_text': u'www.ncbi.nlm.nih.gov/pubmed/17653513',
            "year": "2007",
        }]
        ),

         # example of data citation with a pub-id accession, based on article 07836
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">10.5334/cstp.77</article-id></article-meta></front><back>
<ref-list><ref id="bib105">
<element-citation publication-type="data">
<person-group person-group-type="author">
<name>
<surname>Steinbaugh</surname>
<given-names>MJ</given-names>
</name>
<name>
<surname>Dreyfuss</surname>
<given-names>JM</given-names>
</name>
<name>
<surname>Blackwell</surname>
<given-names>TK</given-names>
</name>
</person-group>
<year iso-8601-date="2015">2015</year>
<data-title>
RNA-seq analysis of germline stem cell removal and loss of SKN-1 in c. elegans
</data-title>
<source>NCBI Gene Expression Omnibus</source>
<pub-id pub-id-type="accession" xlink:href="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63075">GSE63075</pub-id>
</element-citation>
</ref></ref-list></back></article></root>''',
        [
            {
                "data-title": "\nRNA-seq analysis of germline stem cell removal and loss of SKN-1 in c. elegans\n",
                "article_doi": "10.5334/cstp.77",
                "authors": [
                    {
                        "surname": "Steinbaugh",
                        "given-names": "MJ",
                        "group-type": "author"
                    },
                    {
                        "surname": "Dreyfuss",
                        "given-names": "JM",
                        "group-type": "author"
                    },
                    {
                        "surname": "Blackwell",
                        "given-names": "TK",
                        "group-type": "author"
                    }
                ],
                "accession": "GSE63075",
                "publication-type": "data",
                "source": "NCBI Gene Expression Omnibus",
                "year": "2015",
                "position": 1,
                "year-iso-8601-date": "2015",
                "ref": "Steinbaugh MJ Dreyfuss JM Blackwell TK 2015 RNA-seq analysis of germline stem cell removal and loss of SKN-1 in c. elegans NCBI Gene Expression Omnibus GSE63075",
                "id": "bib105"
            }
        ]
        ),

         # example of data citation with a object-id tag accession, based on article 07048
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><front><article-meta><article-id pub-id-type="doi">10.5334/cstp.77</article-id></article-meta></front><back>
<ref-list><ref id="bib15">
<element-citation publication-type="data">
<person-group person-group-type="author">
<name>
<surname>Bollag</surname>
<given-names>RJ</given-names>
</name>
<name>
<surname>Siegfried</surname>
<given-names>Z</given-names>
</name>
<name>
<surname>Cebra-Thomas</surname>
<given-names>J</given-names>
</name>
<name>
<surname>Garvey</surname>
<given-names>N</given-names>
</name>
<name>
<surname>Davison</surname>
<given-names>EM</given-names>
</name>
<name>
<surname>Silver</surname>
<given-names>LM</given-names>
</name>
</person-group>
<year>1994b</year>
<data-title>Mus musculus T-box 2 (Tbx2), mRNA</data-title>
<source>NCBI Nucleotide</source>
<object-id pub-id-type="art-access-id">NM_009324</object-id>
<comment>
<ext-link ext-link-type="uri" xlink:href="http://www.ncbi.nlm.nih.gov/nuccore/120407038">http://www.ncbi.nlm.nih.gov/nuccore/120407038</ext-link>
</comment>
</element-citation>
</ref></ref-list></back></article></root>''',
        [
            {
                "uri_text": "http://www.ncbi.nlm.nih.gov/nuccore/120407038",
                "comment": "\nhttp://www.ncbi.nlm.nih.gov/nuccore/120407038\n",
                "data-title": "Mus musculus T-box 2 (Tbx2), mRNA",
                "article_doi": "10.5334/cstp.77",
                "authors": [
                    {
                        "surname": "Bollag",
                        "given-names": "RJ",
                        "group-type": "author"
                    },
                    {
                        "surname": "Siegfried",
                        "given-names": "Z",
                        "group-type": "author"
                    },
                    {
                        "surname": "Cebra-Thomas",
                        "given-names": "J",
                        "group-type": "author"
                    },
                    {
                        "surname": "Garvey",
                        "given-names": "N",
                        "group-type": "author"
                    },
                    {
                        "surname": "Davison",
                        "given-names": "EM",
                        "group-type": "author"
                    },
                    {
                        "surname": "Silver",
                        "given-names": "LM",
                        "group-type": "author"
                    }
                ],
                "accession": "NM_009324",
                "uri": "http://www.ncbi.nlm.nih.gov/nuccore/120407038",
                "source": "NCBI Nucleotide",
                "year": "1994b",
                "position": 1,
                "publication-type": "data",
                "ref": "Bollag RJ Siegfried Z Cebra-Thomas J Garvey N Davison EM Silver LM 1994b Mus musculus T-box 2 (Tbx2), mRNA NCBI Nucleotide NM_009324 http://www.ncbi.nlm.nih.gov/nuccore/120407038",
                "id": "bib15"
            }
        ]
        ),

         # example of mixed-citation with string-name, based on non-elife article
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><back><ref-list><ref><mixed-citation publication-type="book" meta="no" id="c2"><person-group person-group-type="author"><string-name><surname>Frank</surname>, <given-names>A. W.</given-names></string-name></person-group> (<year>1995</year>). <source>The wounded storyteller: Body, illness, and ethics</source>. <publisher-loc>Chicago</publisher-loc>: <publisher-name>University of Chicago Press</publisher-name>.</mixed-citation></ref></ref-list></back></article></root>',
        [{
            'article_doi': None,
            'authors': [{
                'given-names': u'A. W.',
                'group-type': u'author',
                'surname': u'Frank'}],
            'position': 1,
            'publication-type': u'book',
            'publisher_loc': u'Chicago',
            'publisher_name': u'University of Chicago Press',
            'ref': u'Frank, A. W. (1995). The wounded storyteller: Body, illness, and ethics. Chicago: University of Chicago Press.',
            'source': u'The wounded storyteller: Body, illness, and ethics',
            'year': u'1995'
        }]
        ),

         # example of data citation with a pub-id pub-id-type="archive", parse it as an accession number, based on 00666 kitchen sink example
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><article><back><ref-list>    <ref id="bib34">
        <element-citation publication-type="data">
            <person-group person-group-type="author">
                <name>
                    <surname>Radoshevich</surname>
                    <given-names>L</given-names>
                </name>
                <name>
                    <surname>Impens</surname>
                    <given-names>F</given-names>
                </name>
                <name>
                    <surname>Ribet</surname>
                    <given-names>D</given-names>
                </name>
                <name>
                    <surname>Quereda</surname>
                    <given-names>JJ</given-names>
                </name>
                <name>
                    <surname>Nam Tham</surname>
                    <given-names>T</given-names>
                </name>
                <name>
                    <surname>Nahori</surname>
                    <given-names>MA</given-names>
                </name>
                <name>
                    <surname>Bierne</surname>
                    <given-names>H</given-names>
                </name>
                <name>
                    <surname>Dussurget</surname>
                    <given-names>O</given-names>
                </name>
                <name>
                    <surname>Pizarro-Cerdá</surname>
                    <given-names>J</given-names>
                </name>
                <name>
                    <surname>Knobeloch</surname>
                    <given-names>KP</given-names>
                </name>
                <name>
                    <surname>Cossart</surname>
                    <given-names>P</given-names>
                </name>
            </person-group>
            <year iso-8601-date="2015">2015a</year>
            <data-title>ISG15 counteracts <italic>Listeria monocytogenes</italic>
                infection</data-title>
            <source>ProteomeXchange</source>
            <pub-id pub-id-type="archive"
                xlink:href="http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD001805"
                >PXD001805</pub-id>
        </element-citation>
    </ref></ref-list></back></article></root>''',
        [{
        "data-title": u"ISG15 counteracts <italic>Listeria monocytogenes</italic>\n                infection",
        "article_doi": None,
        "authors": [
            {
                "surname": u"Radoshevich",
                "given-names": u"L",
                "group-type": u"author"
            },
            {
                "surname": u"Impens",
                "given-names": u"F",
                "group-type": u"author"
            },
            {
                "surname": u"Ribet",
                "given-names": u"D",
                "group-type": u"author"
            },
            {
                "surname": u"Quereda",
                "given-names": u"JJ",
                "group-type": u"author"
            },
            {
                "surname": u"Nam Tham",
                "given-names": u"T",
                "group-type": u"author"
            },
            {
                "surname": u"Nahori",
                "given-names": u"MA",
                "group-type": u"author"
            },
            {
                "surname": u"Bierne",
                "given-names": u"H",
                "group-type": u"author"
            },
            {
                "surname": u"Dussurget",
                "given-names": u"O",
                "group-type": u"author"
            },
            {
                "surname": u"Pizarro-Cerd\u00e1",
                "given-names": u"J",
                "group-type": u"author"
            },
            {
                "surname": u"Knobeloch",
                "given-names": u"KP",
                "group-type": u"author"
            },
            {
                "surname": u"Cossart",
                "given-names": u"P",
                "group-type": u"author"
            }
        ],
        "accession": "PXD001805",
        "uri": "http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD001805",
        "publication-type": u"data",
        "source": u"ProteomeXchange",
        "year": u"2015a",
        "position": 1,
        "year-iso-8601-date": u"2015",
        "ref": u"Radoshevich L Impens F Ribet D Quereda JJ Nam Tham T Nahori MA Bierne H Dussurget O Pizarro-Cerd\u00e1 J Knobeloch KP Cossart P 2015a ISG15 counteracts Listeria monocytogenes infection ProteomeXchange PXD001805",
        "id": u"bib34"
        }]
        ),

        )
    def test_refs_edge_cases(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        body_tag = soup.contents[0].contents[0]
        tag_content = parser.refs(body_tag)
        self.assertEqual(expected, tag_content)

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

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">14973</article-id><article-id pub-id-type="doi">10.7554/eLife.14973</article-id><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>Breast cancer</subject></subj-group></article-meta></front></root>',
        u'Breast Cancer'
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">05635</article-id><article-id pub-id-type="doi">10.7554/eLife.05635</article-id><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>The Natural History Of Model Organisms</subject></subj-group></article-meta></front></root>',
        u'The Natural History of Model Organisms'
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">17394</article-id><article-id pub-id-type="doi">10.7554/eLife.17394</article-id><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>p53 Family proteins</subject></subj-group></article-meta></front></root>',
        u'p53 Family Proteins'
        ),

        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">25700</article-id><article-id pub-id-type="doi">10.7554/eLife.25700</article-id><subj-group subj-group-type="display-channel"><subject>Insight</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>TOR signaling</subject></subj-group></article-meta></front></root>',
        u'TOR Signaling'
        ),

        # example from elife-27438-v1.xml has no sub-display-channel and title_prefix is None
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">27438</article-id><article-id pub-id-type="doi">10.7554/eLife.27438</article-id><subj-group subj-group-type="display-channel"><subject>Feature Article</subject></subj-group><subj-group subj-group-type="heading"><subject>Ecology</subject></subj-group></article-meta></front></root>',
        None
        ),

        # example from elife-27438-v2.xml which does have a title_prefix and it rewritten
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><journal-meta><journal-id journal-id-type="publisher-id">eLife</journal-id></journal-meta><article-meta><article-id pub-id-type="publisher-id">27438</article-id><article-id pub-id-type="doi">10.7554/eLife.27438</article-id><subj-group subj-group-type="heading"><subject>Ecology</subject></subj-group><subj-group subj-group-type="sub-display-channel"><subject>Point of view</subject></subj-group><subj-group subj-group-type="display-channel"><subject>Feature article</subject></subj-group></article-meta></front></root>',
        'Point of View'
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

    @unpack
    @data(
        # example issue from a non-eLife article
        ('<root><front><article-meta><issue>1</issue></article-meta></front></root>',
        '1'
        ),
        # example of no article issue
        ('<root><front><article-meta><volume>1</volume></article-meta></front><back><ref-list><ref id="bib1"><element-citation><issue>1</issue></element-citation></ref></ref-list></back></root>',
        None
        ),
    )
    def test_issue(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.issue(soup)
        self.assertEqual(expected, tag_content)

    def test_parse_mixed_citations(self):
        data = parser.mixed_citations(self.soup('elife-kitchen-sink.xml'))
        expected = [{'article': {'authorLine': u'R Straussman et al.', 'authors': [{'given': u'R', 'surname': u'Straussman'}, {'given': u'T', 'surname': u'Morikawa'}, {'given': u'K', 'surname': u'Shee'}, {'given': u'M', 'surname': u'Barzily-Rokni'}, {'given': u'ZR', 'surname': u'Qian'}, {'given': u'J', 'surname': u'Du'}, {'given': u'A', 'surname': u'Davis'}, {'given': u'MM', 'surname': u'Mongare'}, {'given': u'J', 'surname': u'Gould'}, {'given': u'DT', 'surname': u'Frederick'}, {'given': u'ZA', 'surname': u'Cooper'}, {'given': u'PB', 'surname': u'Chapman'}, {'given': u'DB', 'surname': u'Solit'}, {'given': u'A', 'surname': u'Ribas'}, {'given': u'RS', 'surname': u'Lo'}, {'given': u'KT', 'surname': u'Flaherty'}, {'given': u'S', 'surname': u'Ogino'}, {'given': u'JA', 'surname': u'Wargo'}, {'given': u'TR', 'surname': u'Golub'}], 'doi': u'10.1038/nature11183', 'pub-date': [2014, 2, 28], 'title': u'Tumour micro-environment elicits innate resistance to RAF inhibitors through HGF secretion'}, 'journal': {'volume': u'487', 'lpage': u'504', 'name': u'Nature', 'fpage': u'500'}}]
        self.assertEqual(expected, data)


    @unpack
    @data(
        # example with no history
        ('<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta></article-meta></front></root>',
         []
        ),
        # example based on 00666 kitchen sink
        ('''<root xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta><related-object ext-link-type="url" xlink:href="https://elifesciences.org/articles/e00666v1">
<date date-type="v1" iso-8601-date="2016-04-25">
<day>25</day>
<month>04</month>
<year>2016</year>
</date>
</related-object>
<related-object ext-link-type="url" xlink:href="https://elifesciences.org/articles/e00666v2">
<date date-type="v2" iso-8601-date="2016-06-12">
<day>12</day>
<month>06</month>
<year>2016</year>
</date>
<comment>
The first version of this article was enhanced considerably between versions of the XML instance. These changes can bee seen on
<ext-link ext-link-type="uri" xlink:href="https://github.com/elifesciences/XML-mapping/blob/master/eLife00666.xml">Github</ext-link>
.
</comment>
<!--
If subsequent versions (v3 and onwards are published these will look like the below
-->
</related-object>
<related-object ext-link-type="url" xlink:href="https://elifesciences.org/articles/e00666v3">
<date date-type="v3" iso-8601-date="2016-06-27">
<day>27</day>
<month>06</month>
<year>2016</year>
</date>
<comment>
The author Christoph Wuelfing requested has surname was converted to the German spelling of "Wülfing".
</comment>
</related-object></article-meta></front></root>''',
        [
            OrderedDict([
                ('version', u'v1'),
                ('day', u'25'),
                ('month', u'04'),
                ('year', u'2016'),
                ('date', date_struct(2016, 4, 25)),
                ('xlink_href', u'https://elifesciences.org/articles/e00666v1')
            ]), OrderedDict([
                ('version', u'v2'),
                ('day', u'12'),
                ('month', u'06'),
                ('year', u'2016'),
                ('date', date_struct(2016, 6, 12)),
                ('xlink_href', u'https://elifesciences.org/articles/e00666v2'),
                ('comment', u'\nThe first version of this article was enhanced considerably between versions of the XML instance. These changes can bee seen on\n<a href="https://github.com/elifesciences/XML-mapping/blob/master/eLife00666.xml">Github</a>\n.\n')
            ]), OrderedDict([
                ('version', u'v3'),
                ('day', u'27'),
                ('month', u'06'),
                ('year', u'2016'),
                ('date', date_struct(2016, 6, 27)),
                ('xlink_href', u'https://elifesciences.org/articles/e00666v3'),
                ('comment', u'\nThe author Christoph Wuelfing requested has surname was converted to the German spelling of "W\xfclfing".\n')
            ])
        ]
        ),
    )
    def test_version_history(self, xml_content, expected):
        soup = parser.parse_xml(xml_content)
        tag_content = parser.version_history(soup)
        self.assertEqual(expected, tag_content)


if __name__ == '__main__':
    unittest.main()
