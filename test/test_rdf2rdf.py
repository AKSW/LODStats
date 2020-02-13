import unittest
from os.path import exists
import subprocess

from lodstats.util.rdf2rdf import RDF2RDF

import helpers
resources_path = helpers.resources_path

def any23_missing():
    try:
        subprocess.check_call('any23 --help', shell=True)
    except subprocess.CalledProcessError:
        return True
    else:
        return False

class RDF2RDFTest(unittest.TestCase):

    @unittest.skipIf(any23_missing(), 'any23 not available')
    def test_ttl_to_nt(self):
        file_uri = 'file://' + resources_path + 'heb-head-original.ttl'
        rdf2rdf = RDF2RDF(file_uri)
        self.assertTrue(exists(rdf2rdf.convert_ttl_to_nt(file_uri)),
                'converted file not found')
