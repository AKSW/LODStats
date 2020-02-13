import unittest
from os.path import exists

from lodstats.util.rdf2rdf import RDF2RDF

import helpers
resources_path = helpers.resources_path

class RDF2RDFTest(unittest.TestCase):

    def test_ttl_to_nt(self):
        file_uri = 'file://' + resources_path + 'heb-head-original.ttl'
        rdf2rdf = RDF2RDF(file_uri)
        self.assertTrue(exists(rdf2rdf.convert_ttl_to_nt(file_uri)),
                'converted file not found')
