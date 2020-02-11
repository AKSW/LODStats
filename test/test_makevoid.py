import unittest
from os import path

import lodstats
from lodstats.util.makevoid import MakeVoid

from . import helpers

http_base = helpers.webserver(helpers.resources_path)

class MakeVoidTests(unittest.TestCase):

    def setUp(self):
        lodstats.stats.stats_to_do = []
        lodstats.stats.results = {}

    def test_makevoid_local(self):

        uri = 'file://' + helpers.resources_path + 'heb.rdf'
        stats = lodstats.stats.void_stats
        rdf_stats = lodstats.RDFStats(uri, stats=stats)
        rdf_stats.disable_debug()
        rdf_stats.start_statistics()
        mv = MakeVoid(rdf_stats, serialize_as="turtle")
        void_stats = mv.voidify()
        self.assertTrue(void_stats.find('http://rdfs.org/ns/void') != -1)

    def test_makevoid_remote(self):

        uri = http_base + 'heb.rdf'
        stats = lodstats.stats.void_stats
        rdf_stats = lodstats.RDFStats(uri, stats=stats)
        rdf_stats.disable_debug()
        rdf_stats.start_statistics()
        mv = MakeVoid(rdf_stats, serialize_as="turtle")
        void_stats = mv.voidify()
        self.assertTrue(void_stats.find('http://rdfs.org/ns/void') != -1)