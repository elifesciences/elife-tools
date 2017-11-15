import os, unittest

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser

from .file_utils import sample_xml

""" Basic code usage for the elifetools library.

These examples can be run with:
   python -m unittest discover -s tests/ -p *_test.py

"""

class TestBasicUsage(unittest.TestCase):
    def setUp(self):
        kitchen_sink_xml = sample_xml('elife-kitchen-sink.xml')

        # all of these methods are equivalent:
        #self.soup = bss(open(kitchen_sink_xml, 'r').read())
        #self.soup = parser.parse_xml(open(kitchen_sink_xml, 'r'))
        self.soup = parser.parse_document(kitchen_sink_xml)

    def tearDown(self):
        pass

    def test_basic_fetching_of_common_attributes(self):
        "basic extraction of common values from a JATS-NLM XML article"
        self.assertEqual(parser.title(self.soup), u"Bacterial regulation of colony development in the closest living\n                    relatives of animals")
        self.assertEqual(parser.doi(self.soup), u"10.7554/eLife.00013")
        self.assertEqual(parser.keywords(self.soup), [u'\nSalpingoeca rosetta\n', u'Algoriphagus', u'bacterial sulfonolipid', u'multicellular development'])

if __name__ == '__main__':
    unittest.main()
