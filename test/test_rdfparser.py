import unittest

import lodstats
from lodstats.util.rdfparser import RdfParser

from . import helpers

class RdfParserTest(unittest.TestCase):

    def setUp(self):
        lodstats.stats.stats_to_do = []
        lodstats.stats.results = {}

    def test_rdfparser(self):
        uri = 'file://' + helpers.resources_path + 'heb-original.rdf'
        rdfparser = RdfParser([uri])
        self.assertTrue(type(rdfparser.get_stats_results()) == dict)
        self.assertTrue(len(rdfparser.get_stats_results()) == 8)